from typing import Callable
import pygame
from Kompositum.BasicElement import BasicElement

class Image(BasicElement):

    def __init__(self, pos_:tuple[int,int], image_path:pygame.image, scale_:tuple[int,int], reactive_:bool, key_:str or None = "", action_:str or None=None, moveable_:bool or None = False) -> None:
        self.key = key_
        self.pos = pos_
        self.image = self.create_image(image_path)
        self.scale = scale_
        self.reactive = reactive_
        self.moveable = moveable_
        self.moveable = moveable_
        self.mask =  pygame.Rect(self.pos[0],self.pos[1],self.scale[0],self.scale[1])
        self.action = action_
        self.render = True

    def change_image(self,new_image_path:str):
        self.image = pygame.image.load(new_image_path).convert_alpha()

    def create_image(self, image_path):
        return pygame.image.load(image_path).convert_alpha()

    def draw(self):
        pygame.display.get_surface().blit(pygame.transform.scale(self.image,(self.scale)),self.pos)
    
    def mvdraw(self, inter:pygame.Surface):
        inter.blit(pygame.transform.scale(self.image,(self.scale)),self.pos)
    
    def change_pos(self, position:tuple[int,int]) -> None:
        self.pos = position
        self.mask = pygame.Rect(self.pos[0],self.pos[1],self.scale[0],self.scale[1])
    
    def update_mask(self, pos_):
        self.mask = pygame.Rect(pos_[0],pos_[1],self.scale[0],self.scale[1])

    def update_color_reactive(self, case:bool):
        return 

    def check_collision(self) -> tuple[bool, Callable]:
        if self.reactive:
            pos = pygame.mouse.get_pos()
            return (self.mask.collidepoint(pos[0], pos[1]),self)
        return (False, self)
    
    def get_pos(self):
        return self.pos

    def set_render(self):
        self.render = not self.render

    def get_render(self) -> bool:
        return self.render
        
    def get_key(self) -> str:
        return self.key
    
    def set_key(self, new_key:str):
        self.key = new_key