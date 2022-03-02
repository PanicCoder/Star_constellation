import pygame
from Renderer import *


pygame.init()
Width = 1750
Height = 1000
screen = pygame.display.set_mode((Width,Height))
in_Lobby = True
Running = True
freeze = False

pygame.display.set_caption("Sternenbilder","Galaxy")
pygame.display.set_icon(pygame.image.load(r".\Images\icon.jpg"))

def main():
    global Running
    render_s = Game_Render()
    render_s.create_Star_constellation(r".\Starfiles\Adler.json")
    lobby = Game_Lobby()
    while Running:
        screen.fill((0,0,0))
        pygame.display.update()
        if in_Lobby:
            Lobby(lobby)
        else:
            render_s.repaint()
            Game(render_s)
    pygame.quit()

def Lobby(l:Game_Lobby):
    global Running,in_Lobby
    while Running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Running = False
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    in_Lobby = not in_Lobby
                    return
        l.create_lobby()
        l.repaint()
        
        
def Game(r:Game_Render):
    global Running,freeze,in_Lobby
    pygame.display.flip()
    clock = pygame.time.Clock()
    #pygame.mouse.set_visible(0)
    while Running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Running = False
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    in_Lobby = not in_Lobby
                    return
                if event.key == pygame.K_RETURN:
                    freeze = not freeze
                    r.remove_line()
                    r.repaint()
                #only triggers if the keys 0-9 are pressed on the keyboard
                inp = event.key-49
                if inp >-2 and inp < len(r.Star_list):
                    r.set_Star_to_use(inp) 
                    r.update_line_in_use()
                    r.repaint() 

        if not freeze:
            #index 0 checks the actual collision , index 1 gives back the collided star object
            collision = r.check_collision()    
            if pygame.mouse.get_pressed()[0] and collision[0]:
                r.Lock_line(collision[1])
                r.repaint()
                pygame.time.wait(100)
            else:
                r.update_line()
        r.update_mouse_pos()
        clock.tick(60)

if(__name__ == "__main__"):
    main()