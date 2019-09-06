import pygame
import os
import time
import random

from pygame.locals import *
from operator import itemgetter


############################################################
"""
    Main Functions
"""
class Setup():
    def __init__(self):
        """
        Information :
            Background  : Path to the background
            Music       : Path to the music

        State :
            Button      : Displays the buttons in the list of buttons
            Text        : Display the texts in the list of texts

        Tools :
            events      : pygame.event.get()
            event       : event in self.events
        """
        # Information
        self.background     = None
        self.music          = None

        # State
        self.button         = False
        self.list_button    = []
        
        self.text           = False
        self.list_text      = []

        # Tools
        self.event          = ""
        self.events         = "" 


    def update_init(self, background=None, music=None, button=False, text=False):
        self.background = background
        self.update_music(music)

        self.button         = button
        self.list_button    = []
        
        self.text           = text
        self.list_text      = []


    def update_music(self, music):
        if self.music != music and music != None:
            self.music = music
            pygame.mixer.music.load(music)
            pygame.mixer.music.play(-1)
            

    def update_1(self):
        """
        Setup :
            Update game screen and background
            Retrieves game events in global variables
        """
        if self.background != None:
            gameDisplay.blit(self.background, (0,0))
        
        self.events = pygame.event.get()
        for event in self.events:
            self.event = event

        

    def update_2(self):
        """
        Interface :
            Button:
                Length prevents crash from removing an element from the list
                Check for mouse position and call function action() when clicking on it
            Text
        """
        # Button
        if self.button == True:
            for index in self.list_button:
                index.update()

        # Text
        if self.text == True:
            for index in self.list_text:
                index.update()
Setup = Setup()



class Button():
    def __init__(self, text, sound, pos, display, selection, action=None):
        """
        Setup :
            Enable buttons
            Add button to list_button
        
        Position :
            x, y, width, height, border width, border, center
            
        Text :
            Add centered text on the button
            
        Display :
            Active/Inactive button depending of the mouse position
        
        Action :
            Selection   : Variable
            Action      : Callable function
        """
        # Setup
        Setup.button = True
        Setup.list_button.append(self)


        # Text
        self.text, self.font = text[0], text[1]


        # Sound Effect
        self.sound_action   = sound[0]
        self.sound_active   = sound[1]
        self.sound_state    = False


        # Position
        self.center     = pos[0]
        self.x          = pos[1]
        self.y          = pos[2]
        
        if len(pos) > 3:
            self.w      = pos[3]
            self.h      = pos[4]
            self.b      = pos[5]
            self.border = pos[6]


        # Button
        if isinstance(display[0], tuple) == True or display[0] is None:
            self.inactive   = display[0]
            self.active     = display[1]
            self.display    = self.inactive

            # Center
            if self.center == True:
                self.x  = self.x - self.w/2
                self.y  = self.y - self.h/2
            self.rect   = pygame.Rect(self.x, self.y, self.w, self.h)


        # Button Image
        elif isinstance(display[0], pygame.Surface) == True:
            self.inactive   = display[0].convert()
            self.active     = display[1].convert()
            self.display    = self.inactive

            # Center
            if self.center == False:
                self.rect = self.display.get_rect(topleft=(self.x, self.y))

            elif self.center == True:
                self.rect = self.display.get_rect(center=(self.x, self.y))
        
        # Action
        self.selection  = selection
        self.action     = action

        # Scale
        self.factor_w       = 1
        self.factor_h       = 1
        self.x_scaled       = self.rect[0]
        self.y_scaled       = self.rect[1]
        self.w_scaled       = self.rect[2]
        self.h_scaled       = self.rect[3]
        self.rect_scaled    = self.rect
        self.resize         = False


    def update_scale(self):
        if self.factor_w != gameDisplay.factor_w:
            self.factor_w = gameDisplay.factor_w
            self.x_scaled = self.rect[0] * self.factor_w
            self.w_scaled = self.rect[2] * self.factor_w
            self.resize   = True
            
        if self.factor_h != gameDisplay.factor_h:
            self.factor_h = gameDisplay.factor_h
            self.y_scaled = self.rect[1] * self.factor_h
            self.h_scaled = self.rect[3] * self.factor_h
            self.resize   = True

        if self.resize == True:
            self.rect_scaled =  pygame.Rect(self.x_scaled, self.y_scaled, self.w_scaled, self.h_scaled)
            self.resize = False


    def update(self):
        # Button
        if isinstance(self.display, tuple) == True:
            pygame.draw.rect(gameDisplay, self.display, self.rect)

            if self.border == True:
                pygame.draw.rect(gameDisplay, color_black, self.rect, self.b)

        # Button Image
        elif isinstance(self.display, pygame.Surface) == True:
            gameDisplay.blit(self.display, self.rect)

        
        # Text
        if self.text != None or self.font != None:
            font, color     = self.font()
            textSurf        = font.render(self.text, True, color)
            textRect        = textSurf.get_rect()
            textRect.center = (self.x + self.w/2), (self.y + self.h/2)
            gameDisplay.blit(textSurf, textRect)


        for event in Setup.events:
            mouse = pygame.mouse.get_pos()
            self.update_scale()

            if self.rect_scaled.collidepoint(mouse):
                self.display = self.active

                if self.sound_active != None and self.sound_state == False:
                    pygame.mixer.Sound.play(self.sound_active)
                    self.sound_state = True

                if Setup.event.type == pygame.MOUSEBUTTONDOWN and Setup.event.button == 1 and self.action != None:
                    if self.sound_action != None:
                        pygame.mixer.Sound.play(self.sound_action)

                    if self.selection != None:
                        self.action(self.selection)
                    else:
                        self.action()
                
                    
            else:
                self.display     = self.inactive
                self.sound_state = False



class Text():
    def __init__(self, text, pos, hollow=False, outline=False, stroke=0, setup=False):
        """
        Setup       : Add text to the text_list
        Text        : Text string, font, color
        Position    : Position x, y, surface, center
        """
        # Text
        self.text               = text[0]
        self.font, self.color   = text[1]()

        # Position
        self.center      = pos[0]
        self.x           = pos[1]
        self.y           = pos[2]
        self.textSurface = self.font.render(self.text, True, self.color)
    
        # Center
        if self.center == False:
            self.textRect        = (self.x, self.y)
            
        elif self.center == True:
            self.textRect        = self.textSurface.get_rect()
            self.textRect.center = (self.x, self.y)


        # Hollow/Outline
        self.hollow     = hollow
        self.outline    = outline
        self.stroke     = stroke

        if isinstance(self.outline, tuple) == True:
            self.textSurface = self.textOutline(self.font, self.text, self.color, self.outline, self.stroke)

        elif hollow == True:
            self.textSurface = self.textHollow(self.font, self.text, self.color, self.stroke)

        
        # Setup
        if setup == True:
            Setup.text = True
            Setup.list_text.append(self)
            
        elif setup == False:
            gameDisplay.blit(self.textSurface, self.textRect)


    def textHollow(self, font, message, fontcolor, stroke):
        notcolor = [c^0xFF for c in fontcolor]
        base     = font.render(message, 0, fontcolor, notcolor)
        size     = base.get_width() + stroke, base.get_height() + stroke
        img      = pygame.Surface(size, 16)
        img.fill(notcolor)
        base.set_colorkey(0)

        for a in range(-stroke, 3+stroke):
            for b in range(-stroke, 3+stroke):
                img.blit(base, (a, b))

        base.set_colorkey(0)
        base.set_palette_at(1, notcolor)
        img.blit(base, (1, 1))
        img.set_colorkey(notcolor)
        return img

    def textOutline(self, font, message, fontcolor, outlinecolor, stroke):
        base    = font.render(message, 0, fontcolor)
        outline = self.textHollow(font, message, outlinecolor, stroke)
        img     = pygame.Surface(outline.get_size(), 16)
        img.blit(base, (1, 1))
        img.blit(outline, (0, 0))
        img.set_colorkey(0)
        return img
            

    def update(self):
        gameDisplay.blit(self.textSurface, self.textRect)



def text_title():
    font = pygame.font.SysFont(None, 100)
    color = color_button
    return font, color


def Text_Button():
    font = pygame.font.SysFont(None, 40)
    color = color_blue
    return font, color


def text_interface():
    font = pygame.font.SysFont(None, 35)
    color = color_black
    return font, color

def text_interface_2():
    font = pygame.font.SysFont(None, 30)
    color = color_black
    return font, color



############################################################
"""
    ScaledGame
"""
class ScaledGame(pygame.Surface):
    game_size       = None
    screen          = None
    clock           = None
    resize          = True
    game_gap        = None
    game_scaled     = None
    title           = None
    fps             = True
    set_fullscreen  = False
    factor_w        = 1
    factor_h        = 1


    def __init__(self, title, game_size):
        pygame.init()

        # Title
        self.title = title
        pygame.display.set_caption(self.title)

        # Window Settings
        self.game_size  = game_size
        screen_info     = pygame.display.Info()                                 # Required to set a good resolution for the game screen
        first_screen    = (screen_info.current_w, screen_info.current_h - 120)  # Take 120 pixels from the height because of the menu bar, window bar and dock takes space

        # self.screen     = pygame.display.set_mode(first_screen, RESIZABLE)
        self.screen     = pygame.display.set_mode(game_size, RESIZABLE)
        
        pygame.Surface.__init__(self,self.game_size) #Sets up the Surface for the game.
        self.game_gap   = (0,0)

        # Game Settings
        self.clock      = pygame.time.Clock()

        
    def get_resolution(self, ss, gs): 
        gap = float(gs[0]) / float(gs[1])
        sap = float(ss[0]) / float(ss[1])
        if gap > sap:
            #Game aspect ratio is greater than screen (wider) so scale width
            factor = float(gs[0]) /float(ss[0])
            new_h = gs[1]/factor #Divides the height by the factor which the width changes so the aspect ratio remains the same.
            game_scaled = (ss[0],new_h)
        elif gap < sap:
            #Game aspect ratio is less than the screens.
            factor = float(gs[1]) /float(ss[1])
            new_w = gs[0]/factor #Divides the width by the factor which the height changes so the aspect ratio remains the same.
            game_scaled = (new_w,ss[1])
        else:
            game_scaled = self.screen.get_size()
        return game_scaled


    def fullscreen(self):
        if self.set_fullscreen == False:
            self.screen = pygame.display.set_mode(self.game_size, FULLSCREEN)
            self.factor_w = 1
            self.factor_h = 1
            self.set_fullscreen = True
        
        else:
            self.resize = True
            self.set_fullscreen = False


    def update(self):
        # Display FPS in window title
        if self.fps == True:
            pygame.display.set_caption(self.title + " - " + str(int(self.clock.get_fps())) + "fps")


        #Updates screen properly
        win_size_done = False #Changes to True if the window size is got by the VIDEORESIZE event below
        for event in Setup.events:
            if event.type == VIDEORESIZE:
                ss = [event.w, event.h]
                self.resize = True
                win_size_done = True


        # Fullscreen & Resize
        if self.set_fullscreen == False:                
            #Scale game to screen resolution, keeping aspect ratio
            if self.resize == True:
                if(win_size_done == False): #Sizes not gotten by resize event
                    ss = [self.screen.get_width(),self.screen.get_height()]
                self.game_scaled = self.get_resolution(ss,self.game_size)
                self.game_scaled = int(self.game_scaled[0]), int(self.game_scaled[1])
                self.screen = pygame.display.set_mode(self.game_scaled, RESIZABLE)

                # Usable Variable
                self.factor_w = self.game_scaled[0] / self.get_width()
                self.factor_h = self.game_scaled[1] / self.get_height()
                    
            self.resize = False #Next time do not scale unless resize or fullscreen events occur
            self.screen.blit(pygame.transform.scale(self,self.game_scaled), self.game_gap) #Add game to screen with the scaled size and gap required.

        else:
            self.screen.blit(self, self.game_gap)

        pygame.display.flip()
        self.clock.tick(60)



def transparent_image(image, x, y, opacity, screen):
    image = image.convert_alpha()
    alpha_surface = pygame.Surface(image.get_size(), pygame.SRCALPHA)
    alpha_surface.fill((255, 255, 255, opacity))
    image.blit(alpha_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    return screen.blit(image, (x, y))


############################################################
"""
    Settings
"""
# Title
project_title = "Card Meister"


# Screen Size
Screen_size = display_width, display_height = 800, 600
gameDisplay = ScaledGame(project_title, Screen_size)


"""
    Tools Functions
"""
def file_len(file):
    with open(file) as f:
        for i, l in enumerate(f):
            pass
    return i + 1


def load_file(path, image=False):
    """
    Load    : All texts/images in directory. The directory must only contain texts/images.
    Path    : The relative or absolute path to the directory to load texts/images from.
    Image   : Load and convert image in the direcoty path.
    Return  : List of files.
    """
    file = []
    for file_name in os.listdir(path):
        if image == False:
            file.append(path + os.sep + file_name)
        if image == True:
            file.append(pygame.image.load(path + os.sep + file_name).convert())
    return file


def Music_Play(Selection):
    pygame.mixer.music.load(Selection)
    pygame.mixer.music.play(-1)


def quit_game():
    pygame.quit()
    quit()



############################################################
"""
    Ressources
"""
# Colors
color_red           = 255, 20,  0
color_green         = 60,  210, 120
color_blue          = 0,   160, 230
color_grey          = 150, 170, 210
color_white         = 255, 255, 255
color_black         = 1,   0,   0

color_button        = 140, 205, 245
color_title_screen  = 30,  30,  30


background                  = pygame.image.load("Data\Graphics\Background.png").convert()

base_1st_phase              = pygame.image.load('Data\Graphics\Base_1st_phase.png').convert()
base_2nd_phase              = pygame.image.load('Data\Graphics\Base_2nd_phase.png').convert()

base_initiative_attacker    = pygame.image.load('Data\Graphics\Base_initiative_attacker.png').convert()
base_initiative_defender    = pygame.image.load('Data\Graphics\Base_initiative_defender.png').convert()

base_hand_player            = pygame.image.load("Data\Graphics\Base_hand_player.png").convert()
base_hand_enemy             = pygame.image.load("Data\Graphics\Base_hand_enemy.png").convert()
base_board                  = pygame.image.load("Data\Graphics\Base_board.png").convert()

base_status_player          = pygame.image.load("Data\Graphics\Base_status_player.png").convert()
base_status_enemy           = pygame.image.load("Data\Graphics\Base_status_enemy.png").convert()

base_card_ok_inactive       = pygame.image.load("Data\Graphics\Base_card_ok_inactive.png").convert()
base_card_ok_active         = pygame.image.load("Data\Graphics\Base_card_ok_active.png").convert()
base_card_neutral           = pygame.image.load("Data\Graphics\Base_card_neutral.png").convert()
base_card_empty             = pygame.image.load("Data\Graphics\Base_card_empty.png").convert()
base_arrow                  = pygame.image.load("Data\Graphics\Base_arrow.png")

base_card_fire              = pygame.image.load("Data\Graphics\Base_card_fire.png").convert()
base_card_water             = pygame.image.load("Data\Graphics\Base_card_water.png").convert()
base_card_wind              = pygame.image.load("Data\Graphics\Base_card_wind.png").convert()

base_board_fire             = pygame.image.load("Data\Graphics\Base_board_fire.png").convert()
base_board_water            = pygame.image.load("Data\Graphics\Base_board_water.png").convert()
base_board_wind             = pygame.image.load("Data\Graphics\Base_board_wind.png").convert()

base_banner_fire            = pygame.image.load("Data\Graphics\Base_banner_fire.png").convert()
base_banner_water           = pygame.image.load("Data\Graphics\Base_banner_water.png").convert()
base_banner_wind            = pygame.image.load("Data\Graphics\Base_banner_wind.png").convert()

base_number_fire_1          = pygame.image.load("Data\Graphics\Base_number_fire_1.png").convert()
base_number_fire_2          = pygame.image.load("Data\Graphics\Base_number_fire_2.png").convert()
base_number_fire_3          = pygame.image.load("Data\Graphics\Base_number_fire_3.png").convert()
base_number_fire_4          = pygame.image.load("Data\Graphics\Base_number_fire_4.png").convert()
base_number_fire_5          = pygame.image.load("Data\Graphics\Base_number_fire_5.png").convert()
base_number_fire_6          = pygame.image.load("Data\Graphics\Base_number_fire_6.png").convert()
base_number_fire_7          = pygame.image.load("Data\Graphics\Base_number_fire_7.png").convert()
base_number_fire_8          = pygame.image.load("Data\Graphics\Base_number_fire_8.png").convert()
base_number_fire_9          = pygame.image.load("Data\Graphics\Base_number_fire_9.png").convert()

base_number_water_1         = pygame.image.load("Data\Graphics\Base_number_water_1.png").convert()
base_number_water_2         = pygame.image.load("Data\Graphics\Base_number_water_2.png").convert()
base_number_water_3         = pygame.image.load("Data\Graphics\Base_number_water_3.png").convert()
base_number_water_4         = pygame.image.load("Data\Graphics\Base_number_water_4.png").convert()
base_number_water_5         = pygame.image.load("Data\Graphics\Base_number_water_5.png").convert()
base_number_water_6         = pygame.image.load("Data\Graphics\Base_number_water_6.png").convert()
base_number_water_7         = pygame.image.load("Data\Graphics\Base_number_water_7.png").convert()
base_number_water_8         = pygame.image.load("Data\Graphics\Base_number_water_8.png").convert()
base_number_water_9         = pygame.image.load("Data\Graphics\Base_number_water_9.png").convert()

base_number_wind_1          = pygame.image.load("Data\Graphics\Base_number_wind_1.png").convert()
base_number_wind_2          = pygame.image.load("Data\Graphics\Base_number_wind_2.png").convert()
base_number_wind_3          = pygame.image.load("Data\Graphics\Base_number_wind_3.png").convert()
base_number_wind_4          = pygame.image.load("Data\Graphics\Base_number_wind_4.png").convert()
base_number_wind_5          = pygame.image.load("Data\Graphics\Base_number_wind_5.png").convert()
base_number_wind_6          = pygame.image.load("Data\Graphics\Base_number_wind_6.png").convert()
base_number_wind_7          = pygame.image.load("Data\Graphics\Base_number_wind_7.png").convert()
base_number_wind_8          = pygame.image.load("Data\Graphics\Base_number_wind_8.png").convert()
base_number_wind_9          = pygame.image.load("Data\Graphics\Base_number_wind_9.png").convert()

button_fullscreen_inactive  = pygame.image.load("Data\Graphics\Button_fullscreen_inactive.png").convert()
button_fullscreen_active    = pygame.image.load("Data\Graphics\Button_fullscreen_active.png").convert()
button_exit_inactive        = pygame.image.load("Data\Graphics\Button_exit_inactive.png").convert()
button_exit_active          = pygame.image.load("Data\Graphics\Button_exit_active.png").convert()

icon_iris                   = pygame.image.load("Data\Graphics\Icon_iris.png").convert()
icon_wolf                   = pygame.image.load("Data\Graphics\Icon_wolf.png").convert()
icon_direwolf               = pygame.image.load("Data\Graphics\Icon_direwolf.png").convert()
icon_zombie                 = pygame.image.load("Data\Graphics\Icon_zombie.png").convert()
icon_ghoul                  = pygame.image.load("Data\Graphics\Icon_ghoul.png").convert()
icon_shadow_fire            = pygame.image.load("Data\Graphics\Icon_shadow_fire.png").convert()
icon_shadow_water           = pygame.image.load("Data\Graphics\Icon_shadow_water.png").convert()
icon_shadow_wind            = pygame.image.load("Data\Graphics\Icon_shadow_wind.png").convert()
icon_gyrei                  = pygame.image.load("Data\Graphics\Icon_gyrei.png").convert()

base_upgrade                = pygame.image.load("Data\Graphics\Base_upgrade.png").convert()
sprite_iris                 = pygame.image.load("Data\Graphics\Sprite_iris.png")

se_system_1                 = pygame.mixer.Sound("Data\Sound Effect\se_maoudamashii_system14.wav")
se_system_2                 = pygame.mixer.Sound("Data\Sound Effect\se_maoudamashii_system17.wav")
se_system_3                 = pygame.mixer.Sound("Data\Sound Effect\se_maoudamashii_system21.wav")
se_system_4                 = pygame.mixer.Sound("Data\Sound Effect\se_maoudamashii_system48.wav")


############################################################
"""
    Game Functions
"""
def Main_Screen():
    # Setup
    Setup.update_init(background)
    MainIG.title_update(True)

    # Loop
    gameExit = False
    while not gameExit:
        gameDisplay.update()
        Setup.update_1()
        MainIG.update()
        Setup.update_2()
        
        for event in Setup.events:    
            if event.type == pygame.QUIT:
                quit_game()





        
class Player():
    def __init__(self):
        self.name       = "NightFore"
        self.icon       = icon_iris
        self.maxhealth  = 100
        self.health     = self.maxhealth
        self.base_level = [ [3, 3, 3], [6, 6, 6] ] 
        self.experience = 0
PlayerIG = Player()



class Wolf():
    def __init__(self):
        self.name       = "Wolf"
        self.icon       = icon_wolf
        self.maxhealth  = 25
        self.health     = self.maxhealth
        self.base_level = [ [2, 2, 2], [6, 4, 4] ]
        self.experience = 25
WolfIG = Wolf()



class Direwolf():
    def __init__(self):
        self.name       = "Direwolf"
        self.icon       = icon_direwolf
        self.maxhealth  = 40
        self.health     = self.maxhealth
        self.base_level = [ [2, 2, 3], [6, 6, 6] ]
        self.experience = 45
DirewolfIG = Direwolf()



class Zombie():
    def __init__(self):
        self.name       = "Zombie"
        self.icon       = icon_zombie
        self.maxhealth  = 50
        self.health     = self.maxhealth
        self.base_level = [ [3, 4, 3], [6, 8, 8] ]
        self.experience = 70
ZombieIG = Zombie()



class Ghoul():
    def __init__(self):
        self.name       = "Ghoul"
        self.icon       = icon_ghoul
        self.maxhealth  = 60
        self.health     = self.maxhealth
        self.base_level = [ [5, 4, 4], [8, 12, 8] ]
        self.experience = 100
GhoulIG = Ghoul()



class Shadow_fire():
    def __init__(self):
        self.name       = "Fire"
        self.icon       = icon_shadow_fire
        self.maxhealth  = 75
        self.health     = self.maxhealth
        self.base_level = [ [6, 5, 5], [8, 15, 12] ]
        self.experience = 125
Shadow_fireIG = Shadow_fire()



class Shadow_water():
    def __init__(self):
        self.name       = "Water"
        self.icon       = icon_shadow_water
        self.maxhealth  = 75
        self.health     = self.maxhealth
        self.base_level = [ [5, 6, 5], [10, 12, 10] ]
        self.experience = 125
Shadow_waterIG = Shadow_water()



class Shadow_wind():
    def __init__(self):
        self.name       = "Wind"
        self.icon       = icon_shadow_wind
        self.maxhealth  = 75
        self.health     = self.maxhealth
        self.base_level = [ [5, 5, 6], [12, 10, 8] ]
        self.experience = 125
Shadow_windIG = Shadow_wind()



class Gyrei():
    def __init__(self):
        self.name       = "Gyrei (Boss)"
        self.icon       = icon_gyrei
        self.maxhealth  = 50
        self.health     = self.maxhealth
        self.base_level = PlayerIG.base_level
        self.experience = 200
GyreiIG = Gyrei()




class MainIG():
    def __init__(self):
        """
        Game status
        """
        self.background = background
        self.list_music = load_file("Data\Music")
        
        self.fullscreen     = "off"
        self.difficulty     = "Normal"
        self.fast_mode      = "off"
    
        self.title_button   = [ [None, None, None], ["Fullscreen: ", "Difficulty: ", "Fast Mode: "] ]
        self.upgrade_button = [ [None, None, None], [None, None, None] ]
    
        self.title          = False
        self.battle         = False
        self.upgrade        = False

        self.stage          = 0
        self.list_enemy     = [WolfIG, DirewolfIG, ZombieIG, GhoulIG, Shadow_fireIG, Shadow_waterIG, Shadow_windIG, GyreiIG]

        """
        Character status
            base_level:
                -LvL max Card  : 9
                -LvL max Stats : 20
        """
        self.name               = ["", ""]
        self.icon               = [None, None]
        self.maxhealth          = [0, 0]
        self.health             = [self.maxhealth[0], self.maxhealth[1]]
        self.base_level         = [ [ [1, 1, 1], [1, 1, 1] ], [ [1, 1, 1], [1, 1, 1] ] ]    # [Character][Type][Stats]
        self.experience         = [0, 0]
    
        self.battle_character(PlayerIG, 0)        
        
        
        """
        Interface
        """
        self.base_card          = [base_card_fire,      base_card_water,    base_card_wind]
        self.base_number        = [[None, base_number_fire_1,  base_number_fire_2,  base_number_fire_3,  base_number_fire_4,  base_number_fire_5,  base_number_fire_6,  base_number_fire_7,  base_number_fire_8,  base_number_fire_9], [None, base_number_water_1, base_number_water_2, base_number_water_3, base_number_water_4, base_number_water_5, base_number_water_6, base_number_water_7, base_number_water_8, base_number_water_9], [None, base_number_wind_1,  base_number_wind_2,  base_number_wind_3,  base_number_wind_4,  base_number_wind_5,  base_number_wind_6,  base_number_wind_7,  base_number_wind_8,  base_number_wind_9]]

        self.base_status        = [base_status_player,  base_status_enemy]
        self.base_hand          = [base_hand_player,    base_hand_enemy]

        self.base_phase         = [base_1st_phase,              base_2nd_phase]
        self.base_initiative    = [base_initiative_defender,    base_initiative_attacker]
        
        self.base_banner        = [base_banner_fire,    base_banner_water,  base_banner_wind,   None]
        self.base_board         = [base_board_fire,     base_board_water,   base_board_wind]
        
        self.arrow              = base_arrow
        self.arrow_player       = self.arrow
        self.arrow_enemy        = pygame.transform.flip(self.arrow, False, True)
        

        """
        Card                : Card of the character during the turn
        Hand                : Card in the character's hand
        Board               : Card played on the board

        Board Power         : Value played during the round
        Element Type        : Dominant element of cards played on the board
        Advantage           : Bonus power according to the type of card played on the board
        Initiative          : 0 => Defender, 1 => Attacker

        Transition_init     : Transition scene between the different phases
        Transition_x        : Speed of the scrolling image
        Transition_time     : Time since the beginning of the transition

        Upgrade_button      : List of upgrade buttons
        Cancel_experience   : Refunds the experience points spent during the upgrade
        Cancel_level        : Returns the statistics levels at the beginning of the upgrade
        """
        self.card               = [ [ [], [], [], [], [] ],  [ [], [], [], [], [] ] ]
        self.hand               = [ [], [] ]
        self.board              = [ [], [] ]
        
        self.board_power        = [ [0, 0, 0], [0, 0, 0] ]
        self.element_type       = [3, 3]
        self.advantage          = [False, False]
        self.initiative         = [0, 0]

        self.transition_init    = [True, False]
        self.transition_x       = 800
        self.transition_time    = 0
    
        self.cancel_experience  = 0
        self.cancel_level       = [ [0, 0, 0], [0, 0, 0] ]



    def update(self):
        if self.title == True:
            self.title_update()
        
        elif self.battle == True:
            self.battle_update()

        elif self.upgrade == True:
            self.upgrade_update()
     

    def update_init(self, bgm, title=False, battle=False, upgrade=False):
        Setup.update_init(self.background, bgm)
        Button((None, None), (se_system_1, None), (False, 0,    0), (button_fullscreen_inactive,    button_fullscreen_active),  None, gameDisplay.fullscreen)
        Button((None, None), (se_system_1, None), (False, 760,  0), (button_exit_inactive,          button_exit_active),        None, quit_game)
        
        self.title      = title
        self.battle     = battle
        self.upgrade    = upgrade


    def settings_update(self, index):
        Setup.list_button.remove(self.title_button[0][index])
                
        if index == 0:
            gameDisplay.fullscreen()

        elif index == 1:
            if self.difficulty != "Normal":
                self.difficulty = "Normal"
            else:
                self.difficulty = "Easy"
        
        elif index == 2:
            if self.fast_mode != "on":
                self.fast_mode = "on"
            else:
                self.fast_mode = "off"
    
            self.fullscreen = gameDisplay.set_fullscreen
            if self.fullscreen == True:
                self.fullscreen = "on"
            
            elif self.fullscreen == False:
                self.fullscreen = "off"

    def title_update(self, init=False):
        if init == True:
            self.update_init(self.list_music[0], title=True)

            Text((project_title, text_title), (True, display_width/2, display_height/4), True, color_black, 3, setup=True)
            Button(("Start", text_interface), (se_system_1, None), (True, 200, 415, 135, 50, 5, True), (color_green, color_red), True, self.battle_update)
            Button(("Music", text_interface), (se_system_1, None), (True, 400, 415, 135, 50, 5, True), (color_green, color_red), True, self.music_update)
            Button(("Exit",  text_interface), (se_system_1, None), (True, 600, 415, 135, 50, 5, True), (color_green, color_red), None, quit_game)

    
        if init == False:
            settings = [self.fullscreen, self.difficulty, self.fast_mode]
            for index in range(3):
                if self.title_button[0][index] not in Setup.list_button:
                    self.title_button[0][index] = Button((self.title_button[1][index]+settings[index], text_interface),
                                                         (se_system_2, None), (True, 150+250*index, 525, 230, 50, 5, True), (color_green, color_red), index, self.settings_update)

    
    def music_update(self, init=False):
        self.update_init(self.list_music[0])
                
        Text(("Music Gallery", text_title), (True, display_width/2, display_height/12), True, color_black, 3, setup=True)
        Button(("Return", text_interface),  (True, 740, 570, 100, 40, 1, True), (color_button, color_red), True, self.title_update, se_system_1)

        index = 0
        for row in range(round(0.5+len(self.list_music)/5)):
            for col in range(5):
                if index < len(self.list_music):
                    Button(("Music %i" % (index+1), Text_Button), (False, display_width/64 + display_width/5*col, display_height/6 + display_height/9*row, display_width/6, display_height/12, 4, True), (color_green, color_red), self.list_music[index], Music_Play, se_system_3)
                    index += 1
                    

                
    
    def battle_update(self, init=False):
        if init == True:
            self.hand = [ [], [] ]

            if self.stage <= 7:
                enemy = self.list_enemy[self.stage]
                music = self.list_music[1+self.stage]
            else:
                enemy = self.list_enemy[7]
                music = self.list_music[random.randint(1, 8)]


            self.update_init(music, battle=True)

            for index in range(5):
                Button((None, None), (se_system_3, None), (False, 120+65*index, 480, 60, 90, 0, True), (None, None), index, self.battle_select)
            Button((None, None),     (se_system_4, None), (False, 55, 480), (base_card_ok_inactive, base_card_ok_active), None, self.battle_phase)

            self.battle_character(enemy)
            self.battle_card_phase_1()


        elif init == False:
            """
            User Interface
            """
            gameDisplay.blit(base_board, (235, 200))
            for side in range(2):
                gameDisplay.blit(self.base_hand[side],      (50 +370*side, 475-450*side))
                gameDisplay.blit(self.base_status[side],    (505-455*side, 460-435*side))
                gameDisplay.blit(self.icon[side],           (665-615*side, 460-435*side))
                pygame.draw.rect(gameDisplay, color_green,  (510-375*side, 505-435*side, 155*self.health[side]/self.maxhealth[side], 35))


            """
            Card (Hand/Board)
            """
            for side in range(2):
                for index in self.hand[side]:
                    type_card   = self.card[side][index][0]
                    level_card  = self.card[side][index][1]
                    gameDisplay.blit(self.base_card[type_card],                 (120+65*index+305*side, 480-450*side))
                    gameDisplay.blit(self.base_number[type_card][level_card],   (143+65*index+305*side, 529-450*side))

                for index in range(len(self.board[side])):
                    type_card   = self.card[side][index][0]
                    level_card  = self.card[side][index][1]
                    gameDisplay.blit(self.base_card[type_card],                 (305+65*index, 305-100*side))
                    gameDisplay.blit(self.base_number[type_card][level_card],   (328+65*index, 354-100*side))

            """
            Status
            """
            for side in range(2):
                Text(("%s"          % self.name[side],              text_interface),    (True, 589-376*side, 483-435*side))
                Text(("Health: %s"  % self.health[side],            text_interface),    (True, 589-376*side, 523-435*side))
                Text(("AGI:%s"      % self.base_level[side][1][0],  text_interface_2),  (True, 548-456*side, 558-435*side))
                Text(("STR:%s"      % self.base_level[side][1][1],  text_interface_2),  (True, 628-456*side, 558-435*side))
                Text(("DEF:%s"      % self.base_level[side][1][2],  text_interface_2),  (True, 708-456*side, 558-435*side))

            """
            Battle
            """
            # Element Advantage
            if self.arrow != None:
                gameDisplay.blit(self.arrow, (170, 275))
                
            for side in range(2):
                # Attacker/Defender
                if self.initiative != [0, 0]:
                    gameDisplay.blit(self.base_initiative[self.initiative[side]],   (575, 320-100*side))

                # Dominant Element
                if self.element_type[side] != 3:
                    gameDisplay.blit(self.base_banner[self.element_type[side]],     (160, 335-100*side))

                    if self.advantage[side] == True:
                        gameDisplay.blit(self.base_card[self.element_type[side]],   (240, 305-100*side))
                        gameDisplay.blit(self.base_number[self.element_type[side]][self.base_level[side][0][self.element_type[side]]], (263, 354-100*side))

                    else:
                        gameDisplay.blit(self.base_board[self.element_type[side]],  (240, 305-100*side))

            self.battle_unselect()
            self.battle_transition()


    def upgrade_update(self, init=False):
        if init == True:
            self.update_init(self.list_music[9], upgrade=True)

            if self.difficulty == "Easy":
                self.experience[0] += 2*self.experience[1]

            elif self.difficulty == "Normal":
                self.experience[0] += self.experience[1]
            
            Button(("Cancel",  text_interface_2), (True, 635, 570, 100, 40, 1, True), (color_red, color_button), None, self.upgrade_cancel, se_system_1)
            Button(("Confirm", text_interface_2), (True, 740, 570, 100, 40, 1, True), (color_red, color_button), None, self.upgrade_confirm, se_system_4)
        

        elif init == False:
            gameDisplay.blit(base_upgrade, (450, 0))
            gameDisplay.blit(sprite_iris, (20,  110))

            Text(("Status Upgrade", text_interface), (True, 605, 25))

            Statistics  = [ ["Fire",      "Water",    "Wind"], ["Agility",   "Strength", "Defense"] ]
            for upgrade_type in range(2):
                for index in range(3):
                    if self.upgrade_button[upgrade_type][index] not in Setup.list_button and self.base_level[0][upgrade_type][index] < 9+11*upgrade_type:
                        Cost = self.upgrade_cost(index, upgrade_type)
                        self.upgrade_button[upgrade_type][index] = Button(("%i" % Cost, text_interface), (True, 560-55*upgrade_type, 105+305*upgrade_type+(110-55*upgrade_type)*index, 40, 40, 1, True), (color_red, color_button), (index, upgrade_type), self.upgrade_level, se_system_2)

                    Text(("%s"      % Statistics[upgrade_type][index],          text_interface), (True, 640-40*upgrade_type, 105+305*upgrade_type+(110-55*upgrade_type)*index))
                    Text(("LvL %i"  % self.base_level[0][upgrade_type][index],  text_interface), (True, 745-25*upgrade_type, 105+305*upgrade_type+(110-55*upgrade_type)*index))

            Text(("EXP: %i" % self.experience[0], text_interface), (True, 520, 570))

       
############################################################  
    

    def battle_character(self, character, index=1):
        self.name[index]        = character.name
        self.icon[index]        = character.icon
        self.maxhealth[index]   = character.maxhealth
        self.health[index]      = character.health
        self.base_level[index]  = character.base_level
        self.experience[index]  = character.experience   
        
        
    def battle_card_phase_1(self):
        # Reset Board
        self.board = [ [], [] ]

        for side in range(2):
            for index in range(5):
                # Upgrade Card
                if index in self.hand[side]:
                    self.card[side][index] = [self.card[side][index][0], self.card[side][index][1] + 2]
                
                # Random card type & level
                else:       
                    random_type  = random.randint(0, 2)
                    random_level = random.randint(-2, 2) + self.base_level[side][0][random_type]
                    self.card[side][index] = [random_type, random_level]
                    self.hand[side].append(index)
                
                # Minimum level
                if self.card[side][index][1] < 1:
                    self.card[side][index][1] = 1

                # Maximum level
                if self.card[side][index][1] > 9:
                    self.card[side][index][1] = 9

            # Sort card
            self.card[side] = sorted(self.card[side], key=itemgetter(1), reverse=True)  # Level
            self.card[side] = sorted(self.card[side], key=itemgetter(0))                # Type

        # Play enemy cards randomly
        while len(self.board[1]) == 0:
            for index in range(5):
                if len(self.board[1]) < 4 and random.choice([True, False]) == True:
                    self.hand[1].remove(index)
                    self.board[1].append(index)
                
        self.element_update()


    def battle_card_phase_2(self):
        # Reset Board
        self.board = [ [], [] ]

        # Play the remaining enemy cards
        for index in range(5):
            if index in self.hand[1]:
                self.hand[1].remove(index)
                self.board[1].append(index)
            
        self.element_update()


    def battle_select(self, index):
        if len(self.board[0]) < 4 and index in self.hand[0]:
            self.hand[0].remove(index)
            self.board[0].append(index)
            self.element_update()
        

    def battle_unselect(self):
        for event in Setup.events:
            if self.board[0] != [] and Setup.event.type == pygame.MOUSEBUTTONDOWN and Setup.event.button == 3:
                index = self.board[0][len(self.board[0])-1]
                self.hand[0].append(index)
                self.board[0].remove(index)
                self.element_update()


    def element_update(self):
        """
        Element Type:
            Card            : self.card[side][self.board[side][index]] ([0] = Type / [1] = Level)
            Element_type    : Highest power of element in play
            Board_Element   : Update board card element 
            Banner_element  : Update banner element

            Board_power     : Total power of cards in play
        """
        for side in range(2):
            self.board_power[side]  = [0, 0, 0]
        
            if self.board[side] != []:
                for index in range(len(self.board[side])):
                    card_type  = self.card[side][self.board[side][index]][0]
                    card_level = self.card[side][self.board[side][index]][1]
                    self.board_power[side][card_type] += card_level
                
                self.element_type[side] = self.board_power[side].index(max(self.board_power[side]))

            else:
                self.element_type[side] = 3

            self.board_power[side] = sum(self.board_power[side])

        """
        Element Advantage
            p_type      : Player's element
            e_type      : Enemy's element
            Neutral     : No advantage
            Advantage   : Player advantage  (Damage = 1 + Board_power + p_type Card Level)
            Disavantage : Enemy advantage   (Damage = 1 + Board_power + e_type Card Level)  
        """
        if self.element_type[0] != 3 and self.element_type[1] != 3:
            p_type, e_type = self.element_type[0], self.element_type[1]

            # Neutral
            if p_type == e_type:
                self.arrow      = None
                self.advantage  = [False, False]
    
            # Advantage
            elif (p_type == 0 and e_type == 2) or (p_type == 1 and e_type == 0) or (p_type == 2 and e_type == 1):
                self.board_power[0] += self.base_level[0][0][self.element_type[0]]
                self.arrow      = self.arrow_player
                self.advantage  = [True, False]

            # Disavantage
            else:
                self.board_power[1] += self.base_level[1][0][self.element_type[1]]
                self.arrow      = self.arrow_enemy
                self.advantage  = [False, True]
        else:
            self.arrow = None
            self.advantage  = [False, False]
            

    def battle_phase(self):
        if self.board[0] != []:
            if self.initiative == [0, 0]:
                """
                Battle Phase 1 : Initiative Phase   (initiative == [0, 0])
                    Initiative = Board_power + Agility
                        -Initiative Advantage
                        -Update base_initiative display
                    
                    Update Card         : Reset Board and play Enemy remaining card
                    transition_init     : Transition 2nd Phase
                """
                p_initiative = self.board_power[0] + self.base_level[0][1][0]
                e_initiative = self.board_power[1] + self.base_level[1][1][0]
                
                # Player Initiative
                if p_initiative >= e_initiative:
                    self.initiative[0] = 1

                # Enemy Initiative
                else:
                    self.initiative[1] = 1

                self.battle_card_phase_2()
                self.transition_init[1] = True

            
            elif self.initiative != [0, 0]:
                """
                Battle Phase 2 : Attack Phase       (initiative != [0, 0])
                    Attack  = Board_power + Strength
                    Defense = Board_power + Defense
                    Damage  = Attack - Defense
                    
                    Update Card         : Reset Board and Hand
                    transition_init     : Transition 1st Phase
                    Initiative          : Reset initiative advantage
                """
                for side in range(2):
                    if self.initiative[side] == 1:
                        damage = (self.board_power[side] + self.base_level[side][1][1]) - (self.board_power[1-side] + self.base_level[1-side][1][2])

                        if damage > 0:
                            self.health[1-side] -= damage
                            
                            if self.health[1-side] < 0:
                                self.health[1-side] = 0
                        
                self.battle_card_phase_1()
                self.transition_init[0] = True
                self.initiative     = [0, 0]
                self.battle_end()
        

    def battle_transition(self):
        """
        Transparent image   : 1st Phase / 2nd Phase
        Setup.button        : Disable button during transition

        transition_init     : Initiate  Transition
        transition_x        : Slides 18 pixels to the left in each frame
        transition_time     : Sliding time (45 frames) / Waiting time (55 frames)
        wait_time           : Time before the transition ends
        """
        for index in range(2):
            if self.transition_init[index] == True:
                Setup.button            = False
                self.transition_time    += 1
                transparent_image(self.base_phase[index], self.transition_x, 225, 225, gameDisplay)
                
                if self.transition_time < 40:
                    self.transition_x -= 20

                else:
                    self.transition_x = 0

                if self.fast_mode == "on":
                    wait_time = 0

                elif self.fast_mode == "off":
                    wait_time = 70
                
                if self.transition_time >= wait_time:
                    self.transition_init[index] = False
                    self.transition_x           = 800
                    self.transition_time        = 0
                    Setup.button                = True
                    


    def battle_end(self):
        # Win Condition
        if self.health[0] <= 0:
            self.title_update()

        elif self.health[1] <= 0:
            self.upgrade_update(True)
            self.stage += 1


############################################################
            
            
    def upgrade_cost(self, index, upgrade_type):
        Level = self.base_level[0][upgrade_type][index]

        # Card Upgrade
        if upgrade_type == 0:
            Cost = 15 + (Level-3) * (18 + (Level-4) * 2) / 2

        # Stats Upgrade
        elif upgrade_type == 1:
            Cost = 10 + (Level-6) * (8  + (Level-7) * 2) / 2
        
        return Cost
            

    def upgrade_level(self, index):
        index, upgrade_type = index[0], index[1]
        Cost = self.upgrade_cost(index, upgrade_type)

        if self.experience[0] >= Cost:
            # Update Button
            Setup.list_button.remove(self.upgrade_button[upgrade_type][index])
            self.upgrade_button[upgrade_type][index] = None
            
            self.experience[0]      -= Cost
            self.base_level[0][upgrade_type][index] += 1

            self.cancel_experience  -= Cost
            self.cancel_level[upgrade_type][index]  += 1



    def upgrade_cancel(self):
        self.experience[0] -= self.cancel_experience
        
        for upgrade_type in range(2):
            for index in range(3):
                if self.cancel_level[upgrade_type][index] != 0:
                    # Update Button
                    Setup.list_button.remove(self.upgrade_button[upgrade_type][index])
                    self.upgrade_button[upgrade_type][index] = None
                    self.base_level[0][upgrade_type][index] -= self.cancel_level[upgrade_type][index]
            
        self.cancel_experience  = 0
        self.cancel_level       = [ [0, 0, 0], [0, 0, 0] ]


    def upgrade_confirm(self):
        self.cancel_experience  = 0
        self.cancel_level       = [ [0, 0, 0], [0, 0, 0] ]
        self.battle_update(True)


MainIG = MainIG()



Main_Screen()
