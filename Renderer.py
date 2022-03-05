from pickle import TUPLE
from tkinter import Image
from typing import Tuple
import pygame
import json

from Stars import Star
from Lines import Line
from Texts import Text
from Buttons import Buttons
from Images import Image

class Game_Render():
    
    def __init__(self) -> None:
        self.Star_list :Star = [] 
        self.Final_lines :Line = []
        self.Texts :Text =[]
        self.Star_in_use :Star = None
        self.Line_in_use :Line = None
        self.old_pos = pygame.mouse.get_pos()  
        self.screen = pygame.display.get_surface()
        self.old_dimensions = (self.screen.get_width(),self.screen.get_height())

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
        self.check_resize((self.screen.get_width(),self.screen.get_height()))
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

    def check_resize(self, new_dimensions:Tuple[int,int]):
        flag = False
        if self.old_dimensions[0] != new_dimensions[0] or self.old_dimensions[1] != new_dimensions[1]:
            self.__init__()
            self.old_dimensions = new_dimensions
            flag = not flag
            self.create_Star_constellation(r".\Starfiles\Adler.json")

        if flag:
            self.repaint()

    
class Game_Lobby():

    def __init__(self) -> None:
        self.screen  = pygame.display.get_surface()
        self.Buttons :Buttons = []
        self.Images : Image = []
        self.Texts :Text = []
        self.old_pos = pygame.mouse.get_pos()
        self.old_dimensions = (self.screen.get_width(),self.screen.get_height())
    
    def create_lobby(self):
        text_size = pygame.font.SysFont("arial",100).size("Sternbilder")
        caption = Text("Sternbilder",((self.screen.get_width()/2-text_size[0]/2,50)),(194, 194, 214),pygame.font.SysFont("arial",100))
        self.Texts.append(caption)
        self.Buttons.append(Buttons((caption.pos[0],caption.pos[1]+text_size[1]-10),(text_size[0],4),(0,0,0),False))

        i = 75
        for k in range(4):
            self.Buttons.append(Buttons((caption.pos[0]-50,caption.pos[1]+text_size[1]+i),(text_size[0]+100,125),(121,92,174),True,k))
            i+=200

        texts = ["Play","Continue","Level","Settings"]
        for k in range(4):
            text_size = pygame.font.SysFont("arial",50).size(texts[k])
            button = self.Buttons[k+1]
            button.add_text(Text(texts[k],(button.pos[0]+button.dimensions[0]/2-text_size[0]/2,button.pos[1]+button.dimensions[1]/2-text_size[1]/2),(0,0,0),pygame.font.SysFont("arial",50)))
        self.Images.append(Image((0,0),pygame.image.load(r".\Images\galaxy.jpg"),(self.screen.get_width(),self.screen.get_height())))

    def repaint(self):
        self.check_resize((self.screen.get_width(),self.screen.get_height()))
        for images in self.Images:
            images.show_image()

        for buttons in self.Buttons:
            buttons.draw()

        for text in self.Texts:
            text.display_text()
        
        

    def check_collision(self):
        Collisions = []
        for buttons in self.Buttons:
            if buttons.reactive:
                Collisions.append(buttons.check_collision(self.old_pos))
        
        for element in Collisions:
            if element[0]:
                return element

        return (False,None)
    
    def update_mouse_pos(self):
        self.old_pos = pygame.mouse.get_pos()

    def check_resize(self, new_dimensions:Tuple[int,int]):
        flag = False
        if self.old_dimensions[0] != new_dimensions[0] or self.old_dimensions[1] != new_dimensions[1]:
            self.__init__()
            self.old_dimensions = new_dimensions
            flag = not flag
            self.create_lobby()

        if flag:
            self.repaint()
        

class Settings():

    def __init__(self) -> None:
        pass

class Level():

    def __init__(self) -> None:
        pass
