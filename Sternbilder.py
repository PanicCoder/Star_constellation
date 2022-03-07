from Engine import Engine
import pygame

pygame.init()
pygame.display.set_caption("Sternenbilder","Galaxy")
pygame.display.set_icon(pygame.image.load(r".\Images\icon.png"))

if(__name__ == "__main__"):
    Engine().Loop()
    