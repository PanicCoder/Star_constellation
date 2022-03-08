import pygame

class In_common():

    def __init__(self, object_) -> None:
        self.object = object_
        self.screen = pygame.display.get_surface()
        self.object_list = []

    def repaint(self, list_to_draw:list):
        #repaints all stored objects
        for list in list_to_draw:
            for element in list:
                element.draw()

        pygame.display.update()          

    def check_collision(self, collion_list:list, old_pos):
        Collisions = []
        for stars in collion_list:
            Collisions.append(stars.check_collision(old_pos))
        
        for element in Collisions:
            if element[0]:
                return element

        return (False,None)

    def add_objects(self, object_list_:list):
        self.object_list = object_list_



