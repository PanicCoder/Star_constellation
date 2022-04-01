import pygame

class Circle():

    def __init__(self, pos_, radius_:int, color_, reactive_:bool , action_:str or None = None) -> None:

        #X and Y Position on the surface
        self.pos = pos_    
        self.radius = radius_
        self.reactive = reactive_
        self.color = color_
        self.action = action_
        
        #creates mask for collision detection
        self.mask = pygame.Rect(self.pos[0]-self.radius,self.pos[1]-self.radius,self.radius*2,self.radius*2) 

    def draw(self):
        pygame.draw.circle(pygame.display.get_surface(),self.color,self.pos,self.radius,0)
        pygame.display.update()
    
    def change_pos(self, position:tuple[int,int]):
        self.pos = position
    
    def update_color(self, new_color):
        self.color = new_color

    def check_collision(self, pos:tuple[int,int]):
        return (self.mask.collidepoint(pos[0], pos[1]),self)

    def delete(self):
        self.color = (0,0,0)
        self.draw()
    def update_mask(self):
        self.mask = pygame.Rect(self.pos[0]-self.radius,self.pos[1]-self.radius,self.radius*2,self.radius*2)
        
    def get_action(self):
        return self.action

    def get_pos(self):
        return self.pos