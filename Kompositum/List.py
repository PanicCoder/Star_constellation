from Kompositum.Abschluss import Abschluss
from Kompositum.BasicElement import BasicElement
from Kompositum.DatenKnoten import DatenKnoten
import copy

class List():

    def __init__(self) -> None:
        self.first_element = Abschluss()

    def add_element(self, new_element:BasicElement):
        temp = DatenKnoten(Abschluss(), new_element)
        temp.set_next(self.first_element)
        self.first_element = temp

    def add_element_at_end(self, new_element:BasicElement):
        self.first_element = self.first_element.add(new_element)
    
    def add_element_after_element(self, new_element:BasicElement, key:str):
        self.first_element = self.first_element.add_after_element(new_element, key)

    def delete_element(self, key:str):
        self.first_element = self.first_element.delete(key)
    
    def swap_elements(self, key_1:str, key_2:str):
        #create a copy to change the key
        temp_1 = copy.deepcopy(self.get_element_by_key(key_1))
        temp_1.set_key(temp_1.get_key()+"*")
        temp_2 = copy.deepcopy(self.get_element_by_key(key_2))
        temp_2.set_key(temp_2.get_key()+"*")
        #add new elements
        self.add_element_after_element(temp_1,key_2)
        self.add_element_after_element(temp_2,key_1)
        #delete old elements
        self.delete_element(key_1)
        self.delete_element(key_2)
        #reset the key
        temp_1.set_key(key_1)
        temp_2.set_key(key_2)

    def repaint(self):
        self.first_element.repaint()

    def restore_original_color(self):
        self.first_element.restor_color()

    def get_element_by_key(self, key:str) -> BasicElement:
        return self.first_element.find_by_key(key)

    def check_collision(self) -> tuple[bool, BasicElement]:
        return self.first_element.check_collision()
    
    def show_list(self):
        self.first_element.show_list()