#Import Tkinter requirements
from tkinter import Tk
from tkinter.ttk import Progressbar
from tkinter.ttk import Label

#Import other requirements
import requests
import sys
import os
import json

def func_main(datafolder):
  print("Starte Datenübertragung...")

  main = Tk()
  main.geometry("300x100")
  main.title("Aktualisiere...")

  #Add window elements
  progress = Progressbar(main, orient="horizontal", length=300, mode="determinate")
  progress["value"]=0
  progress.grid(row=0, column=0)
  status = Label(main, font='Helvetica 11 bold', padding=4, text="Statusanzeige")
  status.grid(row=1, column=0)
  download = Label(main, font='Helvetica 11', padding=4, text="")
  download.grid(row=2, column=0)
  main.update() #Manually update the window since mainloop() cannot be used

  #Read user data from user.data
  datafolder = os.path.join(datafolder, "")
  usrdata = open(os.path.join(datafolder, "user.data")).read()
  server = usrdata.split("server:")[1].split(";")[0]
  username = usrdata.split("username:")[1].split(";")[0]
  password = usrdata.split("password:")[1].split(";")[0]

  #Get task urls
  urls = open(os.path.join(datafolder, "tasks.list")).read()
  urls = urls.split("\n")
  urls.pop()

  #Read JSON from File
  with open(os.path.join(datafolder, "tasks.json"), 'r') as f:
    data = json.load(f)
  
  #Set some important variables
  title = ""
  start = ""
  taskname1 = "<h1>Details zu "
  taskname2 = "</h1>"
  taskstart = "<th>Starttermin:</th>"
  date1 = "<td>"
  date2 = "</td>"
  headers = {'User-Agent': 'Mozilla/5.0'} #User-Agent (Browser) festlegen
  credits = {'_username': username, '_password': password} #Login-Daten festlegen
  
  #Connect to IServ
  status["text"] = "Verbinde zu IServ..."
  main.update()
  print("Verbinde zu IServ...")
  session = requests.Session()
  session.post('https://' + server + '/iserv/login_check', headers=headers, data=credits)

  #Set progressbar
  progress["maximum"]=len(urls)
  progress["value"] = 0

  #Starting migration
  for i in range(len(urls)):
    status["text"] = "Übertrage Aufgabe " + str(i+1) + " von " + str(len(urls)) + "..."
    progress["value"] = progress["value"] + 1
    main.update()
    print("Übertrage Aufgabe " + str(i+1) + " von " + str(len(urls)) + "...")
    html = session.get(urls[i-1]).text
  
    #Extract title and start
    print(urls[i-1])
    title = html.split(taskname1)[1].split(taskname2)[0] #Tasks name
    start = html.split(taskstart)[1].split(date1)[1].split(date2)[0] #Date when the task starts
  
    #Find task in tasks.json
    for ii in range(data["tasks"]):
      if data[str(ii)]["title"] == title and data[str(ii)]["start"] == start:
        data[str(ii)].update({"url": urls[i-1]})
        data[str(ii)]["url"] == urls[i-1]

  #Add version parameter
  data.update({"version": "1.1"})

  #Update Progress
  status["text"] = "Schreibe Daten..."
  progress["value"] = progress["maximum"]
  main.update()
  print("Schreibe Daten...")

  #Write to file
  with open(os.path.join(datafolder, "tasks.json"), "w") as f:
    json.dump(data, f, indent=2) #Works!

  #Delete tasks.list
  os.remove(os.path.join(datafolder, "tasks.list"))

  #Destroy window
  main.destroy()