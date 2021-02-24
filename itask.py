import requests
import sys

#NUR Dinge unter dieser Linie ändern!
server = "demo-iserv.de" #Domain des IServ-Servers
username = "user.name" #IServ-Benutzername
password = "password" #IServ-Passwort
index = "/home/user/ITask.html" #Datei, in der alle Aufgaben übersichtlich aufgeführt sind
datafolder = "/home/user/.itask/" #Das Verzeichnis, in dem alle Aufgaben gespeichert werden. Achtung: Dem Verzeichnis MUSS ein "/" nachgestellt sein! Das Verzeichnis muss existieren!
filter = "current" #Bestimmt, welche Aufgaben heruntergeladen werden. Mögliche Werte: current; past; all
#NUR Dinge überhalb dieser Linie ändern!

#Variablen definieren
url1 = "<td class=\"iserv-admin-list-field iserv-admin-list-field-textarea\"><a href=\""
url2 = "\">"
name = "</a></td>"
oldtasks = ""
tasks = []
newtasks = []
title = []
start = []
end = []
table1 = "<tbody class=\"bb0\">"
table2 = "</tbody>"
html1 = "<html>\n<head>\n<meta locale=\"utf-8\">\n<style>\ntable, th, td {\nborder: 1px solid black;\nborder-collapse: collapse;\npadding: 8px;\n}\n</style>\n</head>\n<body>\n<table>\n<tbody>"
html2 = "</tbody>\n</table>\n</body>\n</html>"
taskname1 = "<h1>Details zu "
taskname2 = "</h1>"
taskstart = "<th>Starttermin:</th>"
taskend = "<th>Abgabetermin:</th>"
fileurl = "/iserv/fs/file/exercise-dl/"
file1 = "<td><a href=\""
file2 = "\" target=\"_blank\""
date1 = "<td>"
date2 = "</td>"
headers = {'User-Agent': 'Mozilla/5.0'} #User-Agent (Browser) festlegen
credits = {'_username': username, '_password': password} #Login-Daten festlegen

print("IServ Task Downloader v0.0.5 by JonaRL")

#Den Nutzer benachrichtigen, wenn er nichts konfiguriert hat.
if server == "demo-iserv.de":
  print("Bitte konfiguriere dein Profil im Sourcecode dieses Programms. Andernfalls wird es nicht funktionieren!")
  sys.exit(1) #Programm mit Fehlercode verlassen

#Verbindung aufbauen
print("Verbinde zu IServ...")
session = requests.Session()
session.post('https://' + server + '/iserv/login_check', headers=headers, data=credits)

#Aufgaben herunterladen
print("Aufgabenliste wird geladen...")
html = session.get("https://" + server + "/iserv/exercise?filter[status]=" + filter).text

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
      file_object.write(tasks[i] + "\n")

  #HTML-Index schreiben
  with open(index, 'w') as f:
    f.write(html1.split("\n<tbody>")[0])
    f.write("<tr><th>Aufgabe</th><th>Start</th><th>Abgabe</th></tr>")
    f.write(html2.split("</tbody>\n")[1])

#Ausgeben, wie viele Aufgaben heruntergeladen wurden und wie viele davon neu sind
print(str(len(tasks)) + " Aufgaben gefunden, davon " + str(len(newtasks)) + " neue.")
tasks = newtasks #Für die weitere Bearbeitung nur die neuen Aufgaben berücksichtigen

#Aufgabe herunterladen
for i in range(len(tasks)):
  print("Lade Aufgabe " + str(i+1) + " von " + str(len(tasks)) + "...")
  html = session.get(tasks[i]).text

  #Daten fürs spätere Eintragen in Tabelle speichern
  title.append(html.split(taskname1)[1].split(taskname2)[0]) #Name der Aufgabe
  start.append(html.split(taskstart)[1].split(date1)[1].split(date2)[0]) #Datum, an dem die Aufgabe beginnt
  end.append(html.split(taskend)[1].split(date1)[1].split(date2)[0]) #Datum, an dem die Aufgabe endet

  #Heruntergeladene Aufgabe schreiben
  html = html.split(table1)[1].split(table2)[0]
  with open(datafolder + tasks[i].split("/")[6] + '.html', 'w') as f:
    f.write(html1)
    f.write(html)
    f.write(html2)

  #Wenn nötig, zur Aufgabe zugehörige Datei(en) herunterladen und korrekt verlinken
  while html.find(fileurl) != -1:

    #HTML neu schreiben (Tabelle fixen)
    newtml = open(datafolder + tasks[i].split("/")[6] + '.html', "r").read()
    newtml = newtml.replace("<col width=\"1%\">", "").replace("<th></th>", "")
    newtml = newtml.split("<td class=\"pl0\"><div class=\"dropdown\">")[0] + newtml.split("</div>\n</td>", 1)[1]
    with open(datafolder + tasks[i].split("/")[6] + '.html', 'w') as f:
      f.write(html1)
      f.write(newtml)
      f.write(html2)
 
    #Dateinamenserweiterung ermitteln
    fileend = html.split("<span class=\"text-muted\">")[0].rsplit(".", 1)[1].split("</a></td>")[0]

    #Datei herunterladen
    print("Externe Datei wird heruntergeladen... (Dies kann einen Moment dauern)")
    htmlfile = "https://" + server + html.split(file1)[1].split(file2)[0]
    
    #Link ändern
    data =  open(datafolder + tasks[i].split("/")[6] + '.html', 'r').readlines() #1. Datei einlesen
    for ii in range(len(data)): #2. Dinge ändern
      data[ii] = data[ii].replace(htmlfile.split(server)[1], datafolder + htmlfile.split("/")[7] + "." + fileend)
    with open(datafolder + tasks[i].split("/")[6] + '.html', 'w') as f: #3. Geänderte Datei zurückschreiben
      f.writelines(data)

    #Externe Datei speichern
    with open(datafolder + htmlfile.split("/")[7] + "." + fileend, "wb") as f:
      f.write(session.get(htmlfile).content)

    #HTML replacen (bei mehreren Dateien nicht noch einmal die selbe Datei herunterladen oder andere Dinge verwechseln).
    html = html.replace(file1, "|", 1).replace(file2, "|", 1).replace(fileurl, "|", 1).replace("<span class=\"text-muted\">", "|", 1)

#Übersicht schreiben
print("Schreibe Index...")
oldtasks = open(index, "r").read().split("</table>")[0]
with open(index, 'w') as f:
  f.write(oldtasks)
  for i in range(len(tasks)):
    f.write("<tr><th><a href=\"" + datafolder + tasks[i].split("/")[6] + ".html\">" + title[i] + "</a></th><th>" + start[i] + "</th><th>" + end[i] + "</th></tr>")
  f.write(html2.split("</tbody>\n")[1])
