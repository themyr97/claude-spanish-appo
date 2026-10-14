# Bekannte Probleme und frühere Fehlschläge

Vor dem Debuggen lesen. Alle Punkte sind belegt, nicht vermutet.

## Stand v24 (14.10.2026)

- Der **Escucha-Fehler** (ein Buchstabe gilt als richtig) betrifft seit v24
  nur noch die klassische Ansicht `/v23/`, nicht mehr die Haupt-App. Beim
  Wiedereinbau des Hörens in Phase 2 nicht übernehmen.
- **`/mnt/skills/user` wird zurückgesetzt, samt `scripts/`.** Beim
  Wiederherstellen immer den ganzen Ordner `skill/` aus dem Repo holen, nicht
  nur `SKILL.md` — am 14.10. fehlte dadurch `deploy.py`.
- **deploy.py lud Manifest und Symbole nur ins Archiv**, nie in die Wurzel.
  Bemerkt bei v24, als das neue Symbol nicht live ging. Seit 14.10. behoben.
- `¿Qué desean tomar?` steht weiter in zwei Kategorien; die Karte existiert
  einmal (Duplikate werden beim Aufbau entfernt), in der Kategorie
  «Restaurante (formal)» fehlt sie dadurch.

## Offen — noch nicht behoben

### Escucha-Tab wertet fast alles als richtig (nur noch in /v23/)
`checkBtn.onclick` prüft mit
`correctAns.includes(userAns) || userAns.includes(correctAns)`.
Getestet: Die Eingabe **«a»** wird bei jedem Satz als richtig gewertet, ebenso
«is a and I am». Damit ist der Hörtab als Übung wertlos. Der Sprechtab
(`bestMatch`) hat diesen Fehler **nicht** — dort liegt der Schwellwert bei 0.6
der Zielwörter. Behebung würde einen echten Wortabgleich brauchen.
Miro ist informiert; nicht ungefragt umbauen.

### Karteikarten-Fortschritt vor v4 verwaist
Mit den Genusartikeln änderte sich der Speicherschlüssel von `"trabajo"` zu
`"el trabajo"`. Alte Fehlerzähler aus v1–v3 liegen noch im Speicher, passen
aber zu keinem Wort mehr.

### `¿Qué desean tomar?` steht in zwei Kategorien
Bewusst belassen (Phrases und Restaurant formal). Kein Fehler, aber es
verfälscht die Gesamtzahl der Einträge.

### Reflexive Verben
`conjugate()` gibt bei `-se`-Infinitiven `null` zurück. Reflexive daher nicht
als Verb aufnehmen. Ein Ausbau wäre nötig, sobald Reflexive im Unterricht
drankommen.

## Behoben — zur Warnung dokumentiert

### Service Worker lieferte ewig die alte Version (v1–v2)
Cache-first für alles, inklusive `index.html`, und der Service Worker selbst
wurde nie geändert. Das Handy blieb auf v1 hängen. Seit v3: network-first für
HTML, versionierter Cache-Name, Update-Prüfung beim Start.
**Lehre:** `APP_VERSION` muss sich bei jedem Deployment ändern.

### Spracherkennung — drei Fehlversuche
v8–v10 gingen von falschen Ursachen aus (fehlende Berechtigung,
Standalone-Sperre). Die echte Ursache war ein Konflikt der Audio-Session:
Text-to-Speech und Erkennung teilen sie sich, und laufendes TTS killt die
Erkennung ohne Fehlermeldung. Zusätzlich verschluckt WebKit die ersten
Sekunden. Mein eigener `getUserMedia`-Aufruf verschlimmerte es.
Behoben in v11: TTS vorher abbrechen, 350 ms warten, 2-Sekunden-Countdown,
kein `getUserMedia` im Hörpfad.
**Lehre:** Bei unklarer Ursache Diagnose einbauen, statt Hypothesen zu deployen.

### «Lo sé» speicherte nichts (bis v17)
Der Knopf veränderte nur Zustandsvariablen, ohne `saveProgress()`. Nur
`missCounts` wurde je gespeichert. Seit v17 wird die ganze Sitzung gesichert.

### Nichtwörter durch fehlende Konjugationstabellen
Zweimal aufgetreten: *pedo, trao, penso, recomendo, encontro* (v13) und
*deco, vo, pono, salo, seguo, entendo, leió* (v19). Beide Male vor dem
Deployment durch Ausgabeprüfung gefunden.

### Doppelte Einträge
*rico* und *ocupado* seit v13 doppelt in den Adjektiven, erst in v21 bemerkt.

### Teil-Deployment durch Shell-Limit
`index.html` als Argument an `python3` zu übergeben scheitert an ARG_MAX
(«Argument list too long»). Einmal war der Service Worker aktualisiert, die
HTML-Datei aber nicht — der gefährlichste Zustand, weil die Version stimmt und
der Inhalt nicht. `scripts/deploy.py` schreibt den Body deshalb in eine Datei.

## Irreführende Prüfungen

- **`raw.githubusercontent.com`** liefert gecachte Stände; zeigte nach einem
  erfolgreichen Upload noch die Vorversion. Zum Verifizieren die API nehmen.
- **`github.io`** ist aus der Sandbox gesperrt (HTTP 403 vom Egress-Proxy).
  Was das Handy sieht, lässt sich von hier aus nicht feststellen.
