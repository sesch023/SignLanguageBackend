# SignLanguageBackend
Dieses Backend gibt Zugriff auf verschiedene CNN Modelle zur Klassifikation
von Gebärdensprache. Die Modelle werden dabei entweder im FileStorage oder 
Base64 kodierter String in den Postdaten eines Requests übermittelt. Danach
wird es auf verschiedene Arten vorverarbeitet und klassifiziert. Weiterhin gibt 
das Backend Informationen zu verfügbaren Modellen und ihren URLs.
## Installation
Das Backend wurde unter Debian 10 und Linux Mint 19 getestet sowie entwickelt. 
Um möglichen Inkompatibilitäten aus dem Weg zu gehen, werden diese als Betriebssystem
empohlen.
1. Installation von essentiellen Paketen mit: apt-get install build-essential python
2. Installation von Conda oder einem anderen Python Umgebungsmanager.
3. Falls Conda genutzt wird, Installation von uwsgi über folgendee Befehle: 
    - conda config --add channels conda-forge
    - conda install uwsgi 
4. Erstellen einer neuen Python 3.8 Umgebung.
5. Installation der Anforderungen aus der requirements.txt mit PIP.
6. Anpassen des virtualenv Parameters in der sign_language.ini. Wird uwsgi direkt aus der Python Umgebung
   gestartet, so kann diese auskommentiert oder entfernt werden.
7. Starten des UWSGI-Servers aus dem Hauptverzeichnis der Anwendung mit: uwsgi --ini sign_language.ini

Aus diesem Befehl resultiert eine sign_language.sock Datei, auf welche beispielsweise mit NGINX Zugriff 
gewährt werden kann. Wahlweise lässt sich die API auch unter https://jupiter.fh-swf.de/sign-language/ aufrufen, 
wo die neueste Version gehostet ist.
