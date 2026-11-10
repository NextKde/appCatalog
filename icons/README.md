# Application and category artwork

The application family uses a shared continuous rounded tile, soft vertical color,
ivory paper or symbols, a fine edge and restrained depth. The user-provided Notes
reference establishes the visual direction. These are original NextKde drawings;
no Apple image assets are included in the category navigation.

Application SVGs remain canonical in their own repositories. The catalog stores
256 × 256 RGBA PNG exports, rendered with Qt SVG in the dedicated development VM.
ListenFree also ships a 1024 × 1024 PNG and a multiresolution Windows ICO from the
same SVG. No external images, fonts, filters or clipping paths are needed by the
SVGs. Category glyphs remain legible at the 18-pixel navigation size. Material
navigation uses its existing semantic monochrome glyphs.

## Canonical application sources

- `org.nextkde.KMusic`: `NextKde/NkMusic`, `data/kmusic.svg`.
- `org.nextkde.ListenFree`: `NextKde/ListenFree`, `music_player_desktop/assets/icons/app.svg`.
- `org.nextkde.NkMail`: `NextKde/NkMail`, `data/nkmail.svg`.
- `org.nextks.calendar`: `NextKde/kos-apps`, `apps/org.nextks.calendar/data/kos-calendar.svg`.
- `org.nextks.calculator`: `NextKde/kos-apps`, `apps/org.nextks.calculator/data/kos-calculator.svg`.
- `org.nextks.notes`: `NextKde/NkNotes`, `packaging/org.nextks.notes.svg`.
- `org.nextks.weather`: `NextKde/kos-apps`, `apps/org.nextks.weather/data/kos-weather.svg`.

Source revision pins are recorded in `artwork-sources.json`. Existing upstream
licenses and license copies remain applicable. Application identities, approved
package versions, publisher keys and permissions are independent of artwork.
