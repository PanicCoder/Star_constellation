import pygame
import json

from Stars import Star
from Lines import Line
from Texts import Text
from Buttons import Buttons
from Images import Image
from Interface import In_common


class Game_Render():
    
    def __init__(self) -> None:
        self.Star_list :Star = [] 
        self.Final_lines :Line = []
        self.Texts :Text =[]
        self.Star_in_use :Star = None
        self.Line_in_use :Line = None
        self.old_pos = pygame.mouse.get_pos()  
        self.in_common = In_common(self)
        self.create(r".\Starfiles\Adler.json")

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
        content = data["constellation"][0]["constellation_name"]
        self.Texts.append(Text(content,((pygame.display.get_window_size()[0]/2)-(len(content)/2),30),(173,216,230),pygame.font.SysFont('inkfree',32)))

        for Stars in data:
            if(Stars[0:4]=="Star"):
                values = data[Stars][0]
                self.Star_list.append(Star(values["pos"],values["radius"],values["brightness"],values["active"]))
                self.Texts.append(Text(Stars[5:],self.fromat_pos_text(values["pos"],values["radius"]),(173,216,230),pygame.font.SysFont('arial',20)))
        self.set_Star_to_use(0)

    def fromat_pos_text(self, pos:tuple[int,int], radius:int):
        return (pos[0]-radius/2, pos[1]-(radius+20))

    def repaint(self):
        self.in_common.repaint([self.Final_lines,self.Star_list,self.Texts])


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

    def check_resize(self, new_dimensions:tuple[int,int]):
        self.in_common.check_resize(new_dimensions)
    
class Game_Lobby():

    def __init__(self) -> None:
        self.screen  = pygame.display.get_surface()
        self.Buttons :Buttons = []
        self.Images : Image = []
        self.Texts :Text = []
        self.old_pos = pygame.mouse.get_pos()
        self.in_common = In_common(self)
        self.create()
    
    def create(self):
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
        self.Images.append(Image((0,0),pygame.image.load(r".\Images\galaxy.jpg"),(self.screen.get_width(),self.screen.get_height()),False))
        self.Images.append(Image((50,self.screen.get_height()-150),pygame.image.load(r".\Images\Exit.png"),(125,125),True,"QUIT"))

    def repaint(self):
        self.in_common.repaint([self.Images,self.Buttons,self.Texts])

    def check_collision(self):
        return self.in_common.check_collision(self.Buttons,self.old_pos)
    
    def check_collision_images(self):
        return self.in_common.check_collision(self.Images,self.old_pos)

    def update_mouse_pos(self):
        self.old_pos = pygame.mouse.get_pos()

    def check_resize(self, new_dimensions:tuple[int,int]):
        self.in_common.check_resize(new_dimensions)

class Level():

    def __init__(self) -> None:
        self.screen = pygame.display.get_surface()
        self.Buttons:Buttons = []
        self.Texts :Text = []
        self.Images :Image = []
        self.Level_Path:str = None  
        self.in_common = In_common(self) 
        self.create()

    def create(self):
        text_size = pygame.font.SysFont("arial",100).size("Level")
        caption = Text("Level",((self.screen.get_width()/2-text_size[0]/2,50)),(194, 194, 214),pygame.font.SysFont("arial",100))
        self.Texts.append(caption)
        self.Buttons.append(Buttons((caption.pos[0],caption.pos[1]+text_size[1]-10),(text_size[0],4),(0,0,0),False))
        self.Images.append(Image((0,0),pygame.image.load(r".\Images\galaxy.jpg"),(self.screen.get_width(),self.screen.get_height()),False))

    def repaint(self):
        self.in_common.repaint([self.Images,self.Buttons,self.Texts])
    
    def check_resize(self, new_dimensions:tuple[int,int]):
        self.in_common.check_resize(new_dimensions)

class Settings():

    def __init__(self) -> None:
        pass
