from pathlib import Path
from functools import lru_cache
from dataclasses import dataclass
from io import TextIOWrapper
import subprocess
import sys

def excepthook(*args):
    print("==========[ExceptHook]==========")
    print(*args)
    input("Press Enter to close")
sys.excepthook = excepthook

path = Path(__file__).parent.resolve()
path_icons = path / "icons"

import tkinter as tk
import tkinter.font as tkfont
import tkinter.ttk as ttk
import tkinter.messagebox as msgbox
import tkinter.scrolledtext as sttk
import tksvg #type: ignore




root = tk.Tk()
menubar = tk.Menu(root)
root.title("visualpy")
root.config(menu=menubar)

root.option_add("*Background", "#FFFFFF")

@lru_cache
def _open_icon(target: str):
    return (path_icons / target).read_text()
def _create_icon(target: str, fillcolor: str="currentColor") -> tksvg.SvgImage:
    return tksvg.SvgImage(data=_open_icon(target).replace("fill=\"currentColor\"", f"fill=\"{fillcolor}\""))
iconImage: dict[str, tksvg.SvgImage] = {}
_icon_list: list[tuple[str, str]] = [
    ("file-code", "#999999"),
    ("symbol-class", "#e79428"),
    ("symbol-method", "#7c3aed"),
    ("symbol-string", "#98aa48"),
    ("symbol-variable", "#57beda"),
    ("symbol-property", "currentColor"),
    ("symbol-namespace", "#dd9623"),
    
    ("debug-step-over", "#75beff"),
    ("debug-stop", "#f48771"),
    
    ("send", "#999999"),
]
for _register_icon_target, _fill_color in _icon_list:
    iconImage[_register_icon_target]             = _create_icon(_register_icon_target+".svg", _fill_color)
    iconImage[_register_icon_target+":disabled"] = _create_icon(_register_icon_target+".svg", "#999999")

root_grid1 = tk.Frame(root)
root_grid1.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)
root_grid2 = tk.Frame(root)
root_grid2.pack(fill=tk.BOTH, side=tk.RIGHT, expand=True)
root_grid3 = tk.Frame(root_grid2)
root_grid3.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
root_grid4 = tk.Frame(root_grid2)
root_grid4.pack(fill=tk.BOTH, side=tk.TOP, expand=True)

####################################################################################################

dataview_frame = tk.Frame(root_grid1)
dataview_frame.pack(fill=tk.BOTH, expand=True)
style_notreeborder = ttk.Style()
style_notreeborder.layout(
    'Treeview.NoEdge',
    [('Treeview.NoEdge.treearea', {'sticky': 'nsew'})]
)
style_notreeborder.configure('Treeview.NoEdge', background = "white", bd=0)
dataview_tree = ttk.Treeview(dataview_frame, style = "Treeview.NoEdge", columns=("type", "value",))
dataview_tree.heading("#0", text="name")
dataview_tree.heading("type", text="type")
dataview_tree.heading("value", text="value")
dataview_tree.tag_configure("var_add", background="#baffc9")
dataview_tree.tag_configure("var_modify", background="#bae1ff")
dataview_tree.tag_configure("var_remove", background="#ffb3ba")
dataview_tree.tag_configure("frame_remove", background="#ff0000")
dataview_tree.tag_configure("builtin", foreground="gray")
dataview_tree.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)
dataview_scroll = tk.Scrollbar(dataview_frame, command=dataview_tree.yview)
dataview_scroll.pack(fill=tk.Y, side=tk.RIGHT)
dataview_tree.config(yscrollcommand=dataview_scroll.set)
@dataclass(frozen=True)
class FrameInfo:
    filename: str
    line: int
    funcname: str
    
    id: str

dataview_tree_frame_id_stack: list[FrameInfo] = []
dataview_tree_frame_will_remove: list[str] = []
dataview_tree_variable_id_stack: list[dict[str, str]] = []
dataview_tree_variable_to_retag: list[tuple[str, str]] = []
dataview_tree_variable_will_remove: list[str] = []

@dataclass(frozen=True)
class AttributeInfo:
    depth: int
    parentId: str
    path: str
    
    id: str
    name: str
dataview_tree_attribute_info_list: list[AttributeInfo] = []


####################################################################################################


controllbar_frame = tk.Frame(root_grid1)
controllbar_frame.pack(fill=tk.X, side=tk.BOTTOM)

controllbar_step_over_button = tk.Button(controllbar_frame, relief=tk.FLAT, image=iconImage["debug-step-over"])
controllbar_step_over_button.pack(side=tk.LEFT)
controllbar_stop_button = tk.Button(controllbar_frame, relief=tk.FLAT, image=iconImage["debug-stop"])
controllbar_stop_button.pack(side=tk.LEFT)
controllbar_log_in_terminal = tk.BooleanVar(controllbar_frame, False)
controllbar_log_in_terminal_checkbox = tk.Checkbutton(controllbar_frame, variable=controllbar_log_in_terminal, text="Log in terminal")
controllbar_log_in_terminal_checkbox.pack(side=tk.LEFT)

####################################################################################################


codeview_frame = tk.Frame(root_grid3)
codeview_frame.pack(fill=tk.BOTH)

codeview_notebook = ttk.Notebook(codeview_frame)
codeview_notebook.pack(fill=tk.BOTH, expand=True)
codeview_stacks: list[tuple[tk.Frame, tk.Text, tk.Text, tk.Scrollbar]] = []
codeview_will_remove: list[tk.Frame] = []


####################################################################################################


terminalview_frame = tk.Frame(root_grid4)
terminalview_frame.pack(fill=tk.BOTH, expand=True)

terminalview_scrolledtext = sttk.ScrolledText(terminalview_frame)
terminalview_scrolledtext.tag_config('system', foreground="blue")
terminalview_scrolledtext.tag_config('user', foreground="red")
terminalview_scrolledtext.pack(fill=tk.BOTH, side=tk.TOP)
terminalview_scrolledtext.yview_moveto(1)

terminalview_setting_frame = tk.Frame(terminalview_frame)
terminalview_setting_frame.pack(fill=tk.X, side=tk.TOP, expand=True)
terminalview_do_eval_mode = tk.IntVar(terminalview_setting_frame, 1)
terminalview_do_command_radiobutton = tk.Radiobutton(terminalview_setting_frame, text="command", value=0, variable=terminalview_do_eval_mode)
terminalview_do_command_radiobutton.pack(side=tk.LEFT)
terminalview_do_eval_radiobutton = tk.Radiobutton(terminalview_setting_frame, text="eval", value=1, variable=terminalview_do_eval_mode)
terminalview_do_eval_radiobutton.pack(side=tk.LEFT)
terminalview_do_eval_pretty_radiobutton = tk.Radiobutton(terminalview_setting_frame, text="eval (pretty)", value=2, variable=terminalview_do_eval_mode)
terminalview_do_eval_pretty_radiobutton.pack(side=tk.LEFT)

terminalview_command_frame = tk.Frame(terminalview_frame)
terminalview_command_frame.pack(fill=tk.X, side=tk.TOP, expand=True)
terminalview_entry = tk.Entry(terminalview_command_frame)
terminalview_entry.pack(fill=tk.X, side=tk.LEFT, expand=True)
terminalview_compliment_list: list[str] = []
terminalview_compliment = ttk.Treeview(terminalview_frame, height=0, selectmode=tk.NONE, show="tree")
terminalview_compliment.tag_configure("select", background="#bae1ff")
terminalview_compliment.place(x=0, y=-10)
terminalview_compliment_select: int = 0
terminalview_send_button = tk.Button(terminalview_command_frame, image=iconImage["send"])
terminalview_send_button.pack(side=tk.LEFT)

terminalview_may_wrong_label = tk.Label(terminalview_frame, text="Some texts would be missing and some texts would be placed in wrong order.")
terminalview_may_wrong_label.pack(fill=tk.X, side=tk.TOP)


####################################################################################################


license_window = tk.Toplevel(root)
license_window.title("License")
license_window.withdraw()
license_window.protocol("WM_DELETE_WINDOW", license_window.withdraw)
license_notebook = ttk.Notebook(license_window)
license_notebook.pack(fill=tk.BOTH, expand=True)
license_microsoft_codicon = sttk.ScrolledText(license_window)
license_microsoft_codicon.insert(tk.END, (path / "licenses" / "Microsoft-Codicon.txt").read_text("utf-8"))
license_microsoft_codicon.config(state=tk.DISABLED)
license_notebook.add(license_microsoft_codicon, text="codicon")

menubar.add_command(label="License", command=license_window.deiconify)

def thread(func):
    return lambda *args, **kwards: root.after(1, lambda: func(*args, **kwards))

argv = sys.orig_argv.copy()
argv.pop(1)
argv.append("Visual.py-subprocess")
proc = subprocess.Popen(
	argv,
    stdin = subprocess.PIPE,
    stdout = subprocess.PIPE,
    text=True
)

@thread
def communicate(callback, *args, callback_closed = None, log_in_termianl: bool = False, tag: str = "system"):
    assert type(proc.stdin) == TextIOWrapper
    assert type(proc.stdout) == TextIOWrapper
    move_end = terminalview_scrolledtext.yview()[1] == 1
    for s in args:
        if log_in_termianl: terminalview_scrolledtext.insert(tk.END, s+"\n", tag)
        proc.stdin.write(s+'\n')
        proc.stdin.flush()
        

    empty_count = 0
    while not (lineinfo := (line := proc.stdout.readline()).replace("[visual.py] ", "").strip()).startswith("lines: "):
        if log_in_termianl: terminalview_scrolledtext.insert(tk.END, line+"\n")
        if len(lineinfo) == 0: empty_count += 1
        if proc.poll() != None:
            if callback_closed:
                callback_closed()
            return
    lines = int(lineinfo.replace("lines: ", ""))
    text = "\n".join([proc.stdout.readline().rstrip("\n") for _ in range(lines)])
    if log_in_termianl: 
        terminalview_scrolledtext.insert(tk.END, text+"\n")
        if move_end: terminalview_scrolledtext.yview_moveto(1)
    callback(text)
    
def refresh_frames(text: str):
    global dataview_tree_frame_id_stack, dataview_tree_variable_id_stack
    for id_ in dataview_tree_frame_will_remove:
        dataview_tree.delete(id_)
    dataview_tree_frame_will_remove.clear()
    
    for frameWidget in codeview_will_remove:
        frameWidget.destroy()
    codeview_will_remove.clear()
    
    info = text.splitlines()
    frames: list[tuple[str, int, str]] = []
    for line in info:
        filepath, line, funcname = line.replace("File ", "").replace("\"", "").replace(" line ", "").replace(" in ", "").split(",")
        frames.append((filepath, int(line), funcname))
    frames.reverse()
    index = len(dataview_tree_frame_id_stack)
    for i, (frame, tree_element) in enumerate(zip(frames, dataview_tree_frame_id_stack)):
        if frame[0] != tree_element.filename or frame[2] != tree_element.funcname:
            index = i
            for j in range(i, len(dataview_tree_frame_id_stack)):
                dataview_tree.delete(dataview_tree_frame_id_stack[j].id)
            del dataview_tree_frame_id_stack[i:]
            del dataview_tree_variable_id_stack[i:]
            for (codeWidget_frame, codeWidget_lineno, codeWidget_code, codeWidget_scroll) in codeview_stacks[i:]:
                codeWidget_frame.pack_forget()
                codeWidget_frame.destroy()
            del codeview_stacks[i:]
            break
        if frame[1] != tree_element.line:
            id_ = dataview_tree_frame_id_stack[i].id
            dataview_tree_frame_id_stack[i] = FrameInfo(*frame, id_)
            dataview_tree.item(id_, text=f"File {frame[0]}, line {frame[1]}, in {frame[2]}")
    if len(frames) < len(dataview_tree_frame_id_stack):
        for i in range(len(frames), len(dataview_tree_frame_id_stack)):
            dataview_tree.item(dataview_tree_frame_id_stack[i].id, tags="frame_remove")
            dataview_tree_frame_will_remove.append(dataview_tree_frame_id_stack[i].id)
            codeview_will_remove.append(codeview_stacks[i][0])
        del dataview_tree_frame_id_stack[len(frames):]
        del codeview_stacks[len(frames):]
    
    for i in range(index, len(frames)):
        dataview_tree_frame_id_stack.append(FrameInfo(*frames[i], dataview_tree.insert("", 0, text=f"File {frames[i][0]}, line {frames[i][1]}, in {frames[i][2]}")))
        dataview_tree_variable_id_stack.append({})
        
        code_frame = tk.Frame(codeview_notebook)
        code_frame.pack(fill=tk.X, side=tk.BOTTOM, expand=True)
        codeview_notebook.insert("end" if len(dataview_tree_frame_id_stack) == 1 else 0, code_frame, text=f"frame{len(dataview_tree_frame_id_stack)}")
        codeview_notebook.update()
        codeview_notebook.select(0)
        
        max_line = load_codefile(frames[i][0]).count("\n")+1
        lineno_area = tk.Text(code_frame, width=max(len(str(max_line)), 3), bg="lightgray")
        lineno_area.insert(tk.END, "\n".join(map(str, range(1, max_line+1))))
        lineno_area.config(state=tk.DISABLED)
        lineno_area.pack(fill=tk.Y, side=tk.LEFT)
        
        code_area = tk.Text(code_frame)
        code_area.tag_config('current', background='#bae1ff', foreground="blue")
        code_area.insert(tk.END, load_codefile(frames[i][0]))
        code_area.config(state=tk.DISABLED)
        code_area.pack(fill=tk.BOTH, side=tk.LEFT)
        
        scroll = tk.Scrollbar(code_frame)
        scroll.pack(fill=tk.Y, side=tk.LEFT)
        
        def __ysc(first, last):
            lineno_area.yview_moveto(first)
            scroll.set(first, last)
        code_area.config(yscrollcommand=__ysc)
        scroll.config(command=lambda *args: (lineno_area.yview(*args), code_area.yview(*args)))
        
        codeview_stacks.append((code_frame, lineno_area, code_area, scroll))
def getIconImage(typename: str) -> tk.PhotoImage:
    if typename == "module": return iconImage["file-code"]
    if typename == "type": return iconImage["symbol-class"]
    if typename == "method": return iconImage["symbol-method"]
    if typename == "builtin_function_or_method": return iconImage["symbol-method"]
    if typename == "method-wrapper": return iconImage["symbol-method"]
    if typename == "function": return iconImage["symbol-method"]
    if typename == "property": return iconImage["symbol-property"]
    if typename == "dict": return iconImage["symbol-namespace"]
    if typename == "str": return iconImage["symbol-string"]
    return iconImage["symbol-variable"]
def refresh_variables(text: str):
    move_end = dataview_scroll.get()[1] == 1
    
    for id_, tag in dataview_tree_variable_to_retag:
        try: dataview_tree.item(id_, tags=tag)
        except tk.TclError as tcle: print(tcle)
    dataview_tree_variable_to_retag.clear()
    for to_delete in dataview_tree_variable_will_remove:
        try: dataview_tree.delete(to_delete)
        except tk.TclError as tcle: print(tcle)
    dataview_tree_variable_will_remove.clear()
    
    info = text.splitlines()
    for line_index in range(0, len(info), 2):
        frame_index = int(info[line_index].split(" ")[0][1:-1])
        sub_mode = info[line_index+1].index(" ")
        mode = info[line_index+1][:sub_mode]
        sub_name = info[line_index+1].index(" ", sub_mode+1)
        name = info[line_index+1][sub_mode+1:sub_name]
        sub_type = info[line_index+1].index(" ", sub_name+1)
        type_ = info[line_index+1][sub_name+1:sub_type]
        value = info[line_index+1][sub_type+1:]
        if mode == "+":
            id_ = dataview_tree.insert(dataview_tree_frame_id_stack[frame_index].id, "end", text=name, values=(type_, value, ), image=getIconImage(type_), tags="var_add")
            dataview_tree_variable_id_stack[frame_index][name] = id_
            dataview_tree_variable_to_retag.append((id_, "var_keep"))
        elif mode == "*":
            id_ = dataview_tree_variable_id_stack[frame_index][name]
            dataview_tree.item(id_, values=(type_, value,), image=getIconImage(type_), tags="var_modify")
            dataview_tree_variable_to_retag.append((id_, "var_keep"))
        elif mode == "-":
            dataview_tree.item(dataview_tree_variable_id_stack[frame_index][name], tags="var_remove")
            dataview_tree_variable_will_remove.append(dataview_tree_variable_id_stack[frame_index][name])
            del dataview_tree_variable_id_stack[frame_index][name]
        # dataview_tree_variable_id_stack[frame_index]
        
    if move_end: dataview_tree.yview_moveto(1)
    
def refresh_details(text: str, targetId: str):
    lines = text.splitlines()
    if len(lines) < 2: return
    if lines[0] != "Success": return
    line = lines[1]
    sub_name = line.index(" ")
    name = line[:sub_name]
    sub_type = line.index(" ", sub_name+1)
    type_ = line[sub_name+1:sub_type]
    sub_default = line.index(" ", sub_type+1)
    default = line[sub_type+1:sub_default] == "T"
    value = line[sub_default+1:]
    
    dataview_tree.item(targetId, text=name, values=[type_, value], image=getIconImage(type_ + (":disabled" if default else "")), tags="builtin" if default else "")
@lru_cache
def load_codefile(target: str):
    print("Reading code at", target)
    return Path(target).read_text()
def refresh_codes(text: str):
    info = text.splitlines()
    info.reverse()
    for i, line in enumerate(info):
        _, line, _, coderange = line.replace("File ", "").replace("\"", "").replace(" line ", "").replace(" in ", "").replace(" at ", "").split(",")
        codeview_stacks[i][2].tag_remove("current", "1.0", tk.END)
        lineno, _, end_lineno, _ = map(int, coderange.split("_"))
        codeview_stacks[i][2].tag_add("current", f"{lineno}.0", f"{end_lineno+1}.0")
        codeview_stacks[i][1].mark_set("insert", f"{lineno}.0")
        codeview_stacks[i][1].see("insert")
        codeview_stacks[i][2].mark_set("insert", f"{lineno}.0")
        codeview_stacks[i][2].see("insert")
    
def stop_debug():
    proc.kill()
    controllbar_step_over_button.config(image=iconImage["debug-step-over:disabled"], state=tk.DISABLED)
    controllbar_stop_button     .config(image=iconImage["debug-stop:disabled"], state=tk.DISABLED)
def step_over_handler(text):
    refresh_frames(text)
    communicate(refresh_variables, "frames", log_in_termianl=controllbar_log_in_terminal.get())
    for attr in dataview_tree_attribute_info_list:
        func = lambda text, id_=attr.id: refresh_details(text, id_)
        communicate(func, f"detail {attr.depth} {attr.path}", log_in_termianl=controllbar_log_in_terminal.get())
    communicate(refresh_codes, "seek", log_in_termianl=controllbar_log_in_terminal.get())
def step_over():
    communicate(step_over_handler, 
                "step", "where", 
                callback_closed=stop_debug,
                log_in_termianl=controllbar_log_in_terminal.get())
controllbar_step_over_button.config(command=step_over)
controllbar_stop_button     .config(command=lambda: stop_debug() if msgbox.Message(title="msgbox", message="Are you sure to stop now?", icon=msgbox.WARNING, type=msgbox.OKCANCEL).show() in ("ok", True) else None)
step_over()

def send_command():
    terminalview_entry.config(bg="#ffffff")
    move_end = terminalview_scrolledtext.yview()[1] == 1
    
    if terminalview_do_eval_mode.get() == 0:
        if terminalview_entry.get() and terminalview_entry.get().split(" ")[0] not in ("ev", "evp", "where", "seek", "frames"):
            terminalview_entry.config(bg="#ffb3ba")
            return
    communicate(lambda _:None, ("", "ev ", "evp ")[terminalview_do_eval_mode.get()]+terminalview_entry.get(), log_in_termianl=True, tag="user")
    if move_end: terminalview_scrolledtext.yview_moveto(1)
    
    terminalview_entry.delete(0, tk.END)
terminalview_entry.bind("<Return>", lambda _: [send_command(), refresh_compliment()])
terminalview_send_button.config(command=send_command)

def unselect_all_compliment():
    for c in terminalview_compliment.get_children():
        terminalview_compliment.item(c, tag="")

def move_selection_compliment(delta: int):
    global terminalview_compliment_select
    terminalview_compliment_select += delta
    length = len(terminalview_compliment.get_children())
    if terminalview_compliment_select < 0: terminalview_compliment_select += length
    if terminalview_compliment_select >= length: terminalview_compliment_select -= length
    unselect_all_compliment()
    terminalview_compliment.item(f"compliment-{terminalview_compliment_select}", tags="select")
    terminalview_compliment.see(f"compliment-{terminalview_compliment_select}")


def refresh_compliment(text: str = "Success"):
    global terminalview_compliment_select
    terminalview_compliment_select = 0
    
    terminalview_compliment.delete(*terminalview_compliment.get_children())
    
    lines = text.splitlines()
    if not lines[0].startswith("S"): return
    lines = lines[1:]
    
    compliments = []
    for i, line in enumerate(lines):
        index = line.index(" ")
        varname = line[:index]
        typename = line[index+1:]
        compliments.append(varname)
        
        terminalview_compliment.insert("", tk.END, f"compliment-{i}", text=varname, image=iconImage["symbol-method"] if typename == "function" else iconImage["symbol-property"] if typename == "property" else iconImage["symbol-class"] if typename == "type" else iconImage["symbol-variable"])
    terminalview_compliment.config(height=min(4, len(compliments)))
    terminalview_compliment.update()
    
    
    font = tkfont.nametofont("TkDefaultFont")  # Get default font value into Font object
    font.actual()
    text_width = font.measure(terminalview_entry.get())
    x_offset = (terminalview_entry.winfo_rootx() - terminalview_frame.winfo_rootx()) + text_width
    terminalview_compliment.place()
    y_offset = (terminalview_entry.winfo_rooty() - terminalview_frame.winfo_rooty()) - terminalview_compliment.winfo_height()
    if len(compliments) == 0:
        y_offset = -10
    terminalview_compliment.place(x=x_offset, y=y_offset)
        
    global terminalview_compliment_list
    terminalview_compliment_list = compliments

def on_terminalview_entry_write(event: "tk.Event[tk.Entry]"):
    
    if event.char and event.char in "ABCDEFGHIJKLNMOPQRSTUVWXYZ" + "ABCDEFGHIJKLNMOPQRSTUVWXYZ".lower() + "1234567890!@#$%^&*()" + "-_=+[{]}\\|;:\'\",<.>`~":
        terminalview_entry.config(bg="#ffffff")
    if event.keycode == 9: #tab
        text = terminalview_entry.get()
        if "." in text:
            text = text[:text.rindex(".")]
            text += "."
            text += terminalview_compliment_list[terminalview_compliment_select]
        else:
            text = terminalview_compliment_list[terminalview_compliment_select]
        terminalview_entry.delete(0, tk.END)
        terminalview_entry.insert(tk.END, text)
        
        
    communicate(refresh_compliment, f"comp {terminalview_entry.get() + event.char}")
    
    
def on_terminalview_entry_delete(event: "tk.Event[tk.Entry]"):
    terminalview_entry.config(bg="#ffffff")
    if terminalview_entry.get():
        communicate(refresh_compliment, f"comp {terminalview_entry.get()[:-1]}")
for b in ("BackSpace", "Delete", "space"):
    terminalview_entry.bind(f"<{b}>", on_terminalview_entry_delete)
terminalview_entry.bind("<Key>", on_terminalview_entry_write)
terminalview_entry.bind("<Up>", lambda _: move_selection_compliment(-1))
terminalview_entry.bind("<Down>", lambda _: move_selection_compliment(+1))


def create_detail(depth: int, parentPath: str, parentId: str, text: str):
    if not text.startswith("S"):
        return
    lines = text.splitlines()[1:]
    for line in lines:
        sub_name = line.index(" ")
        name = line[:sub_name]
        sub_type = line.index(" ", sub_name+1)
        type_ = line[sub_name+1:sub_type]
        sub_default = line.index(" ", sub_type+1)
        default = line[sub_type+1:sub_default] == "T"
        value = line[sub_default+1:]
        
        dataview_tree.item(parentId, open=True)
        dataview_tree_attribute_info_list.append(AttributeInfo(
            depth,
            parentId,
            parentPath+"."+name,
            dataview_tree.insert(parentId, tk.END, text=name, image=getIconImage(type_ + (":disabled" if default else "")), values=[type_, value], tags="builtin" if default else ""),
            name
        ))

def on_dataview_detail(event: "tk.Event[ttk.Treeview]"):
    
    target, *_ = dataview_tree.selection()
    for fstack in dataview_tree_frame_id_stack:
        if fstack.id == target: return
    
    target_depth = -1
    target_path = ""
    for depth in range(len(dataview_tree_variable_id_stack)):
        if target_depth != -1:
            break
        
        stack = dataview_tree_variable_id_stack[depth]
        for name, id_ in stack.items():
            if id_ == target:
                target_depth = depth
                target_path = name
                break
    
    for attr_info in dataview_tree_attribute_info_list:
        if target_depth != -1:
            break
        
        if attr_info.id == target:
            target_depth = attr_info.depth
            target_path = attr_info.path
        
    if target_depth == -1:
        msgbox.showwarning("tk", "Failed to find target: "+target)
        return
    
    for attr_info in dataview_tree_attribute_info_list: # If already updated
        if attr_info.parentId == target:
            return
    communicate(lambda text: create_detail(target_depth, target_path, target, text), f"detailall {target_depth} {target_path}", log_in_termianl=controllbar_log_in_terminal.get())
dataview_tree.bind("<Double-1>", on_dataview_detail)
def on_dataview_close(event: "tk.Event[ttk.Treeview]"):
    global dataview_tree_attribute_info_list
    target, *_ = dataview_tree.selection()
    is_attr_holder = False
    for depth in range(len(dataview_tree_variable_id_stack)):
        
        stack = dataview_tree_variable_id_stack[depth]
        for _, id_ in stack.items():
            if id_ == target:
                is_attr_holder = True
                break
        if is_attr_holder: break
    for attr_info in dataview_tree_attribute_info_list:
        if attr_info.id == target: is_attr_holder = True
        if is_attr_holder: break
    if not is_attr_holder: return
    
    
    
    deleter_tree_elements = [target]
    while True:
        recently_change = False
        for attr_info in dataview_tree_attribute_info_list:
            if attr_info.id not in deleter_tree_elements and attr_info.parentId in deleter_tree_elements:
                deleter_tree_elements.append(attr_info.id)
                recently_change = True
        if not recently_change: break
    deleter_tree_elements.remove(target)
    dataview_tree.delete(*deleter_tree_elements)
    dataview_tree_attribute_info_list = [e for e in dataview_tree_attribute_info_list if e.id not in deleter_tree_elements]
        
            
dataview_tree.bind("<<TreeviewClose>>", on_dataview_close)

root.mainloop()
