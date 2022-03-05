import pygame
from Renderer import *


pygame.init()
Width = 1750
Height = 1000
screen = pygame.display.set_mode((Width,Height),pygame.RESIZABLE)

#Current status of the game: Play,Continue,Level,Settings
Status = [False,False,False,False]
Running = True
freeze = False
fullscreen = False

pygame.display.set_caption("Sternenbilder","Galaxy")
pygame.display.set_icon(pygame.image.load(r".\Images\icon.png"))

def main():
    global Running
    render_s = Game_Render()
    render_s.create_Star_constellation(r".\Starfiles\Adler.json")
    lobby = Game_Lobby()
    lobby.create_lobby()
    
    while Running:
        screen.fill((0,0,0))
        pygame.display.update()

        if Status[0]:
            del render_s
            render_s = Game_Render()
            render_s.create_Star_constellation(r".\Starfiles\Adler.json")
            render_s.repaint()
            Game(render_s)
            Status[0],Status[1] = False,False

        elif Status[1]:
            render_s.repaint()
            Game(render_s)

        elif Status[2]:
            #TODO
            print("Level")
            Status[2] = False

        elif Status[3]:
            #TODO
            print("Settings")
            Status[3] = False

        else:
            Lobby(lobby)
    pygame.quit()

def Lobby(l:Game_Lobby):
    global Running,Status,screen,fullscreen
    selected_button = None
    l.repaint()
    while Running:
        #looks if the window got resized
        l.check_resize((screen.get_width(),screen.get_height()))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Running = False
                return
            elif event.type == pygame.VIDEORESIZE:
                type = pygame.FULLSCREEN if fullscreen else pygame.RESIZABLE
                screen = pygame.display.set_mode(event.size, type)
                l.repaint()
                pygame.display.update()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    for i in range(len(Status)):
                        Status[i] = False

                if event.key == pygame.K_F11:
                    if fullscreen:
                        pygame.event.post(pygame.event.Event(pygame.VIDEORESIZE, size = (Width, Height)))
                    else:
                        pygame.event.post(pygame.event.Event(pygame.VIDEORESIZE, size = (1920, 1080)))
                    fullscreen = not fullscreen
                         
        collision = l.check_collision()
        if collision[0] and collision[1]!=selected_button:
            selected_button = collision[1]   
            selected_button.update_color((148, 110, 159))
            selected_button.draw()
            pygame.time.wait(10)

        if selected_button!=None:
            if not selected_button.check_collision(pygame.mouse.get_pos())[0]:
                selected_button.update_color((121,92,174))
                selected_button.draw()
                selected_button = None
                pygame.time.wait(10)

        if collision[0] and pygame.mouse.get_pressed()[0]:
            Status[collision[1].get_action()] = not Status[collision[1].get_action()]
            return

        l.update_mouse_pos()
        
        
def Game(r:Game_Render):
    global Running,freeze,Status,fullscreen,screen
    pygame.display.flip()
    clock = pygame.time.Clock()
    #pygame.mouse.set_visible(0)
    r.check_resize((screen.get_width(),screen.get_height()))
    while Running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Running = False
                return
            elif event.type == pygame.VIDEORESIZE:
                type = pygame.FULLSCREEN if fullscreen else pygame.RESIZABLE
                screen = pygame.display.set_mode(event.size, type)
                r.repaint()
                pygame.display.update()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    if fullscreen:
                        pygame.event.post(pygame.event.Event(pygame.VIDEORESIZE, size = (Width, Height)))
                    else:
                        pygame.event.post(pygame.event.Event(pygame.VIDEORESIZE, size = (1920, 1080)))
                    fullscreen = not fullscreen

                if event.key == pygame.K_ESCAPE:
                    for i in range(len(Status)):
                        Status[i] = False
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