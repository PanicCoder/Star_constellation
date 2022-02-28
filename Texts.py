from typing import Tuple
import pygame 

class Text():

    def __init__(self,content:str, position:Tuple[int,int], color:Tuple[int,int,int], size:int) -> None:
        self.screen = pygame.display.get_surface()
        self.content  = content
        self.pos  = position
        self.font_size = size
        self.font_color = color
        self.font = pygame.font.SysFont('inkfree',32)
        
    def display_text(self):
        text_surface = self.font.render(self.content,False,(173,216,230),self.font_size)
        self.screen.blit(text_surface,self.pos)
        pygame.display.update()

    def change_text(self, content:str):
        self.content = content
    
    def change_pos(self, new_pos:Tuple[int,int]):
        self.pos = new_pos
    
    def change_font(self, new_font:pygame.font.SysFont):
        self.font  = new_font