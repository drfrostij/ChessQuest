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

from loginsystem import loginGUI
from mainGUI import mainGUI  # this is for importing the login GUI function
#import # filename          # this is for importing all the varibles from a file

#print(#filename.variable)

##########################
# Main Startup Code Area #
##########################


def startup():
    mainGUI()  # Call the main GUI function


startup()