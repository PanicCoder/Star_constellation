from typing import Tuple
from Stars import Star
import pygame

class Line():

    def __init__(self, position_start:Tuple[int,int], position_end:Tuple[int,int]) -> None:
        self.pos_start = position_start
        self.pos_end = position_end
        self.color = (173,216,230) #Lightblue
        self.screen = pygame.display.get_surface()
        self.thickness = 5
        self.final = False

    def draw(self):
        pygame.draw.line(self.screen,self.color,self.pos_start,self.pos_end,self.thickness)
        pygame.display.update()
    
    def update_line(self, position_start:Tuple[int,int], position_end:Tuple[int,int]):
        self.pos_start = position_start
        self.pos_end = position_end
        self.draw()

    def final_line(self, Star_start:Star, Star_end:Star):
        self.pos_start = Star_start.get_pos()
        self.pos_end = Star_end.get_pos()
        self.final=True
        self.draw()
        return self
        
    def delete(self):
        pygame.draw.line(self.screen,(0,0,0),self.pos_start,self.pos_end,self.thickness)
        pygame.display.update()
    
    def get_final(self):
        return self.final
    