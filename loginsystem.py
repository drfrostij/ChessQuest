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
from mainGUI import *  # this is for importing the main GUI function

#print(#filename.variable)

##########################
# Main Startup Code Area #
##########################

#Encrypting or checking user data


def encryptionandstorage(username, password):
    print(username, "is the username that has been entered")
    #Hashing
    #https://www.geeksforgeeks.org/python/hashing-passwords-in-python-with-bcrypt/
    bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(bytes, salt)
    #Textfile writing
    #https://www.geeksforgeeks.org/python/reading-writing-text-files-python/
    with open("DAdatebase.txt", "a+") as file:
        file.seek(0)
        users = file.readlines()
        for user in users:
            stored_username, stored_hash = user.strip().split(":", 1)
            if stored_username == username:
                if bcrypt.checkpw(password.encode("utf-8"), stored_hash.encode("utf-8")):
                    print("Login successful")
                    #Message box
                    #https://docs.python.org/3/library/tkinter.messagebox.html
                    messagebox.showinfo("ChessQuest Login Page", "Login was successful")
                    #loginpage.destroy()                               #Deletes the window
                else:
                    print("Login unsuccessful")
                    messagebox.showinfo("ChessQuest Login Page", "Incorrect Password")
    with open("DAdatebase.txt", "a") as file:
        file.write(username + ":" + hash.decode("utf-8") + "\n")
        print("User registered")
        messagebox.showinfo("ChessQuest Login Page", "You have been successfully registered")
        #loginpage.destroy()                               #Deletes the window



# Login GUI

def loginGUI():
    global loginpage, password, username
    loginpage = customtkinter.CTk()                           #Creates the Window
    loginpage.title("ChessQuest Login Page")                  #Names the created Window
    loginpage.geometry("350x350")                             #Sets the chesswindowsize
    #Naming section
    titlelogin = customtkinter.CTkButton(loginpage, text="User Login")
    titlelogin.grid(row=0, column=0, padx=20, pady=20)
    titlelogin.configure(state="disabled")
    titlelogin.configure(fg_color="white")
    titlelogin.configure(width=200, height=50)
    titlelogin.configure(font=("Arial", 30))
    #Creating an entry
    #https://customtkinter.tomschimansky.com/documentation/widgets/entry
    username = customtkinter.CTkEntry(loginpage, placeholder_text="Username")
    username.grid(row=1, column=0, padx=20, pady=20)
    password = customtkinter.CTkEntry(loginpage, placeholder_text="Password", show="*")
    password.grid(row=2, column=0, padx=20, pady=20)
    #Creating an button
    #https://customtkinter.tomschimansky.com/tutorial/grid-system
    button = customtkinter.CTkButton(loginpage, text="Login / Signup", command=lambda:encryptionandstorage(username.get(), password.get()))
    button.grid(row=3, column=0, padx=20, pady=20)
    loginpage.grid_columnconfigure(0, weight=1)     #Sets the button in the middle of the GUI
    loginpage.mainloop()                            #Loads the current GUI data


