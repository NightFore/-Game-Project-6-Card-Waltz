import pygame
import os
import time
import random

pygame.init()



############################################################

"""
    Settings
"""
# Title
project_title = "Card Meister"
pygame.display.set_caption(project_title)

# Screen Size
Screen_Size = display_width, display_height = 800, 600
gameDisplay = pygame.display.set_mode((display_width, display_height))

# FPS
FPS = 60
clock = pygame.time.Clock()



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
        
            Fight       : Enable combat status and display user interfaces
            Story       : Enables reading of the text files of the story and displays the user interfaces

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
        
        self.fight  = False
        self.story  = False

        self.inventory  = False
        self.shop       = False
        self.result     = False

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

        

    def update_init(self, background=False, music=False, button=False, sprite=False,  fight=False, text=False, story=False):
        """
        Update :
            Setup   : Load all states
            Reset   : Clean all lists and reset user interface states
            Load    : Load Background & Music
            
        """
        # Setup
        self.button = button
        self.sprite = sprite
        self.fight  = fight
        self.story  = story
        self.text   = text

        # Reset
        self.list_button        = []
        self.list_button_image  = []
        self.list_sprite        = []    # AnimatedSprite()
        self.all_sprites        = []    # Creates a sprite group and adds 'player' to it.
        self.list_text          = []
        
        self.inventory  = False
        self.shop       = False
        self.status     = None
        self.result     = False
        
        # Load
        self.background = background

        if music != False: 
            self.update_music(music)

            

    def update(self):
        """
        Setup :
            Update game screen and background
            Retrieves game events in global variables
            
        """
        pygame.display.update()
        if self.background != False:
            gameDisplay.blit(self.background, (0,0))
            
        Tools.events = pygame.event.get()
        for event in Tools.events:
            Tools.event = event

        self.update_state()

    def update_state(self):
        """
        Interactive interface :
            Button & Sprite:
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
                for index in range(len(self.list_button)):
                    self.list_button[index].update(index)
                for index in range(len(self.list_button_image)):
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
                for index in range(len(self.list_sprite)):
                    if callable(self.list_sprite[index].action) == True:
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

        
    def update(self, index):
        mouse = pygame.mouse.get_pos()
        
        if self.rect.collidepoint(mouse):
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
    
        
    def update(self, index):
        mouse = pygame.mouse.get_pos()
        
        if self.rect.collidepoint(mouse):
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


base_card_ok    = pygame.image.load("Data\Graphics\Base_card_ok.png")
base_card_fire  = pygame.image.load("Data\Graphics\Base_card_fire.png")
base_card_water = pygame.image.load("Data\Graphics\Base_card_water.png")
base_card_wind  = pygame.image.load("Data\Graphics\Base_card_wind.png")



############################################################
"""
    Game Functions
"""
def Title_Screen():
    # Setup
    Setup.update_init()

    # Text
    Text(project_title, display_width/2, display_height/4, True, Text_Title_Screen)
    Button(None, Text_Interface, 0, 200, 800, 200, 10, True, False, Color_Red, Color_Green, None, action=PlayerIG.update_card)
    PlayerIG.update_card()
    
    # Loop
    gameExit = False
    while not gameExit:
        Setup.update()
        for event in Tools.events:
            
            PlayerIG.display_card()
            if event.type == pygame.QUIT:
                Quit_Game()



class PlayerIG():
    def __init__(self):
        self.base_card  = [base_card_fire, base_card_water, base_card_wind]
        self.base_level = [3, 3, 3]
        self.card       = [[],[],[],[],[]]
        print(self.card)


    def update_card(self):
        for index in range(5):
            type_card   = random.randint(0, 2)
            self.card[index] = [self.base_card[type_card], self.base_level[type_card] + random.randint(0, 3)]

    def display_card(self):
        gameDisplay.blit(base_card_ok, (55, 480))
        
        for index in range(5):
            gameDisplay.blit(PlayerIG.card[index][0], (120+65*index, 480))
        
PlayerIG = PlayerIG()



Title_Screen()
