# native imports
import os
import sys
import time
import tkinter as tk
import configparser as cfp
from threading import Thread
from datetime import datetime

# external imports
from PIL import Image, ImageTk, ImageDraw, ImageFont
from playsound import playsound

class Main(tk.Tk):
    '''
    Creates the tkinter window. Plays the current Funday if you open the main file
    directly, or it will run eventually on its own at the designated time
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # instance properties
        self.cfp = cfp.ConfigParser()
        self.in_event = False
        self.current_theme = None
        self.event_times = None
        self.image = None
        self.image_holder = None

        # roughly center window on screen
        self.win_width = 640
        self.win_height = 480
        screen_width = self.winfo_screenwidth()//2 - self.win_width//2
        screen_height = self.winfo_screenheight()//2 - self.win_height//2
        self.geometry(f"{self.win_width}x{self.win_height}+{screen_width}+{screen_height}")

        # Add some constraints to the window
        self.resizable(0, 0)
        self.attributes("-topmost", True)
        self.overrideredirect(1)
        self.update()
        self.protocol("WM_DELETE_WINDOW", lambda: None)

        #self.hideWindow()
        self.readInConfigAndStartListening()

    def readInConfigAndStartListening(self):
        '''
        Reads the config file and sets the required variables and values needed
        to run the Funday program
        '''
        if (not os.path.isfile("fundays.ini")):
            self.writeToLog("Config file missing")

        try:
            self.cfp.read("fundays.ini")
            all_sections = self.cfp.sections()
            self.current_theme = self.cfp["CurrentFundayTheme"]["ThemeName"]
            self.event_times = {t.replace(self.current_theme+" ", ""):0 for t in all_sections if self.current_theme in t}

            self.displayImage(self.cfp["Krabs 14 15"]["image"])
            self.playSound(self.cfp["Krabs 14 15"]["sound"])

            #self.startListening()
        
        except Exception as e:
            self.writeToLog(f"Error while reading config file / listening: {e}")

    def startListening(self):
        if self.in_event is None:
            time.sleep(60)
            self.in_event = False

        while not self.in_event:
            self.checkForEvent()

    def checkForEvent(self):
        time.sleep(1)
        for event in self.event_times.keys():
            args = event.split(" ")
            if (len(args) == 1):
                if (self.matchingWeekday(args[0]) and self.event_times[event] == 0):
                    self.event_times[event] = 1
                    self.showWindow(event)

            elif (len(args) == 2):
                if (self.matchingTime(args[0], args[1])):
                    self.showWindow(event)

            elif (len(args) == 3):
                if (self.matchingWeekday(args[0]) and self.matchingTime(args[1], args[2])):
                    self.showWindow(event)

            else:
                self.writeToLog("Wrong format of event time")

    def matchingWeekday(self, day):
        today = datetime.today().weekday()
        event = time.strptime(day.lower(), "%A").tm_wday
        return event == today

    def matchingTime(self, hour, minute):
        now = datetime.now()
        h = now.hour
        m = now.minute
        return (int(hour) == h and int(minute) == m)

    def showWindow(self, event):
        self.in_event = True

        if (not os.path.isdir("images")):
            self.writeToLog("Images folder missing")

        if (not os.path.isdir("sounds")):
            self.writeToLog("Sounds folder missing")

        event_theme = self.current_theme+" "+event
        self.displayImage(self.cfp[event_theme]["image"])
        self.deiconify()
        self.playSound(self.cfp[event_theme]["sound"])

    def hideWindow(self):
        self.withdraw()

    def displayImage(self, image_file):
        if (self.image_holder != None):
            self.image_holder.pack_forget()
            self.image_holder = None

        img = Image.open("./images/"+image_file)
        img = img.resize((self.win_width, self.win_height))
        self.image = ImageTk.PhotoImage(img)
        self.image_holder = tk.Label(self, image=self.image)
        self.image_holder.image = self.image

        self.image_holder.pack(side="top")

    def playSound(self, sound_file):
        def waitForSoundToFinish(sound_file):
            playsound("./sounds/"+sound_file, block=True)
            self.in_event = None
            self.hideWindow()
            self.startListening()

        T = Thread(target = waitForSoundToFinish, args=(sound_file,))
        T.start()

    def writeToLog(self, msg):
        '''
        Logs issues that happen during the program's life cycle to the log file
        so that you can potentially fix them
        '''
        with open("log.txt", "a") as file:
            file.write(f"{datetime.now()}: {msg}\n")
        
        self.destroy()
        sys.exit(1)


if __name__ == "__main__":
    root = Main()
    root.mainloop()