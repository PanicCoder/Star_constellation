import pygame
import json
import itertools
import os

from Stars import Star
from Lines import Line
from Texts import Text
from Buttons import Buttons
from Images import Image
from Interface import In_common


class Game_Render():
    
    def __init__(self, name_:str) -> None:
        self.id = 0
        self.Star_list :Star = [] 
        self.Final_lines :Line = []
        self.Texts :Text =[]
        self.Images :Image = []
        self.Buttons:Buttons = []
        self.Star_in_use :Star = None
        self.Line_in_use :Line = None
        self.old_pos = pygame.mouse.get_pos()  
        self.in_common = In_common(self)
        self.name = name_
        self.create(os.path.join([x[0] for x in os.walk(os.getcwd())][3], str(self.name)+'.json'))

    def create(self,path:str):
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
        text = str(data["Explanation_text"][0]["text"])
        latin_name = data["Explanation_text"][0]["Latin_name"]
        content = "Sternbild: "+data["constellation"][0]["constellation_name"]
        headline = self.in_common.create_Headline(content,32,'inkfree')
        self.Texts.append(headline[0])
        

        for Stars in data:
            if(Stars[0:4]=="Star"):
                values = data[Stars][0]
                self.Star_list.append(Star(values["pos"],values["radius"],values["brightness"],values["active"]))
                self.Texts.append(Text(Stars[5:],self.fromat_pos_text(values["pos"],values["radius"]),(173,216,230),pygame.font.SysFont('arial',20)))
        dimension = (700,1700)
        t = itertools.chain(self.Texts,self.in_common.format_text(text,dimension,30,(pygame.display.get_surface().get_width()-600,50)))
        self.Texts = list(t)
        self.set_Star_to_use(0)

    def fromat_pos_text(self, pos:tuple[int,int], radius:int):
        return (pos[0]-radius/2, pos[1]-(radius+20))

    def repaint(self):
        self.in_common.repaint([self.Images,self.Final_lines,self.Buttons,self.Star_list,self.Texts])


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
        return self.in_common.check_collision(self.Star_list,self.old_pos)

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

    def __init__(self,name:str) -> None:
        self.screen  = pygame.display.get_surface()
        self.id = 1
        self.Buttons :Buttons = []
        self.Images : Image = []
        self.Texts :Text = []
        self.level_name = name
        self.old_pos = pygame.mouse.get_pos()
        self.in_common = In_common(self)
        self.create()
        self.choosen_level(self.level_name)
    
    def create(self):
        Headlilne = self.in_common.create_Headline("Sternbilder",100)
        caption = Headlilne[0]
        text_size = Headlilne[2]
        self.Texts.append(caption)
        self.Buttons.append(Headlilne[1])

        i = 75
        for k in range(4):
            self.Buttons.append(Buttons((caption.pos[0]-50,caption.pos[1]+text_size[1]+i),(text_size[0]+100,125),(121,92,174),True,k))
            i+=200

        texts = ["Play","Continue","Level","Settings"]
        for k in range(4):
            text_size = pygame.font.SysFont("arial",50).size(texts[k])
            button = self.Buttons[k+1]
            button.add_text(Text(texts[k],(button.pos[0]+button.dimensions[0]/2-text_size[0]/2,button.pos[1]+button.dimensions[1]/2-text_size[1]/2),(0,0,0),pygame.font.SysFont("arial",50)))
        self.Images.append(self.in_common.set_background(os.path.join([x[0] for x in os.walk(os.getcwd())][1], "galaxy.jpg")))
        self.Images.append(self.in_common.create_shutdown_button())
        

    def choosen_level(self, level_name:str):
        text = self.in_common.find_text_object(self.level_name,self.Texts)
        button = self.in_common.find_button_by_text("Level",self.Buttons)
        text_s = pygame.font.SysFont("arial",30).size(level_name)   
        if text != None:
            text.change_text(level_name)   
            text.change_pos((button.pos[0]+button.dimensions[0]/2-text_s[0]/2,button.pos[1]+button.dimensions[1]-(text_s[1]+5)))
        else:
            self.Texts.append(Text(level_name,(button.pos[0]+button.dimensions[0]/2-text_s[0]/2,button.pos[1]+button.dimensions[1]-(text_s[1]+5)),(0,0,0),pygame.font.SysFont("arial",30)))
        self.level_name = level_name
        
    def repaint(self):
        self.in_common.repaint([self.Images,self.Buttons,self.Texts])

    def check_collision(self):
        return self.in_common.check_collision(self.Buttons,self.old_pos)
    
    def check_collision_images(self):
        return self.in_common.check_collision(self.Images,self.old_pos)

    def update_mouse_pos(self):
        self.old_pos = pygame.mouse.get_pos()

    def get_level_text(self):
        return self.in_common.find_text_object(self.level_name,self.Texts)

class Level():

    def __init__(self) -> None:
        self.screen = pygame.display.get_surface()
        self.id = 2
        self.Buttons:Buttons = []
        self.Texts :Text = []
        self.Images :Image = []
        self.old_pos = pygame.mouse.get_pos()  
        self.in_common = In_common(self) 
        self.create()

    def create(self):
        Headlilne = self.in_common.create_Headline("Level",100)
        caption = Headlilne[0]
        text_size = Headlilne[2]
        self.Texts.append(caption)
        self.Buttons.append(Headlilne[1])
        self.Images.append(self.in_common.set_background(os.path.join([x[0] for x in os.walk(os.getcwd())][1], "Level.png")))
        self.Images.append(self.in_common.create_shutdown_button())

        i = 75
        for k in range(5):
            self.Buttons.append(Buttons((caption.pos[0]-250,caption.pos[1]+text_size[1]+i),(text_size[0]+500,125),(7,45,99),True,k))
            i+=135
        texts = ["Adler","Andromeda","Becher","Bootes","Cassiopeia"]
        for k in range(5):
            text_size = pygame.font.SysFont("arial",50).size(texts[k])
            button = self.Buttons[k+1]
            button.add_text(Text(texts[k],(button.pos[0]+button.dimensions[0]/2-text_size[0]/2,button.pos[1]+button.dimensions[1]/2-text_size[1]/2),(0,0,0),pygame.font.SysFont("arial",50)))

    def repaint(self):
        self.in_common.repaint([self.Images,self.Buttons,self.Texts])

    def update_mouse_pos(self):
        self.old_pos = pygame.mouse.get_pos()

    def check_collision(self):
        return self.in_common.check_collision(self.Buttons,self.old_pos)
    
    def check_collision_images(self):
        return self.in_common.check_collision(self.Images,self.old_pos)

class Settings():

    def __init__(self) -> None:
        self.screen = pygame.display.get_surface()
        self.id = 3
        self.Buttons:Buttons = []
        self.Texts :Text = []
        self.Images :Image = []
        self.old_pos = pygame.mouse.get_pos()  
        self.in_common = In_common(self) 
        self.create()

    def create(self):
        Headlilne = self.in_common.create_Headline("Settings",100)
        self.Texts.append(Headlilne[0])
        self.Buttons.append(Headlilne[1])
        self.Images.append(self.in_common.create_shutdown_button())

    def repaint(self):
        self.in_common.repaint([self.Images,self.Buttons,self.Texts])

    def check_collision(self):
        return self.in_common.check_collision(self.Buttons,self.old_pos)
    
    def update_mouse_pos(self):
        self.old_pos = pygame.mouse.get_pos()
        
    def check_collision_images(self):
        return self.in_common.check_collision(self.Images,self.old_pos)
