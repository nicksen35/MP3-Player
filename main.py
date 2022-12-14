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
import random

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


playlist = tkinter.Listbox(musicplayer, font="Arial 12 bold", bg="black", fg="white", width=20, height=30)
#Make our Playlist

global paused
paused = False
#Global pause function. Will Use later

def AddSongs():
    directory = filedialog.askdirectory()
    path = filedialog.askdirectory()
    #ask for the path
    #position variable to determine song's position
    global position
    position = 0
    if path:
        #If the path has been found
        os.chdir(directory)
        global songlist
        songlist = os.listdir(path)
        #Song list is the directory of the path
        playlist.grid(columnspan=5)
        #Make the grid with a column span of 5
        playlist.delete(0, END)
        for songs in songlist:
            if songs.endswith(".mp3"):
                #If the song ends with mp3
                playlist.insert(position, songs)
                position = position + 1
                playlist.select_clear(0, END)
                playlist.select_set(0)
                #Insert the song at the position then add the position by 1
def Play():
    try:
        global paused
        if paused == True:
            mixer.music.unpause()
            paused = False
        statusbar.config(text='')
        songslider.config(value=0)
        musicname = playlist.get(ACTIVE)
        #Music name would be the the active song when play is clicked
        mixer.music.load(playlist.get(ACTIVE))
        #Load the active song
        mixer.music.play(loops=0)
        #Play it with 0 loops
        PlayTime()
        #Run playtime function to track playtime
        songtitle.config(text=f'Current Song Playing: \n{musicname}')
    except:
        pass
def shuffle():
    try:
        playlist.delete(0, END)
        #Delete all the values in the playlist
        for songs in songlist:
            #For every song in the directory
            randomposition = random.choice(range(0, position))
            #Randomly generate a value from the range 0 to the amount of songs
            playlist.insert(randomposition, songs)
        playlist.select_clear(0, END)
        playlist.activate(0)
        playlist.select_set(0)
            #Insert the new shuffled songs
    except:
        pass

def PlayTime():
    try:
    #Get the current song
        song = playlist.get(ACTIVE)
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
            convertedcurrentsongtime = time.strftime('%M:%S', time.gmtime(int(currenttime)))
            #set the song slider's max position to to the song length and the value should be the current time
            statusbar.config(text=f'Time Elapsed: {convertedcurrentsongtime} of {convertedcurrentsonglength}')
            songsliderlabel.config(text=f'Time Elapsed: {convertedcurrentsongtime} of {convertedcurrentsonglength}')
            #Set the status bar to the current time and the song length
            if currenttime >= songlength:
                NextSong(hasbeenqueued=False)
                #If the time has equalled the songlength, then go to the next song
        elif paused:
            pass
        #if its paused, just pass or do nothing
        else:
            songslider.config(to=int(songlength), value=int(songslider.get()))
            #if the slider has been moved set the slider's max position to the song length and the value or position of the slider should be where it was moved to
            convertedcurrentsongtime = time.strftime('%M:%S', time.gmtime(int(songslider.get())))
            #Convert the current position of the slider to minutes and seconds
            songsliderlabel.config(text=f'Time Elapsed: {convertedcurrentsongtime} of {convertedcurrentsonglength}')
            #Change the song slider label
            statusbar.config(text=f'Time Elapsed: {convertedcurrentsongtime} of {convertedcurrentsonglength}')
            #set the status bar
            adjustslidervalue = int(songslider.get()) + 1
            #Increase the songslider by 1
            songslider.config(value=adjustslidervalue)
            if songslider.get() >= int(songlength):
                NextSong(hasbeenqueued=False)
        #Keep increasing the value by 1
        statusbar.after(1000, PlayTime)
    except:
        pass
    #After 1000 miliseconds, update the playtime by 1
global songqueued
#Global song queued
songqueued = False
#Make the variable false



def QueueSong():
    global songqueued
    songqueued = True
    #Make songqueued true
    global queuedsong
    queuedsong = playlist.get(ACTIVE)
    #Declare a global variable called queuedsong so that the song can be called from the nextsong function
    return songqueued
#Return the queued song so that we can call it from the NextSong() Function


def SlideSong(x):
    try:
        #Slider manipulation
        song = playlist.get(ACTIVE)
        mixer.music.load(song)
        mixer.music.play(loops=0, start=int(songslider.get()))
        #Get the song then when it plays, start the song slider
    except:
        pass




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



def NextSong(hasbeenqueued):
    global paused
    global songqueued
    songqueued = hasbeenqueued
    if songqueued:
        if paused == True:
            mixer.music.unpause()
            paused = False
        songqueued = False
        #If there is a song queued
        statusbar.config(text='')
        songslider.config(value=0)
        PlayTime()
        #Reset the slider values to 0
        mixer.music.load(queuedsong)
        #Load the queue song
        mixer.music.play(loops=0)
        #Play the queued song
        songtitle.config(text=f'Current Song:   \n{queuedsong}')
        #Config the text to display the current song
        song = playlist.curselection()
        #Get the song as the current selection
        playlist.selection_clear(0, END)
        playlist.activate(song)
        playlist.select_set(song)

        #Clear the song selection activate the new song and then select the song

    else:
        try:
            if paused == True:
                mixer.music.unpause()
                paused = False
            statusbar.config(text='')
            songslider.config(value=0)
            #Once a next song has been played, reset everything
            nextsong = playlist.curselection()
            #Get the current selection
            nextsong = nextsong[0] + 1
            #We need to call the number of the song playing
            #Since it is stored in a list such as (0, song.mp3) we need to call the number to add it by 1
            song = playlist.get(nextsong)
            songtitle.config(text=f'Current Song: \n{song}')
            #Song would be the nextsong
            mixer.music.load(song)
            #Load the next song
            mixer.music.play(loops=0)
            #Play the next song
            playlist.selection_clear(0, END)
            playlist.activate(nextsong)
            playlist.select_set(nextsong)
            # Clear the selection then activate the next song, making sure that next song has a new number
        except:
            #If an error occurs, go to the previous song
            PreviousSong()
def PreviousSong():
    try:
        global paused
        if paused == True:
            mixer.music.unpause()
            paused = False
        #Try to run this
        statusbar.config(text='')
        songslider.config(value=0)
        #Once the button has been clicked, make the slider and its value 0
        lastsong = playlist.curselection()
        #Get the current selection of the song
        lastsong = lastsong[0] - 1
        #Last song's 1st value or the number would be minused by 1 or reversed
        song = playlist.get(lastsong)
        songtitle.config(text=f'Current Song: \n{song}')
        #Get the last song as the song
        pygame.mixer.music.load(song)
        #Load the song
        pygame.mixer.music.play(loops=0)
        #Play the song with 0 loops
        playlist.selection_clear(0, END)
        playlist.activate(lastsong)
        playlist.select_set(lastsong)
        #Clear the selection then make sure the last song's number
        #is what is active so that it starts at another number than 0 next time you get the current selection
    except:
        #If there is an erorr, play next song
        NextSong(hasbeenqueued=False)

def Volume(x):
    mixer.music.set_volume(volumeslider.get())
    #The volume would be set to wherever the volume slider is
    roundedvolume = round(volumeslider.get(), 2)
    #Round the volume to two decimal places
    roundedvolume = int(roundedvolume * 100)
    #Times it by 100 to get a 1-100 scale
    volumesliderlabel.config(text=roundedvolume)
    #Adjust the slider label to the rounded volume



songtitle = tkinter.Label(musicplayer, font="Helvetica, 20", text='Current Song Playing: ', )
#Title of the label with says the song title

songtitle.place(anchor='center', relx=0.5, rely=0.5)
#Place the song title

playimage = Image.open('playbutton.png')
#Open the play image
playimage = playimage.resize((100, 100))
#Resize the play image
playimage = ImageTk.PhotoImage(playimage)
#Make the play image a photo that is accessible by tkinter
playbutton = Button(musicplayer, image=playimage, command=Play, borderwidth=0,)
#Makes the play button which is a tkinter button inside the music player and has the image of our play image
#Command is our play command
playbutton.place(anchor='s', relx=0.5, rely=0.825)
#Anchor the playbutton to the south and get the relative x position to be at 0.5 or halfway
#Relative y would be 0.825

pauseimage = Image.open('pausebutton.png')
#Open pause image
pauseimage = pauseimage.resize((100, 100))
#Resize Pause Image
pauseimage = ImageTk.PhotoImage(pauseimage)
#Make pause image photo that is accessible by tkinter
pausebutton = Button(musicplayer, image=pauseimage, command=lambda: Pause(paused), borderwidth=0)
#Pause button would have the image of a pause button
#Lambda allows us to have multiple pieces of data
pausebutton.place(anchor='s', relx=0.67, rely=0.825)
#Place the playbutton towards the south at a relative x of 0.67 and a relative y of 0.825

menu = Menu(musicplayer)
#Make the Menu for our music player (dropdown)
musicplayer.config(menu=menu)
#Add our menu to the music player
addsongsmenu = Menu(menu)
#Add songs menu would be our menu
menu.add_cascade(label="Add Songs", menu=addsongsmenu)
#Add bar that says "Add Songs"
addsongsmenu.add_command(label="Add a playlist", command=AddSongs)
#Drop down commands would be "Add a playlist"

skipimage = Image.open("forwardbutton.png")
#Open the skip image
skipimage = skipimage.resize((100, 100))
#Resize the skip image
skipimage = ImageTk.PhotoImage(skipimage)
#Load the skipimage as a tkinter image
skipsongbutton = Button(musicplayer, command=lambda:NextSong(songqueued), image=skipimage, borderwidth=0)
#Button the skip button and have the image be the skip image and the command be to skip to the next song
skipsongbutton.place(anchor='s', relx=0.58, rely=0.825)
#Place the skip song button towards the south with a relative x position of 0.58 and a relative y position of 0.825

lastsongimage = Image.open("backwardbutton.png")
#Open the last song image
lastsongimage = lastsongimage.resize((100, 100))
#Resize the last song image
lastsongimage = ImageTk.PhotoImage(lastsongimage)
#Load the last song image as a tkinter image
lastsongbutton = Button(musicplayer, command=PreviousSong, image=lastsongimage, borderwidth=0,)# background="black")
#Make a button in the music player has the lastsong image and commands to go to the previous song
lastsongbutton.place(anchor='s', relx=0.42, rely=0.825)
#Place the last song button at the south with a relative x position of 0.42 and a relative y position of 0.825

queuebuttonimage = Image.open("queuebutton.png")
#Open queue button image
queuebuttonimage = queuebuttonimage.resize((100, 100))
queuebuttonimage = ImageTk.PhotoImage(queuebuttonimage)
queuebutton= Button(musicplayer, command=QueueSong, image=queuebuttonimage, borderwidth=0)
#Make a queue button with the image of the queue button image and the command of queue song
queuebutton.place(anchor='s', relx=0.33, rely=0.825)
#Place the queue button towards the south with a relative x position of 0.35 and a relative y position of 0.825

shufflebuttonimage = Image.open("shufflebutton.png")
shufflebuttonimage = shufflebuttonimage.resize((100, 100))
shufflebuttonimage = ImageTk.PhotoImage(shufflebuttonimage)
shufflebutton = Button(musicplayer, borderwidth=0, command=shuffle, image=shufflebuttonimage)
#Make a shuffle button with the image of the shuffle image and the command of shuffle
shufflebutton.place(anchor='s', relx=0.24, rely=0.825)
#Place the shuffle button towards the south with a relative x position of 0.3 and a relative y position of 0.825

statusbar = Label(musicplayer, text='', borderwidth=0, relief=GROOVE)
#Make a label for the status bar with text that we manipulated using a function and a relief of groove
statusbar.place(relx=1.0, rely=1.0, anchor='se')
#Place the status bar at the bottom right corner


songslider = ttk.Scale(musicplayer, from_=0, to=100, orient=HORIZONTAL, value=0, length=400, command=SlideSong)
#Create a slider to slide the music along with a lenght of 400 and a value of 1-100
songslider.place(relx=0.5, rely=0.9, anchor='s')
#Place the song slider in the middle and at the bottom
volumeslider = ttk.Scale(musicplayer, from_=0, to=1, orient=VERTICAL, value=1, length=400, command=Volume)
#Make a volume slider that is vertical and has a value of 0-1
volumeslider.place(relx=0.9, rely=0.86, anchor='s')
#Place the volume slider left of the song slider
volumesliderlabel = Label(text="100")
#Make the volume slider label 100 to represent max volume
volumesliderlabel.place(relx=0.9, rely=0.9, anchor='s')
#Place the volume slider label right below the slider

songsliderlabel = Label(text="Time Elapsed: 00:00 of Song Length: 00:00 ")
#Make a song slider label showing the time elapsed and song length
songsliderlabel.place(relx=0.5, rely=0.92, anchor="s")
#Place that below the slider


musicplayer.mainloop()
