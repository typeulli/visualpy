import dis
import inspect
import pdb
import sys
import pprint
from pathlib import Path
from types import FrameType
from typing import Any, cast

from pympler import asizeof
import ctypes

default_types = [type(None.__new__), type(None.__repr__)]
here = Path(__file__).parent.absolute()

def repr_data(target: object):
    return repr(target).replace("\n", "")
    
def suppress_warning(function):
    def inner(*args, **kwargs):
        try: return function(*args, **kwargs)
        except Exception as e:
            print("lines: 1")
            print(e)
    return inner
    

KNOWN_UNITS = {"KB", "MB", "BYTES"}

from dataclasses import dataclass, field

@dataclass(frozen=True)
class FrameLoc:
    filename: str
    lineno: int = field(compare=False, hash=False)
    function: str
    name: str

class Debug(pdb.Pdb):
    def __init__(self, *args, **kwargs):
        super(Debug, self).__init__(*args, **kwargs)
        self.prompt = "[visualpy] "
        self.data: list[dict[FrameLoc, Any]] = [] #type: ignore
        
        self.lastframe = None
        

    def format_bytes(self, value: int, unit: str) -> str:
        upper = unit.upper()

        # Forcing BYTES for unknown units
        base_unit = upper if upper in KNOWN_UNITS else "BYTES"

        if base_unit == "KB":
            converted = value / 1000
        elif base_unit == "MB":
            converted = value / 1000000
        else:
            converted = value

        return f"{converted:.2f} {base_unit}"

    
    def do_where(self, arg: str):
        frame = self.curframe
        text = ""
        while frame != None:
            loc = inspect.getframeinfo(cast(FrameType, frame))
        
            text += f'File "{loc.filename}", line {loc.lineno}, in {loc.function}\n'
            frame = cast(FrameType, frame).f_back
        self.message("lines: "+str(text.count("\n"))) # NOTE don't add 1 line cause each lines are added '\n'
        self.message(text.strip())
    def do_seek(self, arg: str):
        frame = self.curframe
        text = ""
        while frame != None:
            loc = inspect.getframeinfo(cast(FrameType, frame))
            
            positions = cast(dis.Positions, loc.positions)
        
            text += f'File "{loc.filename}", line {loc.lineno}, in {loc.function}, at {positions.lineno}_{positions.col_offset}_{positions.end_lineno}_{positions.end_col_offset}\n'
            frame = cast(FrameType, frame).f_back
        self.message("lines: "+str(text.count("\n"))) # NOTE don't add 1 line cause each lines are added '\n'
        self.message(text.strip())
    def do_ev(self, arg):
        try:
            val = self._getval(arg)
        except Exception as e:
            text = ""
            text += str(e)
            self.message("lines: "+str(text.count("\n")+1))
            self.message(text.strip())
            return  # _getval() has displayed the error
        try:
            text = repr_data(val)
            self.message("lines: "+str(text.count("\n")+1))
            self.message(text.strip())
        except:
            self._error_exc()
    @suppress_warning
    def do_detailall(self, arg):
        depth_str, target = arg.split()
        depth = int(depth_str)
        target_path = target.split(".")
        
        target_object: object = None
        found_init_object = False
        
        for f, v in self.data[depth].items():
            if f.name == target_path[0]:
                target_object = v
                found_init_object = True
                break
        if not found_init_object:
            print("lines: 1")
            print("Failed")
            return

        for p in target_path[1:]:
            target_object = object.__getattribute__(target_object, p)
        
        
        text = "Success"
        
        for key in target_object.__dir__():
            value = object.__getattribute__(target_object, key)
            text += f"\n{key} {type(value).__name__} {'T' if type(value) in default_types else 'F'} {repr_data(value)}"
        
        self.message("lines: "+str(text.count("\n")+1))
        self.message(text.strip())
                
                
    @suppress_warning
    def do_detail(self, arg):
        depth_str, target = arg.split()
        depth = int(depth_str)
        target_path = target.split(".")
        
        target_object: object = None
        found_init_object = False
        
        for f, v in self.data[depth].items():
            if f.name == target_path[0]:
                target_object = v
                found_init_object = True
                break
        if not found_init_object:
            print("lines: 1")
            print("Failed")
            return

        for p in target_path[1:]:
            target_object = object.__getattribute__(target_object, p)
        
        
        text = "Success"
        
        text += f"\n{target_path[-1]} {type(target_object).__name__} {'T' if type(target_object) in default_types else 'F'} {repr_data(target_object)}"
        
        self.message("lines: "+str(text.count("\n")+1))
        self.message(text.strip())


    def do_compliment(self, arg: str):
        isEndDot = arg.endswith(".")
        if isEndDot: arg = arg[:-1]
        target = arg
        compare = ""
        if "." in target:
            ri = target.rindex(".")
            compare = target[ri+1:]
            target = target[:ri]
        elif not isEndDot:
            gd: object = self._getval("globals()")
            ld: object = self._getval("locals()")
            assert type(gd) == dict
            assert type(ld) == dict
            text = "Success.\n" + "\n".join([f"{k} {type(v).__name__}" for k, v in {**gd, **ld}.items() if k.startswith(target)])
            text = text.strip()
            self.message("lines: "+str(text.count("\n")+1))
            self.message(text)
            return
            
        try:
            val = self._getval(target)
            text = "Success.\n" + "\n".join([f"{k} {type(v).__name__}" for k, v in val.__dict__.items() if k.startswith(compare)])
            text = text.strip()
            self.message("lines: "+str(text.count("\n")+1))
            self.message(text)
        except Exception as e:
            text = "Error Occured.\n"
            text += str(e)
            self.message("lines: "+str(text.count("\n")+1))
            self.message(text.strip())
            return  # _getval() has displayed the error
    do_comp = do_compliment
    def do_evp(self, arg):
        try:
            val = self._getval(arg)
        except Exception as e:
            text = ""
            text += str(e)
            self.message("lines: "+str(text.count("\n")+1))
            self.message(text.strip())
            return  # _getval() has displayed the error
        try:
            text = pprint.pformat(repr_data(val))
            self.message("lines: "+str(text.count("\n")+1))
            self.message(text.strip())
        except:
            self._error_exc()
        
    def do_frames(self, arg: str, slient: bool = False):
        
        frame = self.curframe
        if frame == None: return
        frame_depth_counter = frame
        frame_list = [frame]
        while True:
            frame_depth_counter = cast(FrameType, frame_depth_counter).f_back
            if frame_depth_counter == None: break
            frame_list.insert(0, frame_depth_counter)
        frame_depth = len(frame_list) - 1
        
        while frame_depth+1 > len(self.data):
            self.data.append({})
        
            
        newData: list[dict[FrameLoc, Any]] = [{} for _ in range(frame_depth+1)]
        delta: list[dict[FrameLoc, tuple[int, Any]]] = [{} for _ in range(max(frame_depth+1, len(self.data)))]
        
        for depth in range(frame_depth+1):
            frame_info = inspect.getframeinfo(cast(FrameType, frame_list[depth]))
            for key, value in cast(FrameType, frame_list[depth]).f_locals.items():
                loc = FrameLoc(frame_info.filename, frame_info.lineno, frame_info.function, key)
                if loc in self.data[depth]:
                    if value is not self.data[depth][loc]:
                        delta[depth][loc] = (1, value)
                else:
                    delta[depth][loc] = (0, value)
                newData[depth][loc] = value
        
        for depth in range(frame_depth+1):
            for check_deleted in self.data[depth]:
                if check_deleted not in newData[depth]:
                    if check_deleted not in delta[depth].keys():
                        delta[depth][check_deleted] = (2, self.data[depth][check_deleted])
            
        for depth in range(frame_depth+1, len(self.data)):
            for deleted in self.data[depth]:
                delta[depth][deleted] = (2, self.data[depth][deleted])
        self.data = newData
        
        if not slient:
            text = ""
            for frame_index, delta_dict in enumerate(delta):
                for loc, (mode, value) in delta_dict.items():
                    text += f'[{frame_index}] File "{loc.filename}", line {loc.lineno}, in {loc.function}\n'


                    text += "+*-"[mode] + " " + loc.name + " " + str(type(value).__name__) + " " + repr_data(value) +"\n"
        
            self.message("lines: "+str(text.count("\n")))
            self.message(text.strip())
        
        self.lastframe = self.curframe

    def do_args_memory_usage(self, arg: str):
        assert self.curframe != None
        co = cast(FrameType, self.curframe).f_code
        dict = self.curframe_locals
        n = co.co_argcount + co.co_kwonlyargcount
        if co.co_flags & inspect.CO_VARARGS: n = n+1
        if co.co_flags & inspect.CO_VARKEYWORDS: n = n+1

        self.message("---- Args memory usage ----")
        for i in range(n):
            name = co.co_varnames[i]
            if name in dict:
                arg_size = asizeof.asizeof(dict[name])
                self.message('%s = %s' % (name, self.format_bytes(arg_size, arg)))
            else:
                self.message('%s = *** undefined ***' % (name,))

    do_amu = do_args_memory_usage

from ctypes import wintypes as w

SW_SHOWNORMAL = 1

shell32 = ctypes.windll.shell32
shell32.ShellExecuteA.argtypes = w.HWND, w.LPCSTR, w.LPCSTR, w.LPCSTR, w.LPCSTR, w.INT
shell32.ShellExecuteA.restype = w.HINSTANCE

debugger = Debug()
def debug(debugger_path: str, show_console = False):
    if "Visual.py-subprocess" not in sys.argv:
        print("Running visual.py.\nEnsure argument Visual.py-subprocess is not contained originally.")
        print("Arguments:", sys.argv)
        python_path = sys.orig_argv[0]
        shell32.ShellExecuteA(None, b"open", python_path.encode(), (debugger_path + " " + " ".join(sys.argv)).encode(), None, show_console)
        exit()
    else:
        frame = sys._getframe().f_back
        if __name__ != "__main__": frame = cast(FrameType, frame).f_back
        debugger.curframe = frame
        debugger.do_frames("", slient=True)
        debugger.set_trace(frame)



