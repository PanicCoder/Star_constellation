from matplotlib.pyplot import text
import pygame
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

    def create_Headline(self, caption_:str):
        text_size = pygame.font.SysFont("arial",100).size(caption_)
        caption = Text(caption_,((self.screen.get_width()/2-text_size[0]/2,40)),(194, 194, 214),pygame.font.SysFont("arial",100))
        under_line = Buttons((caption.pos[0],caption.pos[1]+text_size[1]-10),(text_size[0],4),(0,0,0),False)
        return (caption, under_line,text_size)

    def create_shutdown_button(self):
        return Image((50,self.screen.get_height()-150),pygame.image.load(r".\Images\Exit.png"),(125,125),True,"QUIT")

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



