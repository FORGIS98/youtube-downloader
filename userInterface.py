#!/usr/bin/env python3

# As information, with python2 the name is Tkinter (capital T)
from tkinter import Frame, Tk, BOTH, Text, Menu, END, filedialog

from youtubeDownloader import downloader

class userInterface(downloader, Frame):

    def __init__(self):
        super().__init__() # We inherits from the Frame container widget.
        self.initUI()

    def initUI(self):
        self.master.title("youtubeDownloader") # Sets the window title.
        self.pack(fill=BOTH, expand=1) # .pack() is one of the three geometry managers
        self.centerWindow()



    def centerWindow(self):
        w = 290 # width
        h = 150 # height

        # This will take the real screen size
        screenW = self.master.winfo_screenwidth()
        screenH = self.master.winfo_screenheight()

        x = (screenW - w)/2
        y = (screenH - h)/2

        # This will put the window in the center of the screen.
        self.master.geometry('%dx%d+%d+%d' % (w, h, x, y)) # Width x High + x + y (coordinates)

def main():

    root = Tk() # root window created
    myInterface = userInterface()
    root.mainloop()

if __name__ == '__main__':
    main()
