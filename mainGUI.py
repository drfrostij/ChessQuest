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


#import # filename          # this is for importing all the varibles from a file
from shopGUI import *  # this is for importing the shop GUI function
#print(#filename.variable)
from realvsreal import *
from realvsbot import main as chessbotmain

##########################
# Main Startup Code Area #
##########################

# Credits Function

def creditfunction():
    messagebox.showinfo("ChessQuest Credits Page", "Owner / Developer / Artist: Daniel Allison")

# Player vs Player Function

def playervsplayerfunction():
    mainpage.destroy()
    main()

# Player vs Chessbot Function

def playervschessbotfunction():
    def show_values():
        chessbot_elo = w1.get()
        slider.destroy()
        chessbotmain(chessbot_elo)
    slider = customtkinter.CTkToplevel(mainpage)
    slider.title("ChessBot Difficulty Slider")
    slider.geometry("300x100")
    slider.resizable(False, False)
    w1 = Scale(
        slider,
        from_=100,
        to=3000,
        orient=HORIZONTAL,
        length=200,
        tickinterval=500,
        resolution=100
    )
    w1.set(1000)
    w1.pack()
    Button(
        slider,
        text="Set ChessBot Difficulty Elo",
        command=show_values
    ).pack()

# Shop GUI area Function

def shopfunction():
    print("hi")
    shopGUI()


# Main GUI
def mainGUI():
    global mainpage
    mainpage = customtkinter.CTk()                           #Creates the Window
    mainpage.title("ChessQuest Menu Page")                   #Names the created Window
    mainpage.geometry("500x450")                             #Sets the chesswindowsize
    #Naming section
    titlelogin = customtkinter.CTkButton(mainpage, text="ChessQuest Menu Page")
    titlelogin.grid(row=0, column=0, padx=20, pady=20)
    titlelogin.configure(state="disabled")
    titlelogin.configure(fg_color="Grey")
    titlelogin.configure(width=200, height=50)
    titlelogin.configure(font=("Arial", 30))
    #Creating an button
    #https://customtkinter.tomschimansky.com/tutorial/grid-system
    creditfunctionbutton = customtkinter.CTkButton(mainpage, text="Credits", command=lambda:creditfunction())  # Credits button
    creditfunctionbutton.grid(row=1, column=0, padx=20, pady=20)
    shopfunctionbutton = customtkinter.CTkButton(mainpage, text="Shop", command=lambda:shopfunction())      # Shop button
    shopfunctionbutton.grid(row=2, column=0, padx=20, pady=20)
    playervsplayerfunctionbutton = customtkinter.CTkButton(mainpage, text="PlayerVsPlayer", command=playervsplayerfunction)      # Player vs player button
    playervsplayerfunctionbutton.grid(row=3, column=0, padx=20, pady=20)
    mainpage.grid_columnconfigure(0, weight=1)     #Sets the button in the middle of the GUI
    playervschessbotfunctionbutton = customtkinter.CTkButton(mainpage, text="PlayerVsChessBot", command=lambda:playervschessbotfunction())      # Player vs chessbot button
    playervschessbotfunctionbutton.grid(row=4, column=0, padx=20, pady=20)
    mainpage.mainloop()                            #Loads the current GUI data

