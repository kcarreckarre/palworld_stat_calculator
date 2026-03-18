// ── State ──────────────────────────────────────────────────────────────────
let palList   = [];
let palImages = {};
let statsLeft  = { hp: 0, defense: 0, attack: 0 };
let statsRight = { hp: 0, defense: 0, attack: 0 };

// ── Utility ────────────────────────────────────────────────────────────────
function debounce(fn, ms) {
  let t;
  return (...args) => { clearTimeout(t); t = setTimeout(() => fn(...args), ms); };
}

function $(id) { return document.getElementById(id); }

function intVal(id) { return parseInt($(id).value) || 0; }

// ── Load pals from API ─────────────────────────────────────────────────────
async function loadPals() {
  const res = await fetch('/api/pals');
  palList   = await res.json();
  palImages = Object.fromEntries(palList.map(p => [p.name, p.image]));

  if (palList.length > 0) {
    selectPal('left',  palList[0].name);
    selectPal('right', palList[0].name);
  }
}

// ── Pal selection ──────────────────────────────────────────────────────────
function selectPal(side, name) {
  $(`name-${side}`).value = name;
  const img = $(`img-${side}`);
  img.src = palImages[name] || '';
  img.alt = name;
  closeAC(side);
  calculateStats(side);
}

// ── Autocomplete ───────────────────────────────────────────────────────────
function setupAC(side) {
  const input = $(`name-${side}`);
  const list  = $(`ac-${side}`);
  let activeIdx = -1;

  function renderList(matches) {
    list.innerHTML = '';
    activeIdx = -1;
    if (matches.length === 0) { closeAC(side); return; }

    matches.forEach((pal, i) => {
      const item = document.createElement('div');
      item.className = 'autocomplete-item';
      item.textContent = pal.name;
      item.addEventListener('mousedown', e => {
        e.preventDefault();
        selectPal(side, pal.name);
      });
      list.appendChild(item);
    });
    list.classList.add('open');
  }

  function moveActive(dir) {
    const items = list.querySelectorAll('.autocomplete-item');
    if (!items.length) return;
    items[activeIdx]?.classList.remove('active');
    activeIdx = (activeIdx + dir + items.length) % items.length;
    items[activeIdx].classList.add('active');
    items[activeIdx].scrollIntoView({ block: 'nearest' });
  }

  input.addEventListener('input', () => {
    const q = input.value.toLowerCase().trim();
    if (!q) { closeAC(side); return; }
    const matches = palList.filter(p => p.name.toLowerCase().includes(q)).slice(0, 25);
    renderList(matches);
  });

  input.addEventListener('keydown', e => {
    if (e.key === 'ArrowDown')  { e.preventDefault(); moveActive(1); }
    if (e.key === 'ArrowUp')    { e.preventDefault(); moveActive(-1); }
    if (e.key === 'Enter') {
      const active = list.querySelector('.autocomplete-item.active');
      if (active) { selectPal(side, active.textContent); return; }
      const exact = palList.find(p => p.name.toLowerCase() === input.value.toLowerCase());
      const first = list.querySelector('.autocomplete-item');
      if (exact)      selectPal(side, exact.name);
      else if (first) selectPal(side, first.textContent);
    }
    if (e.key === 'Escape') closeAC(side);
  });

  input.addEventListener('blur', () => setTimeout(() => closeAC(side), 160));
}

function closeAC(side) {
  $(`ac-${side}`).classList.remove('open');
}

// ── Read all inputs for one side ───────────────────────────────────────────
function readInputs(side) {
  return {
    pal_name:  $(`name-${side}`).value,
    level:     intVal(`lvl-${side}`),
    stars:     intVal(`stars-${side}`),
    iv_hp:     intVal(`iv-hp-${side}`),
    iv_def:    intVal(`iv-def-${side}`),
    iv_att:    intVal(`iv-att-${side}`),
    ev_hp:     intVal(`ev-hp-${side}`),
    ev_def:    intVal(`ev-def-${side}`),
    ev_att:    intVal(`ev-att-${side}`),
    bonus_hp:  intVal(`bonus-hp-${side}`),
    bonus_def: intVal(`bonus-def-${side}`),
    bonus_att: intVal(`bonus-att-${side}`),
  };
}

// ── Calculate stats for one side ──────────────────────────────────────────
async function calculateStats(side) {
  const inputs = readInputs(side);
  if (!inputs.pal_name) return;

  try {
    const res = await fetch('/api/calculate', {
      method:  'POST',
      headers: { 'Content-Type': 'application/json' },
      body:    JSON.stringify(inputs),
    });
    if (!res.ok) return;
    const data = await res.json();

    $(`hp-${side}`).textContent  = data.hp;
    $(`def-${side}`).textContent = data.defense;
    $(`att-${side}`).textContent = data.attack;

    if (side === 'left') statsLeft  = data;
    else                 statsRight = data;

    calculateDamage();
  } catch (e) {
    console.error('calculateStats error:', e);
  }
}

// ── Calculate damage ───────────────────────────────────────────────────────
async function calculateDamage() {
  const movePower     = parseFloat($('move-power').value) || 0;
  const stab          = $('stab').checked;
  const effectiveness = parseFloat($('effectiveness').value);

  const clear = () => {
    $('min-damage').textContent  = '—';
    $('max-damage').textContent  = '—';
    $('hits-to-ko').textContent  = '—';
  };

  if (movePower <= 0 || !statsLeft.attack || !statsRight.defense) { clear(); return; }

  try {
    const res = await fetch('/api/damage', {
      method:  'POST',
      headers: { 'Content-Type': 'application/json' },
      body:    JSON.stringify({
        attacker_level:   intVal('lvl-left'),
        attacker_attack:  statsLeft.attack,
        defender_defense: statsRight.defense,
        defender_hp:      statsRight.hp,
        move_power:       movePower,
        stab,
        effectiveness,
      }),
    });
    if (!res.ok) { clear(); return; }
    const data = await res.json();

    $('min-damage').textContent = data.min_damage.toFixed(2);
    $('max-damage').textContent = data.max_damage.toFixed(2);

    if (data.hits_min !== null) {
      $('hits-to-ko').textContent =
        data.hits_min === data.hits_max
          ? `${data.hits_min}`
          : `${data.hits_min} – ${data.hits_max}`;
    } else {
      $('hits-to-ko').textContent = '—';
    }
  } catch (e) {
    console.error('calculateDamage error:', e);
    clear();
  }
}

// ── Bind inputs for one side ───────────────────────────────────────────────
function bindSide(side) {
  const debounced = debounce(() => calculateStats(side), 280);
  [
    `lvl-${side}`, `stars-${side}`,
    `iv-hp-${side}`,    `iv-def-${side}`,    `iv-att-${side}`,
    `ev-hp-${side}`,    `ev-def-${side}`,    `ev-att-${side}`,
    `bonus-hp-${side}`, `bonus-def-${side}`, `bonus-att-${side}`,
  ].forEach(id => {
    $(id).addEventListener('input',  debounced);
    $(id).addEventListener('change', debounced);
  });
}

// ── Init ───────────────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', async () => {
  setupAC('left');
  setupAC('right');
  bindSide('left');
  bindSide('right');

  const debouncedDmg = debounce(calculateDamage, 200);
  $('move-power').addEventListener('input', debouncedDmg);
  $('stab').addEventListener('change', calculateDamage);
  $('effectiveness').addEventListener('change', calculateDamage);

  await loadPals();
});
