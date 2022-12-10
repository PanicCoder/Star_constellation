from typing import Callable
import pygame
from Basic_elements.Texts import Text
from Kompositum.BasicElement import BasicElement
from Super_Classes.Screen import Screen

class Buttons(Screen, BasicElement):

    def __init__(self, pos_:tuple[int,int], dimensions_:tuple[int,int], color_, reactive_:bool, key_:str or None = "", reactive_color:tuple[int,int,int] or None = None,action_:int or None=None, filled_:int or None = 0, transparent_:float or None = None, moveable_:bool or None = False) -> None:

        super().__init__()
        self.key = key_
        self.pos = pos_    
        self.dimensions = dimensions_
        self.color = color_
        #If the user can interact with the button or not
        self.reactive = reactive_
        self.moveable = moveable_
        self.text = []
        self.filled = filled_
        self.transparent = transparent_
        self.render = True

        #gives back the action to perform
        self.action = action_
        self.color_set = [color_,reactive_color]
        #creates mask for collision detection
        self.mask = pygame.Rect(self.pos[0],self.pos[1],self.dimensions[0],self.dimensions[1]) 

    def draw(self) -> None:
        if self.transparent != None:
            s = pygame.Surface(self.dimensions)
            s.set_alpha(int(256*self.transparent))
            s.fill(self.color)
            pygame.display.get_surface().blit(s,self.pos)
        else: 
            pygame.draw.rect(pygame.display.get_surface(),self.color,(self.pos,self.dimensions),self.filled)
        if self.text != None:
            for t in self.text:
                t.draw()

    def mvdraw(self, inter:pygame.Surface) -> None:
        
        if self.transparent != None:
            s = pygame.Surface(self.dimensions)
            s.set_alpha(int(256*self.transparent))
            s.fill(self.color)
            inter.blit(s,self.pos)
            
        else: 
            pygame.draw.rect(inter,self.color,self.mask,self.filled)
            
        if self.text != None:
            for t in self.text:
                t.mvdraw(inter)
    
    def update_mask(self, pos_):
        self.mask = pygame.Rect(pos_[0],pos_[1],self.dimensions[0],self.dimensions[1])

    def update_color(self, color_:tuple[int,int,int]) -> None:
        self.color = color_

    def update_color_reactive(self, case:bool):
        if case:
            self.update_color(self.color_set[1])
        elif self.reactive:
            self.update_color(self.color_set[0])
            
    def change_pos(self, position:tuple[int,int]) -> None:
        self.pos = position
        self.update_mask(position)
        
    
    def check_collision(self) -> tuple[bool,Callable]:
        if self.reactive:
            pos = pygame.mouse.get_pos()
            return (self.mask.collidepoint(pos[0], pos[1]),self)
        return (False, self)

    def add_text(self, text_:str, size_,font_name:str, orientation:str or None = "center", color:tuple[int,int,int] or None = (0,0,0)) -> Callable:
        text_size = pygame.font.SysFont(font_name,int(size_*self.mt)).size(text_)
        if orientation == "center":
            self.text.append(Text(text_,(self.pos[0]+self.dimensions[0]/2-text_size[0]/2,self.pos[1]+self.dimensions[1]/2-text_size[1]/2),color,pygame.font.SysFont(font_name,int(size_*self.mt))))
        elif orientation == "left":
            self.text.append(Text(text_,(self.pos[0]+25*self.mx,self.pos[1]+self.dimensions[1]/2-text_size[1]/2),color,pygame.font.SysFont(font_name,int(size_*self.mt))))
        elif orientation == "right":
            self.text.append(Text(text_,(self.pos[0]+self.dimensions[0]-text_size[0]-25*self.mx,self.pos[1]+self.dimensions[1]/2-text_size[1]/2),color,pygame.font.SysFont(font_name,int(size_*self.mt))))
        return self

    def get_pos(self) -> tuple[int,int]:
        return self.pos

    def get_action(self) -> int:
        return self.action
    
    def set_render(self):
        self.render = not self.render

    def get_render(self) -> bool:
        return self.render

    def get_key(self) -> str:
        return self.key

    def set_key(self, new_key:str):
        self.key = new_key
