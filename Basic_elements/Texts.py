import pygame
from typing import Callable
from Kompositum.BasicElement import BasicElement 

class Text(BasicElement):

    def __init__(self,content:str, position:tuple[int,int], color:tuple[int,int,int], font_:pygame.font.SysFont, key_:str or None = "") -> None:
        self.key = key_
        self.content  = content
        self.pos  = position
        self.font_color = color
        self.font = font_
        
    def draw(self):
        text_surface = self.font.render(self.content,False,self.font_color)
        pygame.display.get_surface().blit(text_surface,self.pos)

    def change_text(self, content:str):
        self.content = content
    
    def change_pos(self, new_pos:tuple[int,int]):
        self.pos = new_pos
    
    def change_color(self,color):
        self.font_color = color

    def update_color_reactive(self, case:bool):
        return 
        
    def change_font(self, new_font:pygame.font.SysFont):
        self.font  = new_font

    def get_size(self) -> tuple[int,int]:
        return self.font.size(self.content)
    
    def get_key(self) -> str:
        return self.key
    
    def check_collision(self) -> tuple[Callable, bool]:
        return (False,self)

    def set_key(self, new_key:str):
        self.key = new_key