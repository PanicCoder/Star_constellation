from ast import Str
import math
import json
import os
from typing import Callable
import pygame

from Basic_elements.Circle import Circle
from Super_Classes.Screen import Screen
from Basic_elements.Buttons import Buttons
from Basic_elements.Texts import Text
from Basic_elements.Images import Image

class Level(Screen):

    def __init__(self) -> None:
        super().__init__()

    def get_file_path(self,file_name) -> str:
        for root, _, files in os.walk(".", topdown=False):
            for name in files:
                if name == file_name:
                    return os.path.join(root, name)

    def get_folder_path(self,folder_name) -> str:
        for root, folder, _ in os.walk(".", topdown=False):
            for name in folder:
                if name == folder_name:
                    return os.path.join(root, name)

    def element_by_key(self, slist:list, key:str):
        for elements in slist:
            if key == elements.get_key():
                return elements
        return None
    
    def repaint(self, rlist:list, intermediate:pygame.Surface or None = None, scroll_y:float or None = None):
        intermediate.fill(0)
        for lists in rlist:
            for elements in lists:
                if elements.moveable:
                    elements.update_mask([elements.get_pos()[0], elements.get_pos()[1]+scroll_y])
                    elements.mvdraw(intermediate)       
                else:
                    elements.draw()

    def check_collision(self, rlist:list) -> tuple[bool, any]:
        for lists in rlist:
            for elements in lists:
                if elements.check_collision()[0]:
                    return [True,elements]
        return [False, None]

    def restore_color(self,clist:list):
        for lists in clist:
            for elements in lists:
                elements.update_color_reactive(False)

    def load_settings(self) -> dict:
        with open(self.get_file_path("settings.json")) as file:
            return json.load(file)["settings"][0]
        
    def create_music(self, settings:dict) -> dict:
        sound_effects = {}
        pygame.mixer.music.load(self.get_file_path("Background_music.mp3"))
        pygame.mixer.music.set_volume(settings["volume_b"]/10)
        for file in next(os.walk(self.get_folder_path("Sound_effects")))[2]:
            sound_effects.update({file.split(".")[0]:pygame.mixer.Sound(self.get_file_path(file))})
            sound_effects[file.split(".")[0]].set_volume(settings["volume_e"])
        return sound_effects


    def create_Headline(self, caption_:str,size : int, font: str or None ="arial", color:tuple or None = (0,0,0), moveable:bool or None = False) -> tuple[str,Callable,tuple[int,int]]:
        text_size = self.get_text_size(caption_,size,font)
        caption = Text(caption_,((self.screen.get_width()/2-text_size[0]/2,40*self.my)),(194, 194, 214),pygame.font.SysFont(font,size),"Headline "+caption_.split(" ")[0],moveable_=moveable)
        under_line = self.create_underline(caption,text_size,color,True)
        under_line.moveable = moveable
        return (caption, under_line,text_size)
    
    def format_text(self,content_:str,text_dimensions:tuple, size:int, pos:list, font: str or None ="arial", color:tuple or None = (255,255,255)) -> list:
        content = content_.split(" ")
        text_list = []
        stop = False
        i = 0
        while(not stop):
            i+=1
            word_sizes = self.get_text_size(content[1]+" ",size,font)[0]
            word_text = ""
            while(not stop):
                word_sizes += self.get_text_size(content[1]+" ",size,font)[0]
                if word_sizes > text_dimensions[0]:
                    break
                word_text += content[0]+" "
                del content[0]
                if len(content)<2:
                    word_text+=content[0]
                    
                    stop = True
            text_list.append(Text(word_text,tuple(pos),color,pygame.font.SysFont(font,size),"Textline"+str(i),moveable_=True))
            pos[1] += self.get_text_size(word_text,size,font)[1]+10*self.my       
        return text_list

    def create_shutdown_button(self) -> Callable:
        return Image((50*self.mx,self.screen.get_height()-150*self.my),self.get_file_path("Exit.png"),(125*self.mx,125*self.my),True,"Shutdown_Button","QUIT")

    def set_background(self, image_path:str) -> Callable:
        return Image((0,0),image_path,(self.screen.get_width(),self.screen.get_height()),False,"Background")
    
    def flip_switch_state(self, circle:Circle, button:Buttons):
        new_key = button.get_key().split("_")[-1]
        values = [(255,0,0),circle.pos[0]-button.dimensions[0],f"Switch_circle_off_of_{new_key}"] if circle.color == (0,255,0) else [(0,255,0),circle.pos[0]+button.dimensions[0],f"Switch_circle_on_of_{new_key}"]
        circle.update_color(values[0])
        circle.set_key(values[2])
        circle.change_pos((values[1],circle.pos[1]))
        circle.update_mask_2()
    
    def update_slider(self,circle:Circle,button:Buttons, parent_b:Buttons):
        pos = pygame.mouse.get_pos()[0]
        if button.pos[0] <= pos and button.pos[0]+button.dimensions[0] >= pos:
            circle.delete()
            circle.pos = (pos,circle.pos[1])
            circle.update_mask_2()
            parent_b.draw()
            button.draw()
            circle.draw()
            self.Slider_percentage(button,parent_b,pos)

    def Slider_percentage(self,button:Buttons,parent_button:Buttons,pos:int) -> float:
        current_value = pos-button.pos[0]
        max_value = button.dimensions[0]
        percentage = current_value/max_value
        parent_button.text[1].content = str(int(round(percentage*100,0)))+"%"
        return percentage

    def create_table(self, table_size:int, position, dimensions, gap, text_size_caption,color,reactive_color,reactive:bool, text_list:list, text_size_text:int,font_name:str, action:list, text_pos:str or None = "center",transparence:float or None = 1.0, moveable:bool or None = False) -> list:
        B=[]
        i = gap[0][0]*self.my
        for k in range(table_size):
            B.append(Buttons((position[0]-gap[1][0]*self.mx,position[1]+text_size_caption[1]-gap[1][1]+i),(text_size_caption[0]+dimensions[0]*self.mx,dimensions[1]*self.my),color,reactive,f"{str(table_size)}Tb{str(k)}",reactive_color,action[k],transparent_= transparence, moveable_=moveable).add_text(text_list[k],text_size_text,font_name,text_pos))
            i+=gap[0][1]*self.my
        return B

    def create_toggle_switch(self,button:Buttons, color_b:tuple, color_sw:tuple, On:bool,action:str, moveable:bool or None = False) -> list:
        position = (button.pos[0]+button.dimensions[0]-175*self.mx,button.pos[1]+button.dimensions[1]/2)
        radius = button.dimensions[1]/2-10*self.my
        dimension = (button.dimensions[0]-(button.dimensions[0]-125*self.mx),radius*2)
        return [Buttons((position[0],position[1]-radius),dimension,color_b,False,f"Switch_Button_of_{button.get_key()}",moveable_=moveable).add_text("switch_"+str(action),0,"arial"),Circle(position,radius,color_b,False,f"Switch_circle_of_{button.get_key()}",moveable_=moveable),Circle((position[0]+dimension[0],position[1]),radius,color_b,False,f"Switch_circle2_of_{button.get_key()}", moveable_=moveable),Circle(position,radius-8*self.mt,color_sw,True,f"Switch_circle_off_of_{button.get_key()}",action_ = action, moveable_=moveable) if On else Circle(((position[0]+dimension[0],position[1])),radius-8*self.mt,color_sw,True,f"Switch_circle_on_of_{button.get_key()}",action_ = action, moveable_=moveable)]

    def create_slider(self, button:Buttons, color_b:tuple, color_circle:tuple, action:str,percentage:float, moveable:bool or None = False) -> list:
        position = (button.pos[0]+button.dimensions[0]-225*self.mx,button.pos[1]+button.dimensions[1]/2)
        radius = math.floor(button.dimensions[1]/3-10*self.my)
        dimension = (button.dimensions[0]-(button.dimensions[0]-150*self.mx),button.dimensions[1]-10*self.my)
        return[Buttons((position[0],position[1]-radius/2),(dimension[0],radius),color_b,False,f"Slider_Button_of_{button.get_key()}", moveable_=moveable).add_text("slider_"+str(action),0,"arial"),Circle((int(position[0]+dimension[0]*percentage),position[1]),radius,color_circle,True,f"Slider_circle_of_{button.get_key()}",action, moveable_=moveable)]
    
    def create_underline(self,caption:Text,text_size:tuple,color,minigate_space:bool) -> Callable:
        space = 10 if minigate_space else 0
        return Buttons((caption.pos[0],caption.pos[1]+text_size[1]-space),(text_size[0],4),color,False,"Ul"+caption.content)

    def create_side_bar(self, h_height):
        factor = self.screen.get_height()/(self.screen.get_height()+h_height)
        bar_dim = (30,self.screen.get_height()*factor)
        bar = Buttons((self.screen.get_width()-bar_dim[0],0),(bar_dim[0],self.screen.get_height()),(115,147,179),False,"Sb1",transparent_=0.6)
        move_rec = Buttons((self.screen.get_width()-bar_dim[0], 0), bar_dim,(0,0,0),True,"Sb2",(55,55,55),action_ = -1,transparent_=0.6)
        return [bar,move_rec]

    def bar_pos(self,scroll_y:float, inter_h:float):
        y = abs(scroll_y)/(inter_h-self.screen.get_height())
        return y

    def update_sidebar_slider(self, Sbbutton:Buttons, scroll_y, inter_h):
        Sbbutton.change_pos([self.screen.get_width()-Sbbutton.dimensions[0], self.bar_pos(scroll_y, inter_h)*(self.screen.get_height()-Sbbutton.dimensions[1])])

    def get_text_size(self, content:str, font_size:int, font:str) -> tuple[int,int]:
        return pygame.font.SysFont(font,font_size).size(content)
    
    def get_image_size(self, img_name:str) -> tuple[int,int]:
        img = pygame.image.load(self.get_file_path(img_name))
        return img.get_rect().size


