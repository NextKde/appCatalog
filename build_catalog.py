#!/usr/bin/env python3
"""Validate submissions and assemble a catalog. Signing is a separate maintainer step."""
import argparse
import base64
import datetime as dt
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent

def validate_locales(value, maximum):
    if not isinstance(value, dict) or not 1 <= len(value) <= 32 or not value.get("en"):
        raise ValueError("Localized fields require an English fallback and at most 32 locales")
    for locale, text in value.items():
        if not re.fullmatch(r"[a-z]{2,3}(-[A-Za-z0-9]{2,8})*", locale):
            raise ValueError("Invalid locale tag")
        if not isinstance(text, str) or not text.strip() or len(text) > maximum:
            raise ValueError("Invalid localized text length")
        if any(ord(c) < 32 or 127 <= ord(c) <= 159 for c in text):
            raise ValueError("Localized text must not contain control characters")

def load_apps():
    apps, ids, keys = [], set(), set()
    for path in sorted((ROOT / "apps").glob("*.json")):
        raw = path.read_bytes()
        if len(raw) > 128 * 1024:
            raise ValueError(f"Entry too large: {path.name}")
        app = json.loads(raw)
        app_id, key = app["appId"], app["key"]
        if not re.fullmatch(r"[A-Za-z][A-Za-z0-9_-]*(\.[A-Za-z][A-Za-z0-9_-]*){2,}", app_id) or len(app_id) > 200:
            raise ValueError(f"Invalid appId: {path.name}")
        if path.name != app_id + ".json" or app_id in ids or key in keys:
            raise ValueError(f"Duplicate identity or wrong filename: {path.name}")
        if not re.fullmatch(r"[a-z][a-z0-9-]{0,63}", key):
            raise ValueError("Invalid application key")
        repo = app["repository"]
        if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9-]*/[A-Za-z0-9_.-]+", repo) or ".." in repo or len(repo) > 200:
            raise ValueError("Use a GitHub owner/repository, not a URL")
        if app["format"] != "flatpak":
            raise ValueError("Only Flatpak is implemented in the first client release")
        if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{0,180}\.json", app["manifest"]):
            raise ValueError("Invalid release manifest filename")
        validate_locales(app.get("name"), 120)
        validate_locales(app.get("description"), 600)
        if app.get("status", "active") not in ("active", "withdrawn", "revoked"):
            raise ValueError("Invalid entry status")
        if "publisher" in app:
            publisher = app["publisher"]
            if not isinstance(publisher, dict) or not publisher:
                raise ValueError("Invalid optional publisher")
            if not re.fullmatch(r"[0-9A-F]{40}([0-9A-F]{24})?", publisher["fingerprint"]):
                raise ValueError("Use the full primary key fingerprint")
            key_bytes = base64.b64decode(publisher["publicKey"], validate=True)
            if not key_bytes or len(publisher["publicKey"]) > 65536:
                raise ValueError("Invalid exported public key")
        forbidden = {"command", "installCommand", "script", "installRoot", "executable"}.intersection(app)
        if forbidden:
            raise ValueError(f"Catalogs cannot supply commands: {forbidden}")
        ids.add(app_id); keys.add(key); apps.append(app)
    if len(apps) > 1000:
        raise ValueError("Too many entries")
    return apps

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--source-id", default="nextkde")
    parser.add_argument("--sequence", type=int)
    parser.add_argument("--valid-days", type=int, default=30)
    parser.add_argument("--output", type=Path, default=ROOT / "dist/catalog.json")
    args = parser.parse_args()
    apps = load_apps()
    if args.check:
        print(f"Validated {len(apps)} entries")
        return
    if not re.fullmatch(r"[a-z][a-z0-9-]{0,63}", args.source_id):
        parser.error("Invalid source ID")
    if args.sequence is None or not 1 <= args.sequence <= 9007199254740991 or not 1 <= args.valid_days <= 90:
        parser.error("A positive increasing sequence and 1–90 valid days are required")
    now = dt.datetime.now(dt.timezone.utc).replace(microsecond=0)
    catalog = {"schemaVersion": 1, "sourceId": args.source_id, "sequence": args.sequence,
               "issuedAt": now.isoformat().replace("+00:00", "Z"),
               "expiresAt": (now + dt.timedelta(days=args.valid_days)).isoformat().replace("+00:00", "Z"),
               "apps": apps}
    data = (json.dumps(catalog, ensure_ascii=False, indent=2) + "\n").encode()
    if len(data) > 4 * 1024 * 1024:
        raise ValueError("Catalog exceeds the client limit")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(data)

if __name__ == "__main__":
    main()
