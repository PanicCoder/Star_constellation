from typing import Tuple
import pygame

class Star():

    def __init__(self, pos_:Tuple[int,int], radius_:int, bright:float, active_:bool) -> None:

        #X and Y Position on the surface
        self.pos = pos_    
        self.radius = radius_
        self.clock = pygame.time.Clock()

        #1 dark 0 brightest
        self.brightness = bright  
        self.color = (255-(self.brightness*255),255-(self.brightness*255),255-(self.brightness*255))
        self.active = active_
        self.screen = pygame.display.get_surface()
        
        #creates mask for collision detection
        self.mask = pygame.Rect(self.pos[0]-self.radius,self.pos[1]-self.radius,self.radius*2,self.radius*2) 

    def draw(self):
        if(self.active):
            pygame.draw.circle(self.screen,self.color,self.pos,self.radius,0)
            pygame.display.update()

    #gradually decreases the brightness until the star is invisible   
    def animation(self):
        while(self.brightness < 1):
            self.draw()
            self.clock.tick(5)
            self.update_color(self.brightness+0.05)
        self.update_color(1)
        self.draw()

    def update_color(self, bright:float):
        self.color = (255-(bright*255),255-(bright*255),255-(bright*255))
        self.brightness = bright
    
    def change_pos(self, position:Tuple[int,int]):
        self.pos = position
    
    def check_collision(self, pos:Tuple[int,int]):
        return (self.mask.collidepoint(pos[0], pos[1]),self)

    def get_pos(self):
        return self.pos

    def change_status(self, status:bool):
        self.active = status