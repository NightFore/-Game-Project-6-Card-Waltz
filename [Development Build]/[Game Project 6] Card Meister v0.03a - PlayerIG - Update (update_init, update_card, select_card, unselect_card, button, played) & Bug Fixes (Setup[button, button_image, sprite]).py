import pygame
import os
import time
import random

from pygame.locals import *



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
            Sprite      : Displays the sprites in the sprite list
            Text        : Display the texts of the text list

            Inventory   : Displays the inventory user interface
            Shop        : Displays the shop user interface
            Result      : Displays the results user interface

        State Update    : Lists of objects displayed when the respective states are enabled
        """
        
        # Information
        self.background = False
        self.music = False

        # State
        self.button = False
        self.sprite = False
        self.text   = False

        # State Update
        self.list_text          = []
        self.list_button        = []
        self.list_button_image  = []
        self.list_sprite        = []    # AnimatedSprite()
        self.all_sprites        = []    # Creates a sprite group and adds 'player' to it.


    def update_music(self, music):
        """
        Update : Load Music
        """
        if self.music != music:
            self.music = music
            pygame.mixer.music.load(music)
            pygame.mixer.music.play(-1)
        

    def update_init(self, background=None, music=None, button=False, sprite=False, text=False):
        """
        Update :
            Setup   : Load all states
            Reset   : Clean all lists and reset user interface states
            Load    : Load Background & Music
            
        """
        # Setup
        self.button = button
        self.sprite = sprite
        self.text   = text

        # Reset
        self.list_button        = []
        self.list_button_image  = []
        self.list_sprite        = []    # AnimatedSprite()
        self.all_sprites        = []    # Creates a sprite group and adds 'player' to it.
        self.list_text          = []
        
        # Load
        self.background = background

        if music != None: 
            self.update_music(music)

            
    def update(self):
        """
        Setup :
            Update game screen and background
            Retrieves game events in global variables
            
        """
        if self.background != None:
            gameDisplay.blit(self.background, (0,0))
        
        Tools.events = pygame.event.get()
        for event in Tools.events:
            Tools.event = event

        self.update_state()


    def update_state(self):
        """
        Interactive interface :
            Button & Sprite:
                Length prevents crash from removing an element from the list
                Display buttons from the list and check for mouse position.
                Call function action() if clicking on it
            Text
        """
        # Button
        if self.button == True:
            # Display Button
            for index in range(len(self.list_button)):
                self.list_button[index].display(index)
            for index in range(len(self.list_button_image)):
                self.list_button_image[index].display(index)

            # Check Mouse Position & Action
            for event in Tools.events:
                length = len(self.list_button)
                for index in range(length):
                    if length == len(self.list_button):
                        self.list_button[index].update(index)
                    
                length = len(self.list_button_image)
                for index in range(length):
                    if length == len(self.list_button_image):
                        self.list_button_image[index].update(index)

        # Sprite
        if self.sprite == True:
            # Update & Display Sprite
            for index in range(len(self.list_sprite)):
                self.list_sprite[index].dt = clock.tick(FPS)
                self.all_sprites[index].update()
                self.all_sprites[index].draw(gameDisplay)

            # Check Mouse Position & Action
            for event in Tools.events:
                length = len(self.list_sprite)
                for index in range(length):
                    if length == len(self.list_sprite) and callable(self.list_sprite[index].action) == True:
                        self.list_sprite[index].button()

        # Text
        if self.text == True:
            for index in range(len(self.list_text)):
                self.list_text[index].display()
Setup = Setup()



class Text():
    def __init__(self, text, x, y, center, font):
        """
        Setup       : Add text to the text_list
        Text        : Text string, font, color
        Position    : Position x, y, surface, center
        """
        # Setup
        Setup.text = True
        Setup.list_text.append(self)

        # Text
        self.text = text
        self.font, self.color = font()

        # Position
        self.x = x
        self.y = y
        self.center = center
        self.textSurface = self.font.render(self.text, True, self.color)

        if center == False:
            self.textRect = (self.x, self.y)
            
        if center == True:
            self.textRect = self.textSurface.get_rect()
            self.textRect.center = (self.x, self.y)

    def display(self):
        gameDisplay.blit(self.textSurface, self.textRect)



class Button():
    def __init__(self, text, font, x, y, w, h, b, border, center, active, inactive, selection, action=None):
        """
        Setup       :
            Enable buttons
            Add button to list_button
        
        Position    :
            x, y, width, height, border width, border, center
            
        Text        :
            Add the centered text of the button to the text list
            
        Color       :
            Active/Inactive color of the button
            Color changes depending of the mouse position
        
        Action      :
            Selection   : Button index
            Action      : Button action
        """
        # Setup
        Setup.button = True
        Setup.list_button.append(self)

        # Position
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.b = b
        self.border = border
        self.center = center
        
        if self.center == True:
            self.x = x-w/2
            self.y = y-h/2
        self.rect   = pygame.Rect(self.x,self.y,self.w,self.h)

        # Text
        self.text   = text
        self.font   = font

        # Color
        self.active     = active
        self.inactive   = inactive
        self.color      = inactive

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
    
        
    def update(self, index):
        mouse = pygame.mouse.get_pos()
        self.update_scale()

        if self.rect_scaled.collidepoint(mouse):
            self.color = self.active
            if Tools.event.type == pygame.MOUSEBUTTONDOWN:
                if self.action != None and self.selection != None:
                    self.action(self.selection)
                elif self.action != None:
                    self.action()       
        else:
            self.color = self.inactive
        

    def display(self, index):
        # Button
        if self.border == True:
            pygame.draw.rect(gameDisplay, Color_Black, self.rect, self.b)
        pygame.draw.rect(gameDisplay, self.color, self.rect)

        # Text
        if self.text != None:
            font, color = self.font()
            textSurf = font.render(self.text, True, color)
            textRect = textSurf.get_rect()
            textRect.center = self.x+self.w/2, self.y+self.h/2
            gameDisplay.blit(textSurf, textRect)
    


class Button_Image():
    def __init__(self, x, y, center, active, inactive, selection, action=None):
        """
        Setup       :
            Enable buttons
            Add button to list_button_image
            
        Image       :
            Active/Inactive image of the button
            Image changes depending of the mouse position
        
        Position    :
            x, y, center
            
        Action      :
            Selection   : Button index
            Action      : Button action
        """
        # Tools
        Setup.list_button_image.append(self)

        # Image
        self.active     = active.convert()
        self.inactive   = inactive.convert()
        self.image      = inactive.convert()

        # Position
        self.x = x
        self.y = y
        self.center = center
        
        if self.center == False:
            self.rect = self.active.get_rect(topleft=(x,y))

        if self.center == True:
            self.rect = self.active.get_rect(center=(x,y))

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


    def update(self, index):
        mouse = pygame.mouse.get_pos()
        self.update_scale()
        
        if self.rect_scaled.collidepoint(mouse):
            self.image = self.active
            if Tools.event.type == pygame.MOUSEBUTTONDOWN:
                if self.action != None and self.selection != None:
                    self.action(self.selection)
                elif self.action != None:
                    self.action()         
        else:
            self.image = self.inactive


    def display(self, index):
        gameDisplay.blit(self.image, self.rect)



def Text_Title_Screen():
    font = pygame.font.SysFont(None, 100)
    color = Color_Title_Screen
    return font, color


def Text_Button():
    font = pygame.font.SysFont(None, 40)
    color = Color_Blue
    return font, color


def Text_Interface():
    font = pygame.font.SysFont(None, 35)
    color = Color_Black
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
        first_screen    = (screen_info.current_w, screen_info.current_h - 120)  # Take 120 pixels from the height because the menu bar, window bar and dock takes space

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
        for event in Tools.events:
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
class Tools():
    def __init__(self):
        self.event          = ""    # Button
        self.events         = ""    # Text
Tools = Tools()


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


def Quit_Game():
    pygame.quit()
    quit()



############################################################
"""
    Ressources
"""


# Colors
Color_Red           = 255, 20,  0
Color_Green         = 60,  210, 120
Color_Blue          = 0,   160, 230
Color_Black         = 0,   0,   0
Color_Grey          = 150, 170, 210
Color_White         = 255, 255, 255

Color_Button        = 140, 205, 245
Color_Title_Screen  = 210, 100, 240


background      = pygame.image.load("Data\Graphics\Background.png")
base_card_ok    = pygame.image.load("Data\Graphics\Base_card_ok.png")
base_card_fire  = pygame.image.load("Data\Graphics\Base_card_fire.png")
base_card_water = pygame.image.load("Data\Graphics\Base_card_water.png")
base_card_wind  = pygame.image.load("Data\Graphics\Base_card_wind.png")
base_card_enemy = pygame.image.load("Data\Graphics\Base_card_enemy.png")
button_exit_1   = pygame.image.load("Data\Graphics\Button_exit_1.png")
button_exit_2   = pygame.image.load("Data\Graphics\Button_exit_2.png")

icon_status_iris        = pygame.image.load("Data\Graphics\Icon_status_iris.png")
icon_status_direwolf    = pygame.image.load("Data\Graphics\Icon_status_direwolf.png")



############################################################
"""
    Game Functions
"""
def Title_Screen():
    # Setup
    Setup.update_init(background)
    PlayerIG.update_init()

    # Text
    Button(None, None, 400, 300, 800, 300, 10, True, True, Color_Red, Color_Green, None, action=PlayerIG.update_card)
    Button_Image(0, 0, False, button_exit_1, button_exit_2, None, gameDisplay.fullscreen)
    
    # Loop
    gameExit = False
    while not gameExit:
        gameDisplay.update()
        Setup.update()
        PlayerIG.display_card()

        for event in Tools.events:
            if event.type == pygame.QUIT:
                Quit_Game()



class PlayerIG():
    def __init__(self):
        self.base_card  = [base_card_fire, base_card_water, base_card_wind, base_card_enemy, base_card_ok]
        self.base_level = [3, 3, 3]
        self.card       = [ [[], [], [], [], []],  [[], [], [], [], []] ]
        self.button     = [None, None, None, None, None]
        self.played     = [None, None, None, None, None]
        self.init       = False

        self.maxhealth  = 100
        self.health     = self.maxhealth

        self.strength   = 6
        self.agility    = 6
        self.resilience = 6

    def update_init(self):
        self.init = False
        self.update_card()

    def select_card(self, index):
        if self.button[index] in Setup.list_button_image:
            Setup.list_button_image.remove(self.button[index])

            card = self.base_card[self.card[0][index][0]]
            self.played[index] = Button_Image(270+65*index, 300, True, card, card, index, self.unselect_card)

    def unselect_card(self, index):
        if self.played[index] in Setup.list_button_image:
            Setup.list_button_image.remove(self.played[index])

            card = self.base_card[self.card[0][index][0]]
            self.button[index] = Button_Image(120+65*index, 480, False, card, card, index, self.select_card)

    def update_card(self):
        for index in range(5):
            if self.init == True:
                if self.button[index] in Setup.list_button_image:
                    Setup.list_button_image.remove(self.button[index])

                if self.played[index] in Setup.list_button_image:
                    Setup.list_button_image.remove(self.played[index])
                
            type_card   = random.randint(0, 2)
            self.card[0][index] = [type_card, self.base_level[type_card] + random.randint(0, 3)]
            self.card[1][index] = [type_card, self.base_level[type_card] + random.randint(0, 3)]

            card = self.base_card[self.card[0][index][0]]
            self.button[index] = Button_Image(120+65*index, 480, False, card, card, index, self.select_card)
        self.init = True

    def display_card(self):
        gameDisplay.blit(icon_status_iris,      (670, 485))
        gameDisplay.blit(icon_status_direwolf,  (50, 35))
        gameDisplay.blit(base_card_ok,          (55, 480))
        
        for index in range(5):
            gameDisplay.blit(self.base_card[3], (420+65*index, 30))
PlayerIG = PlayerIG()



Title_Screen()
