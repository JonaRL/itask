# ITask

Der "IServ Task Downloader" - kurz "ITask" - ist ein Tool zum automatisierten Herunterladen von IServ-Aufgaben und zugehörigen Dateien, um das Bearbeiten auch offline oder in anderen Situationen, in denen IServ nicht erreichbar ist, möglich zu machen.


## Features
**Aktuell bietet ITask bereits folgende Funktionen:**

- Automatisiertes Herunterladen von Aufgaben und zugehörigen Dateien
- Darstellung aller heruntergeladenen Aufgaben in einem HTML-Tabellendokument
- Unterstützung der IServ-Filtermöglichkeiten (current/past/all)
- Speicherung, welche Aufgaben heruntergeladen wurden (Es werden nicht jedes Mal alle Aufgaben heruntergeladen, sondern lediglich neue)
- Einrichtungsassistent

**Folgende Dinge sind zukünftig geplant:**
- Grafische Benutzeroberfläche
- Sortierfunktion für die Übersichtstabelle

## Installation

Die neueste Version von ITask/itask.py kann unter [Releases](https://github.com/JonaRL/itask/releases) heruntergeladen und anschließend mit dem jeweiligen Python3-Interpreter des Systems in der Kommandozeile heruntergeladen werden. 
>In den gängigen Betriebssystemen geschieht das meist mit folgendem Befehl:
`python3 itask.py`

### Hinweise
>Zum Ausführen des Programms muss die python3-Library *requests* installiert sein. Dies kann unter vielen Linux-Distributionen beispielsweise folgendermaßen erfolgen:
>`sudo pip3 install requests`

> Alle Ordner, die in der Konfigurationsdatei angegeben werden, müssen bereits zuvor vom Nutzer erstellt worden sein
