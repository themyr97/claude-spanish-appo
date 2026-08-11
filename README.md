# Español — Vocabulario y Escucha

Personal Spanish learning PWA. **Live app:** https://themyr97.github.io/claude-spanish-appo/

## Structure

- **Repository root** — the currently live version, served by GitHub Pages. Always mirrors the latest version folder below.
- **`/v1/`, `/v2/`, `/v3/`...** — a frozen snapshot of each major version (new features, structural changes), kept for history and rollback.
- **`/vX/X.1/`, `/vX/X.2/`...** — minor updates within version X (new vocabulary words only, no feature changes), nested under their parent version.

## Version log

- **v1** — Initial release: vocabulary browser with audio pronunciation, verb conjugation tables (present + preterite, Latin American forms with vosotros as reference), listening exercises, flashcards (with direction toggle, difficulty tracking, undo), offline PWA support, progress saved to localStorage.
- **v2** — Default pronunciation voice set to Mónica (Mexican Spanish), when available in the browser/device voice list. Falls back to any es-MX voice, then the first available Spanish voice.
- **v3** — **Update mechanism fixed.** v1/v2 used a cache-first service worker, which meant an installed home-screen app kept serving the originally cached version and never picked up new deploys. v3 switches HTML/navigation to network-first (cache is now only an offline fallback), uses a versioned cache name that purges old caches on activation, actively checks for updates on launch and when the app returns to the foreground, and shows an "Actualizar" banner when a new version is ready. A version badge in the header shows which version is running.

- **v4** — Nouns now display with their definite article (el/la) and a colour-coded m/f badge; audio speaks the article together with the noun, and flashcards use the article form. Added remaining lesson nouns (oficina, jefe/jefa, reunión, correo, teléfono, año, señor). Special case noted for "el agua" (feminine but takes el in the singular).

- **v5** — Added **conjugation drill** ("Conjugar" tab): prompts a random verb + pronoun + tense, you type the form. Distinguishes fully correct, correct-but-missing-accent, and wrong; tracks which forms you miss most and lists them. Filters for present/preterite/both and all-verbs/irregulars-only. Latin American pronoun set (vosotros excluded from drilling). *gustar* excluded from the drill since its everyday use is "me gusta/gustan", not a full personal conjugation. Conjugation engine unit-tested against 31 known forms.

- **v6** — Navigation tabs laid out as a 3-column grid so they wrap onto a second row instead of crowding one line; all modes stay visible at once without horizontal squeezing.

- **v7** — Added **speaking practice** ("Hablar" tab): shows an English sentence, you say it aloud in Spanish via the microphone (Web Speech API). Matching is accent- and punctuation-tolerant and accepts the sentence with or without the subject pronoun. Checks all recognizer alternatives and scores the best one. Falls back to a text input where speech recognition is unavailable. Sentence bank drawn from the lesson exercises; extend `speakSentences` as new material is covered.

- **v8** — **Speech recognition fixes.** v7 never requested microphone permission, so iOS often showed no prompt at all and the mic silently did nothing; v8 calls `getUserMedia` to trigger the permission dialog. Removed `maxAlternatives = 3` (unreliable in WebKit). Added handlers for `onaudiostart`, `onspeechstart`, `onnomatch` and specific messages per error code, plus a 12-second no-result watchdog. New collapsible **microphone diagnostics** panel reports API availability, secure context, standalone-vs-browser mode and permission state, with a live event log and a "Probar micrófono" test button. Note: iOS requires Dictation enabled (Settings → General → Keyboard → Dictation) and may block the microphone entirely for home-screen-installed PWAs.

- **v9** — **Correction:** the default voice was set to Mónica on the assumption it was Mexican; on Apple devices Mónica is the Spain (es-ES) voice and **Paulina** is the Mexican one. Default now prefers Paulina, then any es-MX/es-US voice, with Mónica only as a later fallback. Speech **recognition language is now its own setting** (default es-MX, selectable México/España/EE.UU.) instead of inheriting from the chosen text-to-speech voice. Removed the parallel `getUserMedia` call during recognition, which could starve the recognizer of audio on iOS. Added a prominent warning when running in home-screen (standalone) mode, where iOS commonly fires `onaudiostart` but never returns a dictation result.

## Deploy checklist

When pushing a new version, always bump `APP_VERSION` in `service-worker.js` and the badge in `index.html`. The service worker file must change byte-wise, or browsers will not install the new version.

## Rolling back

To restore an earlier version as live: copy that version folder's files into the repository root and commit.
