from typing import Callable
import pygame

from Kompositum.BasicElement import BasicElement
class Image(BasicElement):

    def __init__(self, pos_:tuple[int,int], image_:pygame.image, scale_:tuple[int,int], reactive_:bool, key_:str or None = "", action_:str or None=None) -> None:
        self.key = key_
        self.pos = pos_
        self.image = image_
        self.scale = scale_
        self.reactive = reactive_
        self.mask =  pygame.Rect(self.pos[0],self.pos[1],self.scale[0],self.scale[1])
        self.action = action_

    def change_image(self,new_image:pygame.image):
        self.image = new_image

    def draw(self):
        pygame.display.get_surface().blit(pygame.transform.scale(self.image,(self.scale)),self.pos)

    def update_color_reactive(self, case:bool):
        return 

    def check_collision(self) -> tuple[bool, Callable]:
        if self.reactive:
            pos = pygame.mouse.get_pos()
            return (self.mask.collidepoint(pos[0], pos[1]),self)
        return (False, self)
    
    def get_key(self) -> str:
        return self.key
    
    def set_key(self, new_key:str):
        self.key = new_key