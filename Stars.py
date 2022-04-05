import pygame
from Texts import Text
from Circle import Circle

class Star():

    def __init__(self, pos_:tuple[int,int], radius_:int, bright:float, active_:bool, id_:int,text_:str) -> None:
        #1 dark 0 brightest
        self.id = id_
        self.brightness = bright  
        self.color = (255-(self.brightness*255),255-(self.brightness*255),255-(self.brightness*255))
        self.circle = Circle(pos_,radius_,self.color,active_)
        self.active = active_
        self.text:Text = self.create_text(text_)

    def draw(self):
        if(self.active):
            self.circle.draw()
            self.text.draw()
            pygame.display.update()


    def create_text(self,content:str):
        return Text(content,(self.circle.pos[0]-self.circle.radius/2, self.circle.pos[1]-(self.circle.radius+20)),(173,216,230),pygame.font.SysFont('arial',20))
        
    #gradually decreases the brightness until the star is invisible   
    def animation(self):
        while(self.brightness < 1):
            self.draw()
            self.clock.tick(5)
            self.update_color(self.brightness+0.05)
        self.update_color(1)
        self.draw()

    def update_color(self, bright:float):
        self.circle.color = (255-(bright*255),255-(bright*255),255-(bright*255))
        self.brightness = bright
    
    def change_pos(self, position:tuple[int,int]):
        self.circle.pos = position
    
    def check_collision(self, pos:tuple[int,int]):
        return (self.circle.check_collision(pos)[0],self)

    def get_pos(self):
        return self.circle.pos

    def change_status(self, status:bool):
        self.active = status