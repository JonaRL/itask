from tkinter import *
from pathlib import Path
import json
import sys
import functools
import os
import platform

import showtask
import gettask
import setup
import popup

if platform.system() == "Linux":
  datafolder = os.path.join(str(Path.home()), ".itask")
  os.chdir(str(Path.home()))
elif platform.system() == "Windows":
  datafolder = os.path.join(str(Path.home()), "AppData", "ITask")
  os.chdir(os.path.join(str(Path.home()), "AppData"))
else:
  datafolder = os.path.join(os.path.dirname(os.path.realpath(__file__)), "itask-data")
  os.chdir(os.path.dirname(os.path.realpath(__file__)))
  print("WARNING: OS not officially supported")

if os.path.isdir(datafolder) == False:
  setup.func_main(datafolder)
  gettask.func_main(datafolder)

page = -1
label = {}
tasks = 0
taskloop = 10

main = Tk()
main.title("ITask v0.1.0")

def func_showtask(num, event):
  global tdata
  global showtask
  if page*10+10 >= tdata["tasks"]:
    showtask.func_main(datafolder, str(10-num))
  else:
    showtask.func_main(datafolder, str(tdata["tasks"]-num-page*10))

def func_download():
  gettask.func_main(datafolder)

b = Label(main, font='Helvetica 11 bold', pady=4, padx=4, text="Name")
b.grid(row=0, column=0)
b = Label(main, font='Helvetica 11 bold', pady=4, padx=4, text="Erstelldatum")
b.grid(row=0, column=2)
b = Label(main, font='Helvetica 11 bold', pady=4, padx=4, text="Abgabedatum")
b.grid(row=0, column=4)

tdata = json.loads(open(os.path.join(datafolder, "tasks.json"), "r").read())

for i in range(1,11,1):
  label[i] = {}
  label[i]["title"] = Label(main, font='Helvetica 11', pady=4, padx=4, cursor="hand1", text=tdata[str(i)]["title"])
  label[i]["start"] = Label(main, font='Helvetica 11', pady=4, padx=4, text=tdata[str(i)]["start"])
  label[i]["end"] = Label(main, font='Helvetica 11', pady=4, padx=4, text=tdata[str(i)]["end"])

def func_back():
  global page
  page = page-1
  if page == 0:
    global back
    back['state'] = 'disabled'
  if page*10+20 >= tdata["tasks"]:
    global next
    next['state'] = 'normal'
  func_page()

def func_next():
  global page
  page = page+1
  if page == 1:
    global back
    back['state'] = 'normal'
  if page*10+10 >= tdata["tasks"]:
    global next
    next['state'] = 'disabled'
  func_page()

def func_page():
  global page
  global tasks
  global label
  global taskloop
  if page == -1 or page*10+10 >= tdata["tasks"]:
    if page == -1:
      tasks = 0
    else:
      tasks = tdata["tasks"]-10
  else:
    tasks = page*10
  if tdata["tasks"] <= 10:
    global next
    next['state'] = 'disabled'
    taskloop = tdata["tasks"]+1
  else:
    taskloop = 11
  for i in range(tdata["tasks"]-1-tasks,tdata["tasks"]-tasks-taskloop,-1):
    label[tdata["tasks"]-i-tasks]["title"].config(text=tdata[str(i)]["title"])
    label[tdata["tasks"]-i-tasks]["start"].config(text=tdata[str(i)]["start"])
    label[tdata["tasks"]-i-tasks]["end"].config(text=tdata[str(i)]["end"])
    if page == -1:
      label[tdata["tasks"]-i-tasks]["title"].grid(row=(tdata["tasks"]-i-tasks)*2, column=0)
      label[tdata["tasks"]-i-tasks]["title"].bind("<Button-1>", functools.partial(func_showtask, tdata["tasks"]-i-tasks))
      label[tdata["tasks"]-i-tasks]["start"].grid(row=(tdata["tasks"]-i-tasks)*2, column=2)
      label[tdata["tasks"]-i-tasks]["end"].grid(row=(tdata["tasks"]-i-tasks)*2, column=4)
      Frame(main, bg="black", height=1, bd=0).grid(column=0, row=(tdata["tasks"]-i)*2-1, columnspan=5, sticky='ew')

Frame(main, bg="black", height=1, bd=0).grid(column=1, row=0, rowspan=21, sticky='ns')
Frame(main, bg="black", height=1, bd=0).grid(column=3, row=0, rowspan=21, sticky='ns')
next = Button(master=main, text="\N{RIGHTWARDS BLACK ARROW}", command=func_next)
next.grid(row=21, column=4, pady=10, sticky='e', padx=10)
back = Button(master=main, text="\N{LEFTWARDS BLACK ARROW}", state=DISABLED, command=func_back)
back.grid(row=21, column=0, pady=10, sticky='w', padx=10)
#TODO: Den Knopf fürs Herunterladen von Aufgaben woanders hinpacken
download = Button(master=main, text="Auf neue Aufgaben prüfen", command=func_download)
download.grid(row=21, column=0, pady=10, sticky='e', padx=10)
func_page()

page = 0

mainloop()
