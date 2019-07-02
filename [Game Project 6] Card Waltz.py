import pygame

from Ressources import *
from Tools      import *




def Quit_Game():
    pygame.quit()
    quit()


    
# Game - Main Function
def Title_Screen():
    # Setup
    Setup.update_init()

    # Text
    Text(project_title, display_width/2, display_height/4, True, Text_Title_Screen)
    
    # Loop
    gameExit = False
    while not gameExit:
        Setup.update()
        for event in Tools.events:
            if event.type == pygame.QUIT:
                Quit_Game()
Title_Screen()
