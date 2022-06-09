import sys
import os
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from Super_Classes.Screen import create_screen
create_screen()
import pygame
from Game_logic.Renderer import Game_Render


g = Game_Render("Adler")
g.list.show_list()
Running = True
pygame.display.set_mode((1750,1000), pygame.DOUBLEBUF | pygame.RESIZABLE | pygame.HWSURFACE, vsync=1)
while Running: 
    clock = pygame.time.Clock()
    
    
                    
                    
    col = g.list.check_collision()
    if col[0] and pygame.mouse.get_pressed()[0]:
        print("----------------------------------------")
        g.Lock_line(g.list.get_element_by_key(col[1].get_key()))
        g.list.show_list()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DELETE:
                if g.connected_stars:
                    id = g.connected_stars[-1]
                    if id in g.Instructions:
                        g.update_instroctions(id)
                    del g.connected_stars[-1]
                    g.list.delete_element(f"Line Star_{id[0]}-Star_{id[1]}")
                    g.set_Star_to_use(f"Star_{id[0]}")
                else:
                    g.set_Star_to_use("Star_1") 
                g.update_line_in_use()
                #self.freeze = False
                #self.r.repaint(False)
                    

            #only triggers if the keys 0-9 are pressed on the keyboard
            inp = event.key-48
            if inp >-1 and g.list.get_element_by_key(f"Star_{inp}") != None:
                g.set_Star_to_use(f"Star_{inp}") 
                g.update_line_in_use()

            if event.key == pygame.K_RIGHT:
                if g.list.get_element_by_key(f"Star_{str(int(g.Star_in_use.id)+1)}") != None:
                   g.set_Star_to_use(f"Star_{str(int(g.Star_in_use.id)+1)}")
                else:
                    g.set_Star_to_use("Star_1")
                g.update_line_in_use()
                
            elif event.key == pygame.K_LEFT:
                if g.list.get_element_by_key(f"Star_{str(int(g.Star_in_use.id)-1)}") != None:
                   g.set_Star_to_use(f"Star_{str(int(g.Star_in_use.id)-1)}")
                else:
                    indx = 0
                    last_star = g.list.get_element_by_key(f"Star_{indx+1}")
                    while last_star != None:
                        indx+=1
                        last_star = g.list.get_element_by_key(f"Star_{indx+1}")
                        
                    g.set_Star_to_use(g.list.get_element_by_key(f"Star_{indx}").get_key())
                g.update_line_in_use()

        if g.completed_star_constellation(None):
            print("complete")

    g.repaint()
    g.update_line_in_use()
    pygame.display.update()
    clock.tick(60)
    