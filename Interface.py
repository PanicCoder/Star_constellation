from matplotlib.pyplot import text
import pygame
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
        text_size = pygame.font.SysFont(font,size).size(caption_)
        caption = Text(caption_,((self.screen.get_width()/2-text_size[0]/2,40)),(194, 194, 214),pygame.font.SysFont(font,size))
        under_line = self.create_underline(caption,text_size,color,True)
        return (caption, under_line,text_size)

    def format_text(self,content:str,text_dimensions:tuple, size:int, pos:tuple, font: str or None ="arial", color:tuple or None = (255,255,255)):
        character_size = self.get_text_size(content,size,font)
        character_in_one_line = text_dimensions[0]/character_size[0]
        max_lines = text_dimensions[1]/character_size[1]
        needed_lines = len(content)/character_in_one_line
        Line_text = []
        start = 0
        end = int(character_in_one_line)
        for _ in range(int(needed_lines)+1):
            Line_text.append(content[start:end])
            start += int(character_in_one_line)
            end += int(character_in_one_line)
        text_list = []
        x = pos[0]
        y = pos[1]
        for texts in Line_text:
            text_list.append(Text(texts,(x,y),color,pygame.font.SysFont(font,size)))
            y+=character_size[1]
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



