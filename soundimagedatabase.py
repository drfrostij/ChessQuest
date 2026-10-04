###################################
#                                 #
#    Created By DrFrostij         #
#                                 #
###################################


########################
# The imports section  #
########################


import os                       # this is used to get the images + sounds we want                   # (needs pip installment)
# https://docs.python.org/3/library/os.html                                                         #OS documentation
import chess                    # this is for the chess board logic                                 # (needs pip installment)
#https://python-chess.readthedocs.io/en/latest/                                                     #Chess documentation
import pygame                   # this is for the graphics and sounds                               # (needs pip installment)
#https://www.pygame.org/docs/                                                                       #Pygame documentation
import customtkinter as customtkinter  # this is for the GUI                                        # (needs pip installment)
#https://customtkinter.tomschimansky.com                                                            #Custom Tkinter documentation
import bcrypt                         # this is for the password hashing                            # (needs pip installment)    
#https://www.geeksforgeeks.org/python/hashing-passwords-in-python-with-bcrypt/                      #Bcrypt documentation
from PIL import Image, ImageTk          # this is for loading images                                # (needs pip installment)
#https://pillow.readthedocs.io/en/stable/                                                           #PIL documentation
from tkinter import HORIZONTAL, Button, Scale, mainloop, messagebox    #pop ups                     # (needs pip installment)
#https://docs.python.org/3/library/tkinter.messagebox.html                                          #Message box documentation    
import tkinter                                                                                      #PIL documentation
#https://docs.python.org/3/library/tkinter.html                                                     #Tkinter documentation

##############################
# Importing from other files #
##############################

import os
import pygame

pygame.init()
pygame.mixer.init()

#import # filename          # this is for importing all the varibles from a file

#print(#filename.variable)


##########################
# Main Startup Code Area #
##########################

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PIECES_DIR = os.path.join(BASE_DIR, "pieces")
SOUNDS_DIR = os.path.join(BASE_DIR, "sounds")


#images as variables
#https://www.pygame.org/docs/ref/image.html#pygame.image.load

pieces = {
    "wp": pygame.image.load(os.path.join(PIECES_DIR, "wp.png")), #White Pawn
    "wR": pygame.image.load(os.path.join(PIECES_DIR, "wR.png")), #White Rook
    "wN": pygame.image.load(os.path.join(PIECES_DIR, "wN.png")), #White Knight
    "wB": pygame.image.load(os.path.join(PIECES_DIR, "wB.png")), #White Bishop
    "wQ": pygame.image.load(os.path.join(PIECES_DIR, "wQ.png")), #White Queen
    "wK": pygame.image.load(os.path.join(PIECES_DIR, "wK.png")), #White King
    "bp": pygame.image.load(os.path.join(PIECES_DIR, "bp.png")), #Black Pawn
    "bR": pygame.image.load(os.path.join(PIECES_DIR, "bR.png")), #Black Rook
    "bN": pygame.image.load(os.path.join(PIECES_DIR, "bN.png")), #Black Knight
    "bB": pygame.image.load(os.path.join(PIECES_DIR, "bB.png")), #Black Bishop
    "bQ": pygame.image.load(os.path.join(PIECES_DIR, "bQ.png")), #Black Queen
    "bK": pygame.image.load(os.path.join(PIECES_DIR, "bK.png")), #Black King
}


#sound as variables
#https://www.pygame.org/docs/ref/mixer.html

sound = {
    "capture": pygame.mixer.Sound(os.path.join(SOUNDS_DIR, "capture.mp3")),
    "castle": pygame.mixer.Sound(os.path.join(SOUNDS_DIR, "castle.mp3")),
    "game-end": pygame.mixer.Sound(os.path.join(SOUNDS_DIR, "game-end.mp3")),
    "game_start": pygame.mixer.Sound(os.path.join(SOUNDS_DIR, "game-start.mp3")),
    "illegal": pygame.mixer.Sound(os.path.join(SOUNDS_DIR, "illegal.mp3")),
    "move-check": pygame.mixer.Sound(os.path.join(SOUNDS_DIR, "move-check.mp3")),
    "move-opponent": pygame.mixer.Sound(os.path.join(SOUNDS_DIR, "move-opponent.mp3")),
    "move-self": pygame.mixer.Sound(os.path.join(SOUNDS_DIR, "move-self.mp3")),
    "premove": pygame.mixer.Sound(os.path.join(SOUNDS_DIR, "premove.mp3")),
    "promote": pygame.mixer.Sound(os.path.join(SOUNDS_DIR, "promote.mp3")),
}


#icons as variables (will be done directly)
#https://customtkinter.tomschimansky.com/documentation/widgets/button