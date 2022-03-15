import pygame
from Renderer import *

class Engine():
    
    def __init__(self) -> None:         
        self.Width = 1750
        self.Height = 1000
        self.screen = pygame.display.set_mode((self.Width,self.Height),pygame.RESIZABLE)
        self.old_dimensions = [pygame.display.get_window_size()]

        #Current status of the game: Play,Continue,Level,Settings,Quit
        self.Status = [False,False,False,False,False]
        self.Level_names = ["Adler","Andromeda","Becher","Bootes","Cassiopeia"]
        self.level_name = self.Level_names[0]
        self.Running = True
        self.freeze = False
        self.return_flag = False
        self.fullscreen = False
        self.star_index = 0
        self.r = Game_Render(self.level_name)
        self.l = Game_Lobby(self.level_name)
        self.level = Level()
        self.settings = Settings()
        self.object_list = [self.r,self.l,self.level,self.settings]

    def check_events(self,object):
        pygame.time.wait(10)
        object_type = type(object)
        if self.old_dimensions != pygame.display.get_window_size():
            for o in self.object_list:
                if o.id != 0 and o.id !=1:
                    o.__init__()
                else:
                    o.__init__(self.level_name)
            self.old_dimensions = pygame.display.get_window_size()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.Running = False
                return
            elif event.type == pygame.VIDEORESIZE:
                type_w = pygame.FULLSCREEN if self.fullscreen else pygame.RESIZABLE
                self.screen = pygame.display.set_mode(event.size, type_w)
                if not object_type == Game_Render and not object_type == Game_Lobby:
                    object.__init__()
                else:
                    object.__init__(self.level_name)
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
                    self.freeze = False
                    return True

                if object_type == Game_Render:    
                    if event.key == pygame.K_RETURN:
                        self.freeze = not self.freeze
                        self.r.remove_line()
                        self.r.reapaint(False)
                    
                    if event.key == pygame.K_DELETE:
                        if self.r.Final_lines and self.r.connected_stars:
                            id = self.r.connected_stars[-1]
                            if id in self.r.Instructions:
                                self.r.update_instroctions(id)
                            del self.r.connected_stars[-1]
                            self.r.Final_lines[-1].delete()
                            del self.r.Final_lines[-1]  
                        else:
                            self.r.set_Star_to_use(0) 
                            self.r.update_line_in_use()
                        self.freeze = False
                        self.r.repaint(False)
                            

                    #only triggers if the keys 0-9 are pressed on the keyboard
                    inp = event.key-49
                    if inp >-2 and inp < len(self.r.Star_list):
                        self.r.set_Star_to_use(inp) 
                        self.r.update_line_in_use()
                        self.r.repaint(False)

                    if event.key == pygame.K_RIGHT:
                        if self.star_index+1 < len(self.r.Star_list):
                            self.star_index += 1
                        else:
                            self.star_index = 0
                        self.r.set_Star_to_use(self.star_index) 
                        self.r.update_line_in_use()
                        self.r.repaint(False)
                        
                    elif event.key == pygame.K_LEFT:
                        if self.star_index -1 >= 0:
                            self.star_index -=1  
                        else: 
                            self.star_index = len(self.r.Star_list)-1
                        self.r.set_Star_to_use(self.star_index) 
                        self.r.update_line_in_use()
                        self.r.repaint(False)
        return False

    def button_reaction(self,object,color:tuple[int,int,int] or None = None,color_update:tuple[int,int,int] or None = None):
        pygame.time.wait(10)
        selected_button = None
        collision = object.check_collision()
        if type(object) == Game_Render: 
            if pygame.mouse.get_pressed()[0] and collision[0]:
                object.Lock_line(collision[1])
                object.repaint()
                pygame.time.wait(100)
            else:
                object.update_line()
            self.update_mouse()
            return
        if collision[0] and collision[1]!=selected_button:
            selected_button = collision[1]   
            selected_button.update_color(color_update)
            selected_button.draw()
            pygame.time.wait(10)

        if selected_button!=None:
            if not selected_button.check_collision(pygame.mouse.get_pos())[0]:
                selected_button.update_color(color)
                selected_button.draw()
                if type(object) == Game_Lobby:
                    t = object.get_level_text()
                    if t != None:
                        t.draw()
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
                self.return_flag = True
                return True

            elif type(object) == Level and not self.return_flag:
                self.level_name = self.Level_names[collision[1].get_action()]
                collision[1].update_color(color)
                self.return_flag = True
                return True

        if self.return_flag and not pygame.mouse.get_pressed()[0]:
            self.return_flag = False

        self.update_mouse()
        return False
    
    def update_mouse(self):
        for object in self.object_list:
            object.update_mouse_pos()

    def Loop(self):
        while self.Running:
            self.screen.fill((0,0,0))
            pygame.display.update()
            self.l.choosen_level(self.level_name)
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
                #TODO add scrolling
                self.Level()
                self.Status[2] = False

            elif self.Status[3]:
                #TODO
                self.Settings()
                self.Status[3] = False
            else:
                self.Lobby()
        pygame.quit()

    def Lobby(self):
        self.l.repaint()
        
        while self.Running:
            if self.button_reaction(self.l,color=(121,92,174),color_update=(148, 110, 159)) or self.check_events(self.l):
                return
            pygame.time.wait(10)
            
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
                self.button_reaction(self.r)
            pygame.time.wait(10)
            clock.tick(60)
            if self.r.completed_star_constellation():
                self.freeze = True

    def Level(self):
        self.level.repaint()
        while self.Running:
            if self.check_events(self.level) or self.button_reaction(self.level,color=(7,45,99),color_update=(34,59,112)):
                return
        pygame.time.wait(10)

    def Settings(self):
        self.settings.repaint()
        while self.Running:
            if self.check_events(self.settings) or self.button_reaction(self.settings,color=(7,45,99),color_update=(34,59,112)):
                return
            pygame.time.wait(10)
            
