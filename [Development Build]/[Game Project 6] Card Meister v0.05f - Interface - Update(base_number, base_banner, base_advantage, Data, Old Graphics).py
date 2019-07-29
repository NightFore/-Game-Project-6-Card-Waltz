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

base_card_ok                = pygame.image.load("Data\Graphics\Base_card_ok.png").convert()
base_card_enemy             = pygame.image.load("Data\Graphics\Base_card_enemy.png").convert()
base_card_empty             = pygame.image.load("Data\Graphics\Base_card_empty.png").convert()

base_card_fire              = pygame.image.load("Data\Graphics\Base_card_fire.png").convert()
base_card_water             = pygame.image.load("Data\Graphics\Base_card_water.png").convert()
base_card_wind              = pygame.image.load("Data\Graphics\Base_card_wind.png").convert()

base_advantage_fire         = pygame.image.load("Data\Graphics\Base_advantage_fire.png").convert()
base_advantage_water        = pygame.image.load("Data\Graphics\Base_advantage_water.png").convert()
base_advantage_wind         = pygame.image.load("Data\Graphics\Base_advantage_wind.png").convert()

base_banner_fire            = pygame.image.load("Data\Graphics\Base_banner_fire.png").convert()
base_banner_water           = pygame.image.load("Data\Graphics\Base_banner_water.png").convert()
base_banner_wind            = pygame.image.load("Data\Graphics\Base_banner_wind.png").convert()

base_board                  = pygame.image.load("Data\Graphics\Base_board.png").convert()
base_hand_player            = pygame.image.load("Data\Graphics\Base_hand_player.png")
base_hand_enemy             = pygame.image.load("Data\Graphics\Base_hand_enemy.png")

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
    Button(None, None, 125, 200, 100, 200, 10, True, False, Color_Red, Color_Green, None, MainIG.update_card)

    # Loop
    gameExit = False
    while not gameExit:
        gameDisplay.update()
        Setup.update()
        MainIG.update()
        
        for event in Tools.events:    
            if event.type == pygame.QUIT:
                quit_game()

class MainIG():
    def __init__(self):
        """
        Card        : [side][index] = [type][level]
        Hand        : [side][index] sorted by type card
        Board       : [side][index] ordered by played card
        
        Card Type   : self.card[0][index][0]
        Card Level  : self.card[0][index][1]
        """
        self.base_card      = [base_card_fire, base_card_water, base_card_wind, base_card_enemy, base_card_ok, base_card_empty]
        self.base_number    = [[None, base_number_red_1, base_number_red_2, base_number_red_3, base_number_red_4, base_number_red_5, base_number_red_6, base_number_red_7, base_number_red_8, base_number_red_9],
                               [None, base_number_blue_1, base_number_blue_2, base_number_blue_3, base_number_blue_4, base_number_blue_5, base_number_blue_6, base_number_blue_7, base_number_blue_8, base_number_blue_9],
                               [None, base_number_green_1, base_number_green_2, base_number_green_3, base_number_green_4, base_number_green_5, base_number_green_6, base_number_green_7, base_number_green_8, base_number_green_9]]
        
        self.base_level = [[1, 1, 1], [1, 1, 1]]
        self.card       = [ [ [], [], [], [], [] ],  [ [], [], [], [], [] ] ]
        self.board      = [ [], [] ]
        self.hand       = [[None, None, None, None, None], [None, None, None, None, None]]
        self.init       = False

        self.maxhealth  = 100
        self.health     = self.maxhealth

        self.strength   = 6
        self.agility    = 6
        self.resilience = 6


    def update_card(self):
        # Card - Update
        for side in range(2):
            # Generate card
            for index in range(5):
                random_type     = random.randint(0, 2)
                random_level    = random.randint(0, 3) + self.base_level[side][random_type]
                self.card[side][index] = [random_type, random_level]


            # Sort Card
                # Sort Type Card
            self.card[side] = sorted(self.card[side], key=itemgetter(1), reverse=True)

                # Sort Level Card
            self.card[side] = sorted(self.card[side], key=itemgetter(0))

            
            # Reset Board
            self.board[side] = []


        # Card - Hand
        for index in range(5):
            if self.hand[0][index] in Setup.list_button_image:
                Setup.list_button_image.remove(self.hand[0][index])
                
            card = self.base_card[self.card[0][index][0]]
            self.hand[0][index] = Button_Image(120+65*index, 480, False, card, card, index, self.select_card)
            self.hand[1][index] = self.card[1][index]


        # Card - Random enemy's played card
        while len(self.board[1]) == 0:
            for index in range(5):
                if len(self.board[1]) < 4 and random.choice([True, False]) == True:
                    self.hand[1][index] = None
                    self.board[1].append(index)


    def select_card(self, index):
        if len(self.board[0]) < 4 and self.hand[0][index] in Setup.list_button_image:
            Setup.list_button_image.remove(self.hand[0][index])
            
            self.hand[0][index] = None
            self.board[0].append(index)


    def unselect_card(self):
        for event in Tools.events:
            if self.board[0] != [] and Tools.event.type == pygame.MOUSEBUTTONDOWN and Tools.event.button == 3:
                index = self.board[0][len(self.board[0])-1]
                card = self.base_card[self.card[0][index][0]]
                
                self.hand[0][index] = Button_Image(120+65*index, 480, False, card, card, index, self.select_card)
                self.board[0].remove(index)

        
    def update(self):
        # Interface
        gameDisplay.blit(icon_status_iris,      (670, 485))
        gameDisplay.blit(icon_status_direwolf,  (50,  35))
        gameDisplay.blit(base_board,           (235, 200))
        gameDisplay.blit(base_hand_player,      (50,  475))
        gameDisplay.blit(base_hand_enemy,       (415, 25))
        gameDisplay.blit(base_card_ok,          (55,  480))


        # Health Bar
        pygame.draw.rect(gameDisplay, Color_Green, (510, 530, 1.5*self.health, 30))
        pygame.draw.rect(gameDisplay, Color_Green, (140, 80,  1.5*self.health, 30))


        # Display Card
        for side in range(2):
            for index in range(5):
            # Hand - Enemy/Empty Card
                if self.hand[side][index] == None:
                    gameDisplay.blit(self.base_card[5], (120+65*index+300*side, 480-450*side))
                    
                if self.hand[1][index] != None:
                    gameDisplay.blit(self.base_card[self.card[1][index][0]], (420+65*index, 30))                   

            # Board - Player/Enemy/Empty Card
            len_board = len(self.board[side])
            for index in range(len_board):
                type_card = self.card[side][self.board[side][index]][0]
                gameDisplay.blit(self.base_card[type_card], (305+65*index, 305-100*side))

            for index in range(4-len_board):
                gameDisplay.blit(self.base_card[5], (500-65*index, 305-100*side))


        # Display Card Level
            # Hand
            for index in range(5):
                if self.hand[side][index] != None:
                    type_card   = self.card[side][index][0]
                    level_card  = self.card[side][index][1]
                    gameDisplay.blit(MainIG.base_number[type_card][level_card], (120+65*index+300*side, 480-450*side)) 

            # Board
            for index in range(len_board):
                type_card   = self.card[side][self.board[side][index]][0] 
                level_card  = self.card[side][self.board[side][index]][1]
                gameDisplay.blit(MainIG.base_number[type_card][level_card], (305+65*index, 305-100*side))

        self.unselect_card()

                    
MainIG = MainIG()



Main_Screen()
