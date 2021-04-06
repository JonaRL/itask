#Import Tkinter requirements
from tkinter import Tk
from tkinter import Label
from tkinter import Entry
from tkinter import StringVar
from tkinter import OptionMenu
from tkinter import Button
from tkinter import mainloop

#Import other requirements
import os
import functools
import requests

#Import internal requirements
import popup

tfilter = "current"
server = ""
username = ""
password = ""
main = ""
datafolder = ""

def func_save(): #Save data
  global server
  global username
  global password
  global tfilter
  global main
  global datafolder

  #Write data
  with open(os.path.join(datafolder, "user.data"), "a") as f:
    f.write("Generated by ITask Version 0.1.3\nserver:" + server.get() + ";\nusername:" + username.get() + ";\npassword:" + password.get() + ";\ntaskfilter:" + tfilter + ";")
  print("Daten wurden gespeichert!")
  main.destroy() #When the process is completed, the window is destroyed

def func_update_tfilter(value): #Update the 'taskfilter' variable to the value selected in the dropdown
  global tfilter
  tfilter = value

def func_main(df):
  global server
  global username
  global password
  global main
  global datafolder
  global popup
  datafolder = df

  print("Einrichtungsassistent wird geöffnet")
  main = Tk()
  main.title("Einrichtung")

  #Add text elements
  Label(main, font='Helvetica 11 bold', pady=4, padx=4, text="Willkommen bei ITask!").grid(row=0, column=0, columnspan=3)
  Label(main, text="Domain:").grid(row=1, column=0)
  Label(main, text="Benutzername:").grid(row=2, column=0)
  Label(main, text="Passwort:").grid(row=3, column=0)
  Label(main, text="Aufgaben:").grid(row=4, column=0)

  #Add text fields
  server = Entry(main)
  username = Entry(main)
  password = Entry(main, show="*")
  server.grid(row=1, column=1)
  username.grid(row=2, column=1)
  password.grid(row=3, column=1)

  #Add popup selector
  value = StringVar(main)
  value.set("current")
  taskfilter = OptionMenu(main, value, "current", "past", "all", command=func_update_tfilter)
  taskfilter.config(font='Helvetica 11')
  taskfilter.grid(row=4, column=1)

  #Add buttons
  Button(main, text="?", command=functools.partial(popup.func_main, 1)).grid(row=1, column=2)
  Button(main, text="?", command=functools.partial(popup.func_main, 2)).grid(row=2, column=2)
  Button(main, text="?", command=functools.partial(popup.func_main, 3)).grid(row=3, column=2)
  Button(main, text="?", command=functools.partial(popup.func_main, 4)).grid(row=4, column=2)

  #Configure submit button
  submit = Button(main, text="Speichern", command=func_save)
  submit.grid(row=5, column=0)

  mainloop()
