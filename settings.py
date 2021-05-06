#Import Tkinter requirements
from tkinter import Tk
from tkinter import Label
from tkinter import Frame
from tkinter import StringVar
from tkinter import OptionMenu
from tkinter import Button
from tkinter import filedialog

#Import other requirements
from zipfile import ZipFile
from pathlib import Path
import os
import functools

#Import internal requirements
import setup
import popup

tfilter = ""
main = ""
datafolder = ""

def func_update_tfilter(value): #Update the 'taskfilter' variable to the value selected in the dropdown
  global tfilter
  tfilter = value

def func_save(): #Save changes
  global tfilter
  global main
  global datafolder

  #Read user data from user.data
  usrdata = open(os.path.join(datafolder, "user.data")).read()
  server = usrdata.split("server:")[1].split(";")[0]
  username = usrdata.split("username:")[1].split(";")[0]
  password = usrdata.split("password:")[1].split(";")[0]

  #Write changes
  with open(os.path.join(datafolder, "user.data"), "w") as f:
    f.write("Generated by ITask Version 0.1.5\nserver:" + server + ";\nusername:" + username + ";\npassword:" + password + ";\ntaskfilter:" + tfilter + ";")
  print("Daten wurden gespeichert!")
  main.destroy()

def func_rewrite(): #Remove user.data and restart setup assistant to update profile data
  global datafolder
  global setup
  print("Einrichtungsassistent wird neu geladen")
  os.remove(os.path.join(datafolder, "user.data"))
  setup.func_main(datafolder)

def func_backup(): #Create .zip file as backup
  global ZipFile
  global os
  global datafolder
  filelinks = []
  
  print("Getting file list...")
  os.chdir(datafolder)
  for root, datafolder, files in os.walk(datafolder):
    print("Root directory: " + root)
    for filename in files: #Every file gets appended to a list
      filelinks.append(filename)

  print('Zipping files...')
  #Write the .zip file
  with ZipFile(filedialog.asksaveasfilename(initialdir = Path.home(), initialfile="ITask-Backup.zip", title = "Speichern unter...", filetypes = (("Zip-Dateien", "*.zip"), ("Alle Dateien", "*.*"))),'w') as zip:
    for file in filelinks:
      zip.write(file)
  print('All files zipped successfully!')

def func_main(dfolder, taskfilter):
  #Initialize Tkinter
  global main
  global datafolder
  datafolder = dfolder

  print("Öffne Einstellungen")
  main = Tk()
  main.title("Einstellungen")

  #Add window elements
  Label(main, font='Helvetica 11 bold', pady=4, padx=4, text="Einstellungen").grid(row=0, column=0, columnspan=3)
  Frame(main, bg="grey", height=1, bd=0).grid(column=0, row=1, columnspan=3, sticky='ew')
  Frame(main, bg="grey", height=1, bd=0).grid(column=0, row=4, columnspan=3, sticky='ew')
  Frame(main, bg="grey", height=1, bd=0).grid(column=0, row=6, columnspan=3, sticky='ew')

  #Add popup to select taskfilter
  Label(main, text="Aufgaben:").grid(row=2, column=0, pady=4, padx=4)
  value = StringVar(main)
  value.set(taskfilter)
  taskfilter = OptionMenu(main, value, "current", "past", "all", command=func_update_tfilter)
  taskfilter.config(font='Helvetica 11')
  taskfilter.grid(row=2, column=1)

  #Add buttons
  Button(master=main, text="?", command=functools.partial(popup.func_main, 4)).grid(row=2, column=2)
  Button(master=main, text="Speichern", command=func_save).grid(row=3, column=1, columnspan=3, pady=5, sticky='e', padx=5)
  Button(master=main, text="Nutzerdaten aktualisieren...", command=func_rewrite).grid(row=5, column=0, columnspan=3, pady=5, padx=5)
  Button(master=main, text="Backup erstellen", command=func_backup).grid(row=7, column=0, columnspan=3, pady=5, padx=5)