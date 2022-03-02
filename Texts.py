from typing import Tuple
import pygame 

class Text():

    def __init__(self,content:str, position:Tuple[int,int], color:Tuple[int,int,int], font_:pygame.font.SysFont) -> None:
        self.screen = pygame.display.get_surface()
        self.content  = content
        self.pos  = position

        self.font_color = color
        self.font = font_
        
    def display_text(self):
        text_surface = self.font.render(self.content,False,self.font_color)
        self.screen.blit(text_surface,self.pos)
        pygame.display.update()

    def change_text(self, content:str):
        self.content = content
    
    def change_pos(self, new_pos:Tuple[int,int]):
        self.pos = new_pos
    
    def change_font(self, new_font:pygame.font.SysFont):
        self.font  = new_font