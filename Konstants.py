import platform
import pygame
from Renderer import *
from Interface import In_common

Height = 1000
Width = 1280
Height = 700
screen = pygame.display.set_mode((Width,Height),pygame.RESIZABLE)
In_common_level = In_common(Level)
In_common_game = In_common(Game_Render)
In_common_lobby = In_common(Game_Lobby)
In_common_setting = In_common(Settings)
mx = screen.get_width()/1750
my = screen.get_height()/1000
mt = mx/2 + my/2
sep = "\\" if platform.system() == 'Windows' else "/"
icon = "."+sep+"Images"+sep+"icon.png"
galaxy = "."+sep+"Images"+sep+"galaxy.jpg"
exit = "."+sep+"Images"+sep+"Exit.png"
level = "."+sep+"Images"+sep+"level.png"
settings = "."+sep+"Images"+sep+"settings.png"
settings_json = "."+sep+"Settings"+sep+"settings.json"
level_json = "."+sep+"Starfiles"+sep
switch = ["."+sep+"Images"+sep+"offswitch.png","."+sep+"Images"+sep+"onswitch.png"]