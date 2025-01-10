from ..structure import ( # type: ignore
    FrameInfo, VariableInfo, AttributeInfo, idToInfo,
    EventListener, eventHandler, addListener,
    createTopLevel, createModuleMenu, 
    getContextTarget, addModuleMenu, addContextCommand
)
import tkinter as tk

class GraphHandler(EventListener):
    @eventHandler
    def onStep(self, info: list[FrameInfo]):
        ...

addListener(GraphHandler())



menu = createModuleMenu(tearoff=False)
addModuleMenu(label="JsonView")



def open_viewer():
    target = getContextTarget()
    
    if target == "":
        return
    info = idToInfo(target)
    if info == None or type(info) == FrameInfo:
        return
    
    window = createTopLevel()
    window.title("Json Viewer")
    
    label = tk.Label(window)
    label.pack(side=tk.TOP)
    
    if type(info) == VariableInfo:
        label.config(text=f"{info.name} at frame #{info.depth}")
    if type(info) == AttributeInfo:
        label.config(text=f"{info.path} at frame #{info.depth}")
    
menu.add_command(label="Open New Viewer", command=open_viewer)
addContextCommand(label="View in Json Viewer", command=open_viewer)