# Aufbau der App

Eine Datei, `index.html`, mit eingebettetem CSS und JS. Daneben
`service-worker.js`, `manifest.json`, zwei Icons.

## Tabs

| Tab | Inhalt |
|---|---|
| Vocabulario | Kartenraster nach Kategorie, Suche, Kategoriefilter, Konjugationstabellen (v-Knopf), Audio |
| Escucha | Hörsätze abspielen, englische Bedeutung eintippen |
| Tarjetas | Karteikarten: Todas / Difíciles / Nuevas, Kategoriezyklus, Richtungswechsel, Fehlerwortliste |
| Conjugar | Verb + Pronomen + Zeit vorgeben, Form eintippen |
| Hablar | Englischer Satz, Antwort auf Spanisch sprechen (oder tippen) |

Die Navigation ist ein 3-Spalten-Raster und bricht um.

## Zentrale Datenstrukturen

- `data` — Vokabeln nach Kategorie; Substantive `[es, en, genus]`, sonst `[es, en]`.
  Genus: `m`, `f`, oder `f-el` (*el agua*, feminin mit männlichem Artikel)
- `irregular` — handgeschriebene Konjugationen, 6 Personen, `pres` und `pret`, plus `note`
- `addedAt` — Wort → ISO-Datum, steuert den Nuevas-Modus
- `speakSentences` — englischer Satz → Liste akzeptierter spanischer Antworten
- `listeningExercises` — spanischer Satz → englische Bedeutung
- `categoryShortLabels` — Kurzbeschriftungen für die Filterknöpfe

## Wichtige Funktionen

`conjugate(inf)` · `buildFcPool()` · `startFcDeck(mode)` · `renderFc()` ·
`renderMissList()` · `buildSessionSnapshot()` / `restoreSession()` ·
`speak(text, rate, cardEl, onEnd)` · `startListening()` · `renderSpeechDiagnostics()`

## Speicherung

Zwei Schlüssel im `localStorage`:

- `flashcard-progress` — `{missCounts, savedAt, session:{deckKeys, index, known, mode, category, spanishFront}}`
  Das Deck speichert **Schlüssel, keine Kartenobjekte**, und wird beim Laden
  gegen den aktuellen Wortschatz neu aufgebaut: entfernte Wörter fallen weg,
  Indizes werden begrenzt, ein unbrauchbares Deck wird neu gemischt.
- `conjugation-drill-progress` — `{drillMistakes, drillRight, drillTotal, savedAt}`

Die Chat-Artefakt-Fassung benutzt `window.storage` statt `localStorage` —
beim Patchen beider Dateien unterscheiden sich diese Stellen.

## Sprachausgabe und -erkennung

Stimmenwahl: Paulina → irgendeine `es-MX` → `es-US` → Mónica → erste spanische.
Die Erkennungssprache ist **getrennt** einstellbar (México/España/EE.UU.,
Standard `es-MX`) und folgt bewusst nicht der Vorlesestimme.
