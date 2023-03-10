# native imports
import configparser as cfp
import os
from playsound import playsound
import tkinter as tk
from threading import Thread
from time import gmtime, strftime
import time
from winsound import *

# external imports


class Main(tk.Tk):
    '''
    Creates the tkinter window. Plays the current Funday if you open the main file
    directly, or it will run eventually on its own at the designated time
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # roughly center window on screen
        win_width = 500
        win_height = 400
        screen_width = self.winfo_screenwidth()//2 - win_width//2
        screen_height = self.winfo_screenheight()//2 - win_height//2
        self.geometry(f"{win_width}x{win_height}+{screen_width}+{screen_height}")

        # Add some constraints to the window
        self.resizable(0, 0)
        self.attributes("-topmost", True)
        self.update()
        #self.protocol("WM_DELETE_WINDOW", lambda: None)
        self.bind("<Unmap>", lambda e: self.deiconify())

        self.readInConfig()

    def readInConfig(self):
        '''
        Reads the config file and sets the required variables and values needed
        to run the Funday program
        '''
        if (not os.path.isfile("fundays.ini")):
            self.writeToLog("Config file missing")

        if (not os.path.isdir("images")):
            self.writeToLog("Images folder missing")

        if (not os.path.isdir("sounds")):
            self.writeToLog("Sounds folder missing")

        try:
            cpr = cfp.ConfigParser()
            cpr.read("fundays.ini")
            all_sections = cpr.sections()
            current_theme = cpr["CurrentFundayTheme"]["ThemeName"]
            
            theme_sections = [t for t in all_sections if current_theme in t]
            print(theme_sections)

            #cpr["Theme Krabs 22 00"]["sound"]
        
        except Exception as e:
            self.writeToLog(f"Error while reading config file: {e}")

    def playSound(self, sound_file):
        T = Thread(target = lambda: playsound("./sounds/"+sound_file))
        T.start()

    def writeToLog(self, msg):
        '''
        Logs issues that happen during the program's life cycle to the log file
        so that you can potentially fix them
        '''
        with open("log.txt", "a") as file:
            file.write(f"{strftime('%Y-%m-%d %H:%M:%S', gmtime())}: {msg}\n")
        
        self.destroy()


if __name__ == "__main__":
    root = Main()
    root.mainloop()