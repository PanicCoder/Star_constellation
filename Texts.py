import pygame 

class Text():

    def __init__(self,content:str, position:tuple[int,int], color:tuple[int,int,int], font_:pygame.font.SysFont) -> None:
        self.screen = pygame.display.get_surface()
        self.content  = content
        self.pos  = position

        self.font_color = color
        self.font = font_
        
    def draw(self):
        text_surface = self.font.render(self.content,False,self.font_color)
        self.screen.blit(text_surface,self.pos)
        pygame.display.update()

    def change_text(self, content:str):
        self.content = content
    
    def change_pos(self, new_pos:tuple[int,int]):
        self.pos = new_pos
    
    def change_color(self,color):
        self.font_color = color
    def change_font(self, new_font:pygame.font.SysFont):
        self.font  = new_font

    def get_size(self):
        return self.font.size(self.content)