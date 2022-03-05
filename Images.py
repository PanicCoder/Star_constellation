from typing import Tuple
import pygame

class Image():

    def __init__(self, pos_:Tuple[int,int], image_:pygame.image, scale_:Tuple[int,int]) -> None:
        self.screen = pygame.display.get_surface()
        self.pos = pos_
        self.image = image_
        self.scale = scale_

    def show_image(self):
        self.screen.blit(pygame.transform.scale(self.image,(self.scale)),self.pos)