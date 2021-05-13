#Import Tkinter requirements
from tkinter import Tk
from tkinter import Label
from tkinter import Text
from tkinter import Scrollbar
from tkinter import mainloop

#Import other requirements
import json
import os
import sys
import html
import webbrowser
import functools

def func_openfile(link, event): #Open an external file
  print("Öffne externe Datei unter " + link)
  webbrowser.open(link)  

def func_main(datafolder, num):
  print("Zeige Aufgabe Nummer " + num) #Print which task will be shown
  tdata = json.loads(open(os.path.join(datafolder, "tasks.json")).read()) #Read task data from tasks.json

  main = Tk()
  main.title("Aufgabendetails")

  #Add window elements
  obj = Label(main, font='Helvetica 11 bold', pady=4, padx=4, text="Name:")
  obj.grid(row=0, column=0)
  obj = Label(main, font='Helvetica 11', pady=4, padx=4, text=tdata[num]["title"])
  obj.grid(row=0, column=1)
  obj = Label(main, font='Helvetica 11 bold', pady=4, padx=4, text="Start:")
  obj.grid(row=1, column=0)
  obj = Label(main, font='Helvetica 11', pady=4, padx=4, text=tdata[num]["start"])
  obj.grid(row=1, column=1)
  obj = Label(main, font='Helvetica 11 bold', pady=4, padx=4, text="Abgabe:")
  obj.grid(row=2, column=0)
  obj = Label(main, font='Helvetica 11', pady=4, padx=4, text=tdata[num]["end"])
  obj.grid(row=2, column=1)
  obj = Label(main, font='Helvetica 11 bold', pady=4, padx=4, text="Beschreibung:")
  obj.grid(row=3, column=0)
  tw = Text(main, font='Helvetica 11', pady=4, padx=4)
  tw.insert("0.0", html.unescape(tdata[num]["description"].split("\n", 1)[1]))
  tw['state'] = "disabled"
  tw.grid(row=3, column=1)
  sb = Scrollbar(main, command=tw.yview)
  sb.grid(row=3, column=2, sticky="ns")
  tw['yscrollcommand'] = sb.set

  if tdata[num]["files"] != 0: #If there are external files, add them as well
    obj = Label(main, font='Helvetica 11 bold', pady=4, padx=4, text="Dateien:")
    obj.grid(row=4, column=0)
    for i in range(tdata[num]["files"]): #For every external file, add an window element with the file name and bind a button to it
      obj = Label(main, font='Helvetica 11', pady=4, padx=4, fg="blue", cursor="hand1", text=tdata[num]["filedetails"][i]["name"])
      obj.bind("<Button-1>", functools.partial(func_openfile, tdata[num]["filedetails"][i]["link"]))
      obj.grid(row=4+i, column=1)

  mainloop()
