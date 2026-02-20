# Diaper Tracker — Claude Notes

## Overview
- URL: (local/internal, no public subdomain)
- App root: `/opt/diaper-tracker/`
- Port: 5003 (proxied via nginx or run directly)
- Stack: Python 3.12 venv, Flask, Gunicorn, SQLite, ReportLab, openpyxl
- Systemd service: `diaper-tracker.service`
- Database: `/opt/diaper-tracker/database.db`
- GitHub repo: `https://github.com/volfan37135/diaper-tracker` (private)

## Key Files
| File | Purpose |
|------|---------|
| `app.py` | Flask app, all routes |
| `models.py` | SQLite queries and migrations |
| `forms.py` | WTForms definitions (PurchaseForm, BrandForm) |
| `templates/base.html` | Base layout with navbar |
| `templates/index.html` | Dashboard (stats + recent purchases) |
| `templates/add_purchase.html` | Add purchase form |
| `templates/history.html` | Full purchase history with box-opening UI |
| `templates/inventory.html` | Inventory tab (read-only, per-size box counts) |
| `templates/manage_brands.html` | Brand management |
| `static/css/style.css` | All styles (light + dark mode via CSS vars) |
| `static/js/main.js` | Nav toggle, dark mode, alert auto-dismiss |

## Routes
| Route | Handler | Purpose |
|-------|---------|---------|
| `/` | `index` | Dashboard |
| `/add` | `add_purchase` | Add purchase form |
| `/inventory` | `inventory` | Per-size inventory summary |
| `/history` | `history` | Full history + box opening |
| `/brands` | `manage_brands` | Brand list management |
| `/export/pdf` | `export_pdf` | PDF report download |
| `/export/excel` | `export_excel` | Excel download |
| `/api/brands` | `api_brands` | JSON brand list |

## Database Schema
### purchases
- `id`, `date`, `size` (e.g. "Size 3"), `num_boxes`, `diapers_per_box`, `brand`, `cost` (nullable), `created_at`

### box_openings
- `id`, `purchase_id` (FK), `box_number`, `date_opened` (nullable), `created_at`
- One row per box per purchase; `date_opened` NULL = unopened

### brands
- `id`, `brand_name` (unique), `created_at`

## Migrations (run automatically on startup)
- `migrate_add_size_column` — adds size column if missing
- `migrate_box_openings` — backfills box_opening rows for old purchases
- `migrate_cost_nullable` — drops NOT NULL from cost column

## Inventory Logic
- `models.get_inventory_by_size()` aggregates by `purchases.size`
- Uses subquery to count opened boxes per purchase, then LEFT JOINs and sums — avoids row-multiplication from direct JOIN
- Boxes Unopened = total boxes purchased − boxes with a non-null `date_opened`
- Boxes Used = boxes with a non-null `date_opened`
- Sorted by canonical `SIZE_ORDER`: Newborn → Size 1 → … → Size 7 (unknowns last)
- Template auto-refreshes every 60 seconds; also has a manual Refresh button
- Zero-stock rows highlighted in red (`--danger` CSS var)

## Diaper Sizes
Defined in `forms.py` `SIZE_CHOICES`: Newborn, Size 1–7

## Cost Field
Optional — leave blank for gift/unknown purchases. Stored as NULL in SQLite.

## CSS / Theming
- No framework — pure custom CSS in `static/css/style.css`
- CSS variables for colors (`--bg`, `--bg-card`, `--primary`, `--danger`, etc.)
- Dark mode: `[data-theme="dark"]` selector; toggled via JS, persisted in localStorage
- Navbar background: `--nav-bg` (#2c3e50 light / #0f3460 dark)

## Screenshots
- Stored in `static/images/` — `screenshot-dashboard.png`, `screenshot-history.png`, `screenshot-inventory.png`
- Referenced in `README.md`
- To retake all:
  ```
  google-chrome --headless --no-sandbox --disable-gpu --screenshot=/opt/diaper-tracker/static/images/screenshot-dashboard.png --window-size=1280,900 http://localhost:5003/
  google-chrome --headless --no-sandbox --disable-gpu --screenshot=/opt/diaper-tracker/static/images/screenshot-history.png --window-size=1280,900 http://localhost:5003/history
  google-chrome --headless --no-sandbox --disable-gpu --screenshot=/opt/diaper-tracker/static/images/screenshot-inventory.png --window-size=1280,900 http://localhost:5003/inventory
  ```

## Notes
- No ORM — raw SQLite3 with `row_factory = sqlite3.Row`
- CSRF protection via Flask-WTF on all POST forms
- `no-store` cache headers on all HTML responses
- Gunicorn workers: check service file if changing (exports use in-memory buffers, safe for multiple workers)
