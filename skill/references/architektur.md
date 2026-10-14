# Aufbau der App (ab v24)

Eine Datei `index.html` mit eingebettetem CSS und JS, dazu `service-worker.js`,
`manifest.json`, `icon-192.png`, `icon-512.png`. Die Quelle ist in zwei Teile
gegliedert, beide in derselben Datei:

1. **Datenblock** (erstes `<script>`): `data`, `irregular`, `nounArticle`,
   `displayForm`, `genderLabel`, `conjugate`, `categoryShortLabels`, `addedAt`,
   `addedDate`, `speakSentences`, `listeningExercises`.
2. **App-Block** (zweites `<script>`): Logik und Ansichten.

Vokabeln ändern = nur den Datenblock anfassen. Prüfpflichten aus SKILL.md gelten.

## Ansichten (untere Leiste)

| Ansicht | Inhalt |
|---|---|
| Hoy | Tagespensum, Ajolote, Trajinera als Fortschritt, Tagesserie, Frase del día, Ajustes |
| Tarjetas | Wiederholungssitzung; im Ruhezustand Kategorien, «Las difíciles», «Las 50 más nuevas», Fehlerwortliste mit Reset |
| Palabras | alle Karten nach Kategorie, Suche, Punkt zeigt Lernstand; Verben öffnen die Tabelle |
| Verbos | Verbliste mit Einordnung, Rückwärtssuche über Formen, Tabelle als Bottom-Sheet |

Escucha, Hablar, Conjugar: nur in der klassischen Ansicht `/v23/` (Link in den
Ajustes). Laut Miro ungenutzt; Phase 2 integriert Hören und Dialoge in Hoy.
`speakSentences` und `listeningExercises` liegen dafür weiter im Datenblock.

## Wiederholungsplanung (SM-2 mit Lernschritten)

`schedule(card, grade, now)` ist eine reine Funktion — gut testbar.
- Zustände: `new` → `learning` (Schritte 1 und 10 min) → `review` →
  bei *Otra vez* `relearning` (10 min) → `review`
- Bewertungen 1–4: Otra vez, Difícil, Bien, Fácil
- Review: `hard = max(ivl+1, ivl·1.2)`, `good = max(hard+1, ivl·ease)`,
  `easy = max(good+1, ivl·ease·1.3)` — die drei sind dadurch nie gleich
- Leichtigkeit: Start 2.5, *Otra vez* −0.2, *Difícil* −0.15, *Fácil* +0.15,
  Minimum 1.3; *Otra vez* halbiert das Intervall und zählt `lapses` hoch
- Neue Karten: Tageslimit `settings.newPerDay` (Standard 20), Reihenfolge nach
  `NEW_ORDER` — Supervivencia zuerst
- Sitzung: fällige Lernkarten zuerst, dann Wiederholungen, jede 4. Karte neu

## Speicher

- `srs-v1`: `{cards:{key:{state,step,ivl,ease,reps,lapses,due}}, day:{date,newDone,reviewsDone},
  streak:{last,count}, settings:{newPerDay,front,theme,voice,autoplay}, migrated}`
- Kartenschlüssel = `displayForm(es, gender)`, also bei Substantiven mit Artikel
  («el trabajo») — derselbe Schlüssel wie im alten Speicher.
- `flashcard-progress` (bis v23): wird beim ersten Start von v24 **einmalig**
  übernommen und **nicht gelöscht**. Wörter mit Fehlern → `review`, heute fällig,
  `ease = 2.5 − 0.15·min(Fehler,5)`, `lapses = Fehler`.
- `conjugation-drill-progress`: nur noch von der klassischen Ansicht benutzt.

## Verbanalyse

`verbInfo(inf)` vergleicht `conjugate()` mit `regularForms()` akzentunabhängig
und ohne vosotros und ordnet ein:
- Präsens: `bota` (yo, tú, él, ellos im Stamm geändert), `yo`, `irregular`
- Pretérito: `fuerte` (yo auf -e, él auf -o, ohne Akzent), `tercera`
  (nur él/ellos), `ortografia` (nur yo), `irregular`

`markDiff()` markiert die Abweichung; Diphthonge werden ganz markiert
(e→**ie**, o/u→**ue**). Reflexive Verben: Basis ohne `-se` konjugieren, Pronomen
davor; dafür stehen `acostar` und `despertar` in `irregular`.
`formIndex()` erlaubt die Suche nach konjugierten Formen.

Getestete Einordnung (Stand v24): 38 Prüfverben, alle korrekt.

## Gestaltung

Tokens auf `:root`, dunkle Werte unter `prefers-color-scheme: dark` und
`[data-theme="dark"]`. Farben tragen Bedeutung: Jacaranda = Stammwechsel,
Cempasúchil = Endungen der starken Präterita, Rosa = Lernkarten, Agua = Aktion.
Schriften Baloo 2 (Titel) und Atkinson Hyperlegible (Text) über Google Fonts —
in der Sandbox nicht ladbar, Screenshots zeigen daher Ersatzschriften.
Ajolote und Trajinera sind Inline-SVG (`ajoloteSVG`, `canalSVG`).

## Prüfen vor dem Deployment

Playwright mit Chromium ist installiert (`PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers`).
Screenshots bei 390 und 320 px, hell und dunkel, und Laufzeitfehler über
`page.on('pageerror')` prüfen. Den Logikteil (alles vor «Ajolote und Kanal»)
mit Node und einem Ersatz-`localStorage` testen.
