import sys
import os
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from Super_Classes.Screen import create_screen
create_screen()
import pygame
from Game_logic.Renderer import Level as lv
g = lv()
g.list.show_list()
Running = 1
while Running: 
    clock = pygame.time.Clock()             
    col = g.list.check_collision()
    if col[0]:
        if pygame.mouse.get_pressed()[0]:
            print("----------------------------------------")
            print(col[1].get_key())
            if col[1].get_key() == "Shutdown_Button":
                Running = 0
        else:
            col[1].update_color_reactive(True)
        #g.list.show_list()
    else:
        g.list.restore_original_color()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Running = 0
    g.repaint()
    pygame.display.update()
    clock.tick(60)