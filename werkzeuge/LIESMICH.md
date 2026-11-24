# Werkzeuge

1. `pip install edge-tts` (Stimme: de-DE-ConradNeural).
2. Je Kapitel eine Textdatei, dann `python3 sprich.py de-DE-ConradNeural kapitel.txt kapitel.mp3`.
3. Kapitel mit 1,2 s Pause per ffmpeg zusammenfügen (concat), Kapitelmarken per FFMETADATA, Ausgabe AAC 64k als .m4a; dazu `chapters.json` (Podcasting 2.0).
4. `python3 -I podcast.py REPO AUDIO.m4a chapters.json "Titel" "Beschreibung" JJJJ-MM-TT-HHMM` – fügt die Folge hinzu, entfernt Folgen älter als 30 Tage, schreibt feed.xml und index.html.
5. Commit und Push auf main.
