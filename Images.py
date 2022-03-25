from webbrowser import Konqueror
import pygame
import Konstants as konst
class Image():

    def __init__(self, pos_:tuple[int,int], image_:pygame.image, scale_:tuple[int,int], interact_:bool, action_:str or None=None) -> None:
        self.pos = pos_
        self.image = image_
        self.scale = scale_
        self.interact = interact_
        self.mask =  pygame.Rect(self.pos[0],self.pos[1],self.scale[0],self.scale[1])
        self.action = action_

    def change_image(self,new_image:pygame.image):
        self.image = new_image

    def draw(self):
        konst.screen.blit(pygame.transform.scale(self.image,(self.scale)),self.pos)

    def check_collision(self, pos:tuple[int,int]):
        if self.interact:
            return (self.mask.collidepoint(pos[0], pos[1]),self)
        return (False,self)