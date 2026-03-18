# Palworld Damage Calculator

A web-based stat and damage calculator for Palworld. Select two Pals, configure their Level, Stars, IVs, EVs, and Passive Skill bonuses, then instantly see calculated HP / DEF / ATT and the full damage range of any move.

## Features

- **Live stat calculation** — updates as you type, no button needed
- **Pal image + autocomplete search** with keyboard navigation
- **All modifiers** — Level (1–60), Stars (0–4), IV (0–100), EV% (0–30), Passive Skill Bonus%
- **Damage calculator** — Move Power, STAB, Type Effectiveness (0× / 0.5× / 1× / 1.5×)
- **Hits to KO** — how many hits the attacker needs to knock out the defender
- **Dark Palworld-themed UI** — runs in any browser, no install needed for end users

## Project Structure

```
├── main.py               # FastAPI backend — API endpoints for stats & damage
├── run.py                # One-command launcher
├── stat_calcul.py        # Core stat formulas (HP, DEF, ATT, damage)
├── store_pal_database.py # Populates pals.db from scraped JSON
├── scrape_pals.js        # Puppeteer scraper — pal base stats & elements
├── scrape_skill.js       # Puppeteer scraper — pal active skills
├── templates/
│   └── index.html        # Single-page UI
├── static/
│   ├── style.css         # Dark theme
│   └── app.js            # Frontend logic (autocomplete, API calls)
├── images/               # Local pal images (downloaded by store_pal_database.py)
├── pals.db               # SQLite database used by the app
└── requirements.txt      # Python dependencies
```

## Quick Start

### 1. Install Python dependencies

```bash
pip install -r requirements.txt
```

> If pip fails due to file locks (Windows), install to a local folder:
> ```bash
> pip install --target .deps fastapi uvicorn jinja2
> ```
> `run.py` handles this automatically.

### 2. Launch the web app

```bash
python run.py
```

Open **http://127.0.0.1:8000** in your browser.

## Data Pipeline (optional — pals.db is already included)

If you want to re-scrape the data from scratch:

### Step 1 — Scrape pal stats
```bash
node scrape_pals.js
```
Produces `pals_data.json`.

### Step 2 — Scrape pal skills
```bash
node scrape_skill.js
```
Produces `pals_skill_details.json`.

### Step 3 — Build the database
```bash
python store_pal_database.py
```
Downloads pal images to `images/` and populates `pals.db`.

## Stat Formulas

Based on community research ([u/blahable](https://www.reddit.com/u/blahable)):

```
HP  = (500 + 5×Lvl + BaseHP  × 0.5   × Lvl × (1 + HP_IV%))  × (1 + PSBonus%) × (1 + EV%) × (1 + Stars×5%)
DEF = ( 50 + BaseDEF × 0.075 × Lvl × (1 + DEF_IV%)) × (1 + PSBonus%) × (1 + EV%) × (1 + Stars×5%)
ATT = (100 + BaseATT × 0.075 × Lvl × (1 + ATT_IV%)) × (1 + PSBonus%) × (1 + EV%) × (1 + Stars×5%)

IV% = TalentInt × 0.3 / 100   (TalentInt: 0–100, IV%: 0–30%)

Damage = 1.1 × ((1.5×Lvl + 20) × MovePower × ATT / DEF) / 15
       × (1.2 if STAB) × TypeEffectiveness × RNG(0.9–1.1)
```

## Requirements

- Python 3.8+
- Node.js (only for scraping)
- `fastapi`, `uvicorn`, `jinja2` (Python)
- `puppeteer` (Node — scraping only)
