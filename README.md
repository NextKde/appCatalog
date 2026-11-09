# NextKde appCatalog

**English** · [简体中文](README.zh-CN.md) · [Português (Brasil)](README.pt-BR.md)

The submission repository for NextKde Settings → **Applications and services**.
Applications live in their developers' **GitHub Releases**. This repository publishes a signed list of approved application identities and release locations; it does not host installers or execute submission scripts.

The client integration is under development. A repository entry alone does not mean an application is available in an existing NextKde release: the client must support signed catalogs, and the application must publish a compatible package. Catalog releases and client releases are separate. The client change is tracked in [NextKde PR #340](https://github.com/NextKde/NextKde/pull/340); [catalog-1](https://github.com/NextKde/appCatalog/releases/tag/catalog-1) is the first signed directory.

## Submit an application

1. Build a Flatpak bundle with a stable application ID. Read the [Qt runtime and packaging guide](docs/QtRuntime.md).
2. Publish a non-draft, non-prerelease GitHub Release tagged `vX.Y.Z`. Attach the bundle and the JSON [release manifest](RELEASE-CONTRACT.md), including SHA-256. Developer signatures are optional.
3. Add `apps/<appId>.json` in a pull request, following this example and the [localization rules](docs/Localization.md).
4. Maintainers review ownership, identity, permissions and release assets, merge the entry, then publish a new signed catalog. Clients learn the new app on refresh, without rebuilding Settings.

```json
{
  "appId": "org.example.Notes",
  "key": "notes",
  "format": "flatpak",
  "name": {"en": "Notes", "zh-CN": "笔记", "pt-BR": "Notas"},
  "description": {"en": "A small notes application", "zh-CN": "轻量笔记应用", "pt-BR": "Um aplicativo simples de notas"},
  "repository": "example-org/notes",
  "manifest": "flatpak-release.json",
  "status": "active"
}
```

`repository` is a GitHub `owner/repository`, not a URL. Use the canonical repository name; repository renames require catalog review. `appId` and `key` are stable identities, never translated. Flatpak is the only implemented package adapter. Future formats require a client adapter; catalogs cannot supply install commands.

Normal new application versions need only a new application Release. No catalog PR is needed unless its identity, description, trust policy or release location changes. To delist, remove the entry or set `status` to `withdrawn`; use `revoked` to stop trusting it. These block later installs/updates without deleting installed apps or user data.

## Trust and publication

Catalog signatures are mandatory; package SHA-256 is mandatory. Optional `publisher` contains a full primary-key `fingerprint` and a Base64 binary OpenPGP `publicKey`. If present, both the release manifest signature (`<manifest>.sig`) and the Flatpak commit signature are required. Failed or missing signatures never fall back to unsigned mode.

Without a publisher key, package authenticity depends on the approved GitHub account and HTTPS. SHA-256 detects a mismatched download, but cannot stop an attacker controlling the repository from replacing both package and manifest. Neither signature nor hash proves that an app is benign.

See [Maintainer publication](MAINTAINING.md) for secrets, expiry, sequence numbers and release steps. The seed entries retain their existing publisher signatures; catalog publication does not publish their application bundles.

## Third-party sources

Use the same catalog format in your own GitHub repository, with your own signing key and a unique `sourceId`. The client requires `catalog.json` and `catalog.json.sig` in a stable GitHub Release. Follow [Maintainer publication](MAINTAINING.md), including changing the workflow's source ID and pinned public key.

Users add the source in Settings → Applications and services → Manage application sources, supplying its ID, GitHub `owner/repository`, binary `.gpg` public-key file and full fingerprint, then explicitly accepting trust. Obtain the fingerprint through an independently trusted channel. The source ID must match the signed document. Sources cannot silently replace each other's app IDs. Removing a source keeps installed app management and rollback-protection history.

The [NextKde architecture guide](https://github.com/NextKde/NextKde/blob/0f8fe2779a049af7d873c7538ab310e67d1fc8be/docs/app-store/SignedCatalog.md) describes the client and automatic update notifications. Settings lists available versions; the background agent checks metadata and notifies, but does not install updates automatically.
