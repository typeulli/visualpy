import json
from ..structure import ( # type: ignore
    FrameInfo, VariableInfo, AttributeInfo, idToInfo,
    EventListener, eventHandler, addListener,
    createTopLevel, createModuleMenu, 
    getContextTarget, addModuleMenu, addContextCommand,
    
    requestData
)
import tkinter as tk
import tkinter.scrolledtext as sttk
import tkinter.messagebox as msgbox

class GraphHandler(EventListener):
    @eventHandler
    def onStep(self, info: list[FrameInfo]):
        ...

addListener(GraphHandler())





def convert_to_json(data: object, *, force: bool = False):
    type_ = type(data)
    if type_ in (str, int, float, None): return data
    if type_ in (list, set):
        assert type(data) == list or type(data) == set
        return [convert_to_json(item, force=force) for item in data]
    if type_ == dict:
        assert type(data) == dict
        return {convert_to_json(key, force=force): convert_to_json(value, force=force) for key, value in data.items()}
    if force: return repr(data)
    raise ValueError(f"{data} is not able to convert into json")

def open_viewer():
    target = getContextTarget()
    
    if target == "":
        return
    info = idToInfo(target)
    if info == None:
        return
    if type(info) == FrameInfo:
        return
    assert type(info) == VariableInfo or type(info) == AttributeInfo
    
    try:
        data = requestData(info.depth, info.path)
    except Exception as e:
        msgbox.showerror("JsonView", str(e))
        return
    
    
    text = ""
    if type(data) == str:
        text = data
    elif type(data) in (int, float, bytes):
        text = str(data)
    else:
        try:
            converted = convert_to_json(data)
            text = json.dumps(converted, indent=4)
        except:
            if not msgbox.askokcancel("JsonView", f"Variable {info.path} at frame #{info.depth} is not convertable into json (type {type(data).__name__})\n\nWould you want to convert all not-convertable items into string?"):
                return
                
            converted = convert_to_json(data, force=True)
            text = json.dumps(converted, indent=4)
            
        
        
    
    window = createTopLevel()
    window.title("Json Viewer")
    
    top_area = tk.Frame(window)
    top_area.pack(side=tk.TOP, fill=tk.X)
    
    label = tk.Label(top_area, text=f"{info.path} at frame #{info.depth}")
    label.pack(side=tk.LEFT)
    
    scrollview = sttk.ScrolledText(window)
    scrollview.insert(tk.END, text)
    scrollview.config(state=tk.DISABLED)
    scrollview.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    
    
addContextCommand(label="View in Json Viewer", command=open_viewer)