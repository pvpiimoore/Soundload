# Changelog

## v0.9.14 - SoundCloud fallback and diagnostics

- Added a SoundCloud download fallback: Soundload tries `scdl` first and falls back to `yt-dlp` for common auth, metadata, or no-file failures.
- Rebuilt portable packaging so bundled Python installs and validates `yt-dlp`, `scdl`, and `spotdl` during release creation.
- Added sanitized automatic error reporting for failed downloads, enabled by default for new installs and configurable from Settings > General.
- Added manual diagnostic report sending from Settings without exposing the internal endpoint in the app UI.
- Discord reports include latest startup context plus recent warnings/errors, even after app restarts.
- Verified Release build, tests, portable tooling, installer, ZIP, and SHA256 hashes.

## v0.9.13 - Public release hygiene and Spotify search plumbing

- Corrected public release notes and documentation for recent versions.
- Added tool updates for `yt-dlp`, `scdl`, and `spotdl` from Settings.
- Added optional Spotify/spotDL Client ID and Client Secret settings, with the secret protected on Windows.
- Added Spotify search in Buscador through Spotify Client Credentials, without user OAuth.
- Portable builds download portable ZIP updates instead of launching the desktop installer.

## v0.9.12 - Search and import cleanup

- Corrected release documentation for Apple Music import, albums, and Buscador features.
- Added Apple Music import through public iTunes metadata and YouTube equivalent downloads.
- Added Apple Music album support as saved lists.
- Improved internal tools update flow and portable Python handling.

## v0.9.11 - Buscador polish

- Hardened the Buscador workflow.
- Added clearer loading and cancel states for searches.
- Improved suggested-result deduplication and queued-result feedback.

## v0.9.10 - Buscador

- Added the Buscador page.
- Added provider tabs for YouTube, SoundCloud, and Apple Music.
- Added result cards with artwork, title, artist, source labels, and direct download enqueue.
- Added configurable result limits, suggested results, and deduplication.

## v0.9.9 - Apple Music import

- Added Apple Music import using public iTunes metadata.
- Added Apple Music album support as saved lists.
- Apple Music audio is not downloaded directly; Soundload downloads legal equivalents through the existing provider flow.

## v0.9.8 - Visual refresh

- Visual refresh for the WinUI app.
- Improved Download, Playlists, Convert, Settings, and About UI states.
- Added cleaner queue rows, playlist status pills, and better empty states.

## v0.9.7 - Spotify via spotDL and language switcher

- Added Spotify imports through spotDL.
- Added spotDL path/version checks.
- Added Spanish/English language switcher.
- Extended YouTube fallback behavior.

## v0.9.6 - Conversion fix and quality of life

- Fixed conversion issues with embedded cover art.
- Added drag-and-drop URL support.
- Improved history and M3U export behavior.

## v0.9.5 - Library features and reliability

- Added YouTube fallback for DRM-protected or failed playlist tracks.
- Added embedded metadata and cover handling.
- Added retry, batch progress, M3U export, notifications, history, and stronger playlist matching.

## v0.9.1 - v0.9.4

- Migrated the app to WinUI.
- Restored playlist context actions, About page, Settings tabs, updater flow, and packaging.
- Improved update checks, installer downloads, portable packaging, diagnostics, and playlist reliability.

## v0.8.x

- Added saved playlists, SoundCloud sync, per-track states, local folder reconciliation, dark mode fixes, Settings tabs, and updater foundations.

## v0.1.0 - v0.7.0

- Initial app foundation, provider detection, SoundCloud metadata/download flow, local conversion, FFmpeg/scdl integration, settings, logs, and packaging groundwork.
