import sys
import os
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from matplotlib.font_manager import json_dump
from Super_Classes.Screen import create_screen
create_screen()
import pygame
import json
import os
from Game_logic.Renderer import Settings


def get_file_path(file_name) -> str:
    for root, _, files in os.walk(".", topdown=False):
        for name in files:
            if name == file_name:
                return os.path.join(root, name)
settings = {}
with open(get_file_path("settings.json")) as file:
    settings = json.load(file)["settings"][0]

g = Settings(settings)
g.list.show_list()
Running = 1
slider_update = False
slider_value = None
while Running: 
    clock = pygame.time.Clock()             
    col = g.list.check_collision()
    pygame.event.get()
    if col[0]:
        
        if pygame.mouse.get_pressed()[0]:
            if col[1].get_key() == "Shutdown_Button":
                Running = 0
            
            with open(get_file_path("settings.json")) as file:
                content = json.load(file)
                if col[1].get_key().split("_")[:2] == ["Switch","circle"]:
                    key = col[1].get_key().split("_")[-1]
                    g.flip_switch_state(col[1],g.list.get_element_by_key(f"Switch_Button_of_{key}"))
                    g.list.repaint()
                    pygame.display.update()
                    content["settings"][0][col[1].get_action()] = not content["settings"][0][col[1].get_action()]
                    json_dump(content,get_file_path("settings.json"))

            if col[1].get_key().split("_")[:2] == ["Slider","circle"]:
                key = col[1].get_key().split("_")[-1]
                button = g.list.get_element_by_key(f"Slider_Button_of_{key}")
                key_2 = button.get_key().split("_")[-1]
                parent_b = g.list.get_element_by_key(key_2)
                g.update_slider(col[1],button, parent_b)
                slider_value = [round(g.slider_percentage(button, parent_b, col[1].get_pos()[0]),4), col[1].get_action()]
                slider_update  = True
                
    if slider_update and not pygame.mouse.get_pressed()[0] and slider_value != None:
        with open(get_file_path("settings.json")) as file:
            content = json.load(file)
            content["settings"][0][slider_value[1]] = slider_value[0]
            json_dump(content,get_file_path("settings.json"))
            slider_update = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Running = 0
            
    g.repaint()
    pygame.display.update()
    clock.tick(60)