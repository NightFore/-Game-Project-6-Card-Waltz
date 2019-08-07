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
        """
        # Information
        self.background = False
        self.music = False

        # State
        self.button = False
        self.text   = False

        # State Update
        self.list_text          = []
        self.list_button        = []
        self.list_button_image  = []


    def update_music(self, music):
        """
        Update : Load Music
        """
        if self.music != music:
            self.music = music
            pygame.mixer.music.load(music)
            pygame.mixer.music.play(-1)
        

    def update_init(self, background=None, music=None, button=False, text=False):
        """
        Update :
            Setup   : Load all states
            Reset   : Clean all lists and reset user interface states
            Load    : Load Background & Music
        """
        # Setup
        self.button = button
        self.text   = text

        # Reset
        self.list_button        = []
        self.list_button_image  = []
        self.list_text          = []
        
        # Load
        self.background = background

        if music != None: 
            self.update_music(music)
            

    def update_1(self):
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

        
        """
        Interface :
            Button:
                Length prevents crash from removing an element from the list
                Check for mouse position and call function action() when clicking on it
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

    def update_2(self):
        # Text
        if self.text == True:
            for index in range(len(self.list_text)):
                self.list_text[index].display()
                
Setup = Setup()

class Text():
    def __init__(self, text, x, y, font, center=False):
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
    def __init__(self, text, font, x, y, w, h, b, border, center, inactive, active, selection, action=None):
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
            if Tools.event.type == pygame.MOUSEBUTTONDOWN and Tools.event.button == 1:
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
    def __init__(self, x, y, center, inactive, active, selection, action=None):
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
        self.inactive   = inactive.convert()
        self.active     = active.convert()
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
            if Tools.event.type == pygame.MOUSEBUTTONDOWN and Tools.event.button == 1:
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


def Text_interface():
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


def quit_game():
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


background                  = pygame.image.load("Data\Graphics\Background.png").convert()

base_1st_phase              = pygame.image.load('Data\Graphics\Base_1st_phase.png')
base_2nd_phase              = pygame.image.load('Data\Graphics\Base_2nd_phase.png')

base_status_player          = pygame.image.load("Data\Graphics\Base_status_player.png")
base_status_enemy           = pygame.image.load("Data\Graphics\Base_status_enemy.png")
base_hand_player            = pygame.image.load("Data\Graphics\Base_hand_player.png")
base_hand_enemy             = pygame.image.load("Data\Graphics\Base_hand_enemy.png")
base_board                  = pygame.image.load("Data\Graphics\Base_board.png").convert()

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

base_number_red_1           = pygame.image.load("Data\Graphics\Base_number_red_1.png")
base_number_red_2           = pygame.image.load("Data\Graphics\Base_number_red_2.png")
base_number_red_3           = pygame.image.load("Data\Graphics\Base_number_red_3.png")
base_number_red_4           = pygame.image.load("Data\Graphics\Base_number_red_4.png")
base_number_red_5           = pygame.image.load("Data\Graphics\Base_number_red_5.png")
base_number_red_6           = pygame.image.load("Data\Graphics\Base_number_red_6.png")
base_number_red_7           = pygame.image.load("Data\Graphics\Base_number_red_7.png")
base_number_red_8           = pygame.image.load("Data\Graphics\Base_number_red_8.png")
base_number_red_9           = pygame.image.load("Data\Graphics\Base_number_red_9.png")

base_number_blue_1          = pygame.image.load("Data\Graphics\Base_number_blue_1.png")
base_number_blue_2          = pygame.image.load("Data\Graphics\Base_number_blue_2.png")
base_number_blue_3          = pygame.image.load("Data\Graphics\Base_number_blue_3.png")
base_number_blue_4          = pygame.image.load("Data\Graphics\Base_number_blue_4.png")
base_number_blue_5          = pygame.image.load("Data\Graphics\Base_number_blue_5.png")
base_number_blue_6          = pygame.image.load("Data\Graphics\Base_number_blue_6.png")
base_number_blue_7          = pygame.image.load("Data\Graphics\Base_number_blue_7.png")
base_number_blue_8          = pygame.image.load("Data\Graphics\Base_number_blue_8.png")
base_number_blue_9          = pygame.image.load("Data\Graphics\Base_number_blue_9.png")

base_number_green_1         = pygame.image.load("Data\Graphics\Base_number_green_1.png")
base_number_green_2         = pygame.image.load("Data\Graphics\Base_number_green_2.png")
base_number_green_3         = pygame.image.load("Data\Graphics\Base_number_green_3.png")
base_number_green_4         = pygame.image.load("Data\Graphics\Base_number_green_4.png")
base_number_green_5         = pygame.image.load("Data\Graphics\Base_number_green_5.png")
base_number_green_6         = pygame.image.load("Data\Graphics\Base_number_green_6.png")
base_number_green_7         = pygame.image.load("Data\Graphics\Base_number_green_7.png")
base_number_green_8         = pygame.image.load("Data\Graphics\Base_number_green_8.png")
base_number_green_9         = pygame.image.load("Data\Graphics\Base_number_green_9.png")

button_fullscreen_inactive  = pygame.image.load("Data\Graphics\Button_fullscreen_inactive.png").convert()
button_fullscreen_active    = pygame.image.load("Data\Graphics\Button_fullscreen_active.png").convert()
button_exit_inactive        = pygame.image.load("Data\Graphics\Button_exit_inactive.png").convert()
button_exit_active          = pygame.image.load("Data\Graphics\Button_exit_active.png").convert()
icon_status_iris            = pygame.image.load("Data\Graphics\Icon_status_iris.png").convert()
icon_status_direwolf        = pygame.image.load("Data\Graphics\Icon_status_direwolf.png").convert()



############################################################
"""
    Game Functions
"""
def Main_Screen():
    # Setup
    Setup.update_init(background)
    MainIG.update_card()
    
    Button_Image(0,     0, False, button_fullscreen_inactive,   button_fullscreen_active,   None, gameDisplay.fullscreen)
    Button_Image(760,   0, False, button_exit_inactive,         button_exit_active,         None, quit_game)

    # Text
    Button(None, None, 575, 200, 100, 200, 10, True, False, Color_Green, Color_Red, None, MainIG.update_card)

    MainIG.battle_init()

    # Loop
    gameExit = False
    while not gameExit:
        gameDisplay.update()
        Setup.update_1()
        MainIG.update()
        Setup.update_2()


        # Test
        transparent_image(base_1st_phase, 0, 0, 225, gameDisplay)
        
        for event in Tools.events:    
            if event.type == pygame.QUIT:
                quit_game()






class Wolf():
    def __init__(self):
        self.name       = "Wolf"
        self.icon       = icon_status_direwolf

        self.base_level = [1, 1, 1]
        self.maxhealth  = 25
        self.health     = self.maxhealth
        
        self.strength   = 6
        self.agility    = 6
        self.defense    = 6
WolfIG = Wolf()


class MainIG():
    def __init__(self):
        """
        Card        : [side][index] = [type][level]
        Hand        : [side][index] sorted by type card
        Board       : [side][index] ordered by played card
        
        Card Type   : self.card[0][index][0]
        Card Level  : self.card[0][index][1]
        """
        # Ressources
        self.base_card      = [base_card_fire,      base_card_water,    base_card_wind]
        self.base_board     = [base_board_fire,     base_board_water,   base_board_wind]
        self.base_banner    = [base_banner_fire,    base_banner_water,  base_banner_wind]
        self.base_number    = [[None, base_number_red_1, base_number_red_2, base_number_red_3, base_number_red_4, base_number_red_5, base_number_red_6, base_number_red_7, base_number_red_8, base_number_red_9],
                               [None, base_number_blue_1, base_number_blue_2, base_number_blue_3, base_number_blue_4, base_number_blue_5, base_number_blue_6, base_number_blue_7, base_number_blue_8, base_number_blue_9],
                               [None, base_number_green_1, base_number_green_2, base_number_green_3, base_number_green_4, base_number_green_5, base_number_green_6, base_number_green_7, base_number_green_8, base_number_green_9]]

        # Status
        self.card           = [ [ [], [], [], [], [] ],  [ [], [], [], [], [] ] ]
        self.hand           = [[None, None, None, None, None], [None, None, None, None, None]]
        self.board          = [ [], [] ]
        
        self.board_element  = [base_card_neutral, base_card_neutral]
        self.banner_element = [None, None]
        self.arrow          = base_arrow
        self.arrow_player   = self.arrow
        self.arrow_enemy    = pygame.transform.flip(self.arrow, False, True)

        # Battle Phase
        self.board_power    = [ [0, 0, 0], [0, 0, 0] ]
        self.element_type   = [None, None]
        self.battle_phase   = False
        self.initiative     = [False, False]

        # Statistics
        self.name       = ["NightFore", "Wolf"]
        self.icon       = [icon_status_iris, icon_status_direwolf]
        
        self.base_level = [[2, 2, 2], [1, 1, 1]]
        self.maxhealth  = [100, 100]
        self.health     = [self.maxhealth[0], self.maxhealth[1]]

        self.strength   = [6, 6]
        self.agility    = [6, 6]
        self.defense    = [6, 6]


    def battle_init(self, enemy=WolfIG):
        # Update
        self.update_enemy(enemy)
        self.update_card()

        # Name
        Text("%s" % self.name[0], 588, 497, Text_interface, True)
        Text("%s" % self.name[1], 212, 47,  Text_interface, True)

        # Health
        Text("Health: %s" % self.health[0], 588, 535, Text_interface, True)
        Text("Health: %s" % self.health[1], 212, 85,  Text_interface, True)
        
        Button_Image(55,  480, False, base_card_ok_inactive, base_card_ok_active, None, self.battle_update)



    def update_enemy(self, enemy):
        self.name[1]        = enemy.name
        self.icon[1]        = enemy.icon

        self.base_level[1]  = enemy.base_level
        self.maxhealth[1]   = enemy.maxhealth
        self.health[1]      = enemy.health

        self.strength[1]    = enemy.strength
        self.agility[1]     = enemy.agility
        self.defense[1]     = enemy.defense

        
    def update_card(self, battle=False):
        if battle == False:
            # Update Card
            for side in range(2):
                # Random Card Level & Type
                for index in range(5):
                    random_type     = random.randint(0, 2)
                    random_level    = random.randint(0, 3) + self.base_level[side][random_type]
                    self.card[side][index] = [random_type, random_level]

                # Sort Card
                self.card[side] = sorted(self.card[side], key=itemgetter(1), reverse=True)  # Level
                self.card[side] = sorted(self.card[side], key=itemgetter(0), reverse=True)  # Type

                # Reset Board
                self.board[side] = []


            # Update Hand
            for index in range(5):
                if self.hand[0][index] in Setup.list_button_image:
                    Setup.list_button_image.remove(self.hand[0][index])
                    
                card = self.base_card[self.card[0][index][0]]
                self.hand[0][index] = Button_Image(120+65*index, 480, False, card, card, index, self.select_card)
                self.hand[1][index] = self.card[1][index]


            # Play random Enemy Card
            while len(self.board[1]) == 0:
                for index in range(5):
                    if len(self.board[1]) < 4 and random.choice([True, False]) == True:
                        self.hand[1][index] = None
                        self.board[1].append(index)

        elif battle == True:
            # Reset Board
            self.board = [ [], [] ]

            # Play remaning Enemy Card
            for index in range(len(self.hand[1])):
                if self.hand[1][index] != None:
                    self.hand[1][index] = None
                    self.board[1].append(index)

        self.element_update()


    def select_card(self, index):
        if len(self.board[0]) < 4 and self.hand[0][index] in Setup.list_button_image:
            Setup.list_button_image.remove(self.hand[0][index])
            
            self.hand[0][index] = None
            self.board[0].append(index)

            self.element_update()
        

    def unselect_card(self):
        for event in Tools.events:
            if self.board[0] != [] and Tools.event.type == pygame.MOUSEBUTTONDOWN and Tools.event.button == 3:
                index = self.board[0][len(self.board[0])-1]
                card = self.base_card[self.card[0][index][0]]
                
                self.hand[0][index] = Button_Image(120+65*index, 480, False, card, card, index, self.select_card)
                self.board[0].remove(index)

                self.element_update()
            

    def battle_update(self):
        if self.board_power[0] != 0:
        
            # Battle Phase 1 - Initiative Phase
            if self.battle_phase == False:
                player_initiative   = self.board_power[0] + self.agility[0]
                enemy_initiative    = self.board_power[1] + self.agility[1]
                
                # Player Initiative
                if player_initiative >= enemy_initiative:
                    self.initiative[0] = True

                # Enemy Initiative
                elif player_initiative < enemy_initiative:
                    self.initiative[1] = True

                self.update_card(battle=True)
                self.battle_phase = True
            

            # Battle Phase 2 - Attack Phase
            elif self.battle_phase == True:
                for side in range(2):
                    if self.initiative[side] == True:
                        damage = (self.board_power[side] + self.strength[side]) - (self.board_power[1-side] + self.defense[1-side])

                        if damage >= 0:
                            self.health[1-side] -= damage
                            
                            if self.health[1-side] < 0:
                                self.health[1-side] = 0
                            
                self.update_card()
                self.battle_phase = False
                self.initiative = [False, False]


    def element_update(self):
        for side in range(2):
            self.board_power[side]  = [0, 0, 0]
            self.element_type[side] = None
        
            if self.board[side] != []:
                for index in range(len(self.board[side])):
                    card_type   = self.card[side][self.board[side][index]][0]
                    card_level  = self.card[side][self.board[side][index]][1]
                    self.board_power[side][card_type] += card_level

                self.element_type[side]     = self.board_power[side].index(max(self.board_power[side]))
                self.board_element[side]    = self.base_board[self.element_type[side]]
                self.banner_element[side]   = self.base_banner[self.element_type[side]]

            else:
                self.board_element[side]    = base_card_neutral
                self.banner_element[side]   = None

            self.board_power[side] = sum(self.board_power[side])

        """
        Element Advantage
            p_type      : Player's element
            e_type      : Enemy's element
            Neutral     : No advantage
            Advantage   : Player advantage
            Disavantage : Enemy advantage
        """
        if self.board[0] != []:
            p_type, e_type = self.element_type[0], self.element_type[1]

            # Neutral
            if p_type == e_type:
                self.arrow = None
    
            # Advantage
            elif (p_type == 0 and e_type == 2) or (p_type == 1 and e_type == 0) or (p_type == 2 and e_type == 1):
                self.board_power[0] += 1 + self.base_level[0][self.element_type[0]]
                self.arrow = self.arrow_player

            # Disavantage
            else:
                self.board_power[1] += 1 + self.base_level[1][self.element_type[1]]
                self.arrow = self.arrow_enemy
                
        else:
            self.arrow = None

        
    def update(self):
        # Interface
        gameDisplay.blit(base_board,            (235, 200))
        
        # Player
        gameDisplay.blit(base_hand_player,      (50,  475))
        gameDisplay.blit(base_status_player,    (500, 475))
        gameDisplay.blit(icon_status_iris,      (670, 475))
        pygame.draw.rect(gameDisplay, Color_Green, (506, 519, 164*self.health[0]/self.maxhealth[0], 30))

        # Enemy
        gameDisplay.blit(base_hand_enemy,       (420, 25))
        gameDisplay.blit(base_status_enemy,     (50,  25))
        gameDisplay.blit(icon_status_direwolf,  (50,  25))
        pygame.draw.rect(gameDisplay, Color_Green, (130, 69,  164*self.health[1]/self.maxhealth[1], 30))


        # Element
        if self.arrow != None:
            gameDisplay.blit(self.arrow, (170, 275))

        for side in range(2):
            gameDisplay.blit(self.board_element[side], (240, 305-100*side))

            if self.banner_element[side] != None:
                gameDisplay.blit(self.banner_element[side], (160, 335-100*side))


        # Display Card
        for side in range(2):
            for index in range(5):
            # Hand - Enemy/Empty Card
                if self.hand[side][index] == None:
                    gameDisplay.blit(base_card_empty, (120+65*index+305*side, 480-450*side))
                    
                if self.hand[1][index] != None:
                    gameDisplay.blit(self.base_card[self.card[1][index][0]], (425+65*index, 30))                   

            # Board - Player/Enemy/Empty Card
            len_board = len(self.board[side])
            for index in range(len_board):
                type_card = self.card[side][self.board[side][index]][0]
                gameDisplay.blit(self.base_card[type_card], (305+65*index, 305-100*side))

            for index in range(4-len_board):
                gameDisplay.blit(base_card_empty, (500-65*index, 305-100*side))


        # Display Card Level
            # Hand
            for index in range(5):
                if self.hand[side][index] != None:
                    type_card   = self.card[side][index][0]
                    level_card  = self.card[side][index][1]
                    gameDisplay.blit(MainIG.base_number[type_card][level_card], (120+65*index+305*side, 480-450*side)) 

            # Board
            for index in range(len_board):
                type_card   = self.card[side][self.board[side][index]][0] 
                level_card  = self.card[side][self.board[side][index]][1]
                gameDisplay.blit(MainIG.base_number[type_card][level_card], (305+65*index, 305-100*side))

        self.unselect_card()

                    
MainIG = MainIG()



Main_Screen()
