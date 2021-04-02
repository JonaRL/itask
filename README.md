# ITask

Der "IServ Task Downloader" - kurz "ITask" - ist ein Tool zum automatisierten Herunterladen von IServ-Aufgaben und zugehörigen Dateien, um das Bearbeiten auch offline oder in anderen Situationen, in denen IServ nicht erreichbar ist, möglich zu machen.


## Features
**Aktuell bietet ITask bereits folgende Funktionen:**

- Komplette Bedienung über eine grafische Oberfläche
- Automatisiertes Herunterladen von Aufgaben und zugehörigen Dateien
- Darstellung aller heruntergeladenen Aufgaben in einer übersichtlichen Tabelle
- Unterstützung der IServ-Filtermöglichkeiten (current/past/all)
- Speicherung, welche Aufgaben heruntergeladen wurden (Es werden nicht jedes Mal alle Aufgaben heruntergeladen, sondern lediglich neue)
- Einrichtungsassistent

**Folgende Dinge sind zukünftig geplant:**
- Unterstützung von Backups

## Installation
Die neueste Version von ITask/itask.py kann unter [Releases](https://github.com/JonaRL/itask/releases) als .deb oder .AppImage (für Linux-Systeme) und .exe (für Windows-Systeme) heruntergeladen und so auf allen unterstützen Betriebssystemen ausgeführt werden. Für andere Betriebssysteme wird derzeit noch keine einfache Installationslösung angeboten, allerdings kann das Programm natürlich auch im Sourcecode heruntergeladen und anschließend mit dem jeweiligen Python3-Interpreter des Systems in der Kommandozeile ausgeführt werden. 

>In den gängigen Betriebssystemen geschieht das meist mit folgendem Befehl:
>`python3 itask.py`

### Hinweise

>Zum Ausführen des Programms als .deb müssen die python3-Librarys *requests* und *tkinter* installiert sein. Dies kann unter vielen Linux-Distributionen beispielsweise folgendermaßen erfolgen:
>`sudo apt install python3-requests python3-tk`

> Unter Linux-Betriebssystemen speichert ITask Daten unter /home/$USER/.itask, auf Windows-Systemen werden diese Daten im Ordner C:\users\$USER\AppData\ITask abgelegt. Auf anderen Systemen wird dort, wo das Programm ausgeführt wird, ein entsprechender Ordner erstellt.
