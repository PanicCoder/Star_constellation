from typing import Callable
from Kompositum.BasicElement import BasicElement
from abc import ABC, abstractmethod


class ListElement(ABC):
    
    @abstractmethod
    def add(new_element:BasicElement):
        """adds a new element to the list"""

    @abstractmethod
    def add_after_element(new_element:BasicElement, key:str):
        """adds the element after an already existing one"""

    @abstractmethod
    def delete(key:str):
        """deletes a given element from the list"""

    @abstractmethod
    def repaint():
        """draws all elements in the list"""
    	
    @abstractmethod
    def restor_color():
        """gives the element its original color back"""
    
    @abstractmethod
    def find_by_key(key:str) -> BasicElement:
        """return the BasicElement with the given key"""

    @abstractmethod
    def get_key() -> str:
        """return the key of the element"""

    @abstractmethod
    def set_next(next_:BasicElement):
        """sets a new next"""

    @abstractmethod
    def get_next() -> Callable:
        """returns the next element"""

    @abstractmethod
    def check_collision() -> tuple[bool,BasicElement]:
        """return the collision of the element"""

    @abstractmethod
    def show_list():
        """prints the elements"""