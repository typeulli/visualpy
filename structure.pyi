from abc import ABCMeta
from tkinter.font import Font
from typing import Literal, ParamSpec, TypeAlias, TypeVar, Generic, Callable, overload, Any
import tkinter as tk
import _tkinter as _tk
from dataclasses import dataclass



@dataclass(frozen=True)
class FrameInfo:
    filename: str
    line: int
    funcname: str
    
    id: str
    
@dataclass(frozen=True)
class VariableInfo:
    depth: int
    path: str
    
    id: str
    name: str
    
    
@dataclass(frozen=True)
class AttributeInfo:
    depth: int
    parentId: str
    path: str
    
    id: str
    name: str

def idToInfo(id: str) -> FrameInfo | VariableInfo | AttributeInfo | None: ...


def requestData(depth: int, target: str, serialize: bool = True) -> object: ...


def setDisplayName(name: str) -> None: ...

def createTopLevel(
    cnf: dict[str, Any] | None = {},
    *,
    background: str = ...,
    bd: tk._ScreenUnits = 0,
    bg: str = ...,
    border: tk._ScreenUnits = 0,
    borderwidth: tk._ScreenUnits = 0,
    class_: str = "Toplevel",
    colormap: tk.Misc | Literal['new', ''] = "",
    container: bool = False,
    cursor: tk._Cursor = "",
    height: tk._ScreenUnits = 0,
    highlightbackground: str = ...,
    highlightcolor: str = ...,
    highlightthickness: tk._ScreenUnits = 0,
    menu: tk.Menu = ...,
    name: str = ...,
    padx: tk._ScreenUnits = 0,
    pady: tk._ScreenUnits = 0,
    relief: tk._Relief = "flat",
    screen: str = "",
    takefocus: tk._TakeFocusValue = 0,
    use: int = ...,
    visual: str | tuple[str, int] = "",
    width: tk._ScreenUnits = 0
) -> tk.Toplevel: ...


_FontDescription: TypeAlias = (
    str  # "Helvetica 12"
    | Font  # A font object constructed in Python
    | list[Any]  # ["Helvetica", 12, BOLD]
    | tuple[str]  # ("Liberation Sans",) needs wrapping in tuple/list to handle spaces
    | tuple[str, int]  # ("Liberation Sans", 12)
    | tuple[str, int, str]  # ("Liberation Sans", 12, "bold")
    | tuple[str, int, list[str] | tuple[str, ...]]  # e.g. bold and italic
    | _tk.Tcl_Obj  # A font object constructed in Tcl
)

def createModuleMenu(
    cnf: dict[str, Any] | None = {},
    *,
    activebackground: str = ...,
    activeborderwidth: tk._ScreenUnits = ...,
    activeforeground: str = ...,
    background: str = ...,
    bd: tk._ScreenUnits = ...,
    bg: str = ...,
    border: tk._ScreenUnits = ...,
    borderwidth: tk._ScreenUnits = ...,
    cursor: tk._Cursor = "arrow",
    disabledforeground: str = ...,
    fg: str = ...,
    font: _FontDescription = ...,
    foreground: str = ...,
    name: str = ...,
    postcommand: Callable[[], object] | str = "",
    relief: tk._Relief = ...,
    selectcolor: str = ...,
    takefocus: tk._TakeFocusValue = 0,
    tearoff: bool | Literal[0, 1] = 1,
    tearoffcommand: Callable[[str, str], object] | str = "",
    title: str = "",
    type: Literal['menubar', 'tearoff', 'normal'] = "normal"
) -> tk.Menu: ...

def addModuleMenu(
    cnf: dict[str, Any] | None = {},
    *,
    accelerator: str = ...,
    activebackground: str = ...,
    activeforeground: str = ...,
    background: str = ...,
    bitmap: str = ...,
    columnbreak: int = ...,
    command: Callable[[], object] | str = ...,
    compound: tk._Compound = ..., 
    font: _FontDescription = ...,
    foreground: str = ...,
    hidemargin: bool = ...,
    image: tk._ImageSpec = ...,
    label: str = ...,
    state: Literal['normal'] | Literal['active'] | Literal['disabled'] = ...,
    underline: int = ...
) -> None: ...

def getContextTarget() -> str: ...
def addContextCascade(
    cnf: dict[str, Any] | None = {},
    *,
    accelerator: str = ...,
    activebackground: str = ...,
    activeforeground: str = ...,
    background: str = ...,
    bitmap: str = ...,
    columnbreak: int = ...,
    command: Callable[[], object] | str = ...,
    compound: tk._Compound = ...,
    font: _FontDescription = ...,
    foreground: str = ...,
    hidemargin: bool = ...,
    image: tk._ImageSpec = ...,
    label: str = ...,
    menu: tk.Menu = ...,
    state: Literal['normal', 'active', 'disabled'] = ...,
    underline: int = ...
) -> None: ...
def addContextCheckbutton(
    cnf: dict[str, Any] | None = {},
    *,
    accelerator: str = ...,
    activebackground: str = ...,
    activeforeground: str = ...,
    background: str = ...,
    bitmap: str = ...,
    columnbreak: int = ...,
    command: Callable[[], object] | str = ...,
    compound: tk._Compound = ...,
    font: _FontDescription = ...,
    foreground: str = ...,
    hidemargin: bool = ...,
    image: tk._ImageSpec = ...,
    indicatoron: bool = ...,
    label: str = ...,
    offvalue: Any = ...,
    onvalue: Any = ...,
    selectcolor: str = ...,
    selectimage: tk._ImageSpec = ...,
    state: Literal['normal', 'active', 'disabled'] = ...,
    underline: int = ...,
    variable: tk.Variable = ...
) -> None: ...
def addContextCommand(
    cnf: dict[str, Any] | None = {},
    *,
    accelerator: str = ...,
    activebackground: str = ...,
    activeforeground: str = ...,
    background: str = ...,
    bitmap: str = ...,
    columnbreak: int = ...,
    command: Callable[[], object] | str = ...,
    compound: tk._Compound = ...,
    font: _FontDescription = ...,
    foreground: str = ...,
    hidemargin: bool = ...,
    image: tk._ImageSpec = ...,
    label: str = ...,
    state: Literal['normal', 'active', 'disabled'] = ...,
    underline: int = ...
) -> None: ...
def addContextRadiobutton(
    cnf: dict[str, Any] | None = {},
    *,
    accelerator: str = ...,
    activebackground: str = ...,
    activeforeground: str = ...,
    background: str = ...,
    bitmap: str = ...,
    columnbreak: int = ...,
    command: Callable[[], object] | str = ...,
    compound: tk._Compound = ...,
    font: _FontDescription = ...,
    foreground: str = ...,
    hidemargin: bool = ...,
    image: tk._ImageSpec = ...,
    indicatoron: bool = ...,
    label: str = ...,
    selectcolor: str = ...,
    selectimage: tk._ImageSpec = ...,
    state: Literal['normal', 'active', 'disabled'] = ...,
    underline: int = ...,
    value: Any = ...,
    variable: tk.Variable = ...
) -> None: ...
def addContextSeparator(
    cnf: dict[str, Any] | None = {},
    *,
    background: str = ...
) -> None: ...



P = ParamSpec("P")
V = TypeVar("V")
class EventHandler(Generic[P, V], metaclass=ABCMeta):
    def __init__(self, fn: Callable[P, V], order: int=0): ...
    def getOrder(self) -> int: ...
    def __call__(self, *args: P.args, **kwds: P.kwargs) -> V: ...

TEventListener = TypeVar("TEventListener", bound="EventListener")
class EventListener(Generic[TEventListener]):
    onStep: EventHandler[[TEventListener, list[FrameInfo]], None]
    
@overload
def eventHandler(order: int = 0) -> Callable[
        [Callable[P, V]], EventHandler[P, V]
    ]: ...
@overload
def eventHandler(function: Callable[P, V]) -> EventHandler[P, V]: ...

def addListener(listener: EventListener) -> None: ...

def call(target: str) -> None: ...





