# Application artwork

These PNGs are catalog presentation assets, named by original application ID. All are 256-pixel previews. Keep artwork attribution and upstream licenses when replacing them.

- Calendar, Calculator, Weather: NextKde/kos-apps revision `98aadc63ea1079eeade823b9ac35c974509a907f`, `apps/org.nextks.<app>/data/kos-<app>.svg`; rasterized with Qt SVG in the development VM. See `kos-apps-LICENSE`.
- ListenFree: NextKde/ListenFree revision `69cb4cb77f28c03348efa5da2bf38ea2228e6fc6`, `music_player_desktop/assets/icons/app.png`; resized in the VM. See `listenfree-LICENSE`.
- KMusic: existing NextKde Settings `apps/settings/icons/kmusic.svg` from commit `2df7e9497ed10af1c75a297876f4b7b28e477af5`; rasterized in the VM. See `NextKde-LICENSE`.
- Notes: NextKde/NkNotes revision `2ca726f3b6e951acb4b79af7c811309c60f3f6b3`, `packaging/org.nextks.notes.svg`; rasterized in the VM. See `NkNotes-LICENSE` (GPL-3.0).

Submissions use PNG only, at most 1024 × 1024 and 512 KiB. The publisher computes SHA-256 and an immutable raw GitHub URL containing the full catalog commit. Icons are never installer inputs. Missing/invalid icons fall back to the client's placeholder.

- NkMail: NextKde/NkMail revision `03d3894d7087203202a7fa33286a028791b5e5ea`, `data/nkmail.svg`; rasterized in the VM. See `NkMail-LICENSE` (GPL-3.0).
