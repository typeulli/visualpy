import visualpy
visualpy.debug(str(visualpy.here / "visualizer.py"), True)

dictionary = {
    "widget": {
        "debug": "on",
        "window": {
            "title": "Sample Konfabulator Widget",
            "name": "main_window",
            "width": 500,
            "height": 500
        },
        "image": { 
            "src": "Images/Sun.png",
            "name": "sun1",
            "hOffset": 250,
            "vOffset": 250,
            "alignment": "center"
        },
        "text": {
            "data": "Click Here",
            "size": 36,
            "style": "bold",
            "name": "text1",
            "hOffset": 250,
            "vOffset": 100,
            "alignment": "center",
            "onMouseUp": "sun1.opacity = (sun1.opacity / 100) * 90;"
        }
    }
}    

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

visualpy.debugger.do_quit("")