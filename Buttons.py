import pygame
from Texts import Text

class Buttons():

    def __init__(self, pos_:tuple[int,int], dimensions_:tuple[int,int], color_, reactive_:bool, action_:int or None=None, filled_:int or None = 0, transparent_:bool or None = False) -> None:

        #X and Y Position on the surface
        self.pos = pos_    
        self.dimensions = dimensions_
        self.clock = pygame.time.Clock()
        self.color = color_
        self.reactive = reactive_
        self.text = None
        self.filled = filled_
        self.transparent = transparent_

        #gives back the action to perform
        self.action = action_
        #creates mask for collision detection
        self.mask = pygame.Rect(self.pos[0],self.pos[1],self.dimensions[0],self.dimensions[1]) 

    def draw(self):
        if self.transparent:
            s = pygame.Surface((1000,50))
            s.set_alpha(128)
            s.fill((255,105,200))
            pygame.display.get_surface().blit(s,(400,300))
        else: 
            pygame.draw.rect(pygame.display.get_surface(),self.color,(self.pos,self.dimensions),self.filled)
        if self.text != None:
            self.text.draw()
        pygame.display.update()

    def update_color(self, color_:tuple[int,int,int]):
        self.color = color_
    
    def change_pos(self, position:tuple[int,int]):
        self.pos = position
    
    def check_collision(self, pos:tuple[int,int]):
        return (self.mask.collidepoint(pos[0], pos[1]),self)

    def add_text(self, text_:Text):
        self.text = text_
        return self

    def get_pos(self):
        return self.pos

    def get_action(self):
        return self.action
