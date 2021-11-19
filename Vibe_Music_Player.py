import tkinter
from tkinter import *
import pygame
from PIL import Image,ImageTk
from tkinter.ttk import Progressbar,Style,Scale
import os
from datetime import datetime, timedelta
from pygame import *
from tkinter import filedialog
import shutil
location=r'C:\Music System'
if not os.path.exists(location):
    os.makedirs(location)

tracks=[os.path.abspath(i) for i in os.scandir('C:\Music System/')]
track_names=[" "+i.name for i in (os.scandir('C:\Music System/'))]
if not tracks:
    track_names.append("No Audio present.")
    # tracks.append("")
play_tracks={x:y for x,y in zip(track_names,tracks)}

window=Tk()
width=800
height=637
window.geometry(f"{width}x{height}")
window.title("Vibe Music Player")
vibe_icon=Image.open('VIBE 2.png')
vibe_icon=vibe_icon.resize((100,100))
vibe_icon=ImageTk.PhotoImage(vibe_icon)
window.iconphoto(False,vibe_icon)
mixer.init()
v=0
export_audio=''
track_position=0
window.resizable(0,0)
clock=2
now=datetime.now()
def repo(time):
    hours=int(time)//3600
    time%=3600
    mins=int(time)//60
    time%=60
    secs=int(time)
    return str(hours),str(mins),str(secs)

# def shift():
#     x1, y1, x2, y2 = now_playing.bbox("marquee")
#     if (x2 < 0 or y1 < 0):  # reset the coordinates
#         x1 = now_playing.winfo_width()
#         y1 = now_playing.winfo_height() // 2
#         canvas.coords("marquee", x1, y1)
#     else:
#         now_playing.move("marquee", -2, 0)
#     now_playing.after(1000 // fps, shift)
def progress(length):
    global v,clock,creator_label,now
    now=datetime.now()
    try:
        while mixer.music.get_busy():
            def redef():
                global clock
                if clock == 1:
                    creator_label.set('Created with love by\nAditya Johorey \nand Akib Hussain')
                    clock += 1
                elif clock == 2:
                    creator_label.set('Desgined for easy use\nby our valued listeners')
                    clock += 1
                elif clock == 3:
                    creator_label.set('Music that matches\n your vibes now in\nyour favorite player')
                    clock = 1
                window.update()
                return
            # print(f"{mixer.music.get_pos()}")
            progress_bar['value']=(mixer.music.get_pos()/(1000*length))*100
            hours,mins,secs=repo(mixer.music.get_pos()/1000)
            current_time.set(f"{hours.zfill(2)}:{mins.zfill(2)}:{secs.zfill(2)}")
            if datetime.now()>now+timedelta(minutes=0.166667):
                redef()
                now=datetime.now()
            if mixer.music.get_pos() >= length * 1000:
                v=1
                play_pause.config(image=start_image)
                play_pause.image=start_image
                song_list.selection_clear(0, END)
                window.update()
            else:
                play_pause.config(image=pause_image)
                play_pause.image = pause_image
                window.update()

            window.update()
    except tkinter.TclError:
        print("Break in progress line")
    except KeyboardInterrupt:
        print("Window is closed abruptly. Please restart the application")
        window.destroy()
def music_player(control=1):
    global play_pause_image,pause_image,start_image,song_duration,track_position,export_audio,clock
    # print(song_list.curselection())
    if control:
        try:
            audio=song_list.get(song_list.curselection())
            track_position = track_names.index(str(audio))
        except TclError:
            print('Unexpected input to the music player list')
        except ValueError:
            print('Not an audio selection')
            song_list.selection_clear(0,END)
    else:
        audio=track_names[track_position]
    export_audio=audio
    try:
        audio_stream = play_tracks[str(audio)]
    except KeyError:
        print('Wrong input to audio player')
    try:
        if audio_stream != '':

            mixer.music.load(audio_stream)
            mixer.music.play()
            play_pause.config(image=pause_image)
            play_pause.image=pause_image
            status.set("Now Playing:")
            print("Playing", audio)
            current_music.set(str(audio))

            song_duration = mixer.Sound(audio_stream).get_length()
            print("Duration:", song_duration, "s")
            song_list.selection_clear(0, END)
            song_list['bd']=0
            # if clock == 1:
            #     creator_label.set('Created with love by\nAditya Johorey \nand Akib Hussain')
            #     print('Label set to:' + 'Created with love by\nAditya Johorey \nand Akib Hussain', clock)
            #     clock += 1
            # elif clock == 2:
            #     creator_label.set('Desgined for easy use\nby our valued listeners')
            #     print('Label set to:' + 'Desgined for easy use\nby our valued listeners', clock)
            #     clock += 1
            # elif clock == 3:
            #     creator_label.set('Music that matches\n your vibes now in\nyour favorite player')
            #     print('Label set to:' + 'Music that matches\n your vibes now in\nyour favorite player', clock)
            #     clock = 1
            # window.update()
            progress(song_duration)

        else:
            print("No audio file present.")
    except pygame.error:
        print("Wrong file format. Please change its format to mp3 or wav or use any other audio")
        song_list.selection_clear(0, END)
    except UnboundLocalError:
        print('Please try some other audio file, or check the audio format, it should be eigther mp3 or wave file.')
        song_list.selection_clear(0, END)
    # if mixer.music.get_busy():
    #     play_pause_image.set(pause_image)
    # else:
    #     play_pause_image.set(start_image)

    try:
        window.update()
    except TclError:
        print("Application Closed abruptly. Pls ignore the above exception")
        print("""If the audio is still playing please shut all the windows and restart the app.""")
        mixer.music.stop()
        mixer.music.unload()
        status.set('')
        current_music.set('')
        current_time.set('00:00')

def rewinding():
    mixer.music.rewind()
    mixer.music.play()
    print("Music rewinded")
    play_pause.config(image=pause_image)
    play_pause.image = pause_image
    progress(song_duration)
def play_pause_actions():
    global play_pause_image,pause_image,start_image,v
    if mixer.music.get_busy():
        mixer.music.pause()
        play_pause.config(image=start_image)
        play_pause.image=start_image
        print("Music Paused")
        v=0
        # play_pause_image.set(start_image)
    elif v:
        rewinding()
        v=0
    else:
        mixer.music.unpause()
        if mixer.music.get_busy():
            play_pause.config(image=pause_image)
            play_pause.image=pause_image
            print("Music Unpaused")
            progress(song_duration)
        else :
            try:
                rewinding()
            except pygame.error:
                print("No audio file loaded. Please select an audio file")

    try:
        window.update()
    except tkinter.TclError:
        print("""Error in window updation.
It is being repaired.
In case of further errors please try the action again or restart the application. """)
        # window.update()
def prev_song():
    global track_position
    songsh.state=DISABLED
    if track_position==0:
        track_position=len(track_names)-1
    else:
        track_position-=1

    songsh.state=NORMAL
    try:
        music_player(0)
    except pygame.error:
        print("Error in loading the music. Please retry.")
    except KeyboardInterrupt:
        print("Invalid input to the player")

def next_song():
    global track_position
    songsh.state=DISABLED
    if track_position==len(track_names)-1:
        track_position=0
    else:
        track_position+=1

    songsh.state=NORMAL
    try:
        music_player(0)
    except error:
        print("Error in loading the music. Please retry.")
def stop_music():
    global v
    mixer.music.stop()
    play_pause.config(image=start_image)
    play_pause.image=start_image
    progress_bar['value']=0
    print("Music Stoped")
    v=1
def add_song():
    global tracks,track_names,play_tracks,listbox_values
    try:
        filename = filedialog.askopenfilename(initialdir="C:/",
                                              title="Select a File",
                                              filetypes=(("mp3 files",
                                                          "*.mp3*"),
                                                         ("wave files",
                                                          "*.wav*")), multiple=True)

    except shutil.Error:
        print("Transfer cancelled")
    if "No Audio present." in track_names:
        song_list.delete(0)
        tracks.clear()
        track_names.clear()
    if not type(filename) == tuple:
        filename = tuple(filename)
    for file in filename:
        shutil.move(file, location)
        tracks = [os.path.abspath(i) for i in os.scandir('C:\Music System/')]
        track_names = [" "+i.name for i in (os.scandir('C:\Music System/'))]
        play_tracks.clear()
        play_tracks = {x: y for x, y in zip(track_names, tracks)}
        song_list.delete(0,END)
        for x in track_names:
            song_list.insert(END,x)
            window.update()
        listbox_values.value=track_names
    print("location of songs : ",tracks)
    print("list of songs:",track_names)
    print("Dictionary:",play_tracks)
    window.update()
    return;
#-----------------------------Frame 2-------------------------------
frame2=Frame(window,bg="black",width=300,height=538)
frame2.grid(row=0,column=0)
frame2.pack_propagate(False)

logo=Image.open("VIBE 1.png")
logo=logo.resize((350,150))
logo=ImageTk.PhotoImage(logo)
vibe=Label(frame2,image=logo,bg="black")
vibe.image=logo
info_image=Image.open('i.png')
info_image=info_image.resize((30,30))
info_image=ImageTk.PhotoImage(info_image)

def key_vol_up(event):
    key_vol=vol_controls.get()
    if key_vol<100:
        vol_controls.set(key_vol+1)
        volume(key_vol+1)
def key_vol_down(event):
    key_vol=vol_controls.get()
    if key_vol>0:
        vol_controls.set(key_vol-1)
        volume(key_vol-1)


def enter_play_pause_rewind_stop(event):
    def disabling():
        songsh.state=DISABLED
    global v
    if (event.keysym).lower()=='p':
        play_pause_actions()
    elif (event.keysym).lower()=='r':
        rewinding()
    elif (event.keysym).lower()=='s':
        stop_music()
    elif (event.keysym)=='Left':
        print(event.keysym)
        songsh.state=DISABLED
        prev_song()
    elif (event.keysym)=='Right':
        print(event.keysym)
        songsh.state=DISABLED
        next_song()
    return;

def info(control=1):
    global vibe_icon,track_position,song_duration,counter

    if control and counter<1:
        try:
            def done():
                global counter
                print("Info page closed")
                counter-=1
                try:
                    root.destroy()
                except tkinter.TclError:
                    print('info page is closed')
        except tkinter.TclError:
            open=0
            print("The info page closed")

        def on_closing():
            global counter
            try:
                global open
                print('Info Page closed')
                counter-=1
                info_button.state = 'normal'
                root.destroy()
                root.update()
            except tkinter.TclError:
                open = 0

        root=Tk()
        # info_button.state='disabled'
        root.title('Vibe.Info')
        counter+=1
        root.iconphoto(False, PhotoImage(master=root,file='VIBE 2.png'))
        root.resizable(0, 0)
        print('Info page poped up')
        size=600
        root.geometry("600x600")
        info=Label(root,width=size,height=size,bg='black')
        vibes=Image.open('VibesInfo.png')
        vibes=vibes.resize((size,size))
        vibes=ImageTk.PhotoImage(master=info,image=vibes)
        info.config(image=vibes)
        info.pack()
        root.bind('<Control-Key-p>', enter_play_pause_rewind_stop)
        root.bind('<Control-Key-P>', enter_play_pause_rewind_stop)
        root.bind('<Control-Key-r>', enter_play_pause_rewind_stop)
        root.bind('<Control-Key-R>', enter_play_pause_rewind_stop)
        root.bind('<Control-Key-s>', enter_play_pause_rewind_stop)
        root.bind('<Control-Key-S>', enter_play_pause_rewind_stop)
        root.bind('<Control-Key-Left>', enter_play_pause_rewind_stop)
        root.bind('<Control-Key-Right>', enter_play_pause_rewind_stop)
        root.bind('<Shift-Key-Up>', key_vol_up)
        root.bind('<Shift-Key-Down>', key_vol_down)
        root.protocol("WM_DELETE_WINDOW", on_closing)
    else:
        print('Info window is already open')
        return;
    # try:
    #     audio = song_list.get(song_list.curselection())
    # except tkinter.TclError:
    #     print("Unable to track audio from list box, extracting it from the backup.")
    #     audio=export_audio
    # track_position = track_names.index(str(audio))
    # audio_stream = play_tracks[str(audio)]
    # song_duration = mixer.Sound(audio_stream).get_length()

    try:

        print("Duration:", song_duration, "s")
        song_list.selection_clear(0, END)
        song_list['bd'] = 0
        progress(song_duration)
        window.update()
    except tkinter.TclError:
        print('Info Page stoped responding.Please Close it if not Closed')
        done()
    except NameError:
        song_duration=0
    # root.protocol("WM_DELETE_WINDOW",done)


    try:
        root.mainloop()
    except KeyboardInterrupt:
        print("Main window closed without closing the info window.\nIf you want to further use the program please restart")
    except tkinter.TclError:
        print('info page closed abruptly')



# def control_info_window():
#     global open,song_duration
#     if open:
#         print('Info window is already open')
#         return;
#     else:
#         info()
#         open=0
#
#     try:
#         song_list.selection_clear(0, END)
#         song_list['bd'] = 0
#         progress(song_duration)
#
#         window.update()
#     # except tkinter.TclError:
#     #     print('Info Page stoped responding.Please Close it if not Closed')
#     #     done()
#     except NameError:
#         song_duration = 0
#     except tkinter.TclError:
#         print('Unable to clear the listbox selection')
#     # root.protocol("WM_DELETE_WINDOW",done)
#
#     # try:
#     #     root.mainloop()
#     # except KeyboardInterrupt:
#     #     print(
#     #         "Main window closed without closing the info window.\nIf you want to further use the program please restart")
#
counter=0
info_button=Button(frame2,image=info_image,bg='black',activebackground='black',borderwidth=0,command=info)
info_button.place(relx=0.07,rely=0.99,anchor='s')

options=['Home']
# clicked=StringVar()
# clicked.set("Playlist")
# playlist=OptionMenu(frame2,clicked,*options);
#
# playlist['width']=14
# playlist['height']=2
# playlist.config(bg="black",fg="yellow",
#                 activebackground='yellow',activeforeground='black',font=('calibre',25))
# playlist['menu'].config(bg='black',fg='yellow',
#                         activebackground='yellow',activeforeground="black",
#                         font=('calibre',15))
# playlist['highlightthickness']=0
#
# create_playlist=Button(frame2,text="Create new playlist",
#                        bg='yellow',font=('calibre',20,"normal"),
#                        activebackground="black",activeforeground="yellow")


add_music=Button(frame2,text='Add music',bg="yellow",
                 font=("calibre",20,"normal"),
                 activebackground='black',activeforeground="yellow",command=add_song)
add_music.pack(side=BOTTOM,pady=30)
# create_playlist.pack(side=BOTTOM,pady=(10,80))
# playlist.pack(side=BOTTOM)
creator_label=StringVar()
creator_label.set('Created with love by\nAditya Johorey \nand Akib Hussain')
creators=Label(frame2,textvariable=creator_label,bg='black',fg='yellow',
               font=('calibra',20,'normal'),height=5)
# vibe.place(relx=0.5,
#            rely=0.2,
#            anchor='center')
creators.pack(side=BOTTOM,pady=30)
vibe.pack(side=BOTTOM,pady=(0,14))
#----------------------------Frame 3--------------------------------
frame3=Frame(window,bg="white",width=500,height=538)
frame3.grid(row=0,column=1)
frame3.pack_propagate(False)
################### Search Box ###################
check={}

def update(access=0):
    global play_tracks, track_names, tracks
    tracks = [os.path.abspath(i) for i in os.scandir('C:\Music System/')]
    track_names = [" " + i.name for i in (os.scandir('C:\Music System/'))]
    if not tracks:
        track_names.append("No Audio present.")
        tracks.append("")
    play_tracks = {x: y for x, y in zip(track_names, tracks)}
    if not access:
        song_list.delete(0, END)
        # box.delete('1.0',END)
        for x in track_names:
            song_list.insert(END,x)
            window.update()
        listbox_values.value=track_names
        print("location of songs : ",tracks)
        print("list of songs:",track_names)
        print("Dictionary:",play_tracks)
        window.update()
def close():
    box.delete(0,'end')
    window.focus()
    print('Search Closed')
    update()
def find():
    global play_tracks,track_names,tracks
    print("Finding",end=" ")
    word=str(name.get())
    for i,j in zip(track_names,tracks):
        if i.lower().find(word.lower())>=0:
            check[i]=j
    print("'"+word+"'...")
    print(check)
    if len(check):
        track_names=[x for x in check.keys()]
        tracks=[x for x in check.values()]
    else:
        track_names=["Search not found"]
        tracks=['']

    print(track_names)
    print(tracks)
    play_tracks.clear()
    play_tracks = {x: y for x, y in zip(track_names, tracks)}
    print(play_tracks)
    song_list.delete(0, END)
    for x in track_names:
        song_list.insert(END, x)
        window.update()
    listbox_values.value = track_names
    window.update()

    # if check:
    #     message.set("Word Found")
    # else:
    #     message.set('Word not found')



    check.clear()
    update(1)
search_image=Image.open('Search Button.png')
close_image=Image.open('Close Button 1.png')
# close_image.putalpha(0)
search_image=search_image.resize((40,40))
search_image=ImageTk.PhotoImage(search_image)
close_image=close_image.resize((10,10))
close_image=ImageTk.PhotoImage(close_image)
# def update_close_image(flag=1):
#     global close_image
#     if flag:
#
#     else:

# def on_enter(event):
#     close_image=Image.open('Close Button 1.png')
#     close_image.putalpha(255)
#     close_image = close_image.resize((10, 10))
#     close_image = ImageTk.PhotoImage(close_image)
#     close_button.config(image=close_image, bg='yellow', activebackground="yellow")
#     close_button['image'] = close_image
#     window.update()
# def on_leave(event):
#     close_image = Image.open('Close Button 1.png')
#     close_image.putalpha(0)
#     close_image = close_image.resize((10, 10))
#     close_image = ImageTk.PhotoImage(close_image)
#     close_button.config(image=close_image, bg='yellow', activebackground="yellow")
#     close_button['image'] = close_image
#     window.update()
def on_enter(event):

    close_image = Image.open('Close Button 1.png')
    close_image = close_image.resize((10, 10))
    close_image = ImageTk.PhotoImage(close_image)
    close_button.config(image=close_image, bg='yellow', activebackground="yellow")
    close_button.image = close_image
    window.update()
def on_leave(event):

    close_image = Image.open('Yellow Background.png')
    close_image = close_image.resize((10, 10))
    close_image = ImageTk.PhotoImage(close_image)
    close_button.config(image=close_image, bg='yellow', activebackground="yellow")
    close_button.image = close_image
    window.update()

name=StringVar()
name.set('')
message=StringVar()
box=tkinter.Entry(frame3,textvariable=name,font=('calibre',20,'normal'),bg='yellow',fg='black',
        width=28,borderwidth=0)
box.pack(side=TOP,padx=(0,77))

frame3.bind("<Leave>",on_leave)
frame3.bind("<Enter>",on_enter)

close_button=Button(frame3,image=close_image,bg='yellow',activebackground='yellow',borderwidth=0,
                    width=35,height=35,command=close)
close_button.place(relx=0.88,rely=0,anchor=N)
search_button=Button(frame3,image=search_image,command=find,bg='yellow',activebackground='yellow',borderwidth=0,
                     width=40)
search_button.place(relx=0.96,rely=0,anchor=N)
def space_find(event):
    if event.keysym=='Return':
        find()
box.bind('<Return>',space_find)
# display=Label(window,textvariable=message,font=('calibre',10,'normal'))
# display.pack()
##################################################
songs=Scrollbar(frame3)
songs.pack(side=RIGHT,fill=Y)
songsh=Scrollbar(frame3,orient=HORIZONTAL)
songsh.pack(side=BOTTOM,fill=X)
listbox_values=tkinter.Variable(value=track_names)
song_list=Listbox(frame3,yscrollcommand=songs.set,xscrollcommand=songsh.set,
                  highlightcolor="black",activestyle='none',
                  bd=1,height=538,width=500,listvariable=listbox_values)
song_list.bind('<<ListboxSelect>>', music_player)

# for song in track_names:
#     song_list.insert(END,song)

song_list.config(bg="#fafafa",fg="black",
                 font=("calibre",30,"normal"))
song_list.pack(side=LEFT,fill=BOTH)
songs.config(command=song_list.yview)
songsh.config(command=song_list.xview)
# button=Button(frame3,text="button",width=50,height=50)
# button.grid(row=0,column=0)

#---------------------------Frame 4---------------------------------
display=Frame(window,bg="yellow",width=300,height=90)
display.grid(row=2,column=0)
display.pack_propagate(False)
status=StringVar()
status.set('')
label=Label(display,textvariable=status,font=('Calibre',11,'normal'),bg='yellow')
label.pack(side=LEFT)



# playlist=Button(frame2,bg="black",width=300,height=50)
# playlist.pack()

# paddingUp=Frame(window,bg="yellow",width=width,height=15)
# paddingDown=Frame(window,bg="yellow",width=width,height=15)

#------------------------Progress Bar----------------------------------
canvas=Canvas(window,relief=FLAT,width=790,background = "#D2D2D2",height=5)
progress_bar=Progressbar(canvas,orient=HORIZONTAL,length=790,mode='determinate')
canvas.create_window(1,1,anchor=NW,window=progress_bar)
canvas.grid(row=1,column=0,columnspan=2)

current_time=StringVar()
current_time.set("00:00")
progress_repo=Label(display,textvariable=current_time,bg="yellow",activebackground="yellow")
progress_repo.pack(side=RIGHT)
#---------------------------------Marquee------------------------------
current_music=StringVar()
current_music.set("")
now_playing=Label(display,textvariable=current_music,bg="yellow",
                  width=150,height=20,borderwidth=0,font=("calibre",10,'normal'))
now_playing.pack(side=BOTTOM,anchor='w')
# text=now_playing.create_text(0,-2000,text=current_music,
#                              font=('Times New Roman',20,'bold'),fill='white',
#                              tags=("marquee",),anchor='w')
# fps=40

#----------------------------------Frame 1-----------------------------
frame1=Frame(window,bg="yellow",width=500,height=90)
frame1.pack_propagate(False)
# paddingUp.grid(row=1,fill=X,side="bottom")
frame1.grid(row=2,column=1)
# paddingDown.grid(row=3,fill=X,side="bottom")

#----------------------------------Volume Controls--------------------
frequency=StringVar()
frequency.set('Volume: 50')
vol_label=Label(frame1,textvariable=frequency,bg="yellow")
style=Style()
style.configure('TScale',background="yellow")
def volume(x):
    x=int(float(x))/100

    mixer.music.set_volume(x)
    frequency.set("Volume: "+str(int(x*100)))
vol_controls=Scale(frame1,from_=0,to=100,command=volume,orient=HORIZONTAL,
                   length=150,value=50)
vol_controls.set("50")


vol_label.place(relx=0.6,
                rely=0.1,
                anchor='n')


window.bind('<Shift-Key-Up>',key_vol_up)
window.bind('<Shift-Key-Down>',key_vol_down)

#----------------------------buttons--------------------------------------
start_image=Image.open('Play button.png')
prev_image=Image.open('Prev button.png')
next_image=Image.open('Next button.png')
pause_image=Image.open("Pause button.png")
replay_image=Image.open("Replay Button.png")
stop_image=Image.open("stop button.png")

start_image=start_image.resize((60,60))
start_image=ImageTk.PhotoImage(start_image)

pause_image=pause_image.resize((45,45))
pause_image=ImageTk.PhotoImage(pause_image)

play_pause_image=start_image

stop_image=stop_image.resize((40,40))
stop_image=ImageTk.PhotoImage(stop_image)

prev_image=prev_image.resize((30,30))
prev_image=ImageTk.PhotoImage(prev_image)

next_image=next_image.resize((30,30))
next_image=ImageTk.PhotoImage(next_image)

replay_image=replay_image.resize((30,30))
replay_image=ImageTk.PhotoImage(replay_image)

prev=Button(frame1,image=prev_image,width=40,height=40,bg='Yellow',
            activebackground='yellow',borderwidth=0,command=prev_song)
prev.pack(side=LEFT,padx=(10,8))

play_pause=Button(frame1,image=play_pause_image,width=50,height=50,bg='yellow',
                  borderwidth=0,activebackground='yellow',command=play_pause_actions)
play_pause.pack(side=LEFT,padx=(20,10))

window.bind('<Control-Key-p>',enter_play_pause_rewind_stop)
window.bind('<Control-Key-P>',enter_play_pause_rewind_stop)
window.bind('<Control-Key-r>',enter_play_pause_rewind_stop)
window.bind('<Control-Key-R>',enter_play_pause_rewind_stop)
window.bind('<Control-Key-s>',enter_play_pause_rewind_stop)
window.bind('<Control-Key-S>',enter_play_pause_rewind_stop)
window.bind('<Control-Key-Left>',enter_play_pause_rewind_stop)
window.bind('<Control-Key-Right>',enter_play_pause_rewind_stop)

next=Button(frame1,image=next_image,width=40,height=40,bg='yellow',
            activebackground='yellow',borderwidth=0,command=next_song)
next.pack(side=LEFT,padx=(10,10))

stop=Button(frame1,image=stop_image,width=40,height=40,bg='yellow',
            activebackground='yellow',borderwidth=0,command=stop_music)


replay_button=Button(frame1,image=replay_image,width=40,height=40,bg='yellow',
            activebackground='yellow',borderwidth=0,command=rewinding)

replay_button.pack(side=RIGHT,padx=(0,15))
stop.pack(side=RIGHT,padx=(10,10))
vol_controls.pack(side=RIGHT)
#-------------------------------------------------------------------------
try:
    def exit():
        window.destroy()
        window.protocol("WM_DELETE_WINDOW", exit)
except TclError:
    print("Application has been destroyed immediately after running.",
          "\nIf you want to further use the program, please restart")
try:
    window.mainloop()
except KeyboardInterrupt:
    print('Main program closed abruptly.\nIf you want to further use the program, please restart')



"""
1.Marquee.
2.Search Bar
3.Playlist
4.Song Queued automatically after ending
"""