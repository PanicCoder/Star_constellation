import pygame
from Renderer import *

class Engine():
    
    def __init__(self) -> None:         
        self.Width = 1750
        self.Height = 1000
        self.screen = pygame.display.set_mode((self.Width,self.Height),pygame.RESIZABLE)

        #Current status of the game: Play,Continue,Level,Settings,Quit
        self.Status = [False,False,False,False,False]
        self.Running = True
        self.freeze = False
        self.fullscreen = False
        self.r = Game_Render()
        self.l = Game_Lobby()


    def Loop(self):
        self.r.create_Star_constellation(r".\Starfiles\Adler.json")
        self.l.create_lobby()
        while self.Running:
            self.screen.fill((0,0,0))
            pygame.display.update()

            if self.Status[0]:
                del self.r
                self.r = Game_Render()
                self.r.create_Star_constellation(r".\Starfiles\Adler.json")
                self.r.repaint()
                self.Game()
                self.Status[0],self.Status[1] = False,False

            elif self.Status[1]:
                self.r.repaint()
                self.Game()

            elif self.Status[2]:
                #TODO
                self.Level()
                self.Status[2] = False

            elif self.Status[3]:
                #TODO
                print("Settings")
                self.Status[3] = False
            else:
                self.Lobby()
        pygame.quit()

    def Lobby(self):
        selected_button = None
        self.l.repaint()
        while self.Running:
            #looks if the window got resized
            self.l.check_resize((self.screen.get_width(),self.screen.get_height()))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.Running = False
                    return
                elif event.type == pygame.VIDEORESIZE:
                    type = pygame.FULLSCREEN if self.fullscreen else pygame.RESIZABLE
                    self.screen = pygame.display.set_mode(event.size, type)
                    self.l.repaint()
                    pygame.display.update()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        for i in range(len(self.Status)):
                            self.Status[i] = False

                    if event.key == pygame.K_F11:
                        if self.fullscreen:
                            pygame.event.post(pygame.event.Event(pygame.VIDEORESIZE, size = (self.Width, self.Height)))
                        else:
                            pygame.event.post(pygame.event.Event(pygame.VIDEORESIZE, size = (1920, 1080)))
                        self.fullscreen = not self.fullscreen
                            
            collision = self.l.check_collision()
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
                self.Status[collision[1].get_action()] = not self.Status[collision[1].get_action()]
                return

            collision_images = self.l.check_collision_images()
            if collision_images[0] and pygame.mouse.get_pressed()[0]:
                if collision_images[1].action == "QUIT":
                    pygame.quit()
                    self.Running = False
                    return
            self.l.update_mouse_pos()
            pygame.time.wait(10)
        
        
    def Game(self):
        pygame.display.flip()
        clock = pygame.time.Clock()
        #pygame.mouse.set_visible(0)
        self.r.check_resize((self.screen.get_width(),self.screen.get_height()))
        while self.Running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    Running = False
                    return
                elif event.type == pygame.VIDEORESIZE:
                    type = pygame.FULLSCREEN if self.fullscreen else pygame.RESIZABLE
                    self.screen = pygame.display.set_mode(event.size, type)
                    self.r.repaint()
                    pygame.display.update()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F11:
                        if self.fullscreen:
                            pygame.event.post(pygame.event.Event(pygame.VIDEORESIZE, size = (self.Width, self.Height)))
                        else:
                            pygame.event.post(pygame.event.Event(pygame.VIDEORESIZE, size = (1920, 1080)))
                        self.fullscreen = not self.fullscreen

                    if event.key == pygame.K_ESCAPE:
                        for i in range(len(self.Status)):
                            self.Status[i] = False
                        return
                        
                    if event.key == pygame.K_RETURN:
                        self.freeze = not self.freeze
                        self.r.remove_line()
                        self.r.repaint()
                    #only triggers if the keys 0-9 are pressed on the keyboard
                    inp = event.key-49
                    if inp >-2 and inp < len(self.r.Star_list):
                        self.r.set_Star_to_use(inp) 
                        self.r.update_line_in_use()
                        self.r.repaint() 

            if not self.freeze:
                #index 0 checks the actual collision , index 1 gives back the collided star object
                collision = self.r.check_collision()    
                if pygame.mouse.get_pressed()[0] and collision[0]:
                    self.r.Lock_line(collision[1])
                    self.r.repaint()
                    pygame.time.wait(100)
                else:
                    self.r.update_line()
            self.r.update_mouse_pos()
            pygame.time.wait(10)
            clock.tick(60)

    def Level(self):
        print("Level")
