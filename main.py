import pygame
import time
from Renderer import Render

pygame.init()
Width = 1750
Height = 1000
screen = pygame.display.set_mode((Width,Height))

pygame.display.set_caption("Sternenbilder","Galaxy")
pygame.display.set_icon(pygame.image.load(r".\Images\icon.jpg"))

def main():
    Running = True
    pygame.display.flip()
    clock = pygame.time.Clock()
    #pygame.mouse.set_visible(0)
    r = Render()
    r.create_Star_constellation()

    while Running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Running = False
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    Running = False
                    break
        if(r.is_next_star()):
            collision = r.check_collision()    #index 0 checks the actual collision , index 1 gives back the collided star object
            if pygame.mouse.get_pressed()[0] and collision[0]:
                r.Lock_line(collision[1])
                r.repaint()
                pygame.time.wait(100)
            else:
                r.update_line()
        r.update_mouse_pos()
        clock.tick(60)   
    pygame.quit()
if(__name__ == "__main__"):
    main()