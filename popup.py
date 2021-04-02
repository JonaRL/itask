#Import Tkinter requirements
from tkinter import Tk
from tkinter import Label
from tkinter import mainloop

#Import other requirements
import sys

def func_main(key):

  main = Tk()
  main.resizable(width=False, height=False)
  print("Öffne Popup mit dem Key " + str(key))

  if key == 0:
    main.title("Über")
    Label(main, font='Helvetica 11 bold', pady=4, padx=4, text="ITask").grid(row=0, column=0)
    Label(main, font='Helvetica 11', pady=0, padx=4, text="Version 0.1.2").grid(row=1, column=0)
    Label(main, font='Helvetica 5', pady=0, padx=4, text="").grid(row=2, column=0)
    Label(main, font='Helvetica 11 bold', pady=4, padx=4, text="Entwickelt von:").grid(row=3, column=0)
    Label(main, font='Helvetica 11', pady=0, padx=4, text="JonaRL").grid(row=4, column=0)
    Label(main, font='Helvetica 11', pady=0, padx=4, text="(https://github.com/jonarl/itask/)").grid(row=5, column=0)
    Label(main, font='Helvetica 5', pady=0, padx=4, text="").grid(row=6, column=0)
    Label(main, font='Helvetica 11 bold', pady=4, padx=4, text="Lizenz:").grid(row=7, column=0)
    Label(main, font='Helvetica 11', pady=0, padx=4, text="GNU GPL Version 3").grid(row=8, column=0)

  if key == 1:
    main.title("Hilfe")
    Label(main, font='Helvetica 11 bold', pady=4, padx=4, text="Domain").grid(row=0, column=0)
    Label(main, font='Helvetica 11', pady=0, padx=4, text="In dieses Feld wird die Domain").grid(row=1, column=0)
    Label(main, font='Helvetica 11', pady=0, padx=4, text="des IServ-Servers eingetragen.").grid(row=2, column=0)
    Label(main, font='Helvetica 5', pady=0, padx=4, text="").grid(row=3, column=0)
    Label(main, font='Helvetica 11 bold', pady=0, padx=4, text="Beispiel:").grid(row=4, column=0)
    Label(main, font='monospace 10', pady=2, padx=4, text="demo-iserv.de").grid(row=5, column=0)

  if key == 2:
    main.title("Hilfe")
    Label(main, font='Helvetica 11 bold', pady=4, padx=4, text="Benutzername").grid(row=0, column=0)
    Label(main, font='Helvetica 11', pady=0, padx=4, text="In dieses Feld wird der Benutzername").grid(row=1, column=0)
    Label(main, font='Helvetica 11', pady=0, padx=4, text="des IServ-Accounts eingetragen.").grid(row=2, column=0)
    Label(main, font='Helvetica 5', pady=0, padx=4, text="").grid(row=3, column=0)
    Label(main, font='Helvetica 11 bold', pady=0, padx=4, text="Beispiel:").grid(row=4, column=0)
    Label(main, font='monospace 10', pady=2, padx=4, text="user.name").grid(row=5, column=0)

  if key == 3:
    main.title("Hilfe")
    Label(main, font='Helvetica 11 bold', pady=4, padx=4, text="Passwort").grid(row=0, column=0)
    Label(main, font='Helvetica 11', pady=0, padx=4, text="In dieses Feld wird das Passwort").grid(row=1, column=0)
    Label(main, font='Helvetica 11', pady=0, padx=4, text="des IServ-Accounts eingetragen.").grid(row=2, column=0)
    Label(main, font='Helvetica 5', pady=0, padx=4, text="").grid(row=3, column=0)
    Label(main, font='Helvetica 11 bold', pady=0, padx=4, text="Beispiel:").grid(row=4, column=0)
    Label(main, font='monospace 10', pady=2, padx=4, text="*********").grid(row=5, column=0)

  if key == 4:
    main.title("Hilfe")
    Label(main, font='Helvetica 11 bold', pady=4, padx=4, text="Aufgaben").grid(row=0, column=0, columnspan=2)
    Label(main, font='Helvetica 11', padx=4, text="Diese Einstellung legt fest, welche").grid(row=1, column=0, columnspan=2)
    Label(main, font='Helvetica 11', padx=4, text="Aufgaben heruntergeladen werden.").grid(row=2, column=0, columnspan=2)
    Label(main, font='Helvetica 11', padx=4, text="Es gibt folgende Optionen:").grid(row=3, column=0, columnspan=2)
    Label(main, font='Helvetica 5', padx=4, text="").grid(row=4, column=0)
    Label(main, font='Helvetica 11 bold', pady=0, padx=4, text="current:").grid(row=5, column=0, sticky="w")
    Label(main, font='Helvetica 11', padx=4, text="Nur aktuelle Aufgaben").grid(row=5, column=1, sticky="w")
    Label(main, font='Helvetica 11 bold', pady=0, padx=4, text="past:").grid(row=6, column=0, sticky="w")
    Label(main, font='Helvetica 11', padx=4, text="Nur vergangene Aufgaben").grid(row=6, column=1, sticky="w")
    Label(main, font='Helvetica 11 bold', pady=0, padx=4, text="all:").grid(row=7, column=0, sticky="w")
    Label(main, font='Helvetica 11', padx=4, text="Alle Aufgaben").grid(row=7, column=1, sticky="w")


  mainloop()
