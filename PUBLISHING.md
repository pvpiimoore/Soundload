# Publishing a SoundLoad product release

Publishing a stable product release marked **Latest** automatically runs **Update platform channels** in GitHub Actions. The product version and the Windows/macOS application versions are independent.

## Before clicking Publish

1. Prepare a draft with a tag such as `v0.9.18` and attach all final packages. Select **Set as the latest release**.
2. For a Windows update, attach exactly one `SoundloadSetup-<WindowsVersion>-win-x64.exe` and `Soundload-share.zip`. Both must come from the same tested Windows build. The workflow generates the Windows manifest from these assets and GitHub SHA-256 digests.
3. For a Mac update, attach the DMG, `appcast.xml`, and `SHA256-macOS-<MacVersion>.txt` generated on the Mac. The checksum file must cover the DMG and the exact XML bytes. The signed appcast must point to the DMG in the new product release and use an increasing Sparkle build. **Never edit a signed appcast.** Signing and key storage remain on the Mac; no private key is required in GitHub Actions.
4. Publish the draft once all uploads have finished. Do not publish first and attach missing packages afterwards.

The automation checks public downloads, asset sizes and hashes, version progression and appcast/DMG consistency. It validates all platforms before changing any channel. It does not replace the Mac's cryptographic signing/verification or application tests; Sparkle verifies its Ed25519 signatures on clients.

## What happens automatically

- Windows changes update `windows-stable/windows-update.json`.
- Mac changes copy the exact signed `appcast.xml` to `macos-updates/appcast.xml`.
- The technical channels remain prereleases and never become Latest.
- The workflow verifies each public channel after updating it.
- If a platform is absent, its channel is untouched. If an identical existing platform version is carried into another product release, its channel is also untouched.
- An unchanged Mac build can carry its existing signed appcast pointing to the older release. A new build must point to the new release.
- Changed Windows binaries require a Windows version bump; changed Mac enclosure metadata requires a Sparkle build bump.
- A failed replacement retains the previous asset for recovery. A failed rename restores the original asset name automatically.

## Retry and validation

In **Actions → Update platform channels → Run workflow**, enter the product release tag.

- Leave **dry_run** checked to validate without modifying channels.
- Uncheck **dry_run** to retry activation after correcting a failed release. Successful platform updates are recognized and skipped on retry.

Only the current stable Latest product release may activate channels; retry the latest release, not an older delivery. Publishing through a GitHub Actions job's `GITHUB_TOKEN` does not trigger another workflow: that publishing job must explicitly dispatch this workflow after uploading and publishing. Publishing through the website or a normal authenticated `gh release` command triggers the release event.

Review the job result and its summary before announcing a release. If channel validation fails, existing clients keep their previous channel. If a public verification fails after replacement, the previous asset is retained under a `.previous-...` name; inspect and restore it if needed.

This workflow does not compile apps, sign Mac artifacts, rewrite release notes, or choose new platform versions. It automates channel activation from the tested release packages.
