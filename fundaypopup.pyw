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

        self.hideWindow()
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

            self.startListening()
        
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
            
            elif (len(args) == 5):
                if (self.matchingDateTime(args)):
                    self.showWindow(event)

            else:
                self.writeToLog("Wrong format of event time")

    def matchingDateTime(self, args):
        now = datetime.now()
        dts = [int(arg) for arg in args]

        return dts[0] == now.day and dts[1] == now.month and dts[2] == now.year and \
               dts[3] == now.hour and dts[4] == now.minute

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
        event_theme = self.current_theme+" "+event

        if (not os.path.isdir("images")):
            self.writeToLog("Images folder missing")

        if (not os.path.isdir("sounds")):
            self.writeToLog("Sounds folder missing")

        if (self.cfp.has_option(event_theme, "font")):
            if (not os.path.isdir("fonts")):
                self.writeToLog("Fonts folder missing")

        self.displayImage(event_theme)
        self.deiconify()
        self.playSound(self.cfp[event_theme]["sound"])

    def hideWindow(self):
        self.withdraw()

    def displayImage(self, theme_name):
        if (self.image_holder != None):
            self.image_holder.pack_forget()
            self.image_holder = None

        image_file = self.cfp[theme_name]["image"]
        img = Image.open("./images/"+image_file)
        img = img.resize((self.win_width, self.win_height))

        if (self.cfp[theme_name]["font"] is not None):
            self.writeCaptionsOnImage(img, theme_name)

        self.image = ImageTk.PhotoImage(img)
        self.image_holder = tk.Label(self, image=self.image)
        self.image_holder.image = self.image

        self.image_holder.pack(side="top")

    def writeCaptionsOnImage(self, img, theme_name):
        editable_image = ImageDraw.Draw(img)
        font_file = ImageFont.truetype("./fonts/"+self.cfp[theme_name]["font"], int(self.cfp[theme_name]["fontsize"]))
        a, d = font_file.getmetrics()

        text_color = self.cfp[theme_name]["color"].lower()
        if (text_color.replace(" ", "").isdigit()):
            rgb = tuple([int(i) for i in text_color.split(" ")])
        else:
            rgb = {
                "white": (255, 255, 255),
                "black": (0, 0, 0),
                "red": (255, 77, 77),
                "blue": (0, 85, 255),
                "green": (119, 255, 51),
                "yellow": (255, 255, 25),
                "orange": (255, 128, 0),
                "pink": (255, 102, 229),
                "purple": (179, 25, 255)
            }[text_color]

        if (self.cfp.has_option(theme_name, "topcaption")):
            text_width = editable_image.textlength(self.cfp[theme_name]["topcaption"], font_file)
            editable_image.text((self.win_width/2-text_width/2, d+5), self.cfp[theme_name]["topcaption"], font=font_file, fill=rgb, stroke_width=1, stroke_fill=(0, 0, 0))

        if (self.cfp.has_option(theme_name, "bottomcaption")):
            text_width = editable_image.textlength(self.cfp[theme_name]["bottomcaption"], font_file)
            editable_image.text((self.win_width/2-text_width/2, self.win_height-(a+d)-5), self.cfp[theme_name]["bottomcaption"], font=font_file, fill=rgb, stroke_width=1, stroke_fill=(0, 0, 0))

    def playSound(self, sound_file):
        def waitForSoundToFinish(sound_file):
            try:
                playsound("./sounds/"+sound_file, block=True)
                self.in_event = None
                self.hideWindow()
                self.startListening()
            except Exception as e:
                self.writeToLog(f"Error during playsound: {e}")

        T = Thread(target = waitForSoundToFinish, args=(sound_file,))
        T.start()

    def writeToLog(self, msg):
        '''
        Writes issues that happen during the program's life cycle to the log file.
        Also exits out of the program
        '''
        with open("log.txt", "a") as file:
            file.write(f"{datetime.now()}: {msg}\n")
        
        self.destroy()
        sys.exit(1)

if __name__ == "__main__":
    root = Main()
    root.mainloop()