#Import Tkinter requirements
from tkinter import Tk
from tkinter.ttk import Progressbar
from tkinter.ttk import Label

#Import other requirements
import requests
import sys
import os

def func_main(datafolder):
  print("Starte Aufgabendownload")

  main = Tk()
  main.geometry("300x100")
  main.title("Herunterladen...")

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
  taskfilter = usrdata.split("taskfilter:")[1].split(";")[0]
  
  url1 = "<td class=\"iserv-admin-list-field iserv-admin-list-field-textarea\"><a href=\""
  url2 = "\">"
  name = "</a></td>"
  oldtasks = ""
  tasks = []
  newtasks = []
  title = ""
  start = ""
  end = ""
  files = 0
  filenames = []
  filelinks = []
  json = []
  taskname1 = "<h1>Details zu "
  taskname2 = "</h1>"
  taskstart = "<th>Starttermin:</th>"
  taskend = "<th>Abgabetermin:</th>"
  textstart = "<div class=\"text-break-word p-3\">"
  textend = "</div>"
  fileurl = "/iserv/fs/file/exercise-dl/"
  file1 = "<a href=\""
  date1 = "<td>"
  date2 = "</td>"
  att1 = "<form name=\"iserv_exercise_attachment\""
  att2 = "</form>"
  fileend1 = "<span class=\"text-muted\">"
  fileend2 = "</a>"
  headers = {'User-Agent': 'Mozilla/5.0'} #User-Agent (Browser) festlegen
  credits = {'_username': username, '_password': password} #Login-Daten festlegen
  
  #Connect to IServ
  status["text"] = "Verbinde zu IServ..."
  main.update()
  print("Verbinde zu IServ...")
  session = requests.Session()
  session.post('https://' + server + '/iserv/login_check', headers=headers, data=credits)
  
  #Download list of tasks
  status["text"] = "Aufgabenliste wird geladen..."
  main.update()
  print("Aufgabenliste wird geladen...")
  html = session.get("https://" + server + "/iserv/exercise?filter[status]=" + taskfilter).text
  
  #Extract Links from the downloaded html file
  i = int(len(html.split(url1))-1)
  searchtml = html
  
  #Index links in an array
  for ii in range(i):
    tasks.append(searchtml.split(url1)[1].split(url2)[0]) #Attach link to the list of all tasks
    newtasks.append(searchtml.split(url1)[1].split(url2)[0]) #Add link to the list of new tasks (if the task is not new, the link will be removed later).
    searchtml = html.split(name)[ii+1] #Limit HTML to be searched so that the same link is not indexed again
  
  #Check, which tasks are new and which have already been downloaded
  try:
    oldtasks = open(datafolder + "tasks.list", "r").read() #Read list of tasks that already have been downloaded
    for i in range(len(tasks)):
      if oldtasks.find(tasks[i]) != -1: #If an entry in the downloaded tasks matches an extry in the list of old tasks, that entry will be removed
        newtasks.remove(tasks[i])
      else: #Otherwise, the task is written to tasks.list
        with open(datafolder + "tasks.list", "a") as f:
          f.write(tasks[i] + "\n")
  except: #If the program is started for the first time, an error occures
  
    #Write all downloaded tasks to tasks.list
    for i in range(len(tasks)):
      with open(datafolder + "tasks.list", "a") as f:
        f.write(tasks[i] + "\n")
  
  #Inform the user how many tasks have been found and how many of them are new
  status["text"] = str(len(tasks)) + " Aufgaben gefunden, davon " + str(len(newtasks)) + " neue."
  progress["maximum"]=len(newtasks)
  progress["value"]=1
  main.update()
  print(str(len(tasks)) + " Aufgaben gefunden, davon " + str(len(newtasks)) + " neue.")
  tasks = newtasks #Consider only new tasks for further processing
  tasks = sorted(tasks) #Sort tasks by ID / creation date
  
  #Download tasks
  for i in range(len(tasks)):
    status["text"] = "Lade Aufgabe " + str(i+1) + " von " + str(len(tasks)) + "..."
    main.update()
    print("Lade Aufgabe " + str(i+1) + " von " + str(len(tasks)) + "...")
    html = session.get(tasks[i]).text
  
    #Save data for later entry
    title = html.split(taskname1)[1].split(taskname2)[0] #Tasks name
    start = html.split(taskstart)[1].split(date1)[1].split(date2)[0] #Date when the task starts
    end = html.split(taskend)[1].split(date1)[1].split(date2)[0] #Date when the task ends
    description = html.split(textstart)[1].split(textend)[0].replace("\n", "\\n").replace("\"", "") #Task description
    while description.find("<") != -1: #Remove HTML tags
      description = description.split("<")[0] + description.split(">", 1)[1]
    files = 0 #Number of external files attached to the task. Will be increased later if there are files.
    filenames = []
    filelinks = []
  
    try:
      #Use <form> to check if attached files exist.
      html = html.split(att1)[1].split(att2)[0]
  
      #If necessary, download file(s) related to the task and link them correctly
      while html.find(fileurl) != -1:
  
        #Determine file data
        fileend = html.split(fileend1)[0].rsplit(".", 1)[1].split(fileend2)[0]
        filelink = "https://" + server + html.split(file1)[1].split("\"")[0]
  
        #Add file data to the array
        files = files + 1
        filenames.append(html.split(".png\">")[1].split("</a></td>")[0])
        filelinks.append(datafolder.replace('\\', '\\\\') + filelink.split("/")[7] + "." + fileend)
  
        #Download and save external file
        download["text"] = "Externe Datei wird heruntergeladen..."
        main.update()
        print("Externe Datei wird heruntergeladen...")
        with open(datafolder + filelink.split("/")[7] + "." + fileend, "wb") as f:
          f.write(session.get(filelink).content)
  
        #Replace HTML (if you have several files, do not download the same file again or mix up other things).
        html = html.replace(file1, "|", 1).replace(fileurl, "|", 1).replace(fileend1, "|", 1).replace(".png\">", "|", 1)
        download["text"] = ""
  
    except:
      pass
  
    #Note in JSON variable
    json.append("{\n\"title\": \"" + title + "\",\n\"start\": \"" + start + "\",\n\"end\": \"" + end + "\",\n\"description\": \"" + description + "\",\n\"files\": " + str(files))
    if files != 0:
      json[-1] = json[-1] + ",\n\"filedetails\": [\n"
      for i in range(files):
        json[-1] = json[-1] + "{\"name\": \"" + filenames[i] + "\",\n\"link\": \"" + filelinks[i] + "\"},\n"
      json[-1] = json[-1].rsplit(",", 1)[0] + "\n]"
    json[-1] = json[-1] + "\n}"
    progress["value"] = progress["value"]+1
  
  #Write overview
  status["text"] = "Schreibe in JSON-Datei..."
  main.update()
  print("Schreibe in JSON-Datei...")
  if not os.path.exists(datafolder + "tasks.json"):
    with open(datafolder + "tasks.json", "w") as f:
      f.write("{\n\"tasks\": 0\n}")
  oldjson = open(datafolder + "tasks.json").read().rsplit("\n}", 1)[0]
  tasks = int(oldjson.split("\"tasks\": ")[1].split(",")[0])
  for i in range(len(json)):
    oldjson = oldjson + ",\n\"" + str(i+tasks) + "\": " + json[i]
  
  #Write JSON to tasks.json
  with open(datafolder + "tasks.json", "w") as f:
    f.write(oldjson.replace(str(tasks), str(tasks+len(json)), 1) + "\n}")
  main.destroy()
