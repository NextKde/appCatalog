# Approved versions and icons

[简体中文](PinnedReleases.zh-CN.md) · [Português (Brasil)](PinnedReleases.pt-BR.md)

Normal Settings checks download one signed catalog per configured source and compare its approved versions with local installations. They do not scan application repositories. Publishing a newer upstream Release alone does not make it available to normal clients; each update needs a catalog PR and a new signed catalog.

## Submission files

Submit `apps/<appId>.json`, `icons/<appId>.png`, and the exact Release manifest downloaded into `releases/<appId>.flatpak-release.json`. If `publisher` is pinned, also include its detached signature as `releases/<appId>.flatpak-release.json.sig`. Do not reformat signed manifests. Installers stay in GitHub Release assets.

The application entry adds:

```json
"icon": "icons/org.example.Notes.png",
"release": {
  "version": "1.2.0",
  "tag": "v1.2.0",
  "manifestFile": "releases/org.example.Notes.flatpak-release.json"
}
```

Add `signatureFile` to `release` when a developer key is configured. Use explicit `"release": null` for listed applications without an approved compatible package; do not invent a version or silently fall back to upstream latest. The manifest supplies architecture-specific bundle filenames, SHA-256, sizes, commits, permissions metadata and runtime dependencies. Its app ID and version must match the entry. Review the actual published tag and attachments before approving a submission.

Use PNG icons, at most 1024 × 1024 and 512 KiB; 256 × 256 is recommended. Keep upstream attribution/licenses in `icons/`. The publisher computes SHA-256 and an immutable `raw.githubusercontent.com/<catalog repository>/<full commit>/icons/<appId>.png` URL. The client checks origin, size, dimensions and hash, caches the image, and falls back to a placeholder when missing or invalid. Icon downloads have a bounded refresh budget and are retried on later refreshes.

## Publishing and compatibility

On the VM/CI run `python3 build_catalog.py --check`, then `python3 build_catalog.py --sequence N --repository OWNER/REPO --revision FULL_COMMIT`. The revision must contain the reviewed icons. Never sign a directory assembled from uncommitted or different icon bytes. The workflow uses its checked-out commit automatically; third-party maintainers must set their own repository/source ID.

The generated **schema 2 catalog** embeds the original manifest bytes and optional developer signature in Base64, with a readable `release.version` and `release.tag`. Package hashes are therefore covered by the catalog signature, even when developer signing is omitted. Replacing both package and manifest upstream cannot change an already approved directory hash. Trust still depends on the catalog maintainer's review/key; this does not prove that an application is safe.

Clients need schema 2 support. Older clients reject schema 2 and retain their previous verified snapshot until expiry; upgrade Settings when migrating the source. New clients preserve schema 1 rollback history but never scan old unpinned entries for normal installations. Existing installations remain manageable. Test mode intentionally keeps explicit/Latest GitHub Release discovery for developer previews; it is separate from normal catalog approval.
