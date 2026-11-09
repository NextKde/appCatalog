# GitHub Release / Flatpak contract

All application discovery uses `https://api.github.com/repos/OWNER/REPOSITORY/releases/latest`.
Only published stable `vX.Y.Z` releases are accepted. Each required asset must be unique in that release.
Asset downloads are confined to the registered GitHub repository and GitHub's release CDN redirects.

The catalog's `manifest` names a JSON release asset. The version must equal the release tag without `v`.
SHA-256 describes the exact bytes of the `.flatpak` attachment. Do not hash the source archive instead.

```json
{
  "schemaVersion": 2,
  "appId": "org.example.Notes",
  "version": "1.0.0",
  "revision": "<40 lowercase hex characters: source revision>",
  "bundles": {
    "x86_64": {
      "asset": "org.example.Notes-1.0.0-x86_64.flatpak",
      "ref": "app/org.example.Notes/x86_64/stable",
      "commit": "<64 lowercase hex characters: OSTree commit>",
      "sha256": "<64 lowercase hex characters: bundle SHA-256>",
      "size": 123456,
      "metadata": "<Base64 of exact Flatpak application metadata bytes>",
      "metadataSha256": "<SHA-256 of decoded metadata, including trailing newline>",
      "installedSize": 234567,
      "runtime": {"ref": "runtime/org.kde.Platform/x86_64/6.8"},
      "requiredExtensions": []
    }
  }
}
```

Angle-bracket values are explanatory placeholders, not valid hashes. Actual sizes and metadata must be extracted from the final bundle. The client compares them before deployment, and independently resolves approved runtime dependencies. The bundle cannot embed online origin or runtime-repository URLs.

If the catalog contains a `publisher`, also publish `<manifest>.sig` signed over the exact JSON bytes, and sign the bundle's OSTree commit with the authorized developer key. Do not ship private keys.

Without `publisher`, no developer signature is required. The client still checks GitHub ownership routing, release identity, architecture, SHA-256, metadata, installation plan, version order and source ownership receipts.

Flatpak is the first backend. The signed catalog's `format` field is the dispatch boundary for future package adapters; it does not contain arbitrary installation commands. GitHub Releases remain mandatory for every format.
