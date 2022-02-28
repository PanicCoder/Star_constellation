import pygame
import json
import time

from Stars import Star
from Lines import Line
from Texts import Text

class Render():
    
    def __init__(self) -> None:
        self.Star_list :Star = [] 
        self.Final_lines :Line = []
        self.Texts :Text =[]
        self.Star_in_use :Star = None
        self.Line_in_use :Line = None
        self.old_pos = pygame.mouse.get_pos()  
        self.star_number = 0

    def create_Star_constellation(self):
        self.load_json()
        self.Line_in_use=Line(self.Star_in_use.get_pos(),pygame.mouse.get_pos())
        self.repaint()

    def set_Star_to_use(self, index:int):
        self.Star_in_use=self.Star_list[index]

    def load_json(self):
        file = open(r".\Starfiles\Adler.json")
        data = json.load(file)
        file.close()
        content = data["constellation"][0]["constellation_name"]
        self.Texts.append(Text(content,((pygame.display.get_window_size()[0]/2)-(len(content)/2),30),(173,216,230),30))

        for Stars in data:
            if(Stars[0:4]=="Star"):
                values = data[Stars][0]
                self.Star_list.append(Star(values["pos"],values["radius"],values["brightness"],values["active"]))
        self.set_Star_to_use(self.star_number)

    def repaint(self):
        #repaints all stored objects
        for lines in self.Final_lines:
            lines.draw()


        for stars in self.Star_list:
            stars.draw()

        for text in self.Texts:
            text.display_text()

        pygame.display.update()


    def update_line(self):
        pos = pygame.mouse.get_pos()
        if(pos != self.old_pos):
            self.old_pos=pos
            self.remove_line()
            self.Line_in_use.update_line(self.Star_in_use.get_pos(),pos)
            self.repaint()
        else:
            self.old_pos=pos

    
    def remove_line(self):
        self.Line_in_use.delete()

    def check_collision(self):
        Collisions = []
        for stars in self.Star_list:
            Collisions.append(stars.check_collision(self.old_pos))
        
        #print(Collisions)
        for element in Collisions:
            if element[0]:
                return element

        return (False,None)

    def Lock_line(self, star_to_lock:Star):
        pygame.display.get_surface().fill((0,0,0))
        self.repaint()
        self.Final_lines.append(self.Line_in_use.final_line(self.Star_in_use,star_to_lock))
        self.star_number+=1
        self.Star_in_use = star_to_lock
        self.Line_in_use = Line(star_to_lock.get_pos(),pygame.mouse.get_pos())

    def is_next_star(self):
        return len(self.Star_list) > self.star_number+1

    def update_mouse_pos(self):
        self.old_pos = pygame.mouse.get_pos()

    def animation(self):
        for stars in self.Star_list:
            stars.animation()