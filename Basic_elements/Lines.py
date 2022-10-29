from typing import Callable
from Basic_elements.Stars import Star
import math
import pygame

from Kompositum.BasicElement import BasicElement

class Line(BasicElement):

    def __init__(self, position_start:tuple[int,int], position_end:tuple[int,int], thickness:float,key_:str or None = "") -> None:
        self.key = key_
        self.pos_start = position_start
        self.pos_end = position_end
        #self.color = (0,0,139) #Darkblue
        self.color = (120,180,230) #Lightblue
        self.thickness = math.floor(thickness)
        self.final = False
        self.render = True

    def draw(self):
        pygame.draw.line(pygame.display.get_surface(),self.color,self.pos_start,self.pos_end,self.thickness)

    def update_pos(self, s_pos,end_pos):
        self.pos_start = s_pos
        self.pos_end = end_pos
        
    def update_color_reactive(self, case:bool):
        return 

    def final_line(self, Star_start:Star, Star_end:Star) -> Callable:
        self.update_pos(Star_start.get_pos(),Star_end.get_pos())
        self.key = f"Line {Star_start.get_key()}-{Star_end.get_key()}"
        self.final=True
        return self
    
    def get_final(self) -> bool:
        return self.final
    
    def get_key(self) -> str:
        return self.key

    def check_collision(self) -> tuple[Callable, bool]:
        return (False,self)

    def set_key(self, new_key:str):
        self.key = new_key
    
    def set_render(self):
        self.render = not self.render

    def get_render(self) -> bool:
        return self.render