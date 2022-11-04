from dis import Instruction
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
        self.star_count = 0
        self.create(self.get_file_path(str(self.name)+'.json'))

    def create(self,path:str):
        self.load_json(path)
        self.Line_in_use=Line(self.Star_in_use.get_pos(),pygame.mouse.get_pos(),5*self.mt,"Line")
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
        l_name = data["Explanation_text"][0]["Latin_name"]
        latin_name = f" (lat.: {l_name})"
        content = data["constellation"][0]["constellation_name"]
        headline = self.create_Headline(content,int(70*self.mt))
        self.Instructions = data["Instructions"][0]["Connections"]
        text_logo = Image((50*self.mx,self.screen.get_height()-150*self.my),self.get_file_path("text_logo.png"),(125*self.mx,125*self.my),True,"Text_logo","TEXT")
        self.list.add_element_after_element(text_logo, "Background")
        #i = 20*self.mx
        #for indx,ins in enumerate(self.Instructions):
        #    self.list.add_element_at_end(Text(str(ins[0])+"-"+str(ins[1]),(10*self.mx+i,pygame.display.get_surface().get_height()-25*self.my-self.get_text_size(str(ins),int(30*self.mt),"arial")[1]),(199,20,80),pygame.font.SysFont("arial",int(30*self.mt)),f"Ins:{str(ins[0])}-{str(ins[1])}"))
        #    i += self.get_text_size(str(ins[0])+"-"+str(ins[1]),int(40*self.mt),"arial")[0]+25*self.mx
        #t_size = self.get_text_size("Verbinde die Sterne:",int(30*self.mt),"arial")
        #self.list.add_element_at_end(Text("Verbinde die Sterne:",(20*self.mx,self.list.get_element_by_key(f"Ins:{str(ins[0])}-{str(ins[1])}").pos[1]-t_size[1]-40*self.my),(173,216,230),pygame.font.SysFont("arial",int(30*self.mt)),key_="Instruction_Headline"))
        #self.list.add_element_at_end(self.create_underline(self.list.get_element_by_key("Instruction_Headline"),t_size,(199,20,80),False))
        self.list.add_element(headline[0])
        self.list.add_element(headline[1])
        
        for Stars in data:
            if(Stars[0:4]=="Star"):
                values = data[Stars][0]
                self.list.add_element_at_end(Star([values["pos"][0]*self.mx,values["pos"][1]*self.my],values["radius"]*self.mt,values["brightness"],values["active"],Stars[5:],Stars[5:],Stars))
                positions.append([values["pos"][0]*self.mx,values["pos"][1]*self.my])
                self.star_count += 1
        pos_points = self.get_pos_points(positions,values["radius"]*self.mt)
        self.mask = self.create_mask(pos_points,values["radius"]*self.mt)
        dimension = (self.screen.get_width()-pos_points[1]-2*values["radius"]*self.mt-30*self.mx,self.screen.get_height())
        self.set_Star_to_use("Star_1")
        self.list.add_element(self.set_background(self.get_file_path("stars.png")))
        #self.list.add_element(self.set_background(self.get_file_path(f"{self.name}.png")))
        

    def create_text(self, dimension):
        t = self.format_text(text,dimension,int(30*self.mt),[self.screen.get_width()-dimension[0],0])
        factor = math.floor(self.get_factor(t))
        for text in t:
            text.change_pos((text.pos[0],text.pos[1]+factor))
            self.list.add_element_after_element(text,"Background")
        
    #nearest_x,nearest_y,furthest_x*2radius-nearest_x,furtest_y-nearest_y
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
    
    
    #returns a mask for the space the star_constellation needs
    def create_mask(self,pos,radius) -> pygame.Rect:
        return pygame.Rect(pos[0],pos[2],pos[1]+2*radius-pos[0],pos[3]-pos[2])

    #factor for text-centering
    def get_factor(self,text_l:list) -> float:
        start_y = text_l[0].pos[1]
        length = text_l[-1].pos[1] - start_y
        y = self.screen.get_height()-50*self.my-start_y
        start_point = start_y+((y/2)-(length/2))
        return start_point -start_y
    
    def highlight_stars_to_connect(self):
        star_index = int(self.Star_in_use.id)
        stars_to_highlight:list = []
        for ins in self.Instructions:
            if ins[0] == star_index:
                stars_to_highlight.append(self.list.get_element_by_key(f"Star_{ins[1]}"))
            elif ins[1] == star_index:
                stars_to_highlight.append(self.list.get_element_by_key(f"Star_{ins[0]}"))
        self.highlight_stars(stars_to_highlight)
    
    def highlight_stars(self, h_list:list):
        for indx in range(self.star_count):
            element = self.list.get_element_by_key(f"Star_{indx+1}")
            con = [int(element.id), int(self.Star_in_use.id)]
            if element in h_list:
                if con in self.connected_stars or con[::-1] in self.connected_stars:
                    element.text.change_color((12,255,23))
                else:
                    element.text.change_color((255, 255, 0))
            else:
                if con in self.connected_stars or con[::-1] in self.connected_stars:
                    element.text.change_color((255,0,0))
                else:
                    element.text.change_color((173,216,230))
        
    def repaint(self):
        self.list.repaint()

    def check_collision(self) -> tuple[bool,Callable]:
        return self.list.check_collision()

    def Lock_line(self, star_to_lock:Star):
        ids = [int(self.Star_in_use.id),int(star_to_lock.id)]
        if self.Star_in_use.id == star_to_lock.id:
            return 
        for connections in self.connected_stars:
            if connections == ids or connections == ids[::-1]:
                return
        reverse = False
        for ins in self.Instructions:
            if ins == ids:
                #self.update_instroctions(ids)
                pass
            elif ins == ids[::-1]:
                #self.update_instroctions(ids[::-1])
                reverse = True
        if reverse:
            self.Line_in_use.final_line(star_to_lock,self.Star_in_use)
            self.change_layer_of_line(ids[::-1])
            self.connected_stars.append(ids[::-1])
        else:
            self.Line_in_use.final_line(self.Star_in_use,star_to_lock)
            self.connected_stars.append(ids)
            self.change_layer_of_line(ids)
        self.Star_in_use = star_to_lock
        self.Line_in_use = Line(star_to_lock.get_pos(),pygame.mouse.get_pos(),5*self.mt,"Line")
        self.list.add_element_at_end(self.Line_in_use)
        
    def unrender_instructions(self):
        for ins in self.Instructions:
            self.list.get_element_by_key(f"Ins:{str(ins[0])}-{str(ins[1])}").set_render()
        self.list.get_element_by_key("Instruction_Headline").set_render()
        self.list.get_element_by_key("UlVerbinde die Sterne:").set_render()

    def update_instroctions(self,ids):
        text = self.list.get_element_by_key(f"Ins:{str(ids[0])}-{str(ids[1])}")
        if not text.get_render():
            self.unrender_instructions()
        text.change_color((199,20,80) if text.font_color == (20,199,80) else (20,199,80))

    def change_layer_of_line(self, ids:list[int,int]):
        key = f"Line Star_{str(ids[0])}-Star_{str(ids[1])}"
        l = self.list.get_element_by_key(key)
        self.list.delete_element(key)
        self.list.add_element_after_element(l,"Instruction_Headline")

    def completed_star_constellation(self) -> bool:
        number_conections = len(self.Instructions)
        count = 0
        for inst in self.Instructions:
            if inst in self.connected_stars:
                count+=1
        #print(str(len(self.connected_stars))+" | "+str(number_conections))
        if number_conections == count and len(self.connected_stars) == number_conections:
            if not self.finished:
                self.Line_in_use.set_render()
                self.list.get_element_by_key("Background").change_image(self.get_file_path(f"{self.name}.png"))
                #self.unrender_instructions()
                for indx in range(self.star_count):
                    self.list.get_element_by_key(f"Star_{indx+1}").text.change_color((173,216,230))
            return True  
        self.finished = False  
        return False

    def resize(self) -> Callable:
        self.__init__(self.name)
        return self    

class Explanation_text(Lv):

    def __init__(self, name_:str) -> None:
        super().__init__()
        self.id = 4
        self.buttons:list = []
        self.texts:list = []
        self.images:list = []
        self.all_lists = [self.images, self.buttons, self.texts]
        self.intermediate:pygame.Surface = None
        self.inter_height = 0
        self.name = name_
        self.scroll_y = 0
    
    def create(self):
        self.screen.fill((0,0,0))
        
    def repaint(self):
        super().repaint(self.all_lists, self.intermediate, self.scroll_y)
        self.screen.blit(self.intermediate, (0,self.scroll_y))
    
    def restore_original_color(self):
        super().restore_color(self.all_lists)

    def check_collision(self) -> tuple[bool,Callable]:
        return super().check_collision(self.all_lists)

    def update_mouse_pos(self):
        self.old_pos = pygame.mouse.get_pos()

    def update_sidebar_slider(self):
        super().update_sidebar_slider(self.element_by_key(self.buttons,"Sb2"), self.scroll_y, self.inter_height)
    
    def resize(self) -> Callable:
        self.__init__(self.name)
        return self 

class Game_Lobby(Lv):

    def __init__(self,name:str) -> None:
        super().__init__()
        self.id = 1
        #self.list = List()
        self.buttons:list = []
        self.texts:list = []
        self.images:list = []
        self.all_lists = [self.images, self.buttons, self.texts]
        self.table_contants = ["Play","Continue","Level","Settings"]
        self.intermediate:pygame.Surface = None
        self.inter_height = 0
        self.level_name = name
        self.scroll_y = 0
        self.create()
    
    def create(self):
        Headlilne = self.create_Headline("Sternbilder",int(100*self.mt),moveable=True)
        self.texts.append(Headlilne[0])
        self.buttons.append(Headlilne[1])
        table = self.create_table(len(self.table_contants),Headlilne[0].pos,(100,125),[(75,200),(50,0)],Headlilne[2],(121,92,174),(148, 110, 159),True, self.table_contants,50,"arial",[i for i in range(len(self.table_contants))], moveable=True)
        images = [self.set_background(self.get_file_path("galaxy.jpg")),self.create_shutdown_button()]
        for elements_table in table:
            self.buttons.append(elements_table)
        last_button = self.element_by_key(self.buttons,f"{len(self.table_contants)}Tb{len(self.table_contants)-1}")
        self.inter_height = last_button.get_pos()[1]+last_button.dimensions[1]+150*self.my
        for elements_images in images:
            self.images.append(elements_images)
        self.buttons += self.create_side_bar()
        bindx = str(self.table_contants.index("Level"))
        button = self.element_by_key(self.buttons,f"{len(self.table_contants)}Tb{bindx}") 
        text_s = pygame.font.SysFont("arial",int(30*self.mt)).size(self.level_name)
        self.texts.append(Text(self.level_name,(button.pos[0]+button.dimensions[0]/2-text_s[0]/2,button.pos[1]+button.dimensions[1]-(text_s[1]+5)),(0,0,0),pygame.font.SysFont("arial",int(30*self.mt)),"Level_text",moveable_=True))
        self.intermediate = pygame.Surface((self.element_by_key(self.images,"Background").image.get_width(), self.screen.get_height()+self.inter_height),pygame.SRCALPHA)

    def change_level_name(self, new_level_name:str):
        bindx = str(self.table_contants.index("Level"))
        button = self.element_by_key(self.buttons, f"{len(self.table_contants)}Tb{bindx}")
        text = self.element_by_key(self.texts, "Level_text")
        text_s = pygame.font.SysFont("arial",int(30*self.mt)).size(new_level_name)
        text.change_text(new_level_name)   
        text.change_pos((button.pos[0]+button.dimensions[0]/2-text_s[0]/2,button.pos[1]+button.dimensions[1]-(text_s[1]+5)))      
        self.level_name = new_level_name
        
    def repaint(self):
        super().repaint(self.all_lists, self.intermediate, self.scroll_y)
        self.screen.blit(self.intermediate, (0,self.scroll_y))
    
    def restore_original_color(self):
        super().restore_color(self.all_lists)

    def check_collision(self) -> tuple[bool,Callable]:
        return super().check_collision(self.all_lists)

    def update_mouse_pos(self):
        self.old_pos = pygame.mouse.get_pos()

    def update_sidebar_slider(self):
        super().update_sidebar_slider(self.element_by_key(self.buttons,"Sb2"), self.scroll_y, self.inter_height)
    
    def get_level_text(self) -> Callable:
        return self.element_by_key(self.texts,"Level_text")
    
    def resize(self) -> Callable:
        self.__init__(self.level_name)
        return self


class Level(Lv):

    def __init__(self) -> None:
        super().__init__()
        self.id = 2
        #self.list = List() 
        self.buttons:list = []
        self.images = []
        self.texts = [] 
        self.all_lists = [self.images, self.buttons, self.texts]
        self.intermediate:pygame.Surface = None
        self.inter_height = 0
        self.scroll_y = 0
        self.create()

    def create(self):
        Headlilne = self.create_Headline("Level",int(100*self.mt), moveable=True)
        self.texts.append(Headlilne[0])
        self.buttons.append(Headlilne[1])
        self.images.append(self.set_background(self.get_file_path("Level.png")))
        self.images.append(self.create_shutdown_button())
        texts = []
        for file in next(os.walk(self.get_folder_path("Starfiles")))[2]:
            texts.append(file.split(".")[0])
            texts.sort()
        table = self.create_table(len(texts),Headlilne[0].pos,(500,125),[(75,150),(250,0)],Headlilne[2],(7,45,99),(34,59,112),True,texts,50,"arial",[i for i in range(len(texts))],moveable=True)
        for elements in table:
            self.buttons.append(elements)
        last_button = self.element_by_key(self.buttons,f"{len(texts)}Tb{len(texts)-1}")
        self.buttons += self.create_side_bar()
        self.inter_height = last_button.get_pos()[1]+last_button.dimensions[1]+150*self.my
        self.intermediate = pygame.Surface((self.element_by_key(self.images,"Background").image.get_width(), self.screen.get_height()+self.inter_height),pygame.SRCALPHA)
        
    def repaint(self):
        super().repaint(self.all_lists, self.intermediate, self.scroll_y)
        self.screen.blit(self.intermediate, (0, self.scroll_y))
    
    def restore_original_color(self):
        super().restore_color(self.all_lists)

    def check_collision(self) -> tuple[bool,Callable]:
        return super().check_collision(self.all_lists)
    
    def update_sidebar_slider(self):
        super().update_sidebar_slider(self.element_by_key(self.buttons,"Sb2"), self.scroll_y, self.inter_height)
    
    def resize(self) -> Callable:
        self.__init__()
        return self
    

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
    
    def resize(self) -> Callable:
        self.__init__(self.settings)
        return self
    

    
        
        
