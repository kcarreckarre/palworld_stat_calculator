import math
import os
import sys

# Add local deps folder so fastapi/uvicorn/jinja2 are importable
_deps = os.path.join(os.path.dirname(__file__), ".deps")
if _deps not in sys.path:
    sys.path.insert(0, _deps)

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import sqlite3

sys.path.insert(0, os.path.dirname(__file__))
from stat_calcul import Stat, Pal, IV, EV, Bonus, calculate_palworld_damage

app = FastAPI(title="Palworld Damage Calculator")

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/images", StaticFiles(directory="images"), name="images")

templates = Jinja2Templates(directory="templates")


def get_db():
    conn = sqlite3.connect("pals.db")
    conn.row_factory = sqlite3.Row
    return conn


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/api/pals")
async def get_pals():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT name, local_img_path FROM pals ORDER BY name")
    rows = cursor.fetchall()
    conn.close()
    return [
        {"name": row["name"], "image": "/images/" + os.path.basename(row["local_img_path"])}
        for row in rows
    ]


class StatRequest(BaseModel):
    pal_name: str
    level: int = 1
    iv_hp: int = 0
    iv_def: int = 0
    iv_att: int = 0
    ev_hp: int = 0
    ev_def: int = 0
    ev_att: int = 0
    stars: int = 0
    bonus_hp: int = 0
    bonus_def: int = 0
    bonus_att: int = 0


@app.post("/api/calculate")
async def calculate(req: StatRequest):
    pal = Pal.from_name(req.pal_name)
    iv = IV(req.iv_hp, req.iv_def, req.iv_att)
    ev = EV(req.ev_hp, req.ev_def, req.ev_att)
    bonus = Bonus(req.bonus_hp, req.bonus_def, req.bonus_att)
    stats = Stat(pal, iv, ev, req.level, req.stars, bonus)
    return {
        "hp": stats.calculate_hp(),
        "defense": stats.calculate_defense(),
        "attack": stats.calculate_att(),
    }


class DamageRequest(BaseModel):
    attacker_level: int
    attacker_attack: float
    defender_defense: float
    defender_hp: float
    move_power: float
    stab: bool = False
    effectiveness: float = 1.0


@app.post("/api/damage")
async def damage(req: DamageRequest):
    if req.move_power <= 0 or req.defender_defense <= 0:
        return {"min_damage": 0, "max_damage": 0, "hits_min": None, "hits_max": None}

    result = calculate_palworld_damage(
        req.attacker_level, req.move_power, req.attacker_attack, req.defender_defense, req.stab
    )
    min_dmg = round(result["min_damage"] * req.effectiveness, 2)
    max_dmg = round(result["max_damage"] * req.effectiveness, 2)

    hits_min = hits_max = None
    if max_dmg > 0 and req.defender_hp > 0:
        hits_min = math.ceil(req.defender_hp / max_dmg)
        hits_max = math.ceil(req.defender_hp / min_dmg) if min_dmg > 0 else 9999

    return {
        "min_damage": min_dmg,
        "max_damage": max_dmg,
        "hits_min": hits_min,
        "hits_max": hits_max,
    }
