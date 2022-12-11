from pygame import mixer
import pygame
from tkinter import *
import tkinter.font
from tkinter import filedialog
import os
import time
from mutagen.mp3 import MP3
import tkinter.ttk as ttk
from PIL import Image
from PIL import ImageTk

print("Hello world")
musicplayer = tkinter.Tk()
musicplayer.title("Bduck Music Player")
musicplayer.geometry("1920x1080")
musicplayer.configure(bg="black")
mixer.init()
pygame.init()
isRunning = True

playlist = tkinter.Listbox(musicplayer, font="Arial 12 bold", bg="black", fg="yellow", selectmode=tkinter.SINGLE, width=20, height=30)


def PlayTime():
    if stopped:
        return
    currentsong = playlist.curselection()
    song = playlist.get(currentsong)
    songmut = MP3(song)
    global songlength
    songlength = songmut.info.length
    currenttime = round(mixer.music.get_pos() / 1000)
    currenttime = currenttime + 1
    convertedcurrentsonglength = time.strftime('%M:%S', time.gmtime(songlength))
    if int(songslider.get()) == int(currenttime):
        #slider hasnt moved
        sliderposition = int(songlength)
        songslider.config(to=sliderposition, value=int(currenttime))
        statusbar.config(text=f'Time Elapsed: {currenttime} of {convertedcurrentsonglength}')
    elif paused:
        pass
    else:
        #slider moved
        sliderposition = int(songlength)
        songslider.config(to=sliderposition, value=int(songslider.get()))
        sliderlabel.config(text=f'Slider{int(songslider.get())} and Song Pos {int(currenttime)}')
        convertedcurrentsongtime = time.strftime('%M:%S', time.gmtime(int(songslider.get())))
        statusbar.config(text=f'Time Elapsed: {convertedcurrentsongtime} of {convertedcurrentsonglength}')
        nexttime = int(songslider.get()) + 1
        songslider.config(value=nexttime)


    statusbar.after(1000, PlayTime)



def SlideSong(x):
    #sliderlabel.config(text=f'{int(songslider.get())} of {int(songlength)}')
    song = playlist.get(ACTIVE)
    mixer.music.load(song)
    mixer.music.play(loops=0, start=int(songslider.get()))
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
def Stop():
    statusbar.config(text='')
    songslider.config(value=0)
    pygame.mixer.music.stop()
    global stopped
    stopped = True
global paused
paused = False

def Pause(ispaused):
    global paused
    paused = ispaused
    if paused:
        mixer.music.unpause()
        paused = False
    else:
        mixer.music.pause()
        paused = True
def NextSong():
    statusbar.config(text='')
    songslider.config(value=0)
    nextsong = playlist.curselection()
    print(playlist.curselection())
    nextsong = nextsong[0] + 1
    song = playlist.get(nextsong)
    print(song)
    print(nextsong)
    mixer.music.load(song)
    mixer.music.play(loops=0)
    playlist.selection_clear(0, END)
    playlist.activate(nextsong)
    playlist.select_set(nextsong)
def PreviousSong():
    statusbar.config(text='')
    songslider.config(value=0)
    lastsong = playlist.curselection()
    print(playlist.curselection())
    lastsong = lastsong[0] - 1
    song = playlist.get(lastsong)
    print(song)
    print(lastsong)
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    playlist.selection_clear(0, END)
    playlist.activate(lastsong)
    playlist.select_set(lastsong)
def Play():
    global stopped
    stopped = False
    global played
    played = True
    musicname = playlist.get(ACTIVE)
    print(musicname[0:-4])
    mixer.music.load(playlist.get(ACTIVE))
    mixer.music.play(loops=0)
    PlayTime()
var = tkinter.StringVar()
songtitle = tkinter.Label(musicplayer, font="Arial", textvariable=var)

playimage = Image.open('playbutton.png')
playimage = playimage.resize((100, 100))
playimage = ImageTk.PhotoImage(playimage)
playbutton = Button(musicplayer, image=playimage, command=Play, borderwidth=0, background="black")
playbutton.grid(row=1, column=0)
playbutton.place(anchor='s', relx=0.5, rely=0.825)

pauseimage = Image.open('pausebutton.png')
pauseimage = pauseimage.resize((100, 100))
pauseimage = ImageTk.PhotoImage(pauseimage)
pausebutton = Button(musicplayer, text="Pause", width =6, command=lambda: Pause(paused))
pausebutton['font'] = "Arial"
pausebutton.grid(row=1, column=1)

menu = Menu(musicplayer)
musicplayer.config(menu=menu)
addsongsmenu = Menu(menu)
menu.add_cascade(label="Add Songs", menu=addsongsmenu)
addsongsmenu.add_command(label="Add one song", command=AddSongs)

skipimage = Image.open("forwardbutton.png")
skipimage = skipimage.resize((100, 100))
skipimage = ImageTk.PhotoImage(skipimage)
skipsongbutton = Button(musicplayer, command=NextSong, image=skipimage, borderwidth=0, background="black")
skipsongbutton['font'] = "Arial"
skipsongbutton.grid(row=1, column=0)
skipsongbutton.place(x=750, y=500)

lastsongimage = Image.open("backwardbutton.png")
lastsongimage = lastsongimage.resize((100, 100))
lastsongimage = ImageTk.PhotoImage(lastsongimage)
lastsongbutton = Button(musicplayer, text="Last Song", command=PreviousSong, image=lastsongimage, borderwidth=0, background="black")
lastsongbutton['font'] = "Arial"
lastsongbutton.grid(row=1, column=0)
lastsongbutton.place(x=510, y=500)

statusbar = Label(musicplayer, text='', borderwidth=0, relief=GROOVE)
statusbar.place(relx=1.0, rely=1.0, anchor='se')

songslider = ttk.Scale(musicplayer, from_=0, to=100, orient=HORIZONTAL, value=0, length=400, command=SlideSong, )
songslider.place(relx=0.5, rely=0.94, anchor='s')

sliderlabel = Label(text="0")
sliderlabel.place(relx=0.5, rely=0.96, anchor="s")
musicplayer.mainloop()
