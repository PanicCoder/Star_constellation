from typing import Callable
from Kompositum.BasicElement import BasicElement
from Kompositum.DatenKnoten import DatenKnoten
from Kompositum.ListElement import ListElement
class Abschluss(ListElement):

    def __init__(self) -> None:
        pass

    def add(self,new_element:BasicElement) -> BasicElement:
        return DatenKnoten(self, new_element)
    
    def add_after_element(self, new_element: BasicElement, key: str):
        return DatenKnoten(self, new_element)

    def delete(self, key:str) -> ListElement:
        return self

    def repaint(self):
        return
    
    def restor_color(self):
        return

    def find_by_key(self,key:str) -> BasicElement:
        return None
    
    def set_next(self,next_: BasicElement):
        return
    
    def get_key(self) -> str:
        return ""

    def get_next(self) -> Callable:
        return None
    
    def check_collision(self) -> tuple[bool, BasicElement]:
        return (False,None)

    def show_list(self):
        return 