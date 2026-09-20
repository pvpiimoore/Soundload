import copy
import importlib.util
import json
import pathlib
import sys
import unittest
from unittest.mock import patch

PATH = pathlib.Path(__file__).parents[1] / "update_channels.py"
spec = importlib.util.spec_from_file_location("update_channels", PATH)
m = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = m
spec.loader.exec_module(m)


def asset(name, data=b"test-package"):
    return dict(name=name, size=len(data), digest="sha256:" + m.sha(data), state="uploaded", data=data)


def release(assets):
    return dict(tag_name="v0.9.18", draft=False, prerelease=False, assets=assets)


def windows(ver="0.9.17"):
    return release([asset(f"SoundloadSetup-{ver}-win-x64.exe"), asset("Soundload-share.zip")])


def mac(build=4, ver="0.2.2", tag="v0.9.18"):
    name = f"SoundLoad-{ver}-macOS27-arm64.dmg"
    dmg = asset(name)
    # Synthetic signatures: tests exercise preservation/binding, not cryptography.
    signature = m.base64.b64encode(bytes(64)).decode()
    data = f'''<rss xmlns:sparkle="{m.SPARKLE}"><channel><item>
      <sparkle:version>{build}</sparkle:version><sparkle:shortVersionString>{ver}</sparkle:shortVersionString>
      <enclosure url="{m.asset_url(tag, name)}" length="{dmg['size']}" sparkle:edSignature="{signature}" />
      </item></channel></rss><!-- sparkle-signatures: synthetic test fixture -->'''.encode()
    sums = f"{m.digest(dmg)}  {name}\n{m.sha(data)}  appcast.xml\n".encode()
    return release([dmg, asset("appcast.xml", data), asset(f"SHA256-macOS-{ver}.txt", sums)])


def read(a):
    return a["data"]


def plan(r, win=None, feed=None):
    return m.plan_release(r, read, lambda channel, name: win if channel == "windows-stable" else feed)


class Rules(unittest.TestCase):
    def test_windows_version_independent_of_product(self):
        result = plan(windows())[0]
        manifest = json.loads(result.data)
        self.assertEqual(manifest["version"], "0.9.17")
        self.assertTrue(manifest["installer"]["url"].endswith("v0.9.18/SoundloadSetup-0.9.17-win-x64.exe"))

    def test_windows_carry_forward_leaves_channel_untouched(self):
        current = plan(windows())[0].data
        self.assertEqual(plan(windows(), win=current), [])

    def test_windows_downgrade_rejected(self):
        current = plan(windows("0.9.19"))[0].data
        with self.assertRaisesRegex(ValueError, "downgrade"):
            plan(windows(), win=current)

    def test_windows_changed_binary_requires_version_bump(self):
        current = plan(windows())[0].data
        changed = windows()
        changed["assets"][0] = asset(changed["assets"][0]["name"], b"changed")
        with self.assertRaisesRegex(ValueError, "version bump"):
            plan(changed, win=current)

    def test_windows_missing_portable_rejected(self):
        r = windows(); r["assets"].pop()
        with self.assertRaisesRegex(ValueError, "installer and portable"):
            plan(r)

    def test_missing_github_digest_rejected(self):
        r = windows(); r["assets"][0]["digest"] = None
        with self.assertRaisesRegex(ValueError, "SHA-256"):
            plan(r)

    def test_mac_feed_bytes_preserved(self):
        r = mac()
        result = plan(r)[0]
        self.assertEqual(result.data, r["assets"][1]["data"])
        self.assertEqual(result.channel, "macos-updates")

    def test_mac_carry_forward_does_not_resign_old_url(self):
        r = mac(tag="v0.9.17")
        self.assertEqual(plan(r, feed=r["assets"][1]["data"]), [])

    def test_mac_new_feed_wrong_release_rejected(self):
        with self.assertRaisesRegex(ValueError, "different release"):
            plan(mac(tag="v0.9.17"))

    def test_mac_downgrade_rejected(self):
        newer = mac(build=5)["assets"][1]["data"]
        with self.assertRaisesRegex(ValueError, "downgrade"):
            plan(mac(), feed=newer)

    def test_mac_changed_payload_requires_build_bump(self):
        old = mac(tag="v0.9.17")["assets"][1]["data"]
        with self.assertRaisesRegex(ValueError, "build bump"):
            plan(mac(), feed=old)

    def test_mac_checksum_mismatch_rejected(self):
        r = mac(); r["assets"][0] = asset(r["assets"][0]["name"], b"bad-package!")
        with self.assertRaises(ValueError):
            plan(r)

    def test_mac_missing_feed_rejected(self):
        r = mac(); del r["assets"][1]
        with self.assertRaisesRegex(ValueError, "signed appcast"):
            plan(r)

    def test_only_mac_does_not_touch_windows(self):
        self.assertEqual([p.channel for p in plan(mac())], ["macos-updates"])

    def test_both_platforms_plan_together(self):
        r = windows(); r["assets"] += mac()["assets"]
        self.assertEqual(len(plan(r)), 2)

    def test_incomplete_second_platform_prevents_any_plan(self):
        r = windows(); r["assets"] += [mac()["assets"][0]]
        with self.assertRaises(ValueError):
            plan(r)

    def test_drafts_prereleases_technical_tags_rejected(self):
        for key, val in [("draft", True), ("prerelease", True), ("tag_name", "windows-stable")]:
            r = windows(); r[key] = val
            with self.assertRaises(ValueError):
                plan(r)

    def test_xml_entities_rejected(self):
        with self.assertRaisesRegex(ValueError, "entities"):
            m.parse_feed(b'<!DOCTYPE rss><rss/>')

    def test_dry_run_never_publishes(self):
        r = windows()
        with patch.object(m, "GitHub") as mock_api, patch.dict(m.os.environ, {"RELEASE_TAG": r["tag_name"], "GITHUB_TOKEN": "test", "DRY_RUN": "true", "GITHUB_REPOSITORY": m.REPO}):
            api = mock_api.return_value
            api.release.return_value = r
            api.api.return_value = r
            api.current.return_value = None
            m.main()
            api.publish.assert_not_called()

    def test_failed_swap_restores_previous_name(self):
        p = plan(windows())[0]
        old = dict(id=1, name=p.name)
        channel = dict(id=9, assets=[old], upload_url="https://uploads.github.com/repos/x/releases/9/assets{?name}")
        calls = []
        api = m.GitHub("test")
        def fake(path, method="GET", payload=None, raw=None):
            calls.append((path, method, payload))
            if method == "POST":
                return dict(id=2, digest="sha256:" + m.sha(p.data), size=len(p.data), name="pending")
            if path == "releases/assets/2" and method == "PATCH":
                raise RuntimeError("rename failed")
        with patch.object(api, "release", return_value=channel), patch.object(api, "api", side_effect=fake):
            with self.assertRaisesRegex(RuntimeError, "rename failed"):
                api.publish(p)
        self.assertEqual(calls[-1], ("releases/assets/1", "PATCH", {"name": p.name}))
        self.assertFalse(any(c[1] == "DELETE" for c in calls))

    def test_successful_swap_verifies_before_removing_old(self):
        p = plan(windows())[0]
        old = dict(id=1, name=p.name)
        staged = dict(id=2, digest="sha256:" + m.sha(p.data), size=len(p.data), name=p.name)
        channel = dict(id=9, assets=[old], upload_url="https://uploads.github.com/repos/x/releases/9/assets{?name}")
        calls = []
        api = m.GitHub("test")
        def fake(path, method="GET", payload=None, raw=None):
            calls.append((path, method, payload))
            if method == "POST":
                return staged
        def verified(asset):
            calls.append(("verified", "READ", None))
            return p.data
        with patch.object(api, "release", side_effect=[channel, dict(assets=[staged])]), patch.object(api, "api", side_effect=fake), patch.object(api, "read", side_effect=verified):
            api.publish(p)
        self.assertEqual(calls[-2][0], "verified")
        self.assertEqual(calls[-1], ("releases/assets/1", "DELETE", None))
        self.assertIn(("releases/9", "PATCH", dict(draft=False, prerelease=True, make_latest="false")), calls)

    def test_invalid_staged_hash_never_renames_old_asset(self):
        p = plan(windows())[0]
        channel = dict(id=9, assets=[dict(id=1, name=p.name)], upload_url="https://uploads.github.com/repos/x/releases/9/assets{?name}")
        api = m.GitHub("test")
        with patch.object(api, "release", return_value=channel), patch.object(api, "api", return_value=dict(name="pending", id=2, digest="sha256:" + "0" * 64, size=len(p.data))) as call:
            with self.assertRaisesRegex(ValueError, "Staged"):
                api.publish(p)
        self.assertEqual(call.call_count, 1)


if __name__ == "__main__":
    unittest.main()
