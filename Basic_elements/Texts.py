import pygame
from typing import Callable
from Kompositum.BasicElement import BasicElement 

class Text(BasicElement):

    def __init__(self,content:str, position:tuple[int,int], color:tuple[int,int,int], font_:pygame.font.SysFont, key_:str or None = "", moveable_:bool or None = False) -> None:
        self.key = key_
        self.content  = content
        self.pos  = position
        self.font_color = color
        self.font = font_
        self.moveable = moveable_
        self.render = True
        
    def draw(self):
        text_surface = self.font.render(self.content,False,self.font_color)
        pygame.display.get_surface().blit(text_surface,self.pos)
    
    def mvdraw(self, inter:pygame.Surface):
        text_surface = self.font.render(self.content,False,self.font_color)
        inter.blit(text_surface,self.pos)

    def change_text(self, content:str):
        self.content = content
    
    def change_pos(self, new_pos:tuple[int,int]):
        self.pos = new_pos
    
    def update_mask(self, pos):
        return

    def get_pos(self):
        return self.pos
    
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

    def set_render(self):
        self.render = not self.render

    def get_render(self) -> bool:
        return self.render