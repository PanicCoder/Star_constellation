
from typing import Callable
from abc import ABC, abstractmethod

class BasicElement(ABC):
    
    @abstractmethod
    def draw():
        """draws the Element"""
    
    @abstractmethod
    def get_key():
        """return the key of the Element"""
    
    @abstractmethod
    def set_key(new_key:str):
        """sets_a_new_key"""

    @abstractmethod
    def set_render():
        """sets the element to be rendered or not"""

    def get_render() -> bool:
        """return if the element should be rendered"""

    @abstractmethod    
    def check_collision() -> tuple[Callable,bool]:
        """returns the collision"""

    @abstractmethod
    def update_color_reactive( case:bool):
        """updates the color to show that the element is selected"""
