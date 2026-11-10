import base64
import hashlib
import copy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import build_catalog

class Submissions(unittest.TestCase):
    def entry(self):
        return {"appId": "org.example.Notes", "key": "notes", "format": "flatpak",
                "repository": "example/notes", "manifest": "flatpak-release.json",
                "name": {"en": "Notes", "zh-CN": "笔记", "pt-BR": "Notas"},
                "description": {"en": "Notes app"}, "status": "active", "release": None}

    def load(self, entry, files=None):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "apps").mkdir()
            (root / "apps/org.example.Notes.json").write_text(json.dumps(entry))
            for name, data in (files or {}).items():
                target = root / name; target.parent.mkdir(parents=True, exist_ok=True); target.write_bytes(data)
            with patch.object(build_catalog, "ROOT", root):
                return build_catalog.load_apps()

    def test_optional_developer_key_and_translations(self):
        self.assertEqual(self.load(self.entry())[0]["name"]["pt-BR"], "Notas")

    def test_unsafe_or_unusable_submissions(self):
        cases = [{"repository": "https://evil.example/download"}, {"format": "script"},
                 {"command": "sh installer"}, {"name": {"zh-CN": "笔记"}},
                 {"description": {"en": 42}}, {"name": {"en": "x" * 121}},
                 {"name": {"en": "bad\nname"}}, {"name": {"en": "Notes", "bad_tag": "x"}},
                 {"publisher": {"fingerprint": "1234", "publicKey": "AAAA"}}]
        for change in cases:
            with self.subTest(change=change):
                entry = self.entry(); entry.update(copy.deepcopy(change))
                with self.assertRaises(ValueError):
                    self.load(entry)

    def test_withdrawal_and_revocation(self):
        for status in ("withdrawn", "revoked"):
            entry = self.entry(); entry["status"] = status
            self.assertEqual(self.load(entry)[0]["status"], status)

    def release_fixture(self):
        entry = self.entry()
        entry["release"] = {"version": "1.2.0", "tag": "v1.2.0", "manifestFile": "releases/notes.json"}
        metadata = b"[Application]\nname=org.example.Notes\n"
        manifest = {"schemaVersion": 2, "appId": entry["appId"], "version": "1.2.0", "revision": "a" * 40,
            "bundles": {"x86_64": {"asset": "notes.flatpak", "ref": "app/org.example.Notes/x86_64/stable",
                "sha256": "b" * 64, "commit": "c" * 64, "size": 1024, "installedSize": 2048,
                "metadata": base64.b64encode(metadata).decode(), "metadataSha256": hashlib.sha256(metadata).hexdigest(),
                "runtime": {"ref": "runtime/org.kde.Platform/x86_64/6.11"}, "requiredExtensions": []}}}
        return entry, manifest

    def test_fixed_release_and_wrong_identity(self):
        entry, manifest = self.release_fixture()
        self.assertEqual(self.load(entry, {"releases/notes.json": json.dumps(manifest).encode()})[0]["release"]["version"], "1.2.0")
        for field, value in [("version", "1.2.1"), ("appId", "org.attacker.App"), ("revision", "main")]:
            changed = copy.deepcopy(manifest); changed[field] = value
            with self.assertRaises(ValueError): self.load(entry, {"releases/notes.json": json.dumps(changed).encode()})

    def test_package_boundaries(self):
        entry, manifest = self.release_fixture()
        for field, value in [("asset", "../notes.flatpak"), ("ref", "app/org.attacker.App/x86_64/stable"),
            ("sha256", "invalid"), ("size", 2**40), ("size", True), ("metadataSha256", "0" * 64),
            ("requiredExtensions", None), ("runtime", {"ref": "https://evil.example"})]:
            changed = copy.deepcopy(manifest); changed["bundles"]["x86_64"][field] = value
            with self.subTest(field=field), self.assertRaises((ValueError, TypeError)):
                self.load(entry, {"releases/notes.json": json.dumps(changed).encode()})

    def test_explicit_unavailable_and_missing_selection(self):
        self.assertIsNone(self.load(self.entry())[0]["release"])
        entry = self.entry(); del entry["release"]
        with self.assertRaises(ValueError): self.load(entry)

    def test_repository_icon_and_limits(self):
        entry = self.entry(); entry["icon"] = "icons/org.example.Notes.png"
        png = base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+/a9sAAAAASUVORK5CYII=")
        self.assertEqual(self.load(entry, {entry["icon"]: png})[0]["icon"], entry["icon"])
        for data in [b"<svg/>", png + b"0" * (512 * 1024), png[:16] + b"\xff" * 8 + png[24:]]:
            with self.assertRaises(ValueError): self.load(entry, {entry["icon"]: data})
        for name in ["https://evil.example/a.png", "icons/../app.png", "icons/Other.png"]:
            entry["icon"] = name
            with self.assertRaises(ValueError): self.load(entry)

    def test_assembled_bytes_are_exact_and_icon_commit_is_pinned(self):
        import sys
        entry, manifest = self.release_fixture()
        raw = (json.dumps(manifest, indent=3) + "\n").encode()
        entry["icon"] = "icons/org.example.Notes.png"
        png = base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+/a9sAAAAASUVORK5CYII=")
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for name, data in {"apps/org.example.Notes.json": json.dumps(entry).encode(), "releases/notes.json": raw, entry["icon"]: png}.items():
                path = root / name; path.parent.mkdir(parents=True, exist_ok=True); path.write_bytes(data)
            output = root / "catalog.json"
            with patch.object(build_catalog, "ROOT", root), patch.object(sys, "argv", ["build_catalog.py", "--sequence", "2", "--repository", "Example/catalog", "--revision", "a" * 40, "--output", str(output)]):
                build_catalog.main()
            catalog = json.loads(output.read_bytes()); approved = catalog["apps"][0]
            self.assertEqual(catalog["schemaVersion"], 2)
            self.assertEqual(base64.b64decode(approved["release"]["manifest"]), raw)
            self.assertEqual(approved["icon"]["sha256"], hashlib.sha256(png).hexdigest())
            self.assertEqual(approved["icon"]["url"], "https://raw.githubusercontent.com/Example/catalog/" + "a" * 40 + "/icons/org.example.Notes.png")
