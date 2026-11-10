#!/usr/bin/env python3
"""Validate submissions and assemble a catalog. Signing is a separate maintainer step."""
import argparse
import base64
import datetime as dt
import json
from pathlib import Path
import re
import hashlib
import struct
import subprocess

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

def local_file(name, prefix, maximum):
    if not isinstance(name, str) or not re.fullmatch(prefix + r"/[A-Za-z0-9][A-Za-z0-9._-]+", name) or ".." in name:
        raise ValueError("Invalid repository asset path")
    path = ROOT / name
    if path.is_symlink() or not path.resolve().is_relative_to(ROOT.resolve()):
        raise ValueError("Repository assets must be regular local files")
    data = path.read_bytes()
    if not data or len(data) > maximum:
        raise ValueError("Repository asset size is invalid")
    return data

def release_data(app):
    release = app.get("release")
    if release is None:
        return None
    version = release.get("version", "")
    if not re.fullmatch(r"(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)(-[0-9A-Za-z.-]+)?", version) or len(version) > 100 or release.get("tag") != "v" + version:
        raise ValueError("Invalid approved version/tag")
    data = local_file(release.get("manifestFile"), "releases", 256 * 1024)
    manifest = json.loads(data)
    if manifest.get("schemaVersion") != 2 or manifest.get("appId") != app["appId"] or manifest.get("version") != version or not re.fullmatch(r"[0-9a-f]{40}", manifest.get("revision", "")):
        raise ValueError("Manifest must match the approved application/version")
    bundles = manifest.get("bundles")
    if not isinstance(bundles, dict) or not 1 <= len(bundles) <= 16:
        raise ValueError("Missing package architectures")
    for arch, bundle in bundles.items():
        if not re.fullmatch(r"[a-zA-Z0-9_]+", arch) or bundle.get("ref") != f"app/{app['appId']}/{arch}/stable":
            raise ValueError("Invalid Flatpak reference")
        if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*\.flatpak", bundle.get("asset", "")):
            raise ValueError("Invalid GitHub Release package filename")
        for field in ("sha256", "commit", "metadataSha256"):
            if not re.fullmatch(r"[0-9a-f]{64}", bundle.get(field, "")):
                raise ValueError("Missing package digest or commit")
        for field in ("size", "installedSize"):
            if type(bundle.get(field)) is not int or not 0 <= bundle[field] <= 2 * 1024**3 or (field == "size" and not bundle[field]):
                raise ValueError("Invalid package size")
        metadata = base64.b64decode(bundle.get("metadata", ""), validate=True)
        if not metadata or hashlib.sha256(metadata).hexdigest() != bundle["metadataSha256"]:
            raise ValueError("Metadata digest mismatch")
        refs = [bundle.get("runtime")] + bundle.get("requiredExtensions", [None])
        if not isinstance(bundle.get("requiredExtensions"), list) or len(refs) > 129:
            raise ValueError("Missing runtime/extension plan")
        for reference in refs:
            if not isinstance(reference, dict) or not re.fullmatch(r"runtime/[A-Za-z0-9.\-]+/[A-Za-z0-9_\-]+/[A-Za-z0-9_.\-]+", reference.get("ref", "")):
                raise ValueError("Invalid runtime reference")
    signature = local_file(release["signatureFile"], "releases", 65536) if release.get("signatureFile") else b""
    if app.get("publisher") and not signature:
        raise ValueError("Pinned developer key requires its manifest signature")
    return {"version": version, "tag": release["tag"], "manifest": base64.b64encode(data).decode(), "signature": base64.b64encode(signature).decode()}

def icon_data(app):
    name = app.get("icon")
    if name is None:
        return None
    if name != "icons/" + app["appId"] + ".png":
        raise ValueError("Use icons/<appId>.png")
    data = local_file(name, "icons", 512 * 1024)
    if len(data) < 33 or data[:8] != bytes.fromhex("89504e470d0a1a0a") or data[12:16] != b"IHDR" or not all(0 < n <= 1024 for n in struct.unpack(">II", data[16:24])):
        raise ValueError("Use a PNG icon no larger than 1024 x 1024 and 512 KiB")
    return {"sha256": hashlib.sha256(data).hexdigest(), "size": len(data)}

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
        if "release" not in app:
            raise ValueError("Specify an approved release or explicit null for unavailable packages")
        release_data(app)
        icon_data(app)
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
    parser.add_argument("--repository", default="NextKde/appCatalog")
    parser.add_argument("--revision", help="Full catalog Git commit containing the reviewed icons")
    args = parser.parse_args()
    apps = load_apps()
    if args.check:
        print(f"Validated {len(apps)} entries")
        return
    if not re.fullmatch(r"[a-z][a-z0-9-]{0,63}", args.source_id):
        parser.error("Invalid source ID")
    if args.sequence is None or not 1 <= args.sequence <= 9007199254740991 or not 1 <= args.valid_days <= 90:
        parser.error("A positive increasing sequence and 1–90 valid days are required")
    revision = args.revision or subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    if not re.fullmatch(r"[0-9a-f]{40}", revision) or not re.fullmatch(r"[A-Za-z0-9-]+/[A-Za-z0-9_.-]+", args.repository) or ".." in args.repository:
        parser.error("Use a GitHub repository and full immutable Git commit")
    for app in apps:
        app["release"] = release_data(app)
        icon = icon_data(app)
        if icon is not None:
            icon["url"] = f"https://raw.githubusercontent.com/{args.repository}/{revision}/{app['icon']}"
            app["icon"] = icon
    now = dt.datetime.now(dt.timezone.utc).replace(microsecond=0)
    catalog = {"schemaVersion": 2, "sourceId": args.source_id, "sequence": args.sequence,
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
