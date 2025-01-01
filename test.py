import visual
visual.debug(str(visual.here / "visual_window.py"), True)

class Class():
    def __init__(self):
        self.number = 3
instance = Class()

instance.number = 4




a = 3

b = a + 6

del a

b = b - 1

def print_the_things(number: int, text: str, list_: list):

    print(f"Number: {number}, Text: {text}, List: {list_}")
    
    if number < 11:
        print_the_things(number+1, text, list_)

print_the_things(
    number=10,
    text="Blame and lies, contradictions arise",
    list_=[1, 2, 3]
)

c = "c" 
c = c + "d"

visual.debugger.do_quit("")