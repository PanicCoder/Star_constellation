import pygame
import json
import math
import os
import Konstants as paths

from Konstants import in_common as ic
from Circle import Circle
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
        self.finished = False
        self.mask = None
        self.create(paths.level_json+str(self.name)+'.json')

    def create(self,path:str):
        self.load_json(path)
        self.Line_in_use=Line(self.Star_in_use.get_pos(),pygame.mouse.get_pos())


    def set_Star_to_use(self, index:int):
        self.Star_in_use=self.Star_list[index]
        
    def update_line_in_use(self):
        self.Line_in_use.delete()
        self.Line_in_use.update_pos(self.Star_in_use.get_pos(),pygame.mouse.get_pos())
        self.Line_in_use.draw()

    def load_json(self,path):
        file = open(path)
        data = json.load(file)
        file.close()
        positions = []
        text = str(data["Explanation_text"][0]["text"])
        latin_name = "\lat.: "+data["Explanation_text"][0]["Latin_name"]
        content = "Sternbild: "+data["constellation"][0]["constellation_name"]
        headline = ic.create_Headline(content+latin_name,int(50*ic.mt),'inkfree')
        self.Instructions = data["Instructions"][0]["Connections"]
        i = 20*ic.mx
        for ins in self.Instructions:
            self.Texts.append(Text(str(ins[0])+"-"+str(ins[1]),(10*ic.mx+i,pygame.display.get_surface().get_height()-25*ic.my-ic.get_text_size(str(ins),int(30*ic.mt),"arial")[1]),(199,20,80),pygame.font.SysFont("arial",int(30*ic.mt))))
            i += ic.get_text_size(str(ins[0])+"-"+str(ins[1]),int(40*ic.mt),"arial")[0]+25*ic.mx
        t_size = ic.get_text_size("Verbinde die Sterne:",int(30*ic.mt),"arial")
        self.Texts.append(Text("Verbinde die Sterne:",(20*ic.mx,self.Texts[-1].pos[1]-t_size[1]-40*ic.my),(173,216,230),pygame.font.SysFont("arial",int(30*ic.mt))))
        self.Buttons.append(ic.create_underline(self.Texts[-1],t_size,(199,20,80),False))
        self.Texts.append(headline[0])
        
        for Stars in data:
            if(Stars[0:4]=="Star"):
                values = data[Stars][0]
                self.Star_list.append(Star([values["pos"][0]*ic.mx,values["pos"][1]*ic.my],values["radius"]*ic.mt,values["brightness"],values["active"],Stars[-1],Stars[5:]))
                positions.append([values["pos"][0]*ic.mx,values["pos"][1]*ic.my])
        pos_points = self.get_pos_points(positions,values["radius"]*ic.mt)
        self.mask = self.create_mask(pos_points,values["radius"]*ic.mt)
        dimension = (ic.screen.get_width()-pos_points[1]-2*values["radius"]*ic.mt-30*ic.mx,ic.screen.get_height())
        t = ic.format_text(text,dimension,int(30*ic.mt),[ic.screen.get_width()-dimension[0],0])
        factor = math.floor(self.get_factor(t))
        for text in t:
            text.change_pos((text.pos[0],text.pos[1]+factor))
            self.Texts.append(text)
        self.set_Star_to_use(0)


    def get_pos_points(self,postion_list, radius:int):
        nearest_x = ic.screen.get_height()
        nearest_y = ic.screen.get_height()
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
        y = ic.screen.get_height()-50*ic.my-start_y
        start_point = start_y+((y/2)-(length/2))
        #factor for text-centering
        return start_point -start_y

    def repaint(self,dont_check:bool or None = True):
        if dont_check:
            ic.repaint([self.Images,self.Final_lines,self.Buttons,self.Star_list,self.Texts])
            return
        if not self.mask.collidepoint(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]):
            ic.repaint([self.Images,self.Final_lines,self.Buttons,self.Star_list,self.Texts])
        else:
            ic.repaint([self.Final_lines,self.Star_list]) 

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
        return ic.check_collision(self.Star_list,self.old_pos)

    def Lock_line(self, star_to_lock:Star):
        pygame.mixer.Sound.set_volume(ic.sound_effects["click"],0.1)
        pygame.mixer.Sound.play(ic.sound_effects["click"])
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
        text = ic.find_text_object(str(ids[0])+"-"+str(ids[1]),self.Texts)
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
            if not self.finished:
                ic.play_sound("complete")
            self.finished = True
            return True
        self.finished = False  
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
        Headlilne = ic.create_Headline("Sternbilder",int(100*ic.mt))
        self.Texts.append(Headlilne[0])
        self.Buttons.append(Headlilne[1])
        self.Buttons+=ic.create_tabel(4,Headlilne[0].pos,(100,125),[(75,200),(50,0)],Headlilne[2],(121,92,174),True,["Play","Continue","Level","Settings"],50,"arial",[0,1,2,3])
        self.Images += [ic.set_background(paths.galaxy),ic.create_shutdown_button()]
        

    def choosen_level(self, level_name:str):
        text = ic.find_text_object(self.level_name,self.Texts)
        button = ic.find_button_by_text("Level",self.Buttons)
        text_s = pygame.font.SysFont("arial",int(30*ic.mt)).size(level_name)   
        if text != None:
            text.change_text(level_name)   
            text.change_pos((button.pos[0]+button.dimensions[0]/2-text_s[0]/2,button.pos[1]+button.dimensions[1]-(text_s[1]+5)))
        else:
            self.Texts.append(Text(level_name,(button.pos[0]+button.dimensions[0]/2-text_s[0]/2,button.pos[1]+button.dimensions[1]-(text_s[1]+5)),(0,0,0),pygame.font.SysFont("arial",int(30*ic.mt))))
        self.level_name = level_name
        
    def repaint(self):
        ic.repaint([self.Images,self.Buttons,self.Texts])

    def check_collision(self):
        return ic.check_collision(self.Buttons,self.old_pos)
    
    def check_collision_images(self):
        return ic.check_collision(self.Images,self.old_pos)

    def update_mouse_pos(self):
        self.old_pos = pygame.mouse.get_pos()

    def get_level_text(self):
        return ic.find_text_object(self.level_name,self.Texts)

class Level():

    def __init__(self) -> None:
        self.id = 2
        self.Buttons:Buttons = []
        self.Texts :Text = []
        self.Images :Image = []
        self.old_pos = pygame.mouse.get_pos()  
        self.create()

    def create(self):
        Headlilne = ic.create_Headline("Level",int(100*ic.mt))
        self.Texts.append(Headlilne[0])
        self.Buttons.append(Headlilne[1])
        self.Images.append(ic.set_background(os.path.join(paths.level)))
        self.Images.append(ic.create_shutdown_button())
        texts = []
        for file in next(os.walk(paths.level_json))[2]:
            texts.append(file.split(".")[0])
            texts.sort()
        self.Buttons+= ic.create_tabel(len(texts),Headlilne[0].pos,(500,125),[(75,135),(250,0)],Headlilne[2],(7,45,99),True,texts,50,"arial",[i for i in range(len(texts))])
        

    def repaint(self):
        ic.repaint([self.Images,self.Buttons,self.Texts])

    def update_mouse_pos(self):
        self.old_pos = pygame.mouse.get_pos()

    def check_collision(self):
        return ic.check_collision(self.Buttons,self.old_pos)
    
    def check_collision_images(self):
        return ic.check_collision(self.Images,self.old_pos)

class Settings():

    def __init__(self) -> None:
        self.id = 3
        self.Buttons:Buttons = []
        self.Texts :Text = []
        self.Images :Image = []
        self.Circle: Circle = []
        self.old_pos = pygame.mouse.get_pos()  
        self.create()

    def create(self):
        Headline = ic.create_Headline("Settings",int(100*ic.mt))
        self.Texts.append(Headline[0])
        self.Buttons.append(Headline[1])
        self.Images += [ic.set_background(paths.settings),ic.create_shutdown_button()]
        
        actions = ["fullscreen","background_music","sound_effects"]
        table = ic.create_tabel(len(actions),(Headline[0].pos),(1000,75),[(75,100),(500,0)],Headline[2],(255,105,200),False,["Fullscreen","Music","Sound_effects"],40,"arial",actions,text_pos="left",transparence=0.5)
        for indx,buttons in enumerate(table):
            self.Buttons.append(buttons)
            x = ic.create_toggle_switch(buttons,(0,0,0),(255,0,0),True,actions[indx])
            self.Circle += x[0]
            self.Buttons += x[1]
            if ic.settings[x[0][-1].get_action()]:  
                self.flip_switch_state(x[0][-1], False)
        actions2 =["volume_b","volume_e"]
        table2 = ic.create_tabel(len(actions2),(Headline[1].pos[0],self.Buttons[-1].pos[1]),(1000,75),[(75,100),(500,0)],Headline[2],(255,105,200),False,["Music_volume","Sound_effect_volume"],40,"arial",["volume_b","volume_e"],"left",0.5)
        for indx,buttons in enumerate(table2):
            percentage = ic.settings[actions2[indx]]
            self.Buttons.append(buttons)
            y = ic.create_slider(buttons,(0,0,0),(255,105,0),actions2[indx],percentage)
            buttons.add_text(str(int(round(percentage*100,0)))+"%",40,"arial")
            self.Buttons.append(y[0])
            self.Circle.append(y[1])
            
        
        
        #(255,105,200)

    def flip_switch_state(self, circle:Circle, repaint:bool or None = True):
        ic.flip_switch_state(circle, self.Buttons,repaint)
    
    def update_slider(self, circle:Circle):
        ic.update_slider(circle, self.Buttons)
    
    def slider_percentage(self, circle:Circle):
        return ic.Slider_percentage(ic.find_button_by_text("slider_"+str(circle.action),self.Buttons),ic.find_button_by_action(str(circle.action),self.Buttons),circle.pos[0])

    def repaint(self):
            ic.repaint([self.Images,self.Buttons,self.Texts,self.Circle])

    def check_collision(self):
        return ic.check_collision(self.Buttons,self.old_pos)
    
    def update_mouse_pos(self):
        self.old_pos = pygame.mouse.get_pos()
        
    def check_collision_images(self):
        return ic.check_collision(self.Images,self.old_pos)

    def check_collision_circle(self):
        return ic.check_collision(self.Circle, self.old_pos)

    
        
        
