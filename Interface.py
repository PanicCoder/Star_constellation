import pygame
import math
import os
from Buttons import Buttons
from Texts import Text
from Images import Image

class In_common():

    def __init__(self, object_) -> None:
        self.object = object_
        self.screen = pygame.display.get_surface()

    def repaint(self, list_to_draw:list):
        #repaints all stored objects
        for list in list_to_draw:
            for element in list:
                element.draw()

        pygame.display.update()          

    def check_collision(self, collision_list:list, old_pos):
        Collisions = []
        for object in collision_list:
            if type(object) == Buttons:
                if not object.reactive:
                    continue
            Collisions.append(object.check_collision(old_pos))
        
        for element in Collisions:
            if element[0]:
                return element

        return (False,None)

    def create_Headline(self, caption_:str,size : int, font: str or None ="arial", color:tuple or None = (0,0,0)):
        text_size = self.get_text_size(caption_,size,font)
        caption = Text(caption_,((self.screen.get_width()/2-text_size[0]/2,40)),(194, 194, 214),pygame.font.SysFont(font,size))
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
            pos[1] += self.get_text_size(word_text,size,font)[1]+10       
        return text_list

    def create_shutdown_button(self):
        return Image((50,self.screen.get_height()-150),pygame.image.load(os.path.join([x[0] for x in os.walk(os.getcwd())][1], "Exit.png")),(125,125),True,"QUIT")

    def set_background(self, image_path:str):
        return Image((0,0),pygame.image.load(image_path),(self.screen.get_width(),self.screen.get_height()),False)

    def find_text_object(self,content:str,text_list:list):
        for t in text_list:
            if t.content == content:
                return t
    def find_button_by_text(self,t:str,button_list:list):
        for button in button_list:
            if button.text!= None:
                if button.text.content == t:
                    return button

    def create_underline(self,caption:Text,text_size:tuple,color,minigate_space:bool):
        space = 10 if minigate_space else 0
        return Buttons((caption.pos[0],caption.pos[1]+text_size[1]-space),(text_size[0],4),color,False)

    def get_text_size(self, content:str, font_size:int, font:str):
        return pygame.font.SysFont(font,font_size).size(content)



