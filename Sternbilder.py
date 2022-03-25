from Engine import Engine
import pygame
import Konstants as paths


pygame.init()
pygame.display.set_caption("Sternenbilder","Galaxy")
e = Engine()
pygame.display.set_icon(pygame.image.load(paths.icon))

if(__name__ == "__main__"):
    e.Loop() 