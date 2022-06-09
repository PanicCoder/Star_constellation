from typing import Callable
from xml.dom.minidom import Element
from Kompositum.BasicElement import BasicElement
from Kompositum.ListElement import ListElement


class DatenKnoten(ListElement):

    def __init__(self, A:ListElement, _Element:BasicElement) -> None:
        self.next = A
        self.Element = _Element

    def add(self, new_element:BasicElement) -> ListElement:
        self.next = self.next.add(new_element)
        return self

    def add_after_element(self, new_element: BasicElement, key: str):
        if self.Element.get_key() == key:
            self.next = DatenKnoten(self.next, new_element)
            return self
        self.next = self.next.add_after_element(new_element, key)
        return self
    
    def delete(self, key:str) -> ListElement:
        if self.Element.get_key() == key:
            return self.next
        self.next = self.next.delete(key)
        return self

    def repaint(self):
        self.Element.draw()
        self.next.repaint()

    def restor_color(self):
        self.Element.update_color_reactive(False)
        self.next.restor_color()

    def find_by_key(self, key: str) -> BasicElement:
        if self.Element.get_key() == key:
            return self.Element
        return self.next.find_by_key(key)

    def set_next(self, next_:BasicElement):
        self.next = next_

    def get_next(self) -> Callable:
        return self.next

    def get_key(self) -> str:
        return self.Element.get_key()

    def check_collision(self) -> tuple[bool, BasicElement]:
        if self.Element.check_collision()[0]:
            return self.Element.check_collision()
        return self.next.check_collision()
    
    def show_list(self):
        print(self.Element.get_key())
        self.next.show_list()