# Charla-App auf claude.ai (seit 17.10.2026)

**URL:** https://claude.ai/artifact/VGMNXae5DLpgK1TXRAbh8R
**Zweck:** Gesprächsübung für Miros Ziel (Alltagsgespräche). Vokabeln lernt er mit
Anki (3000 häufigste Wörter); die App wiederholt deshalb keine Einzelwörter mehr,
sondern seine eigenen korrigierten Sätze.

## Aufbau

| Ansicht | Inhalt |
|---|---|
| Hoy | Tagesplan: eine Charla + fällige eigene Sätze (10–15 Min., Miros Vorgabe) |
| Charla | 10 Szenen (Café, Taquería, Mercado, Taxi, Calle, Hotel, Fiesta, Fin de semana [Pretérito], Día normal [Reflexivos], Farmacia); Claude spielt eine Person aus Mexiko; ~8 Wechsel; danach Korrekturen |
| Frases | eigene korrigierte Sätze: englische Bedeutung → er sagt/tippt Spanisch → Wortvergleich → Otra vez/Difícil/Bien/Fácil |
| Verbos | dieselben Tabellen wie in v24 (Stiefel, starke Präterita, Rückwärtssuche) |

- **Korrekturen nur am Ende** (Miros Wahl). Format = LERNSTAND-Schema; Zeile 1 ist der Satz
  des Partners, auf den er geantwortet hat.
- **Rettungssätze** als Antippfelder über dem Eingabefeld (¿Mande?, ¿Puede repetir?…);
  der Partner ist angewiesen, darauf wirklich einzugehen. Bewusst **kein** Übersetzen-Knopf.
- Sprechen über das Mikrofon der iPhone-Tastatur; die Partnerstimme über speechSynthesis
  (ob sie im claude.ai-Betrachter funktioniert, ist ungeprüft — Knöpfe blenden sich aus,
  wenn nicht verfügbar).
- Partnerniveau einstellbar: Más fácil (A1), Normal (A1–A2), Más reto (A2–B1).

## Technik

- Capabilities: `sample` (Claude als Partner und Korrektor), `db`, `user`.
- Kein Systemprompt möglich: die Spielregeln (`rulesFor`) gehen als erste user-Nachricht mit;
  ab Miros 8. Antwort enthalten sie die Anweisung, sich zu verabschieden.
- Partner: `sample(turns, {cache:false})`; Korrektur: `sample.json(prompt, {cache:false})`,
  Ergebnis wird mit `validCorrections` geprüft (leere Fehler raus, fehlende Felder leer).
- Fehlercodes: dauerhafte (`not_granted` u.a.) sperren die Funktion mit Hinweis; nie
  automatisch wiederholen, nur per «Reintentar».
- Ohne `window.claude` (z.B. Datei lokal geöffnet): Hinweis, Start-Knopf deaktiviert.

## Daten — privat unter `data/users/<id>/`

| Dokument | Inhalt |
|---|---|
| `state` | Tageszähler, Serie, Szenenzähler, Einstellungen |
| `c_<zeit>` (`kind:"convo"`) | Szene, Verlauf `turns:[{r:'p'|'m', t}]`, `items` (Korrekturen), `tips` |
| `f_<zeit>_<i>` (`kind:"frase"`) | `en`, `context`, `his`, `errors`, `correct`, `srs` |

Ohne `db` fällt die App auf `localStorage` zurück (Hinweis in den Ajustes).

## Miros Gespräche lesen (die Brücke zum Unterricht)

Vor einer Lektion im Chat die letzten Gespräche lesen und die Fehler in LERNSTAND
einarbeiten:

    Artifact action "read_db", url = <URL oben>, db_op "query",
    collection "data/users/me", query {where: [["kind","==","convo"]]}

`me` steht für Miros eigene Kennung; das funktioniert, weil die Seite `user` deklariert.

## Ändern

- Kleine Änderungen: Artifact action "edit" mit url und old_str/new_str.
- Danach **die Kopie im Repo aktualisieren** (`charla/ajolote-charla.html`) — sie ist die
  Sicherung, falls die Artifact-Datei verloren geht.
- Getestet wird mit einer Simulation von `window.claude` (sample, db, user) in Playwright:
  ganzer Gesprächsablauf, Speichern, Neuladen, Fall ohne Claude.
