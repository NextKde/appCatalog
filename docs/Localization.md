# Catalog localization

[简体中文](Localization.zh-CN.md) · [Português (Brasil)](Localization.pt-BR.md)

Use locale maps for `name` and `description`. `en` is required as a nonempty fallback in both fields. The current Settings interface supports `en`, `zh-CN` and `pt-BR`; additional valid locale tags may be stored for future clients. Missing translations fall back to English. Documentation languages do not imply UI language support.

```json
"name": {"en": "Calendar", "zh-CN": "日历", "pt-BR": "Calendário"},
"description": {"en": "Plan your days and events", "zh-CN": "安排日程与活动", "pt-BR": "Organize seus dias e eventos"}
```

Keep appId, key, format, repository, manifest, statuses and fingerprints untranslated. Use plain text, no HTML or Markdown. Keep names at most 120 characters and descriptions at most 600; no control characters, empty values or more than 32 locales per field. Translation changes require the same catalog PR and signed publication as other metadata changes, but no new app binary.

App interface translations belong inside the app, independently of catalog translations. The initial bundle workflow should retain them with `separate-locales: false`; do not assume an app-specific Locale extension is available from the approved runtime source. See [Qt runtime](QtRuntime.md).
