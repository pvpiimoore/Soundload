# Changelog

Each product release groups the Windows and macOS apps. App versions are shown in brackets.

## v0.9.23 - Security and maintenance (Windows 0.9.21, macOS 0.5.1)

- Windows: .NET 10.0.14, Windows App SDK 2.6.5, Python 3.14.10 and FFmpeg 9.0.2.
- Both: yt-dlp 2026.10.26, scdl 3.0.9 and spotDL 4.6.0, with provider and search fixes. Deno 2.9.8 is included for yt-dlp JavaScript support.
- Updated libraries for secure connections, compressed responses and artwork.
- Windows: packaging and the tool updater share compatibility rules, validate an update before activating it and can roll back.
- macOS: Sparkle 2.10.1 (installer, feed parsing and translations).

## v0.9.22 - Simpler apps (Windows 0.9.20, macOS 0.5.0)

- Windows: release notes are shown once after updating; the top bar is reserved for downloads pending from the previous session; update checks run in the background.
- Windows: pasting a single link analyzes it automatically. Format, quality and folder are chosen in Download and remembered.
- Windows: fixed a Spotify issue that could save audio outside the temporary folder and report an error after a successful download.
- Windows: Sync updates the playlist and completes missing metadata; playlist folders are checked when opened; filters simplified to All, Pending, Downloaded and With problems.
- Windows: settings reorganized into General, Downloads and audio, Playlists and library, and Advanced; language changes apply immediately.
- macOS: History becomes a tab inside Downloads; the sidebar has four sections (Downloads, Search, Playlists, Converter, ⌘1–⌘4).
- macOS: pasting or dropping links reads title and artwork automatically (up to 10 links); the first launch uses `~/Music/SoundLoad` so Download works without setup.
- macOS: a single Sync button and simplified playlist filters; search runs in its own process and is no longer blocked by other operations.
- macOS: faster with large playlists (the queue and playlists are saved in batches).

## v0.9.21 - Alternatives for failed downloads (macOS 0.4.1)

- macOS: **Find alternatives** from a failed download, searching YouTube and SoundCloud with artwork, artist, duration and preview. The destination, format, quality and playlist link are kept.
- macOS: **Remove finished from queue** clears completed entries without deleting downloaded files.
- macOS: release notes appear once per build at startup.
- Windows stays on 0.9.19.

## v0.9.20 - Resumable sync (macOS 0.4.0)

- macOS: sync and metadata lookup in a single flow, saved per track so it can resume after an interruption; limited concurrency and caching to reduce repeated requests.
- macOS: improved track search and selection, protected edits, history filters, backups that exclude secrets, optional scheduling and M3U options.
- macOS: FLAC and 24-bit output, folders in the converter, Python 3.14.8.
- Windows stays on 0.9.19.

## v0.9.19 - Layout and history (Windows 0.9.19)

- Pages use the available width and no longer resize when switching playlists or opening options.
- Search results adapt their columns to the window size.
- Clearer download history with dates, status icons and badges; search, filter, retry and open completed files.
- The release notes dialog opens automatically after an update.

## v0.9.18 - Simpler Windows experience (Windows 0.9.18, macOS 0.3.0)

- Calmer interface: Download, Search and Convert focus on the next step; settings organized into sections; redesigned What's New dialog.
- Saved batches can be resumed after closing; output profiles remember folder, format, quality, bit depth and file naming.
- YouTube playlists can be saved; songs can be searched, filtered and edited; edits survive synchronization.
- Separate states for DRM, unavailable and removed tracks; reuse of matching local files, auto-updated M3U and scheduled playlist checks.
- Convert files or folders to MP3, WAV, AIFF or FLAC, with 24-bit WAV/AIFF.
- macOS 0.3.0 published with this release.

## v0.9.17 - Independent update channels (Windows 0.9.17, macOS 0.2.2)

- Windows checks its own update channel, independent of the release marked Latest, and validates URL, size and SHA-256.
- Windows portable ZIP published alongside the installer.
- macOS 0.2.2 adds Sparkle updates from a signed feed. Users of macOS 0.2.1 must install 0.2.2 manually once.

## v0.9.16 - Metadata control and queue management

- Metadata lookup skips tracks that already have a title and artist; **Force metadata refresh** refreshes everything.
- Local playlist reconciliation validates audio with FFmpeg before marking files as downloaded.
- Pause and resume the pending queue, reorder pending jobs, and choose an alternative source from failed rows.
- Fewer duplicate error reports and bounded retries when Discord limits requests; expanded English translations.

## v0.9.15 - Playlist sync and reliability

- Synchronization keeps existing titles, artists, albums and artwork when a provider returns incomplete information; partial responses no longer mark tracks as deleted.
- Metadata caching and bounded retries when providers limit requests; playlist downloads use the shared queue and its concurrency limit.
- Pending jobs are recovered when the app reopens; more robust settings and playlist storage with backup recovery.
- Failed conversions keep the original file and clean up temporary output.
- Error reporting covers playlist and metadata failures; automatic reporting requires opt-in on new installations.

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
