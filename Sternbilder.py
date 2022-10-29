import pygame
from Game_logic.Engine import Engine
    
if(__name__ == "__main__"):
    pygame.init()
    pygame.mixer.init()
    pygame.display.set_caption("Sternenbilder","Galaxy")
    #pygame.display.set_mode((1280,800), pygame.DOUBLEBUF | pygame.RESIZABLE | pygame.HWSURFACE, vsync=1)
    pygame.display.set_mode((1750,1000), pygame.DOUBLEBUF | pygame.RESIZABLE | pygame.HWSURFACE, vsync=1)
    Engine().Loop() 