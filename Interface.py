import pygame

class In_common():

    def __init__(self, object_) -> None:
        self.object = object_
        self.screen = pygame.display.get_surface()
        #for every object own pos
        self.old_dimensions = (self.screen.get_width(),self.screen.get_height())
        self.object_list = []

    def repaint(self, list_to_draw:list):
        #repaints all stored objects
        self.check_resize((self.screen.get_width(),self.screen.get_height()))
        for list in list_to_draw:
            for element in list:
                element.draw()

        pygame.display.update()

    def check_resize(self, new_dimensions:tuple[int,int]):
        if self.old_dimensions[0] != new_dimensions[0] or self.old_dimensions[1] != new_dimensions[1]:
            for o in self.object_list:
                if not o.id != 0:
                    o.__init__()
                else:
                    o.__init__(o.self.name)
            self.old_dimensions = new_dimensions

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



