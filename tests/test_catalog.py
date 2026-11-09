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
                "description": {"en": "Notes app"}, "status": "active"}

    def load(self, entry):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "apps").mkdir()
            (root / "apps/org.example.Notes.json").write_text(json.dumps(entry))
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
