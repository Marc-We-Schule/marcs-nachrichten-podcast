# Nutzung: python3 -I podcast.py REPO [AUDIODATEI KAPITEL.json TITEL BESCHREIBUNG ID]
# Fügt optional eine Folge hinzu (folgen/ID.m4a, Kapitel als JSON), löscht Folgen älter als 30 Tage
# aus dem Feed und Ordner, schreibt feed.xml und index.html neu.
import sys, os, json, shutil, subprocess, datetime, html
from email.utils import format_datetime
from zoneinfo import ZoneInfo
BASE='https://raw.githubusercontent.com/Marc-We-Schule/marcs-nachrichten-podcast/main/'
R=sys.argv[1]; os.makedirs(R+'/folgen',exist_ok=True)
lp=R+'/folgen.json'; L=json.load(open(lp,encoding='utf-8')) if os.path.exists(lp) else []
TZ=ZoneInfo('Europe/Berlin')
if len(sys.argv)>2:
    audio,kap,titel,beschr,fid=sys.argv[2:7]
    shutil.copy(audio,f'{R}/folgen/{fid}.m4a')
    shutil.copy(kap,f'{R}/folgen/{fid}.chapters.json')
    dur=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',audio]))
    L=[x for x in L if x['id']!=fid]+[dict(id=fid,titel=titel,beschreibung=beschr,dauer=int(dur),groesse=os.path.getsize(audio),datum=datetime.datetime.now(TZ).isoformat(timespec='seconds'))]
grenze=datetime.datetime.now(TZ)-datetime.timedelta(days=30)
for x in [x for x in L if datetime.datetime.fromisoformat(x['datum'])<grenze]:
    for f in (f"{R}/folgen/{x['id']}.m4a",f"{R}/folgen/{x['id']}.chapters.json"):
        if os.path.exists(f): os.remove(f)
L=[x for x in L if datetime.datetime.fromisoformat(x['datum'])>=grenze]
L.sort(key=lambda x:x['datum'],reverse=True)
json.dump(L,open(lp,'w',encoding='utf-8'),ensure_ascii=False,indent=1)
e=html.escape
items=''.join(f"""
  <item>
   <title>{e(x['titel'])}</title>
   <description>{e(x['beschreibung'])}</description>
   <guid isPermaLink="false">marcs-nachrichten-{x['id']}</guid>
   <pubDate>{format_datetime(datetime.datetime.fromisoformat(x['datum']))}</pubDate>
   <enclosure url="{BASE}folgen/{x['id']}.m4a" length="{x['groesse']}" type="audio/x-m4a"/>
   <itunes:duration>{x['dauer']}</itunes:duration>
   <podcast:chapters url="{BASE}folgen/{x['id']}.chapters.json" type="application/json+chapters"/>
  </item>""" for x in L)
feed=f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd" xmlns:podcast="https://podcastindex.org/namespace/1.0" xmlns:atom="http://www.w3.org/2005/Atom">
 <channel>
  <title>Marcs Nachrichten</title>
  <link>{BASE}</link>
  <atom:link href="{BASE}feed.xml" rel="self" type="application/rss+xml"/>
  <language>de</language>
  <description>Tägliche Nachrichten aus Deutschland, Europa und der Welt, zusammengestellt von Claude (entwickelt von Anthropic) aus vielen Quellen. Computerstimme.</description>
  <itunes:author>Claude für Marc</itunes:author>
  <itunes:image href="{BASE}cover.png"/>
  <itunes:explicit>false</itunes:explicit>
  <itunes:block>Yes</itunes:block>
  <itunes:category text="News"/>{items}
 </channel>
</rss>
"""
open(R+'/feed.xml','w',encoding='utf-8').write(feed)
open(R+'/index.html','w',encoding='utf-8').write(f"""<!DOCTYPE html><html lang="de"><meta charset="utf-8"><meta name="robots" content="noindex"><title>Marcs Nachrichten</title>
<body style="font-family:sans-serif;max-width:40em;margin:2em auto"><h1>Marcs Nachrichten</h1><p>Feed für die Podcast-App: <code>{BASE}feed.xml</code></p><ul>"""+''.join(f"<li><a href='folgen/{x['id']}.m4a'>{e(x['titel'])}</a></li>" for x in L)+"</ul></body></html>\n")
open(R+'/robots.txt','w').write('User-agent: *\nDisallow: /\n')
open(R+'/.nojekyll','w').write('')
print(len(L),'Folgen im Feed')
