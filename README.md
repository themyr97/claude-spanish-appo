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

## Deploy checklist

When pushing a new version, always bump `APP_VERSION` in `service-worker.js` and the badge in `index.html`. The service worker file must change byte-wise, or browsers will not install the new version.

## Rolling back

To restore an earlier version as live: copy that version folder's files into the repository root and commit.
