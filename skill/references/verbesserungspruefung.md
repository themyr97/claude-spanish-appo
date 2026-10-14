# Verbesserungsprüfung: Spanisch-App und Lernmethode

Entstanden am 14.10.2026 auf Basis eines Beitrags über vier Arten von
Ambition im Umgang mit KI (Geschwindigkeit, Höhe, Tiefe, Breite). Aufrufen,
wenn Miro eine grundsätzliche Verbesserung von App oder Lernmethode will —
nicht für einzelne Vokabel- oder Fehlerkorrekturen.

Lies zuerst `skill/SKILL.md`, `skill/references/bekannte-probleme.md` und
`LERNSTAND.md` — **über die API, nicht über raw**. Dann vier Schritte.
**Nichts umsetzen:** Das Ergebnis ist eine priorisierte Liste mit
Rückfragen. Für jede neue Funktion gilt Miros Regel: erst fragen.

## 0. Rohmaterial, bevor du urteilst

Nicht auf eigene Zusammenfassungen verlassen. Hole:
- alle Übungen mit Miros Originalantworten aus den früheren Chats
  (`conversation_search`: «Ejercicio», «Tú:»)
- die aktuelle App aus dem Repo, alle Vokabeln und Konjugationen
- Miros exportierten App-Fortschritt, falls vorhanden. Falls nicht: als
  Lücke benennen.

Zähle die Fehler nach Kategorie aus den Rohantworten. Prüfe dann gegen
LERNSTAND: Stimmen meine Einschätzungen mit den Zahlen überein? Welche Muster
habe ich nach nur einer fehlerfreien Runde als «behoben» verbucht?

## 1. Höhe — das Ziel hinter dem Ziel

- Frage Miro, wofür er Spanisch lernt und bis wann. Schlage danach ein
  konkretes, hartes, messbares Ziel vor (z. B.: zehn Minuten Gespräch über
  Alltag und Vergangenheit, ohne Deutsch und ohne Nachschlagen, bis Datum X).
- Finde Schritte, die Miro heute manuell auslöst und die ein dauerhafter
  Ablauf übernehmen könnte. Bekannt: LERNSTAND und App sind getrennt. Was
  müsste sich am Ablauf ändern, damit Übungsfehler in die App fliessen und
  App-Daten zu mir?

## 2. Tiefe — was eine Spitzenfachperson anders machen würde

Vor jedem Vorschlag beantworten:
1. Was würde eine führende Fachperson für Zweitspracherwerb hier tun, das
   wir nicht tun?
2. Von welchem Rohmaterial würde sie ausgehen?
3. Welche Verfahren und Werkzeuge würde sie einsetzen? (Ansatzpunkte:
   Wiederholungsalgorithmen wie FSRS statt eines Zählers, der nie vergisst;
   Produktion vor Erkennen; verstehbarer Input; Interleaving.)
4. Was — ausser dir oder mir — zeigt, dass ein Ergebnis stimmt?

Für Punkt 4 je einen externen Prüfer finden:
- **Konjugationen:** automatisch gegen eine externe Quelle oder Bibliothek
  prüfen, nicht per Augenschein (die Regeln erzeugten schon *pedo, trao, deco*).
- **Lernstand:** an CEFR-Kannbeschreibungen oder DELE-A1/A2-Aufgaben messen,
  nicht an «bester Durchgang bisher».
- **«Behoben»:** erst nach mehreren fehlerfreien Runden in verschiedenen
  Übungen, mit zeitlichem Abstand.

## 3. Breite — welche Fächer gehören dazu

Die App als Verb: *einem vielbeschäftigten Juristen helfen, im echten
Gespräch unter Zeitdruck das richtige Wort abzurufen.* Leite daraus die
Fächer ab und **tu, was diese Fachleute tun — keine Rollen spielen:**
- Gedächtnisforschung: Abstände, Abrufübung, erwünschte Schwierigkeiten
- Korpuslinguistik: Häufigkeit, Wortverbindungen statt Einzelwörter
- Gewohnheitsdesign: kurzer täglicher Ablauf mit wenig Reibung
- Phonetik: die Hablar-Prüfung vergleicht bisher nur Wörter, nicht die Aussprache
- Nutzungsforschung: Welche Tabs nutzt Miro tatsächlich? Messen statt vermuten.
- Red Team: Bringt die App-Arbeit Miro zum Sprechen, oder entsteht vor allem
  eine schönere App?

Auch prüfen, was aus Miros eigenem Fach übertragbar ist — er arbeitet gern
mit festen Schemata.

## 4. Ergebnis

Höchstens acht Vorschläge, sortiert nach Nutzen für das Ziel aus Schritt 1.
Pro Vorschlag: was sich ändert (App, Übungsablauf oder beides) ·
Ambitionstyp · externer Prüfer · Aufwand und Risiko · was du von Miro
brauchst. Belegtes (aus Rohdaten gezählt) klar von Vermutetem trennen. Dann
fragen, was umgesetzt werden soll.

## Blinde Flecken, nicht übergehen

- `github.io` ist aus der Sandbox nicht erreichbar — was auf dem Handy
  läuft, sieht nur Miro.
- Der Fortschritt auf dem Handy liegt nur im Browserspeicher und ist
  nirgends gesichert.
- Sandbox und `/mnt/skills/user` werden zurückgesetzt; massgeblich ist das Repo.
