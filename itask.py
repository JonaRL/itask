#Import Tkinter requirements
from tkinter import Tk
from tkinter import Label
from tkinter import Frame
from tkinter import Button
from tkinter import Menu
from tkinter import mainloop

#Import other requirements
from pathlib import Path
import json
import sys
import functools
import os
import platform

#Import internal requirements
import showtask
import gettask
import setup
import popup
import settings

print("Iserv Task Downloader (ITask) Version 0.1.4")
print("Erkenne OS...")

#Detecting OS in order to know where files are being saved
if platform.system() == "Linux":
  print("Linux-System erkannt!")
  datafolder = os.path.join(str(Path.home()), ".itask") #Set the datafolder to /home/$USER/.itask/
  os.chdir(str(Path.home()))
elif platform.system() == "Windows":
  print("Windows-System erkannt!")
  datafolder = os.path.join(str(Path.home()), "AppData", "ITask") #Set the datafolder to C:\Users\$USER\AppData\Itask\
  os.chdir(os.path.join(str(Path.home()), "AppData"))
else: #No supported OS has been detected
  datafolder = os.path.join(os.path.dirname(os.path.realpath(__file__)), "itask-data") #Set the datafolder to "itask-data" inside the folder where the program is executed
  os.chdir(os.path.dirname(os.path.realpath(__file__)))
  print("WARNUNG: OS nicht offiziell unterstützt!")
print("Datenverzeichnis: " + datafolder)

if os.path.isdir(datafolder) == False: #If the datafolder does not exist, the program is started for the first time
  print("Datenverzeichnis existiert nicht und wird daher erstellt.")
  os.mkdir(datafolder)
  setup.func_main(datafolder) #Initializing Setup Assistant
  gettask.func_main(datafolder) #Downloading tasks for the first time
elif os.path.isfile(os.path.join(datafolder, "user.data")) == False: #If the datafolder exists but user.data doesn't, the user deleted his userdata in the settings and didn't set new ones
  print("user.data konnte nicht gefunden werden!")
  setup.func_main(datafolder) #Initializing Setup Assistant

#Setting some variables
page = -1
label = {}
tasks = 0
taskloop = 10

usrdata = open(os.path.join(datafolder, "user.data")).read() #Reading information from user.data

print("Initialisiere Tkinter...")
main = Tk()
main.title("ITask v0.1.4")

def func_showtask(num, event): #Used to show details about a task selected in the GUI
  global tdata
  global showtask
  if page*10+10 >= tdata["tasks"]: #If the user is on the last page, a different mechanism has to be used to get the number of the clicked task
    showtask.func_main(datafolder, str(10-num)) #Call showtask.py with datafolder and the task number as parameters
  else: #If the user isn't at the last page, this will be executed
    showtask.func_main(datafolder, str(tdata["tasks"]-num-page*10)) #Call showtask.py with datafolder and the task number as parameters

#Create first row of the table
b = Label(main, font='Helvetica 11 bold', pady=4, padx=4, text="Name")
b.grid(row=0, column=0)
b = Label(main, font='Helvetica 11 bold', pady=4, padx=4, text="Erstelldatum")
b.grid(row=0, column=2)
b = Label(main, font='Helvetica 11 bold', pady=4, padx=4, text="Abgabedatum")
b.grid(row=0, column=4)

print("Lade Aufgaben...")
tdata = json.loads(open(os.path.join(datafolder, "tasks.json"), "r").read()) #Reading information about all tasks from tasks.json

for i in range(1,11,1): #As long as there are tasks ins tdata (which has been read from tasks.json), create a row in the table (current max is 10 rows)
  label[i] = {}
  label[i]["title"] = Label(main, font='Helvetica 11', pady=4, padx=4, cursor="hand1", text=tdata[str(i)]["title"])
  label[i]["start"] = Label(main, font='Helvetica 11', pady=4, padx=4, text=tdata[str(i)]["start"])
  label[i]["end"] = Label(main, font='Helvetica 11', pady=4, padx=4, text=tdata[str(i)]["end"])

def func_back(): #Used to get one page back
  global page
  page = page-1
  if page == 0: #If the user is on the last page, disable the button to get to the previous page
    global back
    back['state'] = 'disabled'
  if page*10+20 >= tdata["tasks"]: #If the user switched from the last page to the page before, enable the button to get to the next page
    global next
    next['state'] = 'normal'
  func_page() #Apply changes

def func_next(): #Used to get one page forward
  global page
  page = page+1
  if page == 1: #If the user switched from the first page to the next page, enable the button to get to the previous page
    global back
    back['state'] = 'normal'
  if page*10+10 >= tdata["tasks"]: #If the user is on the last page, disable the button to get to the next page
    global next
    next['state'] = 'disabled'
  func_page() #Apply changes

def func_page(): #Used to build the selected page
  global page
  global tasks
  global label
  global taskloop
  if page == -1 or page*10+10 >= tdata["tasks"]: #Handle special conditions
    if page == -1: #If page is equals -1, the program has just been initialized.
      tasks = 0
    else: #If the user switches to the last page, the task number may need correcting if the number of tasks cannot be devided by 10
      tasks = tdata["tasks"]-10
  else: #If no special condition has occured, the task number is page*10 (because 10 is the maximum of tasks on one page)
    tasks = page*10
  if tdata["tasks"] <= 10: #If there are not more than 10 tasks in tdata...
    global next
    next['state'] = 'disabled' #Disable the button to get to the next page
    taskloop = tdata["tasks"]+1 #Set the number of times the following loop runs to the number of tasks (to archieve that, the variable has to be set to that number plus one)
  else: #If there are more than 10 tasks, set the variable to 11 so that the loop runs 10 times
    taskloop = 11
  for i in range(tdata["tasks"]-1-tasks,tdata["tasks"]-tasks-taskloop,-1): #Runs as long as a task has to be entered in the table. Explanation at https://pastebin.com/V3CU5ZcH
    #Enter title, start and end into table
    label[tdata["tasks"]-i-tasks]["title"].config(text=tdata[str(i)]["title"])
    label[tdata["tasks"]-i-tasks]["start"].config(text=tdata[str(i)]["start"])
    label[tdata["tasks"]-i-tasks]["end"].config(text=tdata[str(i)]["end"])
    if page == -1: #If the table is initialized for the first time, some more things have to be done
      #Put the corresponding labels in their places in the Tkinter grid
      label[tdata["tasks"]-i-tasks]["title"].grid(row=(tdata["tasks"]-i-tasks)*2, column=0)
      label[tdata["tasks"]-i-tasks]["start"].grid(row=(tdata["tasks"]-i-tasks)*2, column=2)
      label[tdata["tasks"]-i-tasks]["end"].grid(row=(tdata["tasks"]-i-tasks)*2, column=4)
      label[tdata["tasks"]-i-tasks]["title"].bind("<Button-1>", functools.partial(func_showtask, tdata["tasks"]-i-tasks)) #Add a Button to the title label so that it will be clickable
      Frame(main, bg="black", height=1, bd=0).grid(column=0, row=(tdata["tasks"]-i)*2-1, columnspan=5, sticky='ew') #Create a frame which is used to seperate columns

#Put some main elements into their places in the GUI
Frame(main, bg="black", height=1, bd=0).grid(column=1, row=0, rowspan=21, sticky='ns') #Row seperators
Frame(main, bg="black", height=1, bd=0).grid(column=3, row=0, rowspan=21, sticky='ns')
next = Button(master=main, text="\N{RIGHTWARDS BLACK ARROW}", command=func_next) #Button to go to next page
next.grid(row=21, column=4, pady=10, sticky='e', padx=10)
back = Button(master=main, text="\N{LEFTWARDS BLACK ARROW}", state='disabled', command=func_back) #Button to go to previous page
back.grid(row=21, column=0, pady=10, sticky='w', padx=10)

#Create Menus
menubar = Menu(main)
main.config(menu=menubar)
menu_file = Menu(menubar, tearoff=False)
menu_help = Menu(menubar, tearoff=False)

#Configure File Menu
menu_file.add_command(label='Auf neue Aufgaben prüfen (Strg+D)', command=functools.partial(gettask.func_main, datafolder))
menu_file.add_command(label='Einstellungen (Strg+M)', command=functools.partial(settings.func_main, datafolder, usrdata.split("taskfilter:")[1].split(";")[0]))
menu_file.add_separator()
menu_file.add_command(label='Beenden (Strg+Q)', command=main.destroy)
menubar.add_cascade(label="Datei", menu=menu_file)

#Configure Help Menu
menu_help.add_command(label='Über ITask', command=functools.partial(popup.func_main, 0))
menubar.add_cascade(label="Hilfe", menu=menu_help)

#Add Keybinds
main.bind('<Control-d>', lambda event: gettask.func_main(datafolder))
main.bind('<Control-q>', lambda event: main.destroy())
main.bind('<Control-m>', lambda event: settings.func_main(datafolder, usrdata.split("taskfilter:")[1].split(";")[0]))

#Finally, create the page for the first time...
func_page()
page = 0

#...and start the mainloop to wait for user interactions
mainloop()