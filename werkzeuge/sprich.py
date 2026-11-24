# Nutzung: python3 sprich.py STIMME TEXTDATEI AUSGABE.mp3
import sys, certifi
certifi.where = lambda: '/root/.ccr/ca-bundle.crt'
import asyncio, edge_tts
v, tf, out = sys.argv[1:4]
asyncio.run(edge_tts.Communicate(open(tf, encoding='utf-8').read(), v, rate='+0%').save(out))
