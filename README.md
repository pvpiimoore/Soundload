# Soundload

SoundLoad provides desktop applications for Windows and macOS for downloading and working with audio from supported sources. Platform versions and features evolve independently.

The public repository is used for official downloads, release notes, and update checks. The application source code is private.

## Download

Get the latest version from GitHub Releases:

https://github.com/pvpiimoore/Soundload/releases/latest

The current product release, **SoundLoad v0.9.17**, groups **Windows 0.9.17** and **macOS 0.2.2 (build 4)**. Choose the package for your platform:

- `SoundloadSetup-<version>-win-x64.exe`: recommended Windows installer.
- `Soundload-share.zip`: Windows portable version, no installer required.
- `SoundLoad-0.2.2-macOS27-arm64.dmg`: macOS package for Apple Silicon.

## Windows Features

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

Starting with Windows 0.9.17, updates use a dedicated Windows channel and compare the Windows package version, independently of the product release marked Latest. Installed builds download the installer; portable builds download the ZIP. Install Windows 0.9.17 to migrate from the old updater.

macOS 0.2.2 uses Sparkle and its own signed appcast, independently of GitHub Latest and the Windows channel. Users of macOS 0.2.1 must install 0.2.2 manually once to adopt the updater. The app is ad-hoc signed and is not Apple-notarized. The older 0.2.1 DMG is retained for historical reference; use 0.2.2.

## Responsible Use

Use Soundload only with content you have the right to download or process. The app respects DRM errors and is not intended to bypass platform restrictions, technical protections, or copyright law.
