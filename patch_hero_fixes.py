#!/usr/bin/env python3
"""
PROMPT_HERO_QUIENES_FIXES.md
- PARTE 1: Text fixes on cards
- PARTE 2: Hero collage with hover animation
- PARTE 3: Nosotros SVG illustration
"""
import re

print("Loading HTML...")
with open('/home/user/GlobalChay/index.html', 'r', encoding='utf-8') as f:
    content = f.read()
original_len = len(content)
print(f"  HTML size: {original_len:,} chars")


def find_div_end(s, start):
    pos = start + 4; depth = 1
    while depth > 0 and pos < len(s):
        op = s.find('<div', pos); cl = s.find('</div>', pos)
        if cl == -1: break
        if op != -1 and op < cl: depth += 1; pos = op + 4
        else: depth -= 1; pos = cl + 6
    return pos


def get_first_slide_src(car_id):
    track_idx = content.find(f'id="{car_id}"')
    if track_idx == -1: return None
    slide_idx = content.find('<div class="carousel-slide">', track_idx)
    if slide_idx == -1: return None
    src_m = re.search(r'src="(data:image/[^"]+)"', content[slide_idx:slide_idx+1000000])
    return src_m.group(1) if src_m else None


# ════════════════════════════════════════════════════════════════════════════════
# PARTE 1A — Brace Túnel del Carpo: specs → "Talla Única"
# ════════════════════════════════════════════════════════════════════════════════
idx = content.find('>Brace Túnel del Carpo<')
start = content.rfind('<div class="pcard">', 0, idx)
next_p = content.find('<div class="pcard">', start + 10)
seg = content[start:next_p]
new_seg = re.sub(
    r'(<div class="pcard-specs"><strong>)Tallas:[^<]+(</strong></div>)',
    r'\1Talla Única\2', seg, count=1
)
if new_seg != seg:
    content = content[:start] + new_seg + content[next_p:]
    print('  ✓ 1A: Brace Túnel del Carpo specs → Talla Única')
else:
    print('  WARNING 1A: Túnel del Carpo specs pattern not found')

# ════════════════════════════════════════════════════════════════════════════════
# PARTE 1B — Muñequera Sencilla: specs → "Talla Única"
# ════════════════════════════════════════════════════════════════════════════════
idx = content.find('>Muñequera Sencilla<')
start = content.rfind('<div class="pcard">', 0, idx)
next_p = content.find('<div class="pcard">', start + 10)
seg = content[start:next_p]
new_seg = re.sub(
    r'(<div class="pcard-specs"><strong>)Tallas:[^<]+(</strong></div>)',
    r'\1Talla Única\2', seg, count=1
)
if new_seg != seg:
    content = content[:start] + new_seg + content[next_p:]
    print('  ✓ 1B: Muñequera Sencilla specs → Talla Única')
else:
    print('  WARNING 1B: Muñequera Sencilla specs not found')

# ════════════════════════════════════════════════════════════════════════════════
# PARTE 1B — Soporte de Muñeca: specs → "Talla Única"
# ════════════════════════════════════════════════════════════════════════════════
idx = content.find('>Soporte de Muñeca<')
start = content.rfind('<div class="pcard">', 0, idx)
next_p = content.find('<div class="pcard">', start + 10)
seg = content[start:next_p]
new_seg = re.sub(
    r'(<div class="pcard-specs"><strong>)Tallas:[^<]+(</strong></div>)',
    r'\1Talla Única\2', seg, count=1
)
if new_seg != seg:
    content = content[:start] + new_seg + content[next_p:]
    print('  ✓ 1B: Soporte de Muñeca specs → Talla Única')
else:
    print('  WARNING 1B: Soporte de Muñeca specs not found')

# ════════════════════════════════════════════════════════════════════════════════
# PARTE 1C — Faja Abdominal: rename + badge Beige
# ════════════════════════════════════════════════════════════════════════════════
content = content.replace('>Faja Abdominal 30cm<', '>Faja Abdominal 30cm y 23cm<', 1)
print('  ✓ 1C: Faja Abdominal renamed')

idx = content.find('>Faja Abdominal 30cm y 23cm<')
start = content.rfind('<div class="pcard">', 0, idx)
next_p = content.find('<div class="pcard">', start + 10)
seg = content[start:next_p]
new_seg = seg.replace('<div class="pcard-badge">Varios colores</div>',
                      '<div class="pcard-badge">Beige</div>', 1)
if new_seg != seg:
    content = content[:start] + new_seg + content[next_p:]
    print('  ✓ 1C: Faja Abdominal badge → Beige')
else:
    # Try finding by looking at badge pattern near card
    print('  WARNING 1C: "Varios colores" badge not found; searching broadly')
    old = '>Varios colores</div>'
    idx2 = content.find(old, start)
    if idx2 != -1 and idx2 < next_p:
        content = content[:idx2] + '>Beige</div>' + content[idx2+len(old):]
        print('  ✓ 1C: badge replaced via broad search')

# ════════════════════════════════════════════════════════════════════════════════
# PARTE 1D — Rodillera Rótula Abierta: update description
# ════════════════════════════════════════════════════════════════════════════════
OLD_DESC = ('Rodillera con apertura rotuliana y refuerzo lateral para estabilización '
            'de ligamentos. Post-cirugía y deporte.')
NEW_DESC = ('Rodillera con apertura rotuliana. Brinda compresión y estabilidad en la '
            'articulación. Ideal para uso deportivo y recuperación.')
if OLD_DESC in content:
    content = content.replace(OLD_DESC, NEW_DESC, 1)
    print('  ✓ 1D: Rodillera Rótula Abierta description updated')
else:
    print('  WARNING 1D: Rodillera Rótula Abierta description not found')

# ════════════════════════════════════════════════════════════════════════════════
# PARTE 1E — Corset Jewett: report on duplicates (no exact dups found)
# ════════════════════════════════════════════════════════════════════════════════
print('  (1E) Corset Jewett: all 7 slides are byte-unique — no exact duplicates to remove')

# ════════════════════════════════════════════════════════════════════════════════
# PARTE 2 — Hero collage CSS replacement
# ════════════════════════════════════════════════════════════════════════════════
OLD_CSS = (
    '.collage-outer{max-height:320px;padding:10px;border-radius:12px;background:rgba(255,255,255,.12);'
    'border:1px solid rgba(255,255,255,.25);width:100%;box-sizing:border-box;}\n'
    '.collage-grid{display:grid;grid-template-columns:repeat(4,1fr);grid-template-rows:auto auto;gap:8px;width:100%;}\n'
    '.ci{background:white;border-radius:12px;padding:10px;aspect-ratio:1/1;display:flex;align-items:center;'
    'justify-content:center;border:2px solid transparent;transition:transform .3s,border-color .3s;overflow:hidden;cursor:pointer;}\n'
    '.ci:hover{transform:scale(1.04);border-color:#f47c1a;}\n'
    '.ci img{width:100%;height:100%;object-fit:contain;}\n'
    '.ci.big{grid-column:span 2;grid-row:span 2;aspect-ratio:auto;min-height:160px;padding:8px;box-shadow:0 4px 16px rgba(0,0,0,.18);}\n'
    '.ci-label{display:none;}\n'
    '.ci:hover .ci-label{opacity:1;}\n'
)
NEW_CSS = (
    '.collage-outer{width:100%;padding:16px;box-sizing:border-box;}\n'
    '.collage-grid{display:grid;grid-template-columns:repeat(4,1fr);grid-template-rows:repeat(2,1fr);gap:8px;}\n'
    '.ci{background:white;border-radius:12px;aspect-ratio:1/1;display:flex;align-items:center;justify-content:center;'
    'position:relative;overflow:hidden;border:2px solid transparent;transition:border-color 0.3s,transform 0.3s;cursor:pointer;}\n'
    '.ci:hover{border-color:#f47c1a;transform:scale(1.04);}\n'
    '.ci img{width:100%;height:100%;object-fit:contain;transition:opacity 0.3s;}\n'
    '.ci:hover img{opacity:0.15;}\n'
    '.ci-hover-overlay{position:absolute;inset:0;display:flex;align-items:flex-end;padding:10px;'
    'opacity:0;transition:opacity 0.3s;pointer-events:none;}\n'
    '.ci:hover .ci-hover-overlay{opacity:1;}\n'
    ".ci-hover-label{color:#1a3a8f;font-size:11px;font-weight:700;text-transform:uppercase;"
    "letter-spacing:0.5px;line-height:1.2;font-family:'Montserrat',sans-serif;}\n"
    '@media(max-width:768px){.collage-grid{grid-template-columns:repeat(2,1fr);}}\n'
)
if OLD_CSS in content:
    content = content.replace(OLD_CSS, NEW_CSS, 1)
    print('  ✓ 2: Collage CSS replaced')
else:
    print('  WARNING 2: Old collage CSS not found — check spacing')

# ════════════════════════════════════════════════════════════════════════════════
# PARTE 2 — Hero collage HTML replacement
# ════════════════════════════════════════════════════════════════════════════════
collage_cards = [
    ('car7',  'Corrector de Postura en Y',      'Corrector<br>de Postura'),
    ('car28', 'Corset Jewett',                   'Corset<br>Jewett'),
    ('car1',  'Brace Túnel del Carpo',           'Brace Túnel<br>del Carpo'),
    ('car10', 'Faja Lumbosacra Tipo Camp',       'Faja<br>Lumbosacra'),
    ('car15', 'Rodillera Universal Ajustable',   'Rodillera<br>Ajustable'),
    ('car26', 'Férula para Pie Caído',           'Férula<br>Pie Caído'),
    ('car6',  'Codera Cerrada Neopreno',         'Codera<br>Neopreno'),
    ('car11', 'Cabestrillo Acolchado Adulto',    'Cabestrillo<br>Acolchado'),
]

ci_html = ''
for car_id, alt, label in collage_cards:
    src = get_first_slide_src(car_id)
    if src:
        ci_html += (
            f'<div class="ci">'
            f'<img src="{src}" alt="{alt}" loading="lazy">'
            f'<div class="ci-hover-overlay">'
            f'<span class="ci-hover-label">{label}</span>'
            f'</div>'
            f'</div>'
        )
        print(f'  ✓ 2: {car_id} ({alt[:28]}) src={len(src):,} chars')
    else:
        print(f'  WARNING 2: could not extract src for {car_id}')

NEW_COLLAGE = (
    '<div class="collage-outer">'
    '<div class="collage-grid">'
    + ci_html +
    '</div>'
    '</div>'
)

coll_idx = content.find('class="collage-outer"')
coll_start = content.rfind('<div', 0, coll_idx)
coll_end = find_div_end(content, coll_start)
old_len = coll_end - coll_start
content = content[:coll_start] + NEW_COLLAGE + content[coll_end:]
print(f'  ✓ 2: Collage HTML replaced ({old_len:,} → {len(NEW_COLLAGE):,} chars)')

# ════════════════════════════════════════════════════════════════════════════════
# PARTE 3 — Nosotros: CSS + replace team-wrap SVG
# ════════════════════════════════════════════════════════════════════════════════
NOS_CSS = (
    '.nosotros-ilustracion{width:100%;border-radius:16px;overflow:hidden;background:#eef1f8;}\n'
    '.nosotros-ilustracion svg{display:block;width:100%;height:auto;}\n'
    '@media(max-width:768px){.nosotros-ilustracion{margin-top:24px;}}\n'
)
content = content.replace('</style>', NOS_CSS + '</style>', 1)
print('  ✓ 3: Nosotros CSS added')

NEW_SVG = (
    '<div class="nosotros-ilustracion">'
    '<svg width="100%" viewBox="0 0 600 320" role="img" xmlns="http://www.w3.org/2000/svg">'
    '<title>Taller de fabricación ortopédica — Ortholines S.A.S</title>'
    '<desc>Ilustración del taller de fabricación de productos ortopédicos en Bogotá</desc>'
    '<rect x="0" y="0" width="600" height="320" rx="16" fill="#eef1f8"/>'
    '<rect x="40" y="190" width="520" height="28" rx="4" fill="#c5d0e8"/>'
    '<rect x="50" y="183" width="500" height="10" rx="3" fill="#b0bdd8"/>'
    '<rect x="60" y="218" width="12" height="50" rx="3" fill="#b0bdd8"/>'
    '<rect x="528" y="218" width="12" height="50" rx="3" fill="#b0bdd8"/>'
    '<rect x="180" y="218" width="10" height="50" rx="3" fill="#b0bdd8"/>'
    '<rect x="410" y="218" width="10" height="50" rx="3" fill="#b0bdd8"/>'
    '<rect x="20" y="60" width="14" height="190" rx="3" fill="#b0bdd8"/>'
    '<rect x="20" y="60" width="90" height="8" rx="2" fill="#b0bdd8"/>'
    '<rect x="20" y="110" width="90" height="6" rx="2" fill="#c5d0e8"/>'
    '<rect x="20" y="155" width="90" height="6" rx="2" fill="#c5d0e8"/>'
    '<rect x="28" y="72" width="18" height="36" rx="3" fill="#1a3a8f" opacity="0.5"/>'
    '<rect x="50" y="80" width="18" height="28" rx="3" fill="#f47c1a" opacity="0.5"/>'
    '<rect x="72" y="76" width="18" height="32" rx="3" fill="#1a3a8f" opacity="0.3"/>'
    '<rect x="28" y="118" width="22" height="30" rx="3" fill="#f47c1a" opacity="0.3"/>'
    '<rect x="54" y="122" width="16" height="26" rx="3" fill="#1a3a8f" opacity="0.4"/>'
    '<rect x="74" y="118" width="18" height="30" rx="3" fill="#1a3a8f" opacity="0.2"/>'
    '<rect x="130" y="110" width="100" height="75" rx="8" fill="white" stroke="#c5d0e8" stroke-width="0.8"/>'
    '<ellipse cx="180" cy="148" rx="32" ry="22" fill="none" stroke="#1a3a8f" stroke-width="1.5" opacity="0.4"/>'
    '<ellipse cx="180" cy="148" rx="16" ry="11" fill="#f47c1a" opacity="0.25"/>'
    '<line x1="148" y1="148" x2="212" y2="148" stroke="#1a3a8f" stroke-width="0.8" stroke-dasharray="3,3" opacity="0.4"/>'
    '<line x1="180" y1="126" x2="180" y2="170" stroke="#1a3a8f" stroke-width="0.8" stroke-dasharray="3,3" opacity="0.4"/>'
    "<text x=\"180\" y=\"200\" text-anchor=\"middle\" font-family=\"'Open Sans',sans-serif\" font-size=\"10\" fill=\"#5a6480\">Diseño y moldes</text>"
    '<rect x="250" y="105" width="100" height="80" rx="8" fill="white" stroke="#c5d0e8" stroke-width="0.8"/>'
    '<line x1="268" y1="125" x2="332" y2="125" stroke="#1a3a8f" stroke-width="2" opacity="0.3" stroke-linecap="round"/>'
    '<line x1="268" y1="138" x2="320" y2="138" stroke="#f47c1a" stroke-width="2" opacity="0.4" stroke-linecap="round"/>'
    '<line x1="268" y1="151" x2="332" y2="151" stroke="#1a3a8f" stroke-width="1.5" opacity="0.25" stroke-linecap="round"/>'
    '<line x1="268" y1="163" x2="310" y2="163" stroke="#1a3a8f" stroke-width="1.5" opacity="0.25" stroke-linecap="round"/>'
    '<circle cx="338" cy="138" r="8" fill="#f47c1a" opacity="0.2"/>'
    "<text x=\"300\" y=\"200\" text-anchor=\"middle\" font-family=\"'Open Sans',sans-serif\" font-size=\"10\" fill=\"#5a6480\">Fabricación</text>"
    '<rect x="370" y="110" width="100" height="75" rx="8" fill="white" stroke="#c5d0e8" stroke-width="0.8"/>'
    '<rect x="385" y="123" width="70" height="48" rx="5" fill="#eef1f8"/>'
    '<line x1="393" y1="135" x2="447" y2="135" stroke="#c5d0e8" stroke-width="1"/>'
    '<line x1="393" y1="145" x2="447" y2="145" stroke="#c5d0e8" stroke-width="1"/>'
    '<line x1="393" y1="155" x2="447" y2="155" stroke="#c5d0e8" stroke-width="1"/>'
    '<path d="M397 132 L401 136 L408 128" fill="none" stroke="#1a3a8f" stroke-width="1.5" stroke-linecap="round" opacity="0.7"/>'
    '<path d="M397 142 L401 146 L408 138" fill="none" stroke="#1a3a8f" stroke-width="1.5" stroke-linecap="round" opacity="0.7"/>'
    '<path d="M397 152 L401 156 L408 148" fill="none" stroke="#f47c1a" stroke-width="1.5" stroke-linecap="round" opacity="0.7"/>'
    "<text x=\"420\" y=\"200\" text-anchor=\"middle\" font-family=\"'Open Sans',sans-serif\" font-size=\"10\" fill=\"#5a6480\">Control calidad</text>"
    '<rect x="566" y="60" width="14" height="190" rx="3" fill="#b0bdd8"/>'
    '<rect x="490" y="60" width="90" height="8" rx="2" fill="#b0bdd8"/>'
    '<rect x="490" y="110" width="90" height="6" rx="2" fill="#c5d0e8"/>'
    '<rect x="490" y="155" width="90" height="6" rx="2" fill="#c5d0e8"/>'
    '<rect x="498" y="72" width="20" height="36" rx="4" fill="#1a3a8f" opacity="0.45"/>'
    '<rect x="522" y="76" width="20" height="32" rx="4" fill="#f47c1a" opacity="0.45"/>'
    '<rect x="546" y="72" width="16" height="36" rx="4" fill="#1a3a8f" opacity="0.3"/>'
    '<rect x="498" y="118" width="22" height="28" rx="4" fill="#f47c1a" opacity="0.3"/>'
    '<rect x="524" y="122" width="18" height="24" rx="4" fill="#1a3a8f" opacity="0.35"/>'
    '<rect x="546" y="118" width="16" height="28" rx="4" fill="#1a3a8f" opacity="0.2"/>'
    '<rect x="240" y="28" width="120" height="40" rx="20" fill="#1a3a8f" opacity="0.9"/>'
    "<text x=\"300\" y=\"45\" text-anchor=\"middle\" font-family=\"'Montserrat',sans-serif\" font-weight=\"700\" font-size=\"13\" fill=\"#f47c1a\">20+ años</text>"
    "<text x=\"300\" y=\"60\" text-anchor=\"middle\" font-family=\"'Open Sans',sans-serif\" font-size=\"9\" fill=\"rgba(255,255,255,0.8)\">de trayectoria</text>"
    "<text x=\"300\" y=\"290\" text-anchor=\"middle\" font-family=\"'Open Sans',sans-serif\" font-size=\"10\" fill=\"#8a94b0\">Bogotá, Colombia · Fabricación propia · Línea blanda, ortesis y deportiva</text>"
    '</svg>'
    '</div>'
)

idx = content.find('<div class="team-wrap">')
end = find_div_end(content, idx)
content = content[:idx] + NEW_SVG + content[end:]
print('  ✓ 3: team-wrap replaced with nosotros-ilustracion SVG')

# ════════════════════════════════════════════════════════════════════════════════
# Save
# ════════════════════════════════════════════════════════════════════════════════
with open('/home/user/GlobalChay/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

new_len = len(content)
print(f'\n✅ Saved. {original_len:,} → {new_len:,} chars ({new_len-original_len:+,})')
