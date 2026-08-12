# Atlas logo, 2026 mark

Canonical source of truth lives outside the repo, in iCloud at
`AncientAtlas/Brand-Logos-2026/`. What is committed here is only what the
build and the render rigs actually need.

## What is in the repo

| File | Variant | Notes |
|---|---|---|
| `branding/logos-2026/atlas-logo-2026-obsidian-1024.png` | flattened on obsidian, **no alpha** | 1024×1024. Only copy in the repo. Use where a hard background is wanted and compositing is not. |
| `scripts/og-cards/logo.png` | transparent, **alpha** | 1024×1024. Read by `scripts/og-cards/render.py` at a relative path. |
| `scripts/assets/brand-logo.png` | transparent, **alpha** | 1024×1024. Byte-identical twin of the above. |

The two transparent files are the same bytes (`bcc2f8e9…`). They are
duplicated because each rig reads its own copy by relative path. Collapsing
them to one canonical path is worth doing, but it means touching the render
scripts, so it is deliberately left alone rather than half-done.

## Why `_stage/` is ignored

Logos arrive from iCloud into a scratch `_stage/` folder before being placed.
That folder is in `.gitignore` — files sitting there are working copies, not
deliverables, and they were showing up as untracked noise in GitHub Desktop.
Put a file in its permanent home under `branding/` or `scripts/` to commit it.
