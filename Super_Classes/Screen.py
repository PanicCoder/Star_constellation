import pygame
def create_screen():    
    pygame.init()
    pygame.mixer.init()
    pygame.display.set_caption("Sternenbilder","Galaxy")
    #pygame.display.set_mode((1280,800), pygame.DOUBLEBUF | pygame.RESIZABLE | pygame.HWSURFACE, vsync=1)
    pygame.display.set_mode((1750,1000), pygame.DOUBLEBUF | pygame.RESIZABLE | pygame.HWSURFACE, vsync=1)

class Screen():

    def __init__(self) -> None:
        self.screen = pygame.display.get_surface()
        self.mx = self.screen.get_width()/1750
        self.my = self.screen.get_height()/1000
        self.mt = self.mx/2 + self.my/2

    def update_window_scale(self):
        self.mx = self.screen.get_width()/1750
        self.my = self.screen.get_height()/1000
        self.mt = self.mx/2 + self.my/2

