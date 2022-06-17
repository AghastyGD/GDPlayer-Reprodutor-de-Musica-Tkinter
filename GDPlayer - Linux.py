'''
GDPlayer (Reprodutor de Música) - Tkinter + PyGame 
Autor: Augusto Domingos (Aghasty GD)
Data de Ínicio: 1 de Maio de 2022
Última actualização: 31 de Maio de 2022

'''

import os
import threading
import time
import tkinter.messagebox
from tkinter import *
from tkinter import filedialog
import webbrowser
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from mutagen.mp3 import MP3
from pygame import mixer

pastaApp1 = os.path.dirname(__file__)

root = ttk.Window(themename="superhero")

statusbar = ttk.Label(root, text="Bem vindo ao GDPlayer", relief=SUNKEN, anchor=W, font='Times 10 italic')
statusbar.pack(side=BOTTOM, fill=X)

# Cria a barra de menu
menubar = Menu(root)
root.config(menu=menubar)

# Cria o submenu

subMenu = Menu(menubar, tearoff=0)

playlist = []


# playlist - contém o caminho completo e o nome do arquivo
# playlistbox - contém apenas o nome do arquivo
# Fullpath + filename é necessário para reproduzir a música durante a função play_music 

def browse_file():
    global filename_path
    filename_path = filedialog.askopenfilename()
    add_to_playlist(filename_path)

    mixer.music.queue(filename_path)


def add_to_playlist(filename):
    filename = os.path.basename(filename)
    index = 0
    playlistbox.insert(index, filename)
    playlist.insert(index, filename_path)
    index += 1


menubar.add_cascade(label="Arquivo", menu=subMenu)
subMenu.add_command(label="Abrir", command=browse_file)
subMenu.add_command(label="Sair", command=root.destroy)


def about_us():
    tkinter.messagebox.showinfo('Sobre GDPlayer', 'Este é um player de música desenvolvido por @AghastyGD')


subMenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Ajuda", menu=subMenu)
subMenu.add_command(label="Sobre Nós", command=about_us)
subMenu.add_command(label="Portfólio", command=lambda: webbrowser.open("https://augustodomingos.netlify.app/"))

mixer.init()  # Iniciando o Reprodutor

root.title("GDPlayer")
root.tk.call('wm', 'iconphoto', root._w, ttk.PhotoImage(file= 'images/gd_player.png'))

# Root Window - StatusBar, LeftFrame, RightFrame
# LeftFrame - A lista das músicas (playlist)
# RightFrame - TopFrame,MiddleFrame e BottomFrame

leftframe = Frame(root)
leftframe.pack(side=LEFT, padx=30, pady=30)

playlistbox = Listbox(leftframe)
playlistbox.pack(ipadx=80, ipady=90)

addBtn = ttk.Button(leftframe, text="+ Adicionar", command=browse_file)
addBtn.pack(side=LEFT)


def del_song():
    selected_song = playlistbox.curselection()
    selected_song = int(selected_song[0])
    playlistbox.delete(selected_song)
    playlist.pop(selected_song)


delBtn = ttk.Button(leftframe, text="- Remover", bootstyle = DANGER, command=del_song)
delBtn.pack(side=RIGHT)

rightframe = Frame(root)
rightframe.pack(pady=30)

topframe = Frame(rightframe)
topframe.pack()

lengthlabel = ttk.Label(topframe, text='--:--')
lengthlabel.pack(padx = 200)

currenttimelabel = ttk.Label(topframe, text='--:--')
currenttimelabel.pack(padx = 20)


def show_details(play_song):
    file_data = os.path.splitext(play_song)

    if file_data[1] == '.mp3':
        audio = MP3(play_song)
        total_length = audio.info.length
    else:
        a = mixer.Sound(play_song)
        total_length = a.get_length()

    # div - total_length/60, mod - total_length % 60
    mins, secs = divmod(total_length, 60)
    mins = round(mins)
    secs = round(secs)
    timeformat = '{:02d}:{:02d}'.format(mins, secs)
    lengthlabel['text'] = "" + '' + timeformat

    t1 = threading.Thread(target=start_count, args=(total_length,))
    t1.start()


def start_count(t):
    global paused
    # mixer.music.get_busy(): - Retorna FALSE quando pressionamos o botão para parar.
    # Continue - Ignora todas as atribuições abaixo dela. Nós checamos se a música está em pausa ou não.
    current_time = 0
    while current_time <= t and mixer.music.get_busy():
        if paused:
            continue
        else:
            mins, secs = divmod(current_time, 60)
            mins = round(mins)
            secs = round(secs)
            timeformat = '{:02d}:{:02d}'.format(mins, secs)
            currenttimelabel['text'] = "" + '' + timeformat
            time.sleep(1)
            current_time += 1


def play_music():
    global paused

    if paused:
        mixer.music.unpause()
        statusbar['text'] = "Reproduziu a Música"
        paused = FALSE
    else:
        try:
            stop_music()
            time.sleep(1)
            selected_song = playlistbox.curselection()
            selected_song = int(selected_song[0])
            play_it = playlist[selected_song]
            mixer.music.load(play_it)
            mixer.music.play()
            statusbar['text'] = "Reproduzindo: " + os.path.basename(play_it)
            show_details(play_it)
        except:
            tkinter.messagebox.showerror('Arquivo não encontrado', 'GD Player não encontrou o arquivo. Por favor, tente de novo.')


def stop_music():
    mixer.music.stop()
    statusbar['text'] = "Parou a Música"


paused = FALSE


def pause_music():
    global paused
    paused = TRUE
    mixer.music.pause()
    statusbar['text'] = "Pausou a Música"


def rewind_music():
    play_music()
    statusbar['text'] = "Reiniciou a Música"


def set_vol(val):
    volume = float(val) / 100
    mixer.music.set_volume(volume)
    # define_volume do mixer obtendo um valor de 0 a 1. Exemplo - 0, 0.1,0.55,0.54.0.99,1


muted = FALSE


def mute_music():
    global muted
    if muted:  # Restaura o áudio
        mixer.music.set_volume(0.7)
        volumeBtn.configure(image=volumePhoto)
        scale.set(70)
        muted = FALSE
    else:  # Desativa o aúdio
        mixer.music.set_volume(0)
        volumeBtn.configure(image=mutePhoto)
        scale.set(0)
        muted = TRUE


middleframe = Frame(rightframe)
middleframe.pack(pady=30, padx=30)

playPhoto = PhotoImage(file= pastaApp1 +'//images//play.png')
playBtn = ttk.Button(middleframe, image=playPhoto, bootstyle = DARK, command=play_music)
playBtn.grid(row=0, column=0, padx=10)

stopPhoto = PhotoImage(file= pastaApp1 +'//images//stop.png')
stopBtn = ttk.Button(middleframe, image=stopPhoto, bootstyle = DARK, command=stop_music)
stopBtn.grid(row=0, column=1, padx=10)

pausePhoto = PhotoImage(file= pastaApp1 +'//images//pause.png')
pauseBtn = ttk.Button(middleframe, image=pausePhoto, bootstyle = DARK, command=pause_music)
pauseBtn.grid(row=0, column=2, padx=10)

# Bottom Frame para volume, recomeçar, silencio etc.

bottomframe = Frame(rightframe)
bottomframe.pack()

rewindPhoto = PhotoImage(file= pastaApp1 + '//images//rewind.png')
rewindBtn = ttk.Button(bottomframe, image=rewindPhoto, bootstyle = DARK, command=rewind_music)
rewindBtn.grid(row=0, column=0)

mutePhoto = PhotoImage(file= pastaApp1 + '//images//mute.png')
volumePhoto = PhotoImage(file= pastaApp1 + '//images//volume.png')
volumeBtn = ttk.Button(bottomframe, image=volumePhoto, bootstyle = DARK, command=mute_music)
volumeBtn.grid(row=0, column=1)

scale = ttk.Scale(bottomframe, from_=0, to=100, orient=HORIZONTAL, command=set_vol)
scale.set(70) # Implementa o valor padrão da escala quando a música começa               
mixer.music.set_volume(0.7)
scale.grid(row=0, column=2, pady=15, padx=30)


def on_closing():
    stop_music()
    root.destroy()


root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
