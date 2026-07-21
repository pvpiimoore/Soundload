# Changelog

## v0.9.13

- Added integrated playback in the Buscador page.
- YouTube and SoundCloud results can be played as full tracks through resolved provider streams.
- Spotify and Apple Music results use official preview URLs when available.
- Added a native WinUI player panel with artwork, title, provider, and transport controls.
- Playback failures now show clear messages without affecting downloads or the queue.

## v0.9.12

- Corrected release documentation and public release notes.
- Added tool updates for `yt-dlp`, `scdl`, and `spotdl` from Settings.
- Added clear pip availability errors for portable Python tool updates.
- Added optional Spotify/spotDL Client ID and Client Secret settings, with the secret protected on Windows.
- Added Spotify search in Buscador through Spotify Client Credentials, without user OAuth.
- Portable builds now download the portable ZIP from the updater instead of launching the desktop installer.

## v0.9.11

- Hardened the Buscador workflow.
- Added clearer loading/cancel states for searches.
- Improved suggested-result deduplication and queued-result feedback.
- Cleaned public repository release hygiene.

## v0.9.10

- Added the Buscador page.
- Added provider tabs for YouTube, SoundCloud, and Apple Music.
- Added result cards with artwork, title, artist, source labels, and direct download enqueue.
- Added configurable result limits, suggested results, and deduplication.

## v0.9.9

- Added Apple Music import using public iTunes metadata.
- Added Apple Music album support as saved lists.
- Apple Music audio is not downloaded directly; Soundload downloads legal equivalents through the existing provider flow.

## v0.9.8

- Visual refresh for the WinUI app.
- Improved Download, Playlists, Convert, Settings, and About UI states.
- Added cleaner queue rows, playlist status pills, and better empty states.

## v0.9.7

- Added Spotify imports through spotDL.
- Added spotDL path/version checks.
- Added Spanish/English language switcher.
- Extended YouTube fallback behavior.

## v0.9.6

- Fixed conversion issues with embedded cover art.
- Added drag-and-drop URL support.
- Improved history and M3U export behavior.

## v0.9.5

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

