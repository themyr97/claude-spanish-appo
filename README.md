# Español — Vocabulario y Escucha

Personal Spanish learning PWA. **Live app:** https://themyr97.github.io/claude-spanish-appo/

## Structure

- **Repository root** — the currently live version, served by GitHub Pages. Always mirrors the latest version folder below.
- **`/v1/`, `/v2/`, `/v3/`...** — a frozen snapshot of each major version (new features, structural changes), kept for history and rollback.
- **`/vX/X.1/`, `/vX/X.2/`...** — minor updates within version X (new vocabulary words only, no feature changes), nested under their parent version.

## Version log

- **v1** — Initial release: vocabulary browser with audio pronunciation, verb conjugation tables (present + preterite, Latin American forms with vosotros as reference), listening exercises, flashcards (with direction toggle, difficulty tracking, undo), offline PWA support, progress saved to localStorage.

## Rolling back

To restore an earlier version as live: copy that version folder's files into the repository root and commit.
