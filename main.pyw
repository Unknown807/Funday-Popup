# native imports
import tkinter as tk

# external imports

#custom imports

class Main(tk.Tk):
    '''
    Creates the tkinter window. Used for letting users configure their Fundays.
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Add some constraints to the window
        self.geometry("300x300")
        self.resizable(0, 0)
        self.attributes("-topmost", True)
        self.update()
        #self.protocol("WM_DELETE_WINDOW", lambda: None)
        self.bind("<Unmap>", lambda e: self.deiconify())

        self.title("Title here")






if __name__ == "__main__":
    root = Main()
    root.mainloop()