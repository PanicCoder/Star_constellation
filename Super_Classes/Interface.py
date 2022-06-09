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

    def load_settings(self) -> dict:
        with open(self.get_file_path("settings.json")) as file:
            return json.load(file)["settings"][0]
        
    def create_music(self, settings:dict) -> dict:
        sound_effects = {}
        pygame.mixer.music.load(self.get_file_path("Background_music.mp3"))
        pygame.mixer.music.set_volume(settings["volume_b"])
        for file in next(os.walk(self.get_folder_path("Sound_effects")))[2]:
            sound_effects.update({file.split(".")[0]:pygame.mixer.Sound(self.get_file_path(file))})
            sound_effects[file.split(".")[0]].set_volume(settings["volume_e"])
        return sound_effects


    def create_Headline(self, caption_:str,size : int, font: str or None ="arial", color:tuple or None = (0,0,0)) -> tuple[str,Callable,tuple[int,int]]:
        text_size = self.get_text_size(caption_,size,font)
        caption = Text(caption_,((self.screen.get_width()/2-text_size[0]/2,40*self.my)),(194, 194, 214),pygame.font.SysFont(font,size),"Headline "+caption_.split(" ")[0])
        under_line = self.create_underline(caption,text_size,color,True)
        return (caption, under_line,text_size)
    
    def format_text(self,content_:str,text_dimensions:tuple, size:int, pos, font: str or None ="arial", color:tuple or None = (255,255,255)) -> list:
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
            text_list.append(Text(word_text,tuple(pos),color,pygame.font.SysFont(font,size),"Textline"+str(i)))
            pos[1] += self.get_text_size(word_text,size,font)[1]+10*self.my       
        return text_list

    def create_shutdown_button(self) -> Callable:
        return Image((50*self.mx,self.screen.get_height()-150*self.my),pygame.image.load(self.get_file_path("Exit.png")),(125*self.mx,125*self.my),True,"Shutdown_Button","QUIT")

    def set_background(self, image_path:str) -> Callable:
        return Image((0,0),pygame.image.load(image_path),(self.screen.get_width(),self.screen.get_height()),False,"Background")
    
    def flip_switch_state(self, circle:Circle, button:Buttons):
        new_key = button.get_key().split("_")[-1]
        values = [(255,0,0),circle.pos[0]-button.dimensions[0],f"Switch_circle_off_of_{new_key}"] if circle.color == (0,255,0) else [(0,255,0),circle.pos[0]+button.dimensions[0],f"Switch_circle_on_of_{new_key}"]
        circle.update_color(values[0])
        circle.set_key(values[2])
        circle.change_pos((values[1],circle.pos[1]))
        circle.update_mask()
    
    def update_slider(self,circle:Circle,button:Buttons, parent_b:Buttons):
        pos = pygame.mouse.get_pos()[0]
        if button.pos[0] <= pos and button.pos[0]+button.dimensions[0] >= pos:
            circle.delete()
            circle.pos = (pos,circle.pos[1])
            circle.update_mask()
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

    def create_table(self, table_size:int, position, dimensions, gap, text_size_caption,color,reactive_color,reactive:bool, text_list:list, text_size_text:int,font_name:str, action:list, text_pos:str or None = "center",transparence:float or None = 1.0) -> list:
        B=[]
        i = gap[0][0]*self.my
        for k in range(table_size):
            B.append(Buttons((position[0]-gap[1][0]*self.mx,position[1]+text_size_caption[1]-gap[1][1]+i),(text_size_caption[0]+dimensions[0]*self.mx,dimensions[1]*self.my),color,reactive,f"{str(table_size)}Tb{str(k)}",reactive_color,action[k],transparent_= transparence).add_text(text_list[k],text_size_text,font_name,text_pos))
            i+=gap[0][1]*self.my
        return B

    def create_toggle_switch(self,button:Buttons, color_b:tuple, color_sw:tuple, On:bool,action:str) -> list:
        position = (button.pos[0]+button.dimensions[0]-175*self.mx,button.pos[1]+button.dimensions[1]/2)
        radius = button.dimensions[1]/2-10*self.my
        dimension = (button.dimensions[0]-(button.dimensions[0]-125*self.mx),radius*2)
        return [Buttons((position[0],position[1]-radius),dimension,color_b,False,f"Switch_Button_of_{button.get_key()}").add_text("switch_"+str(action),0,"arial",),Circle(position,radius,color_b,False,f"Switch_circle_of_{button.get_key()}"),Circle((position[0]+dimension[0],position[1]),radius,color_b,False,f"Switch_circle2_of_{button.get_key()}"),Circle(position,radius-8*self.mt,color_sw,True,f"Switch_circle_off_of_{button.get_key()}",action_ = action) if On else Circle(((position[0]+dimension[0],position[1])),radius-8*self.mt,color_sw,True,f"Switch_circle_on_of_{button.get_key()}",action_ = action)]

    def create_slider(self, button:Buttons, color_b:tuple, color_circle:tuple, action:str,percentage:float) -> list:
        position = (button.pos[0]+button.dimensions[0]-225*self.mx,button.pos[1]+button.dimensions[1]/2)
        radius = math.floor(button.dimensions[1]/3-10*self.my)
        dimension = (button.dimensions[0]-(button.dimensions[0]-150*self.mx),button.dimensions[1]-10*self.my)
        return[Buttons((position[0],position[1]-radius/2),(dimension[0],radius),color_b,False,f"Slider_Button_of_{button.get_key()}").add_text("slider_"+str(action),0,"arial"),Circle((int(position[0]+dimension[0]*percentage),position[1]),radius,color_circle,True,f"Slider_circle_of_{button.get_key()}",action)]
    
    def create_underline(self,caption:Text,text_size:tuple,color,minigate_space:bool) -> Callable:
        space = 10 if minigate_space else 0
        return Buttons((caption.pos[0],caption.pos[1]+text_size[1]-space),(text_size[0],4),color,False,"Ul"+caption.content)

    def get_text_size(self, content:str, font_size:int, font:str) -> tuple[int,int]:
        return pygame.font.SysFont(font,font_size).size(content)


