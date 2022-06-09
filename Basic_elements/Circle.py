from typing import Callable
import pygame
from Basic_elements.Texts import Text
from Kompositum.BasicElement import BasicElement

class Circle(BasicElement):

    def __init__(self, pos_, radius_:int, color_, reactive_:bool , key_:str or None = "",action_:str or None = None) -> None:

        #X and Y Position on the surface
        self.key = key_
        self.pos = pos_    
        self.radius = radius_
        self.reactive = reactive_
        self.color = color_
        self.action = action_
        
        #creates mask for collision detection
        self.mask = pygame.Rect(self.pos[0]-self.radius,self.pos[1]-self.radius,self.radius*2,self.radius*2) 

    def draw(self, r:bool or None = True) -> None:
        if r:
            pygame.draw.circle(pygame.display.get_surface(),self.color,self.pos,self.radius,0)
    
    def create_text(self,content:str) -> Callable:
        return Text(content,(self.pos[0]-self.radius/2, self.pos[1]-(self.radius+20)),(173,216,230),pygame.font.SysFont('arial',20),"StarText"+content)
    
    def change_pos(self, position:tuple[int,int]):
        self.pos = position
    
    def update_color(self, new_color):
        self.color = new_color

    def update_color_reactive(self, case:bool):
        return 

    def check_collision(self) -> tuple[bool,Callable]:
        if self.reactive:
            pos = pygame.mouse.get_pos()
            return (self.mask.collidepoint(pos[0], pos[1]),self)
        return (False, self)


    def delete(self, r:bool or None = True):
        if r:
            c = self.color
            self.color = (0,0,0)
            self.draw()
            self.color = c

    def update_mask(self):
        self.mask = pygame.Rect(self.pos[0]-self.radius,self.pos[1]-self.radius,self.radius*2,self.radius*2)
        
    def get_action(self) -> int:
        return self.action

    def get_pos(self) -> tuple[int,int]:
        return self.pos
    
    def get_key(self) -> str:
        return self.key

    def set_key(self, new_key:str):
        self.key = new_key