---
name: spanisch-app
description: >
  Arbeitsanweisungen für Miros selbstgebaute Spanisch-Lern-PWA im GitHub-Repo
  themyr97/claude-spanish-appo (Vokabeln, Konjugationstabellen, Hörübungen,
  Karteikarten, Sprechübung). Diesen Skill aufrufen, BEVOR an der App
  gearbeitet wird: bei Wünschen wie «aktualisiere meine App», «füge die neuen
  Wörter hinzu», «bau eine Funktion ein», «die App zeigt X falsch an»,
  «Fortschritt wird nicht gespeichert», sowie bei jeder Änderung an Vokabeln,
  Konjugationen, Übungssätzen oder Deployment. Enthält Deployment-Ablauf,
  Verifikationspflichten, bekannte Fehlerquellen und Prüfschritte vor dem
  Hinzufügen von Verben. NICHT für den Spanischunterricht selbst (Lektionen,
  Korrekturen) — dafür gilt LERNSTAND.md im selben Repo.
---

# Spanisch-App — Arbeitsanweisungen

## Grundregeln

1. **Vor dem Hinzufügen neuer Funktionen immer zuerst fragen.** Ausdrückliche
   Vorgabe von Miro. Vokabel- und Inhaltsupdates auf Wunsch sind davon
   ausgenommen. Bei Funktionswünschen zuerst Rückfragen zur Ausgestaltung
   stellen (Umfang, Form, Verhalten bei Filtern), dann bauen.
2. **Nichts behaupten, was nicht geprüft wurde.** Ein HTTP 200 beim Upload ist
   kein Beweis, dass die richtige Datei live ist — siehe Verifikation.
3. **Fokus lateinamerikanisches Spanisch (Mexiko).** *vosotros* nur als
   Referenz anzeigen, nie abfragen. Standardstimme mexikanisch (Paulina;
   Mónica ist die Spanien-Stimme).
4. **Antwortsprache Deutsch**, spanische Beispiele im Original.

## Repo und Struktur

- Repo: `themyr97/claude-spanish-appo`, öffentlich, GitHub Pages
- Live: `https://themyr97.github.io/claude-spanish-appo/`
- Wurzel = ausgelieferte Version; `/v1/`…`/vN/` = Archiv jeder Version
- `README.md` = Changelog, `LERNSTAND.md` = Lernfortschritt
- Die App ist **eine einzelne HTML-Datei** mit eingebettetem CSS und JS

Lesen ohne Token (immer möglich):
`https://raw.githubusercontent.com/themyr97/claude-spanish-appo/main/index.html`
Achtung: Diese URL wird vom CDN gecacht und kann veraltet sein — zum
Verifizieren die API verwenden.

## Ablauf jeder Änderung

1. Aktuellen Stand frisch aus dem Repo holen (nie auf lokale Reste vertrauen,
   das Sandbox-Dateisystem wird zwischen Sitzungen gelöscht)
2. Änderung anwenden
3. **Versionsnummer an zwei Stellen erhöhen** — `APP_VERSION` in
   `service-worker.js` UND das Badge in `index.html`. Wird der Service Worker
   nicht geändert, erreicht das Update das Handy nie; wird das Badge vergessen,
   zeigt die App eine falsche Version an.
4. Syntaxprüfung aller `<script>`-Blöcke mit Node
5. Logik testen (siehe Prüfpflichten)
6. README-Changelog ergänzen
7. Deployment mit `scripts/deploy.py` (nicht von Hand)
8. Über die API gegenprüfen

## Prüfpflichten vor dem Hinzufügen von Vokabeln

**Verben:** Jedes neue Verb durch `conjugate()` laufen lassen und die Ausgabe
lesen, bevor es aufgenommen wird. Die regelmässigen Regeln erzeugen bei
unregelmässigen Verben Nichtwörter (*pedo, trao, penso, deco, vo, pono, leió*).
Wenn falsch → Eintrag in `irregular` von Hand schreiben, mit `note`.

**Reflexive Verben (`-se`):** `conjugate()` liefert `null`. Nicht als Verb
aufnehmen, sonst zeigt die App eine leere Tabelle. In «Phrases» aufnehmen
(z.B. *no te preocupes*), bis Reflexive im Unterricht behandelt sind.

**Duplikate:** Vor dem Anhängen prüfen, ob das Wort schon existiert. In v13
landeten *rico* und *ocupado* doppelt in derselben Kategorie.

**Datum:** Neue Wörter in die `addedAt`-Tabelle eintragen (ISO-Datum), sonst
erscheinen sie nicht im Nuevas-Modus.

**Nach jeder Vokabeländerung:** Gesamtzahl, Duplikate und `null`-Konjugationen
prüfen.

## Verifikation nach dem Deployment

Verbindlich, in dieser Reihenfolge:

1. Datei über die **API** zurückladen (`Accept: application/vnd.github.raw`)
   und byteweise mit der lokalen Datei vergleichen
2. Badge und `APP_VERSION` in der zurückgeladenen Datei prüfen
3. Neue Funktion im Live-Text suchen (z.B. `grep -c renderMissList`)

**Nicht verifizierbar:** `github.io` ist aus der Sandbox nicht erreichbar
(HTTP 403 durch den Egress-Proxy). Ob das Handy die neue Version zieht, kann
nur Miro am Badge sehen. Das offen sagen, nicht so tun, als sei es geprüft.

## Token

Schreibzugriff braucht einen Fine-grained PAT (Contents: Read and write,
nur dieses Repo). Tokens laufen nach ~90 Tagen ab; der erste ist im August
2026 abgelaufen. Bei HTTP 401: Miro um einen neuen Token bitten und erklären,
wie er ihn erstellt. Lesen funktioniert weiterhin ohne Token, es lässt sich
also immer Auskunft geben, auch wenn gerade nicht geschrieben werden kann.
Token niemals in Dateien oder ins Gedächtnis schreiben.

## Weiterführende Dateien

- `references/bekannte-probleme.md` — offene Bugs und frühere Fehlschläge,
  vor Debugging lesen
- `references/architektur.md` — Aufbau der App, Speicherformat, Funktionsnamen
- `scripts/deploy.py` — Upload inklusive Archiv und Verifikation
