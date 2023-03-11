# Funday-Popup
<p align="center">
  <img src="https://github.com/Unknown807/Funday-Popup/blob/main/repo_images/monday.PNG" />
</p>

## Description
Funday-Popup is a small program that listens in the background for user specified date time events. When an event occurs, the program will appear on top of all other applications and will show an image and play some music (as setup in the config). The program can be used to setup fun little reminders, celebrations and other events at regular intervals (i.e every Monday at 9:30 AM).

## How To Use
Go to releases and download the zip file, and extract it to any folder you want. In the extracted folder, you should see a fundays.ini config file, a sounds, images and fonts folder.

- There are no constraints on the size of images (as they are resized), though large images may appear lower quality
as the dimensions of the program are 640x480. Images currently work for jpg and png.

- Sound files currently work for wav and mp3 formats.

- Font files currently work for otf and ttf formats.

- In any of these folders you can drop your own sounds, fonts and images and use them in the config. Any issues that arise when running the program are written to a log.txt file (raise an issue if so).

- The program checks every other second for an event, once an event occurs they'll be a delay of 1 minute before
listening will resume again (to prevent the same event fireing).

### Config File
```
[CurrentFundayTheme]
ThemeName = Krabs

[Krabs Monday 09 30]
sound = krabsmonday.mp3
image = krabsmonday.jpg
topcaption = Rise N shine Sailors
bottomcaption = It be a Monday
font = krabs.otf
fontsize = 32
color = white
```

The above is what a part of the config file (fundays.ini) looks like, There must be a section called 'CurrentFundayTheme' with ThemeName set to the word(s) that prepend the series of events you want the program to listen for. E.g. Krabs will match all events that beging with Krabs followed by a space.

#### Event Formats:
```
[EventName Weekday]
[EventName Hour Minute]
[EventName Weekday Hour Minute]
[EventName Day Month Year Hour Minute]
```
- Weekday is literally Monday/Tuesday/Wednesday/Thursday/Friday/Saturday/Sunday
- Hour is in 24 hour format
- Minute is 1-60, can be zero-padded or not (06, 6)
- Day is 1-31 (depending on month)
- Month is 1-12
- Year would be something like 2023

Specifying weekday means the event will happen every week on that day, whenever the program can try an execute it (same with 'Hour Minute' format). These formats cannot be mixed around.

#### Event Properties:
- An event has to have an 'image' and 'sound' specified, with both including the filenames with their extensions and being stored in the images/ and sounds/ folders.

- An event doesn't need to have 'topcaption' nor a 'bottomcaption' option, or you can just one or the other (e.g just specifying a 'topcaption'). If you do specify captions, you need to have a 'font', 'fontsize' and 'color' option. The 'font' option should refer to the name of the font file (with its extension) which is stored in the fonts/ folder.

- Captions can have spaces, upper case, lower case letters and a good amount of special characters (comma, exclamation mark, apostrophe)

- For 'color', you can either specify the name of some in built colors (white, black, red, blue, green, yellow, orange, pink, purple) or three rgb values separated by spaces, e.g. '255 125 25', to use a custom color.

- Note: a good 'fontsize' is around 24

### On Startup
This program works best when set to run on startup, so you don't have to run it manually for it to start listening for events (though you can if you want).

To make it run on start up if you press 'Windows Key + R' and type in the popup run dialog 'shell:startup' then you'll open the Windows startup folder. If you then create a shortcut to the 'Funday Popup.exe' file and drag it into the startup folder, the next time to boot up your computer it will be running in the background.
