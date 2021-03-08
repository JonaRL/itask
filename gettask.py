from tkinter import *
import requests
import sys
import os

def func_main(datafolder):
  print("IServ Task Downloader v0.1.0 by JonaRL - Module: Downloader")

  main = Tk()
  main.geometry("500x200")
  main.title("Herunterladen...")

  status = Label(main, font='Helvetica 11 bold', pady=4, padx=4, text="Statusanzeige")
  status.grid(row=0, column=0)
  main.update()

  #Benutzerdaten auslesen
  datafolder = os.path.join(datafolder, "")
  usrdata = open(os.path.join(datafolder, "user.data")).read()
  server = usrdata.split("server:")[1].split(";")[0]
  username = usrdata.split("username:")[1].split(";")[0]
  password = usrdata.split("password:")[1].split(";")[0]
  taskfilter = usrdata.split("taskfilter:")[1].split(";")[0]
  
  #Variablen definieren
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
  table1 = "<tbody class=\"bb0\">"
  table2 = "</tbody>"
  html1 = "<html>\n<head>\n<meta locale=\"utf-8\">\n<style>\ntable, th, td {\nborder: 1px solid black;\nborder-collapse: collapse;\npadding: 8px;\n}\n</style>\n</head>\n<body>\n<table>\n<tbody>"
  html2 = "</tbody>\n</table>\n</body>\n</html>"
  taskname1 = "<h1>Details zu "
  taskname2 = "</h1>"
  taskstart = "<th>Starttermin:</th>"
  taskend = "<th>Abgabetermin:</th>"
  textstart = "<div class=\"text-break-word p-3\">"
  textend = "</div>"
  fileurl = "/iserv/fs/file/exercise-dl/"
  file1 = "<a href=\""
  #file2 = "\">"
  date1 = "<td>"
  date2 = "</td>"
  headers = {'User-Agent': 'Mozilla/5.0'} #User-Agent (Browser) festlegen
  credits = {'_username': username, '_password': password} #Login-Daten festlegen
  
  #Verbindung aufbauen
  status["text"] = "Verbinde zu IServ..."
  main.update()
  print("Verbinde zu IServ...")
  session = requests.Session()
  session.post('https://' + server + '/iserv/login_check', headers=headers, data=credits)
  
  #Aufgaben herunterladen
  status["text"] = "Aufgabenliste wird geladen..."
  main.update()
  print("Aufgabenliste wird geladen...")
  html = session.get("https://" + server + "/iserv/exercise?filter[status]=" + taskfilter).text
  
  #Aufgabenlinks extrahieren
  i = int(len(html.split(url1))-1)
  searchtml = html
  
  #Extrahierte Links in Arrays indexieren
  for ii in range(i):
    tasks.append(searchtml.split(url1)[1].split(url2)[0]) #Link an die Liste aller Aufgaben anfügen
    newtasks.append(searchtml.split(url1)[1].split(url2)[0]) #Link an die Liste neuer Aufgaben anfügen (Ist die Aufgabe nicht neu, wird der Link hier später wieder entfernt)
    searchtml = html.split(name)[ii+1] #Zu durchsuchendes HTML begrenzen, damit nicht der selbe Link erneut indexiert wird
  
  #Prüfen, welche Aufgaben neu sind und welche bereits heruntergeladen wurden
  try:
    oldtasks = open(datafolder + "tasks.list", "r").read()
    for i in range(len(tasks)):
      if oldtasks.find(tasks[i]) != -1:
        newtasks.remove(tasks[i])
      else:
        with open(datafolder + "tasks.list", "a") as f:
          f.write(tasks[i] + "\n")
  except: #Sollte das Programm zum ersten Mal gestartet werden und es noch keine Liste geben, gibt es einen Fehler.
  
    #Alle Aufgaben in die Liste aller Aufgaben schreiben
    for i in range(len(tasks)):
      with open(datafolder + "tasks.list", "a") as f:
        f.write(tasks[i] + "\n")
  
  #Ausgeben, wie viele Aufgaben heruntergeladen wurden und wie viele davon neu sind
  status["text"] = str(len(tasks)) + " Aufgaben gefunden, davon " + str(len(newtasks)) + " neue."
  main.update()
  print(str(len(tasks)) + " Aufgaben gefunden, davon " + str(len(newtasks)) + " neue.")
  tasks = newtasks #Für die weitere Bearbeitung nur die neuen Aufgaben berücksichtigen
  tasks = sorted(tasks) #Aufgaben nach ID bzw. Erstelldatum sortieren
  
  #Aufgabe herunterladen
  for i in range(len(tasks)):
    status["text"] = "Lade Aufgabe " + str(i+1) + " von " + str(len(tasks)) + "..."
    main.update()
    print("Lade Aufgabe " + str(i+1) + " von " + str(len(tasks)) + "...")
    html = session.get(tasks[i]).text
  
    #Daten fürs spätere Eintragen speichern
    title = html.split(taskname1)[1].split(taskname2)[0] #Name der Aufgaben
    start = html.split(taskstart)[1].split(date1)[1].split(date2)[0] #Datum, an dem die Aufgabe beginnt
    end = html.split(taskend)[1].split(date1)[1].split(date2)[0] #Datum, an dem die Aufgabe endet
    description = html.split(textstart)[1].split(textend)[0].replace("\n", "\\n").replace("\"", "") #Aufgabenbeschreibung
    while description.find("<") != -1: #HTML-Tags entfernen
      description = description.split("<")[0] + description.split(">", 1)[1]
    files = 0 #Anzahl von externen Dateien, die der Aufgabe anhängen. Wird erhöht, wenn es Dateien gibt.
    filenames = []
    filelinks = []
  
    try:
      #Mit <form> prüfen, ob ein Download existiert.
      html = html.split("<form name=\"iserv_exercise_attachment\"")[1].split("</form>")[0]
  
      #Wenn nötig, zur Aufgabe zugehörige Datei(en) herunterladen und korrekt verlinken
      while html.find(fileurl) != -1:
  
        #Dateidaten ermitteln
        fileend = html.split("<span class=\"text-muted\">")[0].rsplit(".", 1)[1].split("</a>")[0]
        filelink = "https://" + server + html.split(file1)[1].split("\"")[0]
  
        #Dateidaten den Arrays hinzufügen
        files = files + 1
        filenames.append(html.split(".png\">")[1].split("</a></td>")[0])
        filelinks.append(datafolder + filelink.split("/")[7] + "." + fileend) 
  
        #Externe Datei speichern
        status["text"] = "Externe Datei wird heruntergeladen... (Dies kann einen Moment dauern)"
        main.update()
        print("Externe Datei wird heruntergeladen... (Dies kann einen Moment dauern)")
        with open(datafolder + filelink.split("/")[7] + "." + fileend, "wb") as f:
          f.write(session.get(filelink).content)
  
        #HTML replacen (bei mehreren Dateien nicht noch einmal die selbe Datei herunterladen oder andere Dinge verwechseln).
        html = html.replace(file1, "|", 1).replace(fileurl, "|", 1).replace("<span class=\"text-muted\">", "|", 1).replace(".png\">", "|", 1)
  
    except:
      pass
  
    #In JSON-Variable vermerken
    json.append("{\n\"title\": \"" + title + "\",\n\"start\": \"" + start + "\",\n\"end\": \"" + end + "\",\n\"description\": \"" + description + "\",\n\"files\": " + str(files))
    if files != 0:
      json[-1] = json[-1] + ",\n\"filedetails\": [\n"
      for i in range(files):
        json[-1] = json[-1] + "{\"name\": \"" + filenames[i] + "\",\n\"link\": \"" + filelinks[i] + "\"},\n"
      json[-1] = json[-1].rsplit(",", 1)[0] + "\n]"
    json[-1] = json[-1] + "\n}"
  
  #Übersicht schreiben
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
  
  #JSON schreiben
  with open(datafolder + "tasks.json", "w") as f:
    f.write(oldjson.replace(str(tasks), str(tasks+len(json)), 1) + "\n}")
  main.destroy()
