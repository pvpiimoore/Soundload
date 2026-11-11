# Soundload

SoundLoad provides desktop applications for Windows and macOS for downloading and working with audio from supported sources. Each platform has its own version number and update channel.

The public repository is used for official downloads, release notes, and update checks. The application source code is private.

## Download

Get the latest version from GitHub Releases:

https://github.com/pvpiimoore/Soundload/releases/latest

The current product release, **SoundLoad v0.10.1**, groups **Windows 0.10.0** and **macOS 0.6.1 (build 11)**. Choose the package for your platform:

- `SoundloadSetup-0.10.0-win-x64.exe`: Windows installer (x64).
- `SoundLoad-0.6.1-macOS27-arm64.dmg`: macOS 27 package for Apple Silicon.

Recent releases include only the Windows installer. Older portable ZIP builds remain available in their original releases.

## Features

Both apps:

- Download and convert audio from SoundCloud, YouTube and Bandcamp, plus Spotify imports through spotDL and Apple Music imports through public iTunes metadata.
- Search YouTube, SoundCloud, Spotify and Apple Music, with artwork, previews, suggested results and direct download.
- Saved playlists linked to a local folder: sync, per-track status (downloaded, pending, failed, unavailable, DRM), local file reconciliation, scheduled checks and M3U export.
- Find an alternative source for failed or DRM-protected tracks when a legal equivalent exists.
- Download queue with pause, resume, retry and recovery after closing the app.
- Edit title, artist, album and cover of saved tracks; your edits are kept when syncing.
- Output to MP3, WAV, AIFF, FLAC or the original format, with 24-bit WAV/AIFF and metadata and cover handling.
- **Send to rekordbox (beta):** analyzes BPM, beatgrid, downbeat and key and delivers the playlist to rekordbox, ready to export to a USB drive. Beta feature: it may contain errors, so always check the beatgrid before playing.
- Edit title, artist, album and cover inside the audio file, without re-encoding.
- Spanish and English interface.

Windows:

- Installer with its own update channel; the app runtime and the audio tools are included.
- Send to rekordbox analyzes faster on a dedicated DirectX 12 graphics card (NVIDIA, AMD or Intel Arc), with the same results; other computers use the processor.

macOS:

- Native app for macOS 27 on Apple Silicon, with Sparkle updates from a signed feed.
- Bundled audio tools (Python, yt-dlp, scdl, spotDL, FFmpeg, Deno): nothing else to install.

## Updates

Publishing a stable product release marked Latest updates its platform channels automatically through GitHub Actions.

- **Windows** (0.9.17 and later) checks its own channel and compares the Windows package version, independently of the release marked Latest.
- **macOS** (0.2.2 and later) uses Sparkle and its own signed appcast. Users of macOS 0.2.1 must install a newer DMG manually once.

The macOS app is ad-hoc signed and is not Apple-notarized. On first launch, macOS may ask you to confirm opening it.

## Responsible Use

Use Soundload only with content you have the right to download or process. The app respects DRM errors and is not intended to bypass platform restrictions, technical protections, or copyright law.
