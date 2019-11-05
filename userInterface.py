
# As information, with python2 the name is Tkinter (capital T)
import tkinter
from youtubeDownloader import downloader

class userInterface(youtubeDownloader):
    # We create the main window
    window = tkinter.Tk() 
    # We create a label with a text
    myLabel = tkinter.Label(window, text="Click Me!")
    # We "start" the Label we just create
    myLabel.pack()




    # This is a event that calls the window
    window.mainloop() 

