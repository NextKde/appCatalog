# Qt runtime and Flatpak packaging

[简体中文](QtRuntime.zh-CN.md) · [Português (Brasil)](QtRuntime.pt-BR.md)

For Qt 6 / Qt Quick applications, use **`org.kde.Platform`** to run the app and the matching **`org.kde.Sdk`** to build it. Keep the branch and architecture identical. These are shared Flatpak runtimes, not a separate NextKde QtRuntime package. The host's Qt, Plasma and Quickshell installations do not satisfy a sandbox's dependencies.

The current `NextKde/kos-apps` manifests use branch **6.11**. This is a concrete project reference, not a promise that every Qt app is compatible or that the branch is always the latest. Choose a maintained branch containing the Qt modules your app needs, and check it in the build VM before publishing. See the [official Flatpak runtime guide](https://docs.flatpak.org/en/latest/available-runtimes.html) and [KDE manifest guide](https://develop.kde.org/docs/packaging/flatpak/manifest/).

## Manifest starting point

```json
{
  "app-id": "org.example.Notes",
  "runtime": "org.kde.Platform",
  "runtime-version": "6.11",
  "sdk": "org.kde.Sdk",
  "command": "example-notes",
  "separate-locales": false,
  "finish-args": ["--socket=wayland", "--socket=fallback-x11", "--share=ipc", "--device=dri"],
  "modules": [{
    "name": "notes",
    "buildsystem": "cmake-ninja",
    "sources": [{"type": "git", "url": "https://github.com/example-org/notes.git", "commit": "REPLACE_WITH_FULL_SOURCE_COMMIT"}]
  }]
}
```

This is a template: replace the source commit, executable and build system with real values. Add network, audio, filesystem or D-Bus permissions only when the app needs them. Prefer portals for file selection. Bundle app-specific libraries under `/app`; do not replace runtime Qt libraries with host paths or global library-path hacks. Install QML modules, plugins, desktop metadata and icons as part of the app build.

Keep app translations in the bundle (`separate-locales: false`) for this initial client. An app-specific `.Locale` or other required extension is not automatically published to the approved runtime source by uploading one bundle. The client cannot resolve arbitrary developer extension repositories. Runtime locale data and catalog translations are separate concerns. See [Localization](Localization.md).

## Build and release

Build and validate in a development VM or CI. Install the matching SDK/runtime there, run `flatpak-builder` for the chosen architecture and export a `stable` app ref. Export using `flatpak build-bundle` **without** `--repo-url` or `--runtime-repo`; bundles must not inject online origins.

Generate the schema-2 [release manifest](../RELEASE-CONTRACT.md) from the final bundle and its exact OSTree metadata: commit, ref, sizes, SHA-256, runtime and required extensions. Metadata is bytes: preserve the trailing newline when hashing and Base64-encoding. A source archive hash is not the package hash. The [kos-apps producer](https://github.com/NextKde/kos-apps/blob/main/packaging/flatpak/prepare-bundle.py) demonstrates extraction and signing for those applications; it is not a generic tool for arbitrary app IDs.

Test first install, upgrade, uninstall with data preserved, offline launch and each advertised architecture. Publish a stable `vX.Y.Z` GitHub Release with the manifest and bundle(s), and signatures if configured. Then submit the catalog entry. Do not advertise architectures for which no final bundle exists.

## What the client downloads

The application always comes from its registered GitHub Release. Missing runtime dependencies come only from the client's separately approved, pinned Flathub runtime source; the app itself does not need a Flathub listing. Explicit Install/Update may prepare that runtime source. Adding an application catalog does not grant authority to add arbitrary runtime sources.

Compatible installed runtimes are reused by ID, architecture, branch and approved origin. The first download may be large; apps sharing the same runtime do not each ship another full Qt copy. The user sees the dependency/download plan before deployment. A cancelled plan may leave the prepared runtime source in place. A missing or unsupported dependency blocks installation; it does not fall back to native Qt.
