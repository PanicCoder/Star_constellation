from typing import Tuple
import pygame

class Buttons():

    def __init__(self, pos_:Tuple[int,int], dimensions_:Tuple[int,int], color_, reactive_:bool, action_:int or None=None) -> None:

        #X and Y Position on the surface
        self.pos = pos_    
        self.dimensions = dimensions_
        self.clock = pygame.time.Clock()
        self.color = color_
        self.screen = pygame.display.get_surface()
        self.reactive = reactive_

        #gives back the action to perform
        self.action = action_
        #creates mask for collision detection
        self.mask = pygame.Rect(self.pos[0],self.pos[1],self.dimensions[0],self.dimensions[1]) 

    def draw(self):
        pygame.draw.rect(self.screen,self.color,(self.pos,self.dimensions),0)
        pygame.display.update()

    def update_color(self, color_:Tuple[int,int,int]):
        self.color = color_
    
    def change_pos(self, position:Tuple[int,int]):
        self.pos = position
    
    def check_collision(self, pos:Tuple[int,int]):
        return (self.mask.collidepoint(pos[0], pos[1]),self)

    def get_pos(self):
        return self.pos

    def get_action(self):
        return self.action
