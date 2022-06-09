
from typing import Callable


class BasicElement:
    
    def draw():
        """draws the Element"""
    
    def get_key():
        """return the key of the Element"""
    
    def set_key(new_key:str):
        """sets_a_new_key"""
        
    def check_collision() -> tuple[Callable,bool]:
        """returns the collision"""

    def update_color_reactive( case:bool):
        """updates the color to show that the element is selected"""
