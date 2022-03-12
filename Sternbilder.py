from Engine import Engine
import pygame
import os
pygame.init()
pygame.display.set_caption("Sternenbilder","Galaxy")
pygame.display.set_icon(pygame.image.load(os.path.join([x[0] for x in os.walk(os.getcwd())][1], "icon.png")))

if(__name__ == "__main__"):
    Engine().Loop()
    