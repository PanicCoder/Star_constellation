
from typing import Callable
from Kompositum.BasicElement import BasicElement


class ListElement:
    
    def add(new_element:BasicElement):
        """adds a new element to the list"""

    def add_after_element(new_element:BasicElement, key:str):
        """adds the element after an already existing one"""

    def delete(key:str):
        """deletes a given element from the list"""

    def repaint():
        """draws all elements in the list"""

    def restor_color():
        """gives the element its original color back"""

    def find_by_key(key:str) -> BasicElement:
        """return the BasicElement with the given key"""

    def get_key() -> str:
        """return the key of the element"""

    def set_next(next_:BasicElement):
        """sets a new next"""
    
    def get_next() -> Callable:
        """returns the next element"""

    def check_collision() -> tuple[bool,BasicElement]:
        """return the collision of the element"""

    def show_list():
        """prints the elements"""