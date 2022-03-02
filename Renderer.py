from typing import Tuple
import pygame
import json

from Stars import Star
from Lines import Line
from Texts import Text
from Buttons import Buttons

class Game_Render():
    
    def __init__(self) -> None:
        self.Star_list :Star = [] 
        self.Final_lines :Line = []
        self.Texts :Text =[]
        self.Star_in_use :Star = None
        self.Line_in_use :Line = None
        self.old_pos = pygame.mouse.get_pos()  

    def create_Star_constellation(self,path:str):
        self.load_json(path)
        self.Line_in_use=Line(self.Star_in_use.get_pos(),pygame.mouse.get_pos())

    def set_Star_to_use(self, index:int):
        self.Star_in_use=self.Star_list[index]
        

    def update_line_in_use(self):
        self.Line_in_use.delete()
        self.Line_in_use = Line(self.Star_in_use.get_pos(),pygame.mouse.get_pos())
        self.Line_in_use.draw()

    def load_json(self,path):
        file = open(path)
        data = json.load(file)
        file.close()
        content = data["constellation"][0]["constellation_name"]
        self.Texts.append(Text(content,((pygame.display.get_window_size()[0]/2)-(len(content)/2),30),(173,216,230),pygame.font.SysFont('inkfree',32)))

        for Stars in data:
            if(Stars[0:4]=="Star"):
                values = data[Stars][0]
                self.Star_list.append(Star(values["pos"],values["radius"],values["brightness"],values["active"]))
                self.Texts.append(Text(Stars[5:],self.fromat_pos_text(values["pos"],values["radius"]),(173,216,230),pygame.font.SysFont('arial',20)))
        self.set_Star_to_use(0)

    def fromat_pos_text(self, pos:Tuple[int,int], radius:int):
        return (pos[0]-radius/2, pos[1]-(radius+20))

    def repaint(self):
        #repaints all stored objects
        for lines in self.Final_lines:
            lines.draw()


        for stars in self.Star_list:
            stars.draw()

        for text in self.Texts:
            text.display_text()

        pygame.display.update()


    def update_line(self):
        pos = pygame.mouse.get_pos()
        if(pos != self.old_pos):
            self.old_pos=pos
            self.remove_line()
            self.Line_in_use.update_line(self.Star_in_use.get_pos(),pos)
            self.repaint()
        else:
            self.old_pos=pos

    
    def remove_line(self):
        self.Line_in_use.delete()

    def check_collision(self):
        Collisions = []
        for stars in self.Star_list:
            Collisions.append(stars.check_collision(self.old_pos))
        
        #print(Collisions)
        for element in Collisions:
            if element[0]:
                return element

        return (False,None)

    def Lock_line(self, star_to_lock:Star):
        pygame.display.get_surface().fill((0,0,0))
        self.repaint()
        self.Final_lines.append(self.Line_in_use.final_line(self.Star_in_use,star_to_lock))
        self.Star_in_use = star_to_lock
        self.Line_in_use = Line(star_to_lock.get_pos(),pygame.mouse.get_pos())

    def update_mouse_pos(self):
        self.old_pos = pygame.mouse.get_pos()

    def animation(self):
        for stars in self.Star_list:
            stars.animation()

class Game_Lobby():

    def __init__(self) -> None:
        self.screen  = pygame.display.get_surface()
        self.Buttons :pygame.surface = []
        self.Images : pygame.surface = []
        self.old_pos = pygame.mouse.get_pos()
    
    def create_lobby(self):
        self.Buttons.append(Buttons((self.screen.get_width()/2,self.screen.get_height()/2),(50,50)))

    def repaint(self):
        for buttons in self.Buttons:
            buttons.draw()

        for images in self.Images:
            images.draw()

    def check_collision(self):
        Collisions = []
        for buttons in self.Buttons:
            Collisions.append(buttons.check_collision(self.old_pos))
        
        for element in Collisions:
            if element[0]:
                return element

        return (False,None)
    
    def update_mouse_pos(self):
        self.old_pos = pygame.mouse.get_pos()



class Settings():

    def __init__(self) -> None:
        pass

class Level():

    def __init__(self) -> None:
        pass
