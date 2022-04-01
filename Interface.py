import json
import os
import pygame
from Circle import Circle
import Konstants as paths

from Buttons import Buttons
from Texts import Text
from Images import Image

class In_common():

    def __init__(self) -> None:
        self.screen = pygame.display.get_surface()
        self.mx = self.screen.get_width()/1750
        self.my = self.screen.get_height()/1000
        self.mt = self.mx/2 + self.my/2
        self.settings = {}
        self.sound_effects = {}
    
    def load_settings(self):
        file = open(paths.settings_json)
        self.settings = json.load(file)
        file.close()

    def create_music(self):
        pygame.mixer.music.load(paths.music+"Background_music.mp3")
        pygame.mixer.music.set_volume(self.settings["sound"][0]["volume_b"])
        for file in next(os.walk(paths.sound_effects))[2]:
            self.sound_effects.update({file.split(".")[0]:pygame.mixer.Sound(paths.sound_effects+file)})
            self.sound_effects[file.split(".")[0]].set_volume(self.settings["sound"][0]["volume_e"])

    def play_sound(self,sound_name):
        if self.settings["sound"][0]["sound_effects"]:
            pygame.mixer.Sound.play(self.sound_effects[sound_name])

    def update_window_scale(self):
        self.mx = self.screen.get_width()/1750
        self.my = self.screen.get_height()/1000
        self.mt = self.mx/2 + self.my/2
        
    def repaint(self, list_to_draw:list):
        #repaints all stored objects
        for list in list_to_draw:
            for element in list:
                element.draw()

        pygame.display.update()          

    def check_collision(self, collision_list:list, old_pos):
        Collisions = []
        for object in collision_list:
            if type(object) == Buttons or type(object) == Circle:
                if not object.reactive:
                    continue
            Collisions.append(object.check_collision(old_pos))
        
        for element in Collisions:
            if element[0]:
                return element

        return (False,None)

    def create_Headline(self, caption_:str,size : int, font: str or None ="arial", color:tuple or None = (0,0,0)):
        text_size = self.get_text_size(caption_,size,font)
        caption = Text(caption_,((self.screen.get_width()/2-text_size[0]/2,40*self.my)),(194, 194, 214),pygame.font.SysFont(font,size))
        under_line = self.create_underline(caption,text_size,color,True)
        return (caption, under_line,text_size)
    
    def format_text(self,content_:str,text_dimensions:tuple, size:int, pos, font: str or None ="arial", color:tuple or None = (255,255,255)):
        content = content_.split(" ")
        text_list = []
        stop = False
        while(not stop):
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
            text_list.append(Text(word_text,tuple(pos),color,pygame.font.SysFont(font,size)))
            pos[1] += self.get_text_size(word_text,size,font)[1]+10*self.my       
        return text_list

    def create_shutdown_button(self):
        return Image((50*self.mx,self.screen.get_height()-150*self.my),pygame.image.load(paths.exit),(125*self.mx,125*self.my),True,"QUIT")

    def set_background(self, image_path:str):
        return Image((0,0),pygame.image.load(image_path),(self.screen.get_width(),self.screen.get_height()),False)

    def find_text_object(self,content:str,text_list:list):
        for t in text_list:
            if t.content == content:
                return t

    def find_button_by_text(self,t:str,button_list:list):
        for button in button_list:
            if button.text!= []:
                for text in button.text:
                    if text.content == t:
                        return button

    def create_tabel(self, table_size:int, position, dimensions, gap, text_size_caption,color,reactive:bool, text_list:list, text_size_text:int,font_name:str,):
        B=[]
        i = gap[0][0]*self.my
        for k in range(table_size):
            B.append(Buttons((position[0]-gap[1][0]*self.mx,position[1]+text_size_caption[1]-gap[1][1]+i),(text_size_caption[0]+dimensions[0]*self.mx,dimensions[1]*self.my),color,reactive,k).add_text(text_list[k],text_size_text,font_name))
            i+=gap[0][1]*self.my
        return B

    def create_toggle_switch(self, position:tuple, radius:int, dimension:tuple, color_b:tuple, color_sw:tuple, action:str):
        return [[Circle(position,radius,color_b,False),Circle((position[0]+dimension[0],position[1]),radius,color_b,False),Circle(position,radius-8*self.mt,color_sw,True,action_ = action)],[Buttons((position[0],position[1]-radius),dimension,color_b,False).add_text("switch1",0,"arial",)]]

    def create_underline(self,caption:Text,text_size:tuple,color,minigate_space:bool):
        space = 10 if minigate_space else 0
        return Buttons((caption.pos[0],caption.pos[1]+text_size[1]-space),(text_size[0],4),color,False)

    def get_text_size(self, content:str, font_size:int, font:str):
        return pygame.font.SysFont(font,font_size).size(content)



