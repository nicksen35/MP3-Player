from pygame import mixer
import pygame
from tkinter import *
import tkinter.font
from tkinter import filedialog
#For directory
import os
import time
from mutagen.mp3 import MP3
#To adjust the music
import tkinter.ttk as ttk
#Whenever I need to call tkinter.tkk I refer to tkk
from PIL import Image
from PIL import ImageTk
#For image scaling

musicplayer = tkinter.Tk()
#Launch our musicplayer screen
musicplayer.title("Bduck Music Player")
#Title the music player's screen
musicplayer.geometry("1920x1080")
#Dimensions
#musicplayer.configure(bg="black")
mixer.init()
pygame.init()
#Initialize Mixer and Pygame


playlist = tkinter.Listbox(musicplayer, font="Arial 12 bold", bg="black", fg="yellow", width=20, height=30)
#Make our Playlist


def PlayTime():
#Playtime variables
    if stopped:
        return
#If the music is stopped just return as nothing
    currentsong = playlist.curselection()
#Get the current song
    song = playlist.get(currentsong)
#The song would be the current song playing
    songmut = MP3(song)
#Get the song
    global songlength
    songlength = songmut.info.length
#Global variable of songlength and get the length of the song
    currenttime = round(mixer.music.get_pos() / 1000)
#Round the time of the music so it appears as an integer and divide by 1000 to display in seconds
    currenttime = currenttime + 1
#Pygame error: adding 1 to fix the current time glitch
    convertedcurrentsonglength = time.strftime('%M:%S', time.gmtime(songlength))
#Convert the songlength into minutes and seconds
    if int(songslider.get()) == int(currenttime):
        #slider hasnt moved
        sliderposition = int(songlength)
        #the slider position is where the songlength is
        songslider.config(to=sliderposition, value=int(currenttime))
        #set the song slider's max position to to the song length and the value should be the current time
        statusbar.config(text=f'Time Elapsed: {currenttime} of {convertedcurrentsonglength}')
        #Set the status bar to the current time and the song length
    elif paused:
        pass
    #if its paused, just pass or do nothing
    else:
        sliderposition = int(songlength)
        #Slider position length of the song
        songslider.config(to=sliderposition, value=int(songslider.get()))
        #if the slider has been moved set the slider's max position to the song length and the value or position of the slider should be where it was moved to
        convertedcurrentsongtime = time.strftime('%M:%S', time.gmtime(int(songslider.get())))
        #Convert the current position of the slider to minutes and seconds
        songsliderlabel.config(text=f'Time Elapsed: {convertedcurrentsongtime} of {convertedcurrentsonglength}')
        #Change the song slider label
        statusbar.config(text=f'Time Elapsed: {convertedcurrentsongtime} of {convertedcurrentsonglength}')
        #set the status bar
        nexttime = int(songslider.get()) + 1
        #Increase the songslider by 1
        songslider.config(value=nexttime)
    #Keep increasing the value by 1


    statusbar.after(1000, PlayTime)
#After 1000 miliseconds, update the playtime by 1


def SlideSong(x):
    #Slider manipulation
    song = playlist.get(ACTIVE)
    mixer.music.load(song)
    mixer.music.play(loops=0, start=int(songslider.get()))
    #Get the song then when it plays, start the song slider
def AddSongs():
    directory = filedialog.askdirectory()
    path = filedialog.askdirectory()
    if path:
        os.chdir(directory)
        songlist = os.listdir(path)
        playlist.grid(columnspan=5)
        for songs in songlist:
            if songs.endswith(".mp3"):
                playlist.insert(END, songs)
global stopped
stopped = False
#Make a global variable called stopped
#Global = can be called from anywhere
def Stop():
    statusbar.config(text='')
    #Make the statusbar nothing if it's stopped
    songslider.config(value=0)
    #Make the song slider back to 0
    pygame.mixer.music.stop()
    #Stop the music
    global stopped
    stopped = True
    #Make the global variable stopped, True
global paused
paused = False
#Global pause variable
def Pause(ispaused):
    #ispaused is just a parameter that will be passed to use the pause variable
    global paused
    paused = ispaused
    #call pause and make it the parameter ispaused
    if paused:
        mixer.music.unpause()
        paused = False
    #if the song is already paused, unpause it
    else:
        mixer.music.pause()
        paused = True
    #If the song isn't already paused, pause it
def NextSong():
    statusbar.config(text='')
    songslider.config(value=0)
    #Once a next song has been played, reset everything
    nextsong = playlist.curselection()
    #Get the current selection
    print(playlist.curselection())
    #Print to test
    nextsong = nextsong[0] + 1
    #We need to call the number of the song playing
    #Since it is stored in a list such as (0, song.mp3) we need to call the number to add it by 1
    song = playlist.get(nextsong)
    #Song would be the nextsong
    mixer.music.load(song)
    #Load the next song
    mixer.music.play(loops=0)
    #Play the next song
    playlist.selection_clear(0, END)
    playlist.activate(nextsong)
    playlist.select_set(nextsong)
    # Clear the selection then activate the next song, making sure that next song has a new number
def PreviousSong():
    statusbar.config(text='')
    songslider.config(value=0)
    #Once the button has been clicked, make the slider and its value 0
    lastsong = playlist.curselection()
    #Get the current selection of the song
    print(playlist.curselection())
    #Print to test
    lastsong = lastsong[0] - 1
    #Last song's 1st value or the number would be minused by 1 or reversed
    song = playlist.get(lastsong)
    #Get the last song as the song
    print(song)
    print(lastsong)
    pygame.mixer.music.load(song)
    #Load the song
    pygame.mixer.music.play(loops=0)
    playlist.selection_clear(0, END)
    playlist.activate(lastsong)
    playlist.select_set(lastsong)
    #Clear the selection then make sure the last song's number
    #is what is active so that it starts at another number than 0 next time you get the current selection
def Play():
    global stopped
    #Global stopped variable
    stopped = False
    musicname = playlist.get(ACTIVE)
    #Music name would be the the active song when play is clicked
    print(musicname[0:-4])
    mixer.music.load(playlist.get(ACTIVE))
    #Load the active song
    mixer.music.play(loops=0)
    #Play it with 0 loops
    PlayTime()
    #Run playtime function to track playtime
    songtitle.config(text=f'Current Song Playing: \n{musicname}')
def Volume(x):
    mixer.music.set_volume(volumeslider.get())
    #The volume would be set to wherever the volume slider is
    roundedvolume = round(volumeslider.get(), 2)
    #Round the volume to two decimal places
    roundedvolume = int(roundedvolume * 100)
    #Times it by 100 to get a 1-100 scale
    volumesliderlabel.config(text=roundedvolume)
    #Adjust the slider label to the rounded volume
    print(roundedvolume)
    #Outputs volume



songtitle = tkinter.Label(musicplayer, font="Helvetica, 20", text='Current Song Playing: ', )

songtitle.place(anchor='center', relx=0.5, rely=0.5)

playimage = Image.open('playbutton.png')
playimage = playimage.resize((100, 100))
playimage = ImageTk.PhotoImage(playimage)
playbutton = Button(musicplayer, image=playimage, command=Play, borderwidth=0,) #background="black"
playbutton.grid(row=1, column=0)
playbutton.place(anchor='s', relx=0.5, rely=0.825)

pauseimage = Image.open('pausebutton.png')
pauseimage = pauseimage.resize((100, 100))
pauseimage = ImageTk.PhotoImage(pauseimage)
pausebutton = Button(musicplayer, image=pauseimage, command=lambda: Pause(paused), borderwidth=0)
pausebutton['font'] = "Arial"
pausebutton.place(anchor='s', relx=0.62, rely=0.825)

menu = Menu(musicplayer)
musicplayer.config(menu=menu)
addsongsmenu = Menu(menu)
menu.add_cascade(label="Add Songs", menu=addsongsmenu)
addsongsmenu.add_command(label="Add one song", command=AddSongs)

skipimage = Image.open("forwardbutton.png")
skipimage = skipimage.resize((100, 100))
skipimage = ImageTk.PhotoImage(skipimage)
skipsongbutton = Button(musicplayer, command=NextSong, image=skipimage, borderwidth=0) #background="black")
skipsongbutton['font'] = "Arial"
skipsongbutton.grid(row=1, column=0)
skipsongbutton.place(anchor='s', relx=0.56, rely=0.825)

lastsongimage = Image.open("backwardbutton.png")
lastsongimage = lastsongimage.resize((100, 100))
lastsongimage = ImageTk.PhotoImage(lastsongimage)
lastsongbutton = Button(musicplayer, text="Last Song", command=PreviousSong, image=lastsongimage, borderwidth=0,)# background="black")
lastsongbutton['font'] = "Arial"
lastsongbutton.grid(row=1, column=0)
lastsongbutton.place(anchor='s', relx=0.44, rely=0.825)

statusbar = Label(musicplayer, text='', borderwidth=0, relief=GROOVE)
statusbar.place(relx=1.0, rely=1.0, anchor='se')

baseframe = Frame(musicplayer)

songslider = ttk.Scale(musicplayer, from_=0, to=100, orient=HORIZONTAL, value=0, length=400, command=SlideSong,)
songslider.place(relx=0.5, rely=0.9, anchor='s')

volumeslider = ttk.Scale(musicplayer, from_=0, to=1, orient=VERTICAL, value=1, length=400, command=Volume)
volumeslider.place(relx=0.9, rely=0.86, anchor='s')
volumesliderlabel = Label(text="100")
volumesliderlabel.place(relx=0.9, rely=0.9, anchor='s')

songsliderlabel = Label(text="Time Elapsed: 0:0 of Song Length: 0:0 ")
songsliderlabel.place(relx=0.5, rely=0.92, anchor="s")


musicplayer.mainloop()
