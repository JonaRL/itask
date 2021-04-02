#Import Tkinter requirements
from tkinter import Tk
from tkinter import Label
from tkinter import Frame
from tkinter import StringVar
from tkinter import OptionMenu
from tkinter import Button

#Import other requirements
import os

#Import internal requirements
import setup

tfilter = ""
main = ""
datafolder = ""

def func_update_tfilter(value):
  global tfilter
  tfilter = value
  print("Taskfilter updated to: " + value)

def func_save():
  global tfilter
  global main
  global datafolder

  usrdata = open(os.path.join(datafolder, "user.data")).read()
  server = usrdata.split("server:")[1].split(";")[0]
  username = usrdata.split("username:")[1].split(";")[0]
  password = usrdata.split("password:")[1].split(";")[0]

  #Daten schreiben
  with open(os.path.join(datafolder, "user.data"), "w") as f:
    f.write("Generated by ITask Version 0.1.2\nserver:" + server + ";\nusername:" + username + ";\npassword:" + password + ";\ntaskfilter:" + tfilter + ";")
  main.destroy()

def func_rewrite():
  global datafolder
  global setup
  os.remove(os.path.join(datafolder, "user.data"))
  setup.func_main(datafolder)

def func_main(dfolder, taskfilter):
  #Tkinter initialisieren
  global main
  global datafolder
  datafolder = dfolder

  main = Tk()
  main.title("Einstellungen")

  #Elemente hinzufügen
  Label(main, font='Helvetica 11 bold', pady=4, padx=4, text="Einstellungen").grid(row=0, column=0, columnspan=2)
  Frame(main, bg="grey", height=1, bd=0).grid(column=0, row=1, columnspan=2, sticky='ew')
  Frame(main, bg="grey", height=1, bd=0).grid(column=0, row=4, columnspan=2, sticky='ew')

  #Auswahl: taskfilter
  Label(main, text="Aufgaben:").grid(row=2, column=0, pady=4, padx=4)
  value = StringVar(main)
  value.set(taskfilter)
  taskfilter = OptionMenu(main, value, "current", "past", "all", command=func_update_tfilter)
  taskfilter.config(font='Helvetica 11')
  taskfilter.grid(row=2, column=1)

  #Buttons
  Button(master=main, text="Speichern", command=func_save).grid(row=3, column=1, pady=5, sticky='e', padx=5)
  Button(master=main, text="Nutzerdaten aktualisieren...", command=func_rewrite).grid(row=5, column=0, columnspan=2, pady=5, padx=5, sticky="w")