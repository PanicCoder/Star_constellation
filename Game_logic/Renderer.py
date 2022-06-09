from typing import Callable
import pygame
import json
import math
import os

from Basic_elements.Circle import Circle
from Basic_elements.Stars import Star
from Basic_elements.Lines import Line
from Basic_elements.Texts import Text
from Basic_elements.Buttons import Buttons
from Basic_elements.Images import Image
from Super_Classes.Interface import Level as Lv
from Kompositum.List import List

class Game_Render(Lv):
    
    def __init__(self, name_:str) -> None:
        super().__init__()
        self.id = 0
        self.list = List()
        self.Instructions:list = []
        self.connected_stars:list = []
        self.Star_in_use :Star = None
        self.Line_in_use :Line = None
        self.name = name_
        self.finished = False
        self.mask = None
        self.create(self.get_file_path(str(self.name)+'.json'))

    def create(self,path:str):
        self.load_json(path)
        self.Line_in_use=Line(self.Star_in_use.get_pos(),pygame.mouse.get_pos(),"Line")
        self.list.add_element_at_end(self.Line_in_use)

    def set_Star_to_use(self, key_star:str):
        self.Star_in_use= self.list.get_element_by_key(key_star)
        
    def update_line_in_use(self):
        self.Line_in_use.update_pos(self.Star_in_use.get_pos(),pygame.mouse.get_pos())

    def load_json(self,path):
        file = open(path)
        data = json.load(file)
        file.close()
        positions = []
        text = str(data["Explanation_text"][0]["text"])
        latin_name = "\lat.: "+data["Explanation_text"][0]["Latin_name"]
        content = "Sternbild: "+data["constellation"][0]["constellation_name"]
        headline = self.create_Headline(content+latin_name,int(50*self.mt),'inkfree')
        self.Instructions = data["Instructions"][0]["Connections"]
        i = 20*self.mx
        for indx,ins in enumerate(self.Instructions):
            self.list.add_element_at_end(Text(str(ins[0])+"-"+str(ins[1]),(10*self.mx+i,pygame.display.get_surface().get_height()-25*self.my-self.get_text_size(str(ins),int(30*self.mt),"arial")[1]),(199,20,80),pygame.font.SysFont("arial",int(30*self.mt)),"Ins:" + str(ins[0])+"-"+str(ins[1])))
            i += self.get_text_size(str(ins[0])+"-"+str(ins[1]),int(40*self.mt),"arial")[0]+25*self.mx
        t_size = self.get_text_size("Verbinde die Sterne:",int(30*self.mt),"arial")
        self.list.add_element_at_end(Text("Verbinde die Sterne:",(20*self.mx,self.list.get_element_by_key("Ins:" + str(ins[0])+"-"+str(ins[1])).pos[1]-t_size[1]-40*self.my),(173,216,230),pygame.font.SysFont("arial",int(30*self.mt)),"Instruction_Headline"))
        self.list.add_element_at_end(self.create_underline(self.list.get_element_by_key("Instruction_Headline"),t_size,(199,20,80),False))
        self.list.add_element(headline[0])
        
        for Stars in data:
            if(Stars[0:4]=="Star"):
                values = data[Stars][0]
                self.list.add_element_at_end(Star([values["pos"][0]*self.mx,values["pos"][1]*self.my],values["radius"]*self.mt,values["brightness"],values["active"],Stars[-1],Stars[5:],Stars))
                positions.append([values["pos"][0]*self.mx,values["pos"][1]*self.my])
        pos_points = self.get_pos_points(positions,values["radius"]*self.mt)
        self.mask = self.create_mask(pos_points,values["radius"]*self.mt)
        dimension = (self.screen.get_width()-pos_points[1]-2*values["radius"]*self.mt-30*self.mx,self.screen.get_height())
        t = self.format_text(text,dimension,int(30*self.mt),[self.screen.get_width()-dimension[0],0])
        factor = math.floor(self.get_factor(t))
        self.list.add_element(self.set_background(self.get_file_path("Stars.png")))
        
        for text in t:
            text.change_pos((text.pos[0],text.pos[1]+factor))
            self.list.add_element_after_element(text,"Background")
        self.set_Star_to_use("Star_1")


    #returns a mask for the space the star_constellation needs
    def get_pos_points(self,postion_list, radius:int) -> list:
        nearest_x = self.screen.get_height()
        nearest_y = self.screen.get_height()
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
                furthest_y = pos[1]+radius
        return [nearest_x,furthest_x,nearest_y,furthest_y]
    
    #nearest_x,nearest_y,furthest_x*2radius-nearest_x,furtest_y-nearest_y
    def create_mask(self,pos,radius) -> pygame.Rect:
        #self.list.add_element(Buttons((pos[0],pos[2]),(pos[1]+2*radius-pos[0],pos[3]-pos[2]),(0,0,0),False,"Constelation_Background"))
        return pygame.Rect(pos[0],pos[2],pos[1]+2*radius-pos[0],pos[3]-pos[2])

    #factor for text-centering
    def get_factor(self,text_l:list) -> float:
        start_y = text_l[0].pos[1]
        length = text_l[-1].pos[1] - start_y
        y = self.screen.get_height()-50*self.my-start_y
        start_point = start_y+((y/2)-(length/2))
        return start_point -start_y

    def repaint(self):
        self.list.repaint()

    def check_collision(self) -> tuple[bool,Callable]:
        return self.list.check_collision()

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
        if reverse:
            self.Line_in_use.final_line(star_to_lock,self.Star_in_use)
            self.connected_stars.append(ids[::-1])
        else:
            self.Line_in_use.final_line(self.Star_in_use,star_to_lock)
            self.connected_stars.append(ids)
        self.Star_in_use = star_to_lock
        self.Line_in_use = Line(star_to_lock.get_pos(),pygame.mouse.get_pos(),"Line")
        self.list.add_element_at_end(self.Line_in_use)
        

    def update_instroctions(self,ids):
        text = self.list.get_element_by_key("Ins:"+str(ids[0])+"-"+str(ids[1]))
        text.change_color((199,20,80) if text.font_color == (20,199,80) else (20,199,80))

    def completed_star_constellation(self, object) -> bool:
        number_conections = len(self.Instructions)
        count = 0
        for inst in self.Instructions:
            if inst in self.connected_stars:
                count+=1
        #print(str(len(self.connected_stars))+" | "+str(number_conections))
        if number_conections == count and len(self.connected_stars) == number_conections:
            if not self.finished:
                object.play_sound("complete")
                self.finished = True
            return True
        self.finished = False  
        return False
    
class Game_Lobby(Lv):

    def __init__(self,name:str) -> None:
        super().__init__()
        self.id = 1
        self.list = List()
        self.level_name = name
        self.create()
    
    def create(self):
        Headlilne = self.create_Headline("Sternbilder",int(100*self.mt))
        self.list.add_element_at_end(Headlilne[0])
        self.list.add_element_at_end(Headlilne[1])
        table = self.create_table(4,Headlilne[0].pos,(100,125),[(75,200),(50,0)],Headlilne[2],(121,92,174),(148, 110, 159),True,["Play","Continue","Level","Settings"],50,"arial",[0,1,2,3])
        images = [self.create_shutdown_button(),self.set_background(self.get_file_path("galaxy.jpg"))]
        for elements_table in table:
            self.list.add_element_at_end(elements_table)
        for elements_images in images:
            self.list.add_element(elements_images)
        button = self.list.get_element_by_key("4Tb2")  
        text_s = pygame.font.SysFont("arial",int(30*self.mt)).size(self.level_name)
        self.list.add_element_at_end(Text(self.level_name,(button.pos[0]+button.dimensions[0]/2-text_s[0]/2,button.pos[1]+button.dimensions[1]-(text_s[1]+5)),(0,0,0),pygame.font.SysFont("arial",int(30*self.mt)),"Level_text")) 

    def change_level_name(self, new_level_name:str):
        button = self.list.get_element_by_key("4Tb2")
        text = self.list.get_element_by_key("Level_text")
        text_s = pygame.font.SysFont("arial",int(30*self.mt)).size(new_level_name)
        text.change_text(new_level_name)   
        text.change_pos((button.pos[0]+button.dimensions[0]/2-text_s[0]/2,button.pos[1]+button.dimensions[1]-(text_s[1]+5)))      
        self.level_name = new_level_name
        
    def repaint(self):
        self.list.repaint()

    def check_collision(self) -> tuple[bool,Callable]:
        return self.list.check_collision()

    def update_mouse_pos(self):
        self.old_pos = pygame.mouse.get_pos()

    def get_level_text(self) -> Callable:
        return self.list.get_element_by_key("Level_text")


class Level(Lv):

    def __init__(self) -> None:
        super().__init__()
        self.id = 2
        self.list = List()  
        self.create()

    def create(self):
        Headlilne = self.create_Headline("Level",int(100*self.mt))
        self.list.add_element(Headlilne[0])
        self.list.add_element_at_end(Headlilne[1])
        self.list.add_element(self.set_background(self.get_file_path("Level.png")))
        self.list.add_element_after_element(self.create_shutdown_button(), "Background")
        texts = []
        for file in next(os.walk(self.get_folder_path("Starfiles")))[2]:
            texts.append(file.split(".")[0])
            texts.sort()
        table = self.create_table(len(texts),Headlilne[0].pos,(500,125),[(75,150),(250,0)],Headlilne[2],(7,45,99),(34,59,112),True,texts,50,"arial",[i for i in range(len(texts))])
        for elements in table:
            self.list.add_element_at_end(elements)
        
    def repaint(self):
        self.list.repaint()

    def check_collision(self) -> tuple[bool,Callable]:
        return self.list.check_collision()
    

class Settings(Lv):

    def __init__(self, settings_:dict) -> None:
        super().__init__()
        self.id = 3
        self.settings = settings_
        self.list = List() 
        self.create()

    def create(self):
        Headline = self.create_Headline("Settings",int(100*self.mt))
        self.list.add_element_at_end(Headline[0])
        self.list.add_element_at_end(Headline[1])
        self.list.add_element(self.create_shutdown_button())
        self.list.add_element(self.set_background(self.get_file_path("Settings.png")))
        
        actions = ["fullscreen","background_music","sound_effects"]
        table = self.create_table(len(actions),(Headline[0].pos),(1000,75),[(75,100),(500,0)],Headline[2],(255,105,200),(255,105,200),False,["Fullscreen","Music","Sound_effects"],40,"arial",actions,text_pos="left",transparence=0.5)
        for indx,buttons in enumerate(table):
            self.list.add_element_at_end(buttons)
            t_switch = self.create_toggle_switch(buttons,(0,0,0),(255,0,0),True,actions[indx])
            for element in t_switch:
                self.list.add_element_at_end(element)
            if self.settings[t_switch[-1].get_action()]:  
                self.flip_switch_state(t_switch[-1], t_switch[0])
        actions2 =["volume_b","volume_e"]
        table2 = self.create_table(len(actions2),(Headline[1].pos[0],self.list.get_element_by_key(f"{str(len(actions))}Tb{str(len(actions)-1)}").pos[1]),(1000,75),[(75,100),(500,0)],Headline[2],(255,105,200),(255,105,200),False,["Music_volume","Sound_effect_volume"],40,"arial",["volume_b","volume_e"],"left",0.5)
        for indx,buttons in enumerate(table2):
            percentage = self.settings[actions2[indx]]
            self.list.add_element_at_end(buttons)
            slider = self.create_slider(buttons,(0,0,0),(255,105,0),actions2[indx],percentage)
            buttons.add_text(str(int(round(percentage*100,0)))+"%",40,"arial")
            for element in slider:
                self.list.add_element_at_end(element)

        #(255,105,200)

    def flip_switch_state(self, circle:Circle, button:Buttons):
        super().flip_switch_state(circle, button)
    
    def update_slider(self, circle:Circle, button:Buttons, parent_b:Buttons):
        super().update_slider(circle, button, parent_b)
    
    def slider_percentage(self, button:Buttons, parent_b:Buttons, pos) -> float:
        return super().Slider_percentage(button, parent_b, pos)

    def repaint(self):
        self.list.repaint()

    def check_collision(self) -> tuple[bool,Callable]:
        return self.list.check_collision()
    

    
        
        
