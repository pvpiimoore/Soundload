"""Publish platform metadata after a stable product release is public.

Only distribution metadata lives here; application source and signing keys do not.
"""
import base64
import hashlib
import json
import os
import re
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
import xml.etree.ElementTree as ET
from dataclasses import dataclass

REPO = "pvpiimoore/Soundload"
BASE = f"https://github.com/{REPO}/releases"
SPARKLE = "http://www.andymatuschak.org/xml-namespaces/sparkle"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def version(value):
    require(isinstance(value, str) and re.fullmatch(r"\d+\.\d+\.\d+", value), "Invalid platform version")
    return tuple(map(int, value.split(".")))


def sha(data):
    return hashlib.sha256(data).hexdigest()


def asset_map(release):
    assets = release.get("assets", [])
    require(len({a["name"] for a in assets}) == len(assets), "Duplicate asset names")
    require(all(a.get("state") == "uploaded" and a.get("size", 0) > 0 for a in assets), "Incomplete assets")
    return {a["name"]: a for a in assets}


def digest(asset):
    value = asset.get("digest", "") or ""
    require(re.fullmatch(r"sha256:[a-fA-F0-9]{64}", value), f"Missing GitHub SHA-256: {asset['name']}")
    return value[7:].lower()


def asset_url(tag, name):
    return f"{BASE}/download/{urllib.parse.quote(tag, safe='')}/{urllib.parse.quote(name, safe='')}"


def checksums(data):
    result = {}
    for line in data.decode("utf-8-sig").splitlines():
        if not line.strip():
            continue
        match = re.fullmatch(r"([a-fA-F0-9]{64})\s+\*?([^/\\]+)", line)
        require(match is not None, "Invalid checksum file")
        checksum, name = match.groups()
        require(name not in result, "Duplicate checksum entry")
        result[name] = checksum.lower()
    return result


def parse_feed(data):
    require(b"<!DOCTYPE" not in data.upper() and b"<!ENTITY" not in data.upper(), "XML entities are not allowed")
    require(b"sparkle-signatures:" in data, "Feed must be signed by the Mac publishing tools")
    root = ET.fromstring(data)
    item = root.find("./channel/item")
    require(item is not None, "Empty appcast")
    build = item.findtext(f"{{{SPARKLE}}}version", "")
    require(build.isdigit() and int(build) > 0, "Invalid Sparkle build")
    short = item.findtext(f"{{{SPARKLE}}}shortVersionString", "")
    version(short)
    enclosure = item.find("enclosure")
    require(enclosure is not None, "Missing DMG enclosure")
    signature = enclosure.get(f"{{{SPARKLE}}}edSignature", "")
    require(len(base64.b64decode(signature, validate=True)) == 64, "Missing Ed25519 DMG signature")
    return int(build), short, enclosure.attrib


@dataclass
class Plan:
    channel: str
    name: str
    data: bytes
    version: str


def plan_release(release, read, current):
    """Validate every platform before allowing any channel mutation."""
    tag = release["tag_name"]
    require(re.fullmatch(r"v\d+\.\d+\.\d+", tag), "Not a product release tag")
    require(not release["draft"] and not release["prerelease"], "Product release must be public and stable")
    assets = asset_map(release)
    plans = []
    installers = [a for a in assets if re.fullmatch(r"SoundloadSetup-\d+\.\d+\.\d+-win-x64\.exe", a)]
    require(len(installers) <= 1, "Ambiguous Windows installers")
    if installers or "Soundload-share.zip" in assets:
        require(len(installers) == 1 and "Soundload-share.zip" in assets, "Windows requires installer and portable ZIP")
        name = installers[0]
        win_version = name[len("SoundloadSetup-"):-len("-win-x64.exe")]
        old_data = current("windows-stable", "windows-update.json")
        old = json.loads(old_data) if old_data else None
        files = {}
        for kind, filename in [("installer", name), ("portable", "Soundload-share.zip")]:
            a = assets[filename]
            files[kind] = dict(name=filename, url=asset_url(tag, filename), size=a["size"], sha256=digest(a))
        if old:
            require(version(win_version) >= version(old["version"]), "Refusing Windows downgrade")
            if version(win_version) == version(old["version"]):
                require(all(old[k]["sha256"].lower() == files[k]["sha256"] and old[k]["size"] == files[k]["size"] for k in files),
                        "Windows binaries changed without a version bump")
                files = None  # Same platform version carried forward: preserve its channel.
        if files:
            data = dict(schemaVersion=1, platform="windows", architecture="x64", version=win_version,
                        releaseUrl=f"{BASE}/tag/{tag}", **files)
            plans.append(Plan("windows-stable", "windows-update.json", (json.dumps(data, indent=2) + "\n").encode(), win_version))

    # Older DMGs may be retained in a release; only the signed appcast selects the current one.
    dmgs = [a for a in assets if a.endswith(".dmg")]
    if dmgs or "appcast.xml" in assets:
        require("appcast.xml" in assets, "A macOS release requires its signed appcast")
        data = read(assets["appcast.xml"])
        build, mac_version, enclosure = parse_feed(data)
        name = f"SoundLoad-{mac_version}-macOS27-arm64.dmg"
        require(name in assets, "Appcast DMG is not in this product release")
        require(enclosure.get("length") == str(assets[name]["size"]), "DMG length mismatch")
        checksum_name = f"SHA256-macOS-{mac_version}.txt"
        require(checksum_name in assets, "Mac checksum file is required")
        sums = checksums(read(assets[checksum_name]))
        require(sums.get(name) == digest(assets[name]), "DMG checksum mismatch")
        require(sums.get("appcast.xml") == sha(data) == digest(assets["appcast.xml"]), "Appcast checksum mismatch")
        old_data = current("macos-updates", "appcast.xml")
        if old_data:
            old_build, old_version, old_enclosure = parse_feed(old_data)
            require(build >= old_build and version(mac_version) >= version(old_version), "Refusing macOS downgrade")
            if build == old_build:
                require(mac_version == old_version and enclosure == old_enclosure, "macOS payload changed without a build bump")
                data = None
        if data is not None:
            require(enclosure.get("url") == asset_url(tag, name), "New appcast points to a different release or DMG")
            plans.append(Plan("macos-updates", "appcast.xml", data, f"{mac_version} (build {build})"))
    require(installers or dmgs or "appcast.xml" in assets, "No platform packages found")
    return plans


class GitHub:
    def __init__(self, token):
        self.token = token

    def api(self, path, method="GET", payload=None, raw=None):
        url = path if path.startswith("https://uploads.github.com/") else f"https://api.github.com/repos/{REPO}/{path}"
        data = raw if raw is not None else json.dumps(payload).encode() if payload is not None else None
        headers = {"Authorization": f"Bearer {self.token}", "Accept": "application/vnd.github+json",
                   "X-GitHub-Api-Version": "2022-11-28", "Content-Type": "application/octet-stream" if raw is not None else "application/json"}
        with urllib.request.urlopen(urllib.request.Request(url, data=data, headers=headers, method=method), timeout=120) as response:
            body = response.read()
            return json.loads(body) if body else None

    def release(self, tag):
        try:
            return self.api("releases/tags/" + urllib.parse.quote(tag, safe=""))
        except urllib.error.HTTPError as error:
            if error.code == 404:
                return None
            raise

    def read(self, asset):
        require(asset["size"] <= 2 * 1024 * 1024, "Metadata asset too large")
        url = asset["browser_download_url"]
        require(url.startswith(BASE + "/download/"), "Unexpected asset repository")
        with urllib.request.urlopen(url, timeout=60) as response:
            data = response.read(2 * 1024 * 1024 + 1)
        require(len(data) == asset["size"] and sha(data) == digest(asset), "Downloaded metadata failed verification")
        return data

    def current(self, tag, name):
        release = self.release(tag)
        if release is None:
            return None
        require(not release["draft"], "Existing channel is still a draft; publish it before automation")
        assets = asset_map(release)
        require(name in assets, f"Existing channel {tag} is incomplete")
        return self.read(assets[name])

    def verify_public_packages(self, release):
        for asset in release["assets"]:
            if not asset["name"].endswith((".exe", ".zip", ".dmg")):
                continue
            request = urllib.request.Request(asset_url(release["tag_name"], asset["name"]), method="HEAD")
            with urllib.request.urlopen(request, timeout=60) as response:
                require(response.status == 200 and int(response.headers.get("Content-Length", "0")) == asset["size"],
                        f"Package is not publicly available at the expected size: {asset['name']}")

    def publish(self, plan):
        release = self.release(plan.channel)
        if release is None:
            release = self.api("releases", "POST", dict(tag_name=plan.channel, name=f"Update channel: {plan.channel}",
                body="Technical update metadata. User downloads are in the product release marked Latest.",
                draft=True, prerelease=True, make_latest="false"))
        old = next((a for a in release["assets"] if a["name"] == plan.name), None)
        pending = plan.name + ".pending-" + uuid.uuid4().hex
        upload = release["upload_url"].split("{")[0] + "?name=" + urllib.parse.quote(pending)
        staged = self.api(upload, "POST", raw=plan.data)
        require(digest(staged) == sha(plan.data) and staged["size"] == len(plan.data), "Staged channel metadata failed verification")
        # Keep the old asset recoverable until the new name has been assigned.
        if old:
            self.api(f"releases/assets/{old['id']}", "PATCH", {"name": plan.name + ".previous-" + uuid.uuid4().hex})
        try:
            self.api(f"releases/assets/{staged['id']}", "PATCH", {"name": plan.name})
        except Exception:
            if old:
                self.api(f"releases/assets/{old['id']}", "PATCH", {"name": plan.name})
            raise
        self.api(f"releases/{release['id']}", "PATCH", dict(draft=False, prerelease=True, make_latest="false"))
        verified = False
        for attempt in range(4):
            try:
                channel = self.release(plan.channel)
                actual = next(a for a in channel["assets"] if a["name"] == plan.name)
                verified = self.read(actual) == plan.data
                if verified:
                    break
            except (urllib.error.URLError, ValueError, StopIteration):
                pass
            time.sleep(2 ** attempt)
        require(verified, "Public channel verification failed; previous asset retained for recovery")
        if old:
            self.api(f"releases/assets/{old['id']}", "DELETE")


def main():
    tag = os.environ.get("RELEASE_TAG", "")
    require(os.environ.get("GITHUB_REPOSITORY", REPO) == REPO, "Wrong repository")
    api = GitHub(os.environ["GITHUB_TOKEN"])
    release = api.release(tag)
    require(release is not None, "Release does not exist")
    latest = api.api("releases/latest")
    require(latest["tag_name"] == tag, "Only the current product Latest can activate platform channels")
    plans = plan_release(release, api.read, api.current)
    api.verify_public_packages(release)
    dry = os.environ.get("DRY_RUN", "true").lower() == "true"
    lines = [f"Product release: {tag}. Dry run: {dry}."]
    for plan in plans:
        lines.append(f"{'Would update' if dry else 'Updating'} {plan.channel}: {plan.version}, SHA-256 {sha(plan.data)}")
        if not dry:
            # Another product release may have been published while this job was validating.
            require(api.api("releases/latest")["tag_name"] == tag, "Latest changed; retry the newer release")
            api.publish(plan)
    if not plans:
        lines.append("Platform channels already match. No changes needed.")
    require(api.api("releases/latest")["tag_name"] == tag, "Latest changed during this run")
    summary = "\n".join(lines) + "\n"
    print(summary)
    if os.environ.get("GITHUB_STEP_SUMMARY"):
        with open(os.environ["GITHUB_STEP_SUMMARY"], "a", encoding="utf-8") as output:
            output.write(summary)


if __name__ == "__main__":
    main()
