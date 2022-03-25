import pygame
import json
import math
import os
import Konstants as paths
import Konstants as konst

from Stars import Star
from Lines import Line
from Texts import Text
from Buttons import Buttons
from Images import Image


class Game_Render():
    
    def __init__(self, name_:str) -> None:
        self.id = 0
        self.Star_list :Star = [] 
        self.Final_lines :Line = []
        self.Texts :Text =[]
        self.Images :Image = []
        self.Buttons:Buttons = []
        self.Instructions:list = []
        self.connected_stars:list = []
        self.Star_in_use :Star = None
        self.Line_in_use :Line = None
        self.old_pos = pygame.mouse.get_pos()  

        self.name = name_
        self.mask = None
        self.create(paths.level_json+str(self.name)+'.json')

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
        positions = []
        text = str(data["Explanation_text"][0]["text"])
        latin_name = "\lat.: "+data["Explanation_text"][0]["Latin_name"]
        content = "Sternbild: "+data["constellation"][0]["constellation_name"]
        headline = konst.In_common_game.create_Headline(content+latin_name,int(50*konst.mt),'inkfree')
        self.Instructions = data["Instructions"][0]["Connections"]
        i = 20*konst.mx
        for ins in self.Instructions:
            self.Texts.append(Text(str(ins[0])+"-"+str(ins[1]),(10*konst.mx+i,pygame.display.get_surface().get_height()-25*konst.my-konst.In_common_game.get_text_size(str(ins),int(30*konst.mt),"arial")[1]),(199,20,80),pygame.font.SysFont("arial",int(30*konst.mt))))
            i += konst.In_common_game.get_text_size(str(ins[0])+"-"+str(ins[1]),int(40*konst.mt),"arial")[0]+25*konst.mx
        t_size = konst.In_common_game.get_text_size("Verbinde die Sterne:",int(30*konst.mt),"arial")
        self.Texts.append(Text("Verbinde die Sterne:",(20*konst.mx,self.Texts[-1].pos[1]-t_size[1]-40*konst.my),(173,216,230),pygame.font.SysFont("arial",int(30*konst.mt))))
        self.Buttons.append(konst.In_common_game.create_underline(self.Texts[-1],t_size,(199,20,80),False))
        self.Texts.append(headline[0])
        
        for Stars in data:
            if(Stars[0:4]=="Star"):
                values = data[Stars][0]
                self.Star_list.append(Star([values["pos"][0]*konst.mx,values["pos"][1]*konst.my],values["radius"]*konst.mt,values["brightness"],values["active"],Stars[-1],Stars[5:]))
                positions.append([values["pos"][0]*konst.mx,values["pos"][1]*konst.my])
        pos_points = self.get_pos_points(positions,values["radius"]*konst.mt)
        self.mask = self.create_mask(pos_points,values["radius"]*konst.mt)
        dimension = (konst.screen.get_width()-pos_points[1]-2*values["radius"]*konst.mt-30*konst.mx,konst.screen.get_height())
        t = konst.In_common_game.format_text(text,dimension,int(30*konst.mt),[konst.screen.get_width()-dimension[0],0])
        factor = math.floor(self.get_factor(t))
        for text in t:
            text.change_pos((text.pos[0],text.pos[1]+factor))
            self.Texts.append(text)
        self.set_Star_to_use(0)


    def get_pos_points(self,postion_list, radius:int):
        nearest_x = konst.screen.get_height()
        nearest_y = konst.screen.get_height()
        furthest_x = 0
        furthest_y = 0
        for pos in postion_list:
            if pos[0]-radius < nearest_x:
                nearest_x = pos[0]-radius
            if pos[0]-radius > furthest_x:
                furthest_x = pos[0]-radius
            if pos[1]-radius < nearest_y:
                nearest_y = pos[1]-radius
            if pos[1]-radius > furthest_y:
                furthest_y = pos[1]-radius
        return [nearest_x,furthest_x,nearest_y,furthest_y]
    #returns a mask for the space the star_constellation need
    def create_mask(self,pos,radius):
        #nearest_x,nearest_y,furthest_x*2radius-nearest_x,furtest_y-nearest_y
        return pygame.Rect(pos[0],pos[2],pos[1]+2*radius-pos[0],pos[3]-pos[2])

    def get_factor(self,text_l:list):
        start_y = text_l[0].pos[1]
        length = text_l[-1].pos[1] - start_y
        y = konst.screen.get_height()-50-start_y
        start_point = start_y+((y/2)-(length/2))
        return start_point -start_y

    def repaint(self,dont_check:bool or None = True):
        if dont_check:
            konst.In_common_game.repaint([self.Images,self.Final_lines,self.Buttons,self.Star_list,self.Texts])
            return
        if not self.mask.collidepoint(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]):
            konst.In_common_game.repaint([self.Images,self.Final_lines,self.Buttons,self.Star_list,self.Texts])
        else:
            konst.In_common_game.repaint([self.Final_lines,self.Star_list]) 

    def update_line(self):
        pos = pygame.mouse.get_pos()
        if(pos != self.old_pos):
            self.old_pos=pos
            self.remove_line()
            self.Line_in_use.update_line(self.Star_in_use.get_pos(),pos)
            self.repaint(False)
        else:
            self.old_pos=pos
 
    def remove_line(self):
        self.Line_in_use.delete()

    def check_collision(self):
        return konst.In_common_game.check_collision(self.Star_list,self.old_pos)

    def Lock_line(self, star_to_lock:Star):
        reverse = False
        ids = [int(self.Star_in_use.id),int(star_to_lock.id)]
        if self.Star_in_use.id == star_to_lock.id:
            return 
        for connections in self.connected_stars:
            if connections == ids or connections == [int(star_to_lock.id),int(self.Star_in_use.id)]:
                return
        for ins in self.Instructions:
            if ins == ids:
                self.update_instroctions(ids)
            elif ins == ids[::-1]:
                self.update_instroctions(ids[::-1])
                reverse = True
        self.Line_in_use.delete()
        self.repaint(False)
        if reverse:
            self.Final_lines.append(self.Line_in_use.final_line(star_to_lock,self.Star_in_use))
            self.connected_stars.append(ids[::-1])
        else:
            self.Final_lines.append(self.Line_in_use.final_line(self.Star_in_use,star_to_lock))
            self.connected_stars.append(ids)
        self.Star_in_use = star_to_lock
        self.Line_in_use = Line(star_to_lock.get_pos(),pygame.mouse.get_pos())
        
        
    def update_mouse_pos(self):
        self.old_pos = pygame.mouse.get_pos()

    def animation(self):
        for stars in self.Star_list:
            stars.animation()

    def update_instroctions(self,ids):
        text = konst.In_common_game.find_text_object(str(ids[0])+"-"+str(ids[1]),self.Texts)
        text.change_color((199,20,80) if text.font_color == (20,199,80) else (20,199,80))
        text.draw()

    def completed_star_constellation(self):
        number_conections = len(self.Instructions)
        count = 0
        for inst in self.Instructions:
            if inst in self.connected_stars:
                count+=1
        #print(str(len(self.connected_stars))+" | "+str(number_conections))
        if number_conections == count and len(self.connected_stars) == number_conections:
            return True  
        return False
    
class Game_Lobby():

    def __init__(self,name:str) -> None:
        self.id = 1
        self.Buttons :Buttons = []
        self.Images : Image = []
        self.Texts :Text = []
        self.level_name = name
        self.old_pos = pygame.mouse.get_pos()
        self.create()
        self.choosen_level(self.level_name)
    
    def create(self):
        Headlilne = konst.In_common_lobby.create_Headline("Sternbilder",int(100*konst.mt))
        caption = Headlilne[0]
        text_size = Headlilne[2]
        self.Texts.append(caption)
        self.Buttons.append(Headlilne[1])

        i = 75*konst.my
        for k in range(4):
            self.Buttons.append(Buttons((caption.pos[0]-50*konst.mx,caption.pos[1]+text_size[1]+i),(text_size[0]+100*konst.mx,125*konst.my),(121,92,174),True,k))
            i+=200*konst.my

        texts = ["Play","Continue","Level","Settings"]
        for k in range(4):
            text_size = pygame.font.SysFont("arial",int(50*konst.mt)).size(texts[k])
            button = self.Buttons[k+1]
            button.add_text(Text(texts[k],(button.pos[0]+button.dimensions[0]/2-text_size[0]/2,button.pos[1]+button.dimensions[1]/2-text_size[1]/2),(0,0,0),pygame.font.SysFont("arial",int(50*konst.mt))))
        self.Images.append(konst.In_common_lobby.set_background(paths.galaxy))
        self.Images.append(konst.In_common_lobby.create_shutdown_button())
        

    def choosen_level(self, level_name:str):
        text = konst.In_common_lobby.find_text_object(self.level_name,self.Texts)
        button = konst.In_common_lobby.find_button_by_text("Level",self.Buttons)
        text_s = pygame.font.SysFont("arial",int(30*konst.mt)).size(level_name)   
        if text != None:
            text.change_text(level_name)   
            text.change_pos((button.pos[0]+button.dimensions[0]/2-text_s[0]/2,button.pos[1]+button.dimensions[1]-(text_s[1]+5)))
        else:
            self.Texts.append(Text(level_name,(button.pos[0]+button.dimensions[0]/2-text_s[0]/2,button.pos[1]+button.dimensions[1]-(text_s[1]+5)),(0,0,0),pygame.font.SysFont("arial",int(30*konst.mt))))
        self.level_name = level_name
        
    def repaint(self):
        konst.In_common_lobby.repaint([self.Images,self.Buttons,self.Texts])

    def check_collision(self):
        return konst.In_common_lobby.check_collision(self.Buttons,self.old_pos)
    
    def check_collision_images(self):
        return konst.In_common_lobby.check_collision(self.Images,self.old_pos)

    def update_mouse_pos(self):
        self.old_pos = pygame.mouse.get_pos()

    def get_level_text(self):
        return konst.In_common_lobby.find_text_object(self.level_name,self.Texts)

class Level():

    def __init__(self) -> None:
        self.id = 2
        self.Buttons:Buttons = []
        self.Texts :Text = []
        self.Images :Image = []
        self.old_pos = pygame.mouse.get_pos()  
        self.create()

    def create(self):
        Headlilne = konst.In_common_level.create_Headline("Level",int(100*konst.mt))
        caption = Headlilne[0]
        text_size = Headlilne[2]
        self.Texts.append(caption)
        self.Buttons.append(Headlilne[1])
        self.Images.append(konst.In_common_level.set_background(os.path.join(paths.level)))
        self.Images.append(konst.In_common_level.create_shutdown_button())

        i = 75*konst.my
        for k in range(5):
            self.Buttons.append(Buttons((caption.pos[0]-250*konst.mx,caption.pos[1]+text_size[1]+i),(text_size[0]+500*konst.mx,125*konst.my),(7,45,99),True,k))
            i+=135*konst.my
        texts = ["Adler","Andromeda","Becher","Bootes","Cassiopeia"]
        for k in range(5):
            text_size = pygame.font.SysFont("arial",int(50*konst.mt)).size(texts[k])
            button = self.Buttons[k+1]
            button.add_text(Text(texts[k],(button.pos[0]+button.dimensions[0]/2-text_size[0]/2,button.pos[1]+button.dimensions[1]/2-text_size[1]/2),(0,0,0),pygame.font.SysFont("arial",int(50*konst.mt))))

    def repaint(self):
        konst.In_common_level.repaint([self.Images,self.Buttons,self.Texts])

    def update_mouse_pos(self):
        self.old_pos = pygame.mouse.get_pos()

    def check_collision(self):
        return konst.In_common_level.check_collision(self.Buttons,self.old_pos)
    
    def check_collision_images(self):
        return konst.In_common_level.check_collision(self.Images,self.old_pos)

class Settings():

    def __init__(self) -> None:
        self.id = 3
        self.Buttons:Buttons = []
        self.Texts :Text = []
        self.Images :Image = []
        self.old_pos = pygame.mouse.get_pos()  
        self.create()

    def create(self):
        Headlilne = konst.In_common_setting.create_Headline("Settings",int(100*konst.mt))
        self.Texts.append(Headlilne[0])
        self.Buttons.append(Headlilne[1])
        self.Images.append(konst.In_common_setting.set_background(paths.settings))
        self.Images.append(konst.In_common_setting.create_shutdown_button())
        self.Images.append(Image((konst.screen.get_width()/2,350*konst.my),pygame.image.load(paths.switch[0]),(200,100),True,"set_fullscreen"))

    def repaint(self):
        konst.In_common_setting.repaint([self.Images,self.Buttons,self.Texts])

    def check_collision(self):
        return konst.In_common_setting.check_collision(self.Buttons,self.old_pos)
    
    def update_mouse_pos(self):
        self.old_pos = pygame.mouse.get_pos()
        
    def check_collision_images(self):
        return konst.In_common_setting.check_collision(self.Images,self.old_pos)
