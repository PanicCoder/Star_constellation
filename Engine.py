import pygame
from Renderer import *

class Engine():
    
    def __init__(self) -> None:         
        self.Width = 1750
        self.Height = 1000
        self.screen = pygame.display.set_mode((self.Width,self.Height),pygame.RESIZABLE)

        #Current status of the game: Play,Continue,Level,Settings,Quit
        self.Status = [False,False,False,False,False]
        self.Level_names = ["Adler","Andromeda","Becher","Bootes","Cassiopeia"]
        self.level_name = self.Level_names[0]
        self.Running = True
        self.freeze = False
        self.return_flag = False
        self.fullscreen = False
        self.r = Game_Render(self.level_name)
        self.l = Game_Lobby()
        self.level = Level()

    def check_events(self,object):
        object_type = type(object)
        object.check_resize((self.screen.get_width(),self.screen.get_height()))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.Running = False
                return
            elif event.type == pygame.VIDEORESIZE:
                type_w = pygame.FULLSCREEN if self.fullscreen else pygame.RESIZABLE
                self.screen = pygame.display.set_mode(event.size, type_w)
                object.__init__()
                object.repaint()
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
                    return True

                if object_type == Game_Render:    
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
        return False

    def button_reaction(self,object,color:tuple[int,int,int],color_update:tuple[int,int,int]):
        selected_button = None
        collision = object.check_collision()
        if collision[0] and collision[1]!=selected_button:
            selected_button = collision[1]   
            selected_button.update_color(color_update)
            selected_button.draw()
            pygame.time.wait(10)

        if selected_button!=None:
            if not selected_button.check_collision(pygame.mouse.get_pos())[0]:
                selected_button.update_color(color)
                selected_button.draw()
                selected_button = None
                pygame.time.wait(10)
        
        collision_images = object.check_collision_images()
        if collision_images[0] and pygame.mouse.get_pressed()[0]:
            if collision_images[1].action == "QUIT":
                self.Running = False
                return True
        if collision[0] and pygame.mouse.get_pressed()[0] and not self.return_flag:
            if type(object) == Game_Lobby: 
                self.Status[collision[1].get_action()] = not self.Status[collision[1].get_action()]
                collision[1].update_color(color)
                return True

            elif type(object) == Level:
                self.level_name = self.Level_names[collision[1].get_action()]
                collision[1].update_color(color)
                self.return_flag = True
                return True

        if self.return_flag and not pygame.mouse.get_pressed()[0]:
            self.return_flag = False

        self.update_mouse()
        return False
    
    def update_mouse(self):
        self.l.update_mouse_pos()
        self.level.update_mouse_pos()
        self.r.update_mouse_pos()

    def Loop(self):
        while self.Running:
            self.screen.fill((0,0,0))
            pygame.display.update()
            self.update_mouse()
            if self.Status[0]:
                del self.r
                self.r = Game_Render(self.level_name)
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
        self.l.repaint()
        while self.Running:
            if self.button_reaction(self.l,(121,92,174),(148, 110, 159)) or self.check_events(self.l):
                pygame.time.wait(10)
                return
            
        
        
    def Game(self):
        pygame.display.flip()
        clock = pygame.time.Clock() 
        #pygame.mouse.set_visible(0)
        exit = False
        while self.Running:
            if exit:
                return
            exit = self.check_events(self.r)
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
        self.level.repaint()
        while self.Running:
            if self.check_events(self.level) or self.button_reaction(self.level,(7,45,99),(34,59,112)):
                pygame.time.wait(10)
                return
            
