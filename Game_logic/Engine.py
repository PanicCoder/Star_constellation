from matplotlib.font_manager import json_dump
import pygame
from Game_logic.Renderer import *
import json
from Super_Classes.Interface import Level as lv

class Engine(lv):
    
    def __init__(self) -> None: 
        super().__init__()   
        self.screen = pygame.display.get_surface()  
        self.settings = self.load_settings()
        self.sound_effects = self.create_music(self.settings)
        if self.settings["fullscreen"]:
            self.screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
            self.update_window_scale()
        if self.settings["background_music"]:
            pygame.mixer.music.play(-1)
        pygame.display.set_icon(pygame.image.load(self.get_file_path("Icon.png")))
        self.old_dimensions = [pygame.display.get_window_size()]

        #Current status of the game: Play,Continue,Level,Settings,Quit
        self.Status = [False,False,False,False,False]
        self.Level_names = []
        for file in next(os.walk(self.get_folder_path("Starfiles")))[2]:
            self.Level_names.append(file.split(".")[0])
        self.Level_names.sort()
        self.level_name = self.Level_names[0]
        self.Running = True
        self.freeze = False
        self.return_flag = False
        self.fullscreen = False

        self.r = Game_Render(self.level_name)
        self.l = Game_Lobby(self.level_name)
        self.level = Level()
        self.s = Settings(self.settings)
        self.object_list = [self.r,self.l,self.level,self.s]
        self.clock = pygame.time.Clock()
        
    
    def play_sound(self,sound_name):
        if self.settings["sound_effects"]:
            pygame.mixer.Sound.play(self.sound_effects[sound_name])
    
    def switch_sound(self):
        if self.settings["sound_effects"]:
            pygame.mixer.Sound.play(self.sound_effects["switch_window"])

    def check_events(self,object):
        object_type = type(object)
        if self.old_dimensions != pygame.display.get_window_size():
            for o in self.object_list:
                if o.id == 2:
                    o.__init__()
                elif o.id == 3:
                    o.__init__(self.settings)
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
                self.update_window_scale()
                if not object_type == Game_Render and not object_type == Game_Lobby:
                    object.__init__()
                elif object_type == Settings:
                    object.__init__(self.settings)
                else:
                    object.__init__(self.level_name)
                object.repaint()
                pygame.display.update()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    if self.fullscreen:
                        pygame.event.post(pygame.event.Event(pygame.VIDEORESIZE, size = (self.screen.get_size())))
                    else:
                        pygame.event.post(pygame.event.Event(pygame.VIDEORESIZE, size = (1920, 1080)))
                    self.fullscreen = not self.fullscreen

                if event.key == pygame.K_ESCAPE:
                    if object_type == Game_Lobby:
                        return
                    for i in range(len(self.Status)):
                        self.Status[i] = False
                    self.freeze = False
                    return True

                if object_type == Game_Render:    
                    if event.key == pygame.K_RETURN:
                        self.freeze = not self.freeze
                    
                    if event.key == pygame.K_DELETE:
                        if self.r.connected_stars:
                            id = self.r.connected_stars[-1]
                            if id in self.r.Instructions:
                                self.r.update_instroctions(id)
                            del self.r.connected_stars[-1]
                            self.r.list.delete_element(f"Line Star_{id[0]}-Star_{id[1]}")
                            self.r.set_Star_to_use(f"Star_{id[0]}")
                        else:
                            self.r.set_Star_to_use("Star_1") 
                        self.r.update_line_in_use()
                        self.freeze = False
                            

                    #only triggers if the keys 0-9 are pressed on the keyboard
                    inp = event.key-48
                    if inp >-1 and self.r.list.get_element_by_key(f"Star_{inp}") != None:
                        self.r.set_Star_to_use(f"Star_{inp}") 
                        self.r.update_line_in_use()

                    if event.key == pygame.K_RIGHT:
                        if self.r.list.get_element_by_key(f"Star_{str(int(self.r.Star_in_use.id)+1)}") != None:
                            self.r.set_Star_to_use(f"Star_{str(int(self.r.Star_in_use.id)+1)}")
                        else:
                            self.r.set_Star_to_use("Star_1")
                        self.r.update_line_in_use()
                        
                    elif event.key == pygame.K_LEFT:
                        if self.r.list.get_element_by_key(f"Star_{str(int(self.r.Star_in_use.id)-1)}") != None:
                            self.r.set_Star_to_use(f"Star_{str(int(self.r.Star_in_use.id)-1)}")
                        else:
                            indx = 0
                            last_star = self.r.list.get_element_by_key(f"Star_{indx+1}")
                            while last_star != None:
                                indx+=1
                                last_star = self.r.list.get_element_by_key(f"Star_{indx+1}")
                                
                            self.r.set_Star_to_use(self.r.list.get_element_by_key(f"Star_{indx}").get_key())
                        self.r.update_line_in_use()
        return False

    def r_flag(self) -> bool:
        while self.return_flag:
            pygame.event.get()
            if not pygame.mouse.get_pressed()[0]:
                self.return_flag =  False
        
    def Loop(self):
        while self.Running:
            #checks if u return from a Layer
            self.r_flag()

            if self.Status[0]:
                del self.r
                self.r = Game_Render(self.level_name)
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
        while self.Running:
            if self.check_events(self.l):
                self.switch_sound()
                return
            collision = self.l.check_collision()
            if collision[0]:
                if pygame.mouse.get_pressed()[0]:
                    if collision[1].get_key() == "Shutdown_Button":
                        self.Running = False
                        return
                    else:
                        self.Status[collision[1].get_action()] = not self.Status[collision[1].get_action()]
                        self.return_flag = True
                        return
                else:
                    collision[1].update_color_reactive(True)
            else:
                self.l.list.restore_original_color()
            self.clock.tick(60)
            self.l.repaint()
            pygame.display.update()

    def Game(self):    
        #pygame.mouse.set_visible(0)
        exit = False
        while self.Running:
            if exit:
                self.switch_sound()
                return
            exit = self.check_events(self.r)
            if not self.freeze:
                collision = self.r.check_collision()
                if collision[0] and pygame.mouse.get_pressed()[0]:
                    self.r.Lock_line(self.r.list.get_element_by_key(collision[1].get_key()))
                    pygame.mixer.Sound.set_volume(self.sound_effects["click"],0.1)
                    pygame.mixer.Sound.play(self.sound_effects["click"])
                else:
                    self.r.update_line_in_use()
            if self.r.completed_star_constellation(self):
                self.r.list.delete_element("Line")
                self.freeze = True
            self.r.repaint()
            pygame.display.update()
            self.clock.tick(60)

    def Level(self):
        while self.Running:
            if self.check_events(self.level):
                self.switch_sound()
                return
            collision = self.level.check_collision()
            if collision[0]:
                if pygame.mouse.get_pressed()[0]:
                    self.level_name = self.Level_names[collision[1].get_action()]
                    self.l.change_level_name(self.level_name)
                    self.return_flag = True
                    return
                else:
                    collision[1].update_color_reactive(True)
            else:
                self.level.list.restore_original_color()
            
            self.clock.tick(60)
            self.level.repaint()
            pygame.display.update()
            

    def Settings(self):
        slider_update = False
        slider_value = None
        exit = False
        while self.Running:
            if exit:
                self.switch_sound()
                return
            exit = self.check_events(self.s)
            collision = self.s.check_collision()
            if collision[0]:
                if pygame.mouse.get_pressed()[0]:
                    if collision[1].get_key() == "Shutdown_Button":
                        self.Running = False
                        return
                    with open(self.get_file_path("settings.json")) as file:
                        content = json.load(file)
                        if collision[1].get_key().split("_")[:2] == ["Switch","circle"]:
                            key = collision[1].get_key().split("_")[-1]
                            self.s.flip_switch_state(collision[1],self.s.list.get_element_by_key(f"Switch_Button_of_{key}"))
                            self.s.list.repaint()
                            pygame.display.update()
                            content["settings"][0][collision[1].get_action()] = not content["settings"][0][collision[1].get_action()]
                            json_dump(content,self.get_file_path("settings.json"))
                            self.__init__()

                    if collision[1].get_key().split("_")[:2] == ["Slider","circle"]:
                        key = collision[1].get_key().split("_")[-1]
                        button = self.s.list.get_element_by_key(f"Slider_Button_of_{key}")
                        key_2 = button.get_key().split("_")[-1]
                        parent_b = self.s.list.get_element_by_key(key_2)
                        self.s.update_slider(collision[1],button, parent_b)
                        slider_value = [round(self.s.slider_percentage(button, parent_b, collision[1].get_pos()[0]),4), collision[1].get_action()]
                        slider_update  = True
                        
            if slider_update and not pygame.mouse.get_pressed()[0] and slider_value != None:
                with open(self.get_file_path("settings.json")) as file:
                    content = json.load(file)
                    content["settings"][0][slider_value[1]] = slider_value[0]
                    json_dump(content,self.get_file_path("settings.json"))
                    slider_update = False 
                    self.__init__()

            self.s.repaint()
            pygame.display.update()
            self.clock.tick(60)
            
