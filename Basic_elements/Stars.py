from Basic_elements.Texts import Text
from Basic_elements.Circle import Circle

class Star(Circle):

    def __init__(self, pos_:tuple[int,int], radius_:int, bright:float, active_:bool, id_:int,text_:str, key:str or None = "") -> None:
        #0 dark 1 brightest
        super().__init__(pos_,radius_,(255-(bright*255),255-(bright*255),255-(bright*255)),active_, key)
        self.id = id_
        self.active = active_
        self.text:Text = self.create_text(text_)

    def draw(self):
        if(self.active):
            super().draw()
            self.text.draw()

    def change_status(self, status:bool):
        self.active = status
