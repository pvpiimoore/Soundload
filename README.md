# Soundload

Soundload is a Windows desktop app for downloading, organizing, searching, and converting audio from supported sources.

The public repository is used for official downloads, release notes, and update checks. The application source code is private.

## Download

Get the latest version from GitHub Releases:

https://github.com/pvpiimoore/Soundload/releases/latest

Each release includes:

- `SoundloadSetup-<version>-win-x64.exe`: recommended Windows installer.
- `Soundload-share.zip`: portable version, no installer required.

## Features

- Download and convert audio from supported sources.
- SoundCloud, YouTube, Bandcamp, Spotify import through spotDL, and Apple Music import through public iTunes metadata.
- Buscador page for YouTube, SoundCloud, Spotify, and Apple Music search with artwork, result limits, suggested results, deduplication, and direct enqueue.
- Integrated player in Buscador: full playback for YouTube/SoundCloud and official previews for Spotify/Apple Music when available.
- SoundCloud playlist management with linked local folders.
- Apple Music album import as saved lists using public iTunes metadata.
- Playlist sync, per-track state, DRM/error/downloaded indicators, and local file reconciliation.
- YouTube fallback for DRM-protected or failed tracks when a legal equivalent exists.
- Metadata and cover handling for downloaded files.
- MP3/WAV/AIFF/original output options.
- Download queue, progress, logs, diagnostics, update checks, and optional error reporting.
- Spanish / English UI language switcher.
- Installer and portable builds for Windows.

## Portable Version

Extract the full ZIP and keep the Soundload folder intact. Do not move only the executable out of the folder, because bundled tools are resolved from the folder structure.

Use the included launcher/shortcut files if you want a movable shortcut.

## Updates

Soundload checks GitHub Releases for updates. Installed builds use the Windows installer flow. Portable builds download the portable ZIP so they do not accidentally launch the desktop installer.

## Responsible Use

Use Soundload only with content you have the right to download or process. The app respects DRM errors and is not intended to bypass platform restrictions, technical protections, or copyright law.
