from code import interact
from typing import Tuple
import pygame

class Image():

    def __init__(self, pos_:Tuple[int,int], image_:pygame.image, scale_:Tuple[int,int], interact_:bool, action_:str or None=None) -> None:
        self.screen = pygame.display.get_surface()
        self.pos = pos_
        self.image = image_
        self.scale = scale_
        self.interact = interact_
        self.mask =  pygame.Rect(self.pos[0],self.pos[1],self.scale[0],self.scale[1])
        self.action = action_

    def show_image(self):
        self.screen.blit(pygame.transform.scale(self.image,(self.scale)),self.pos)

    def check_collision(self, pos:Tuple[int,int]):
        return (self.mask.collidepoint(pos[0], pos[1]),self)