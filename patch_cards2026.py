#!/usr/bin/env python3
"""
PARTE 2: Replace images in existing cards
PARTE 3: Create 12 new cards
PARTE 4: Add rodilla-sec to cat-nav and create rodilla section
"""
import re, os

# ── Load all b64 images ──────────────────────────────────────────────────────
print("Loading images...")
imgs = {}
for f in sorted(os.listdir('/tmp/ortho_imgs/')):
    key = f.replace('.b64', '')
    with open(f'/tmp/ortho_imgs/{f}', 'r') as fh:
        imgs[key] = fh.read().strip()
print(f"  Loaded {len(imgs)} images")

# ── Load HTML ────────────────────────────────────────────────────────────────
with open('/home/user/GlobalChay/index.html', 'r', encoding='utf-8') as f:
    content = f.read()
original_len = len(content)
print(f"  HTML size: {original_len:,} chars")

# ── Extract WS gif ───────────────────────────────────────────────────────────
ws_m = re.search(r'"(data:image/gif;base64,[^"]+)"[^>]*alt="WS"', content)
WS_GIF = ws_m.group(1) if ws_m else 'data:image/gif;base64,'

# ────────────────────────────────────────────────────────────────────────────
# PARTE 2: Replace images in existing cards
# ────────────────────────────────────────────────────────────────────────────

def replace_card_imgs(card_name, img_keys):
    """Replace product PNG images in a pcard (img_keys=[main, hover, ...])"""
    global content
    idx_name = content.find(f'>{card_name}<')
    if idx_name == -1:
        print(f'  WARNING: card "{card_name}" not found')
        return
    start = content.rfind('<div class="pcard">', 0, idx_name)
    next_pcard = content.find('<div class="pcard">', start + 10)
    end = next_pcard if next_pcard > 0 else start + 3000000
    segment = content[start:end]

    # Find all PNG img positions in this segment
    pattern = r'src="data:image/png;base64,[^"]+"'
    matches = list(re.finditer(pattern, segment))

    # Replace in reverse order to preserve offsets
    changes = []
    for i, key in enumerate(img_keys):
        if i >= len(matches):
            print(f'  WARNING: slot {i} not found in "{card_name}" ({len(matches)} slots)')
            continue
        if key not in imgs:
            print(f'  WARNING: image "{key}" not in imgs')
            continue
        changes.append((i, key))

    for i, key in reversed(changes):
        m = matches[i]
        new_src = f'src="data:image/png;base64,{imgs[key]}"'
        segment = segment[:m.start()] + new_src + segment[m.end():]

    content = content[:start] + segment + content[end:]
    print(f'  ✓ PARTE 2: "{card_name}" → {len(changes)} image(s) replaced')

def replace_ocard_img(card_name, img_key):
    """Replace the single PNG image in an ocard"""
    global content
    idx_name = content.find(f'>{card_name}<')
    if idx_name == -1:
        print(f'  WARNING: ocard "{card_name}" not found')
        return
    start = content.rfind('<div class="ocard">', 0, idx_name)
    next_ocard = content.find('<div class="ocard">', start + 10)
    end = next_ocard if next_ocard > 0 else start + 1500000
    segment = content[start:end]

    pattern = r'src="data:image/png;base64,[^"]+"'
    m = re.search(pattern, segment)
    if not m:
        print(f'  WARNING: no PNG img found in ocard "{card_name}"')
        return
    if img_key not in imgs:
        print(f'  WARNING: image "{img_key}" not in imgs')
        return
    new_src = f'src="data:image/png;base64,{imgs[img_key]}"'
    segment = segment[:m.start()] + new_src + segment[m.end():]
    content = content[:start] + segment + content[end:]
    print(f'  ✓ PARTE 2 (ocard): "{card_name}" image replaced')

# Brace Túnel del Carpo: replace main image only
replace_card_imgs('Brace Túnel del Carpo', ['tunel_carpo'])

# Muñequera de Inmovilización Flexible: main + hover
replace_card_imgs('Muñequera de Inmovilización Flexible', ['munequera_s0', 'munequera_s1'])

# Faja Abdominal 30cm (already renamed): main + hover
replace_card_imgs('Faja Abdominal 30cm', ['faja_abd30cm_0', 'faja_abd30cm_1'])

# Costillero Elástico: main + hover
replace_card_imgs('Costillero Elástico', ['costillero_0', 'costillero_1'])

# Milgram: update the existing ocard image
replace_ocard_img('Férula de Milgram', 'milgram_0')

# ────────────────────────────────────────────────────────────────────────────
# PARTE 3: Build new card HTML
# ────────────────────────────────────────────────────────────────────────────

WA_MAIN = '573222236174'

def url_encode(s):
    return s.replace(' ', '%20').replace('&', '%26').replace('á','á').replace('é','é').replace('í','í').replace('ó','ó').replace('ú','ú').replace('ñ','ñ')

def mk_pcard(name, cat, desc, specs, price, main_key, hover_key=None, cotizar=False, wa=WA_MAIN):
    main_b64 = f'data:image/png;base64,{imgs[main_key]}'
    hover_src = f'data:image/png;base64,{imgs[hover_key]}' if (hover_key and hover_key in imgs) else main_b64
    price_html = ('<div class="pcard-price">Cotizar</div>' if cotizar
                  else f'<div class="pcard-price">{price} <small>COP</small></div>')
    wa_name = url_encode(name)
    return (
        f'<div class="pcard">'
        f'<div class="pcard-imgs">'
        f'<div class="pcard-img-main"><img src="{main_b64}" alt="{name}"></div>'
        f'<div class="pcard-img-alt"><img src="{hover_src}" alt="{name}"></div>'
        f'<div class="pcard-badge">⭐ Popular</div>'
        f'</div>'
        f'<div class="pcard-body">'
        f'<div class="pcard-cat">{cat}</div>'
        f'<div class="pcard-name">{name}</div>'
        f'<div class="pcard-desc">{desc}</div>'
        f'<div class="pcard-specs"><strong>{specs}</strong></div>'
        f'{price_html}'
        f'<a href="https://wa.me/{wa}?text=Hola!%20Me%20interesa%20{wa_name}" target="_blank" class="btn-ws">'
        f'<img src="{WS_GIF}" alt="WS"> Consultar disponibilidad</a>'
        f'</div></div>'
    )

def mk_ocard(name, cat, desc, specs, main_key, wa=WA_MAIN):
    main_b64 = f'data:image/png;base64,{imgs[main_key]}'
    wa_name = url_encode(name)
    return (
        f'<div class="ocard">'
        f'<div class="ocard-img"><img src="{main_b64}" alt="{name}"></div>'
        f'<div class="ocard-body">'
        f'<div class="medida-badge">📐 Fabricada a medida</div>'
        f'<div class="ocard-cat">{cat}</div>'
        f'<div class="ocard-name">{name}</div>'
        f'<div class="ocard-desc">{desc}</div>'
        f'<div class="ocard-specs"><strong>{specs}</strong></div>'
        f'<div class="ocard-price">Cotizar <small style="font-size:12px;color:rgba(255,255,255,.45)">COP</small></div>'
        f'<a href="https://wa.me/{wa}?text=Hola!%20Me%20interesa%20{wa_name}" target="_blank" class="btn-ws">'
        f'<img src="{WS_GIF}" alt="WS"> Solicitar cotización</a>'
        f'</div></div>'
    )

# Build all new cards
card1 = mk_pcard(
    'Muñequera Sencilla', 'Muñeca',
    'Muñequera de compresión leve. Material elástico transpirable. Alivia el dolor y reduce la inflamación.',
    'Tallas: XS · S · M · L · XL',
    '$15.300', 'munequera_s0', 'munequera_s1'
)

card2 = mk_pcard(
    'Soporte de Muñeca', 'Muñeca',
    'Soporte con barras laterales para mayor estabilización de la muñeca. Ideal post-lesión y actividad deportiva.',
    'Tallas: XS · S · M · L · XL',
    '$20.600', 'soporte_muneca_0', 'soporte_muneca_1'
)

card3 = mk_pcard(
    'Faja para Hernia Inguinal', 'Abdomen',
    'Faja de compresión para hernias inguinales uni o bilaterales. Con pelota de presión ajustable.',
    'Tallas: S · M · L · XL · XXL',
    '$58.900', 'hernia_0', 'hernia_1'
)

card4 = mk_pcard(
    'Cabestrillo Acolchado Adulto', 'Hombro & Brazo',
    'Cabestrillo ergonómico acolchado para inmovilización del brazo. Ajustable en longitud. Tela suave.',
    'Talla única ajustable',
    '$24.200', 'cabestrillo_0', 'cabestrillo_1'
)

card5 = mk_pcard(
    'Rodillera Universal Ajustable', 'Rodilla',
    'Rodillera con tiras ajustables para soporte ligero a moderado. Material transpirable. Alivio del dolor.',
    'Tallas: S · M · L · XL',
    '$35.800', 'rodilla_univ_0', 'rodilla_univ_1'
)

card6 = mk_pcard(
    'Rodillera Rótula Abierta', 'Rodilla',
    'Rodillera con apertura rotuliana y refuerzo lateral para estabilización de ligamentos. Post-cirugía y deporte.',
    'Tallas: S · M · L · XL',
    '$28.700', 'rodilla_rotula_0', 'rodilla_rotula_1'
)

card7 = mk_ocard(
    'Férula para Pie Caído', 'Tobillo & Pie',
    'Ortesis de tobillo-pie (AFO) para corrección del pie caído. Termoplástico ultraligero y transpirable.',
    'Métricas: Sobre medidas del paciente',
    'pie_caido_0'
)

card9 = mk_ocard(
    'Ponseti', 'Ortesis Pediátrica',
    'Barra de Denis Browne con botines Ponseti para tratamiento conservador del pie equino varo en neonatos.',
    'Métricas: Sobre medidas del bebé',
    'ponseti_0'
)

card10 = mk_ocard(
    'Corset Jewett', 'Ortesis',
    'Ortesis de hiperextensión para fracturas vertebrales por compresión. Protección y estabilización de columna.',
    'Métricas: Sobre medidas del paciente',
    'corset_jewett_0'
)

card11 = mk_ocard(
    'Arnés de Paulik', 'Ortesis Pediátrica',
    'Arnés dinámico para tratamiento de displasia del desarrollo de cadera (DDC) en bebés. Material hipoalergénico.',
    'Métricas: Sobre medidas del bebé',
    'arnes_paulik_0'
)

card12 = mk_pcard(
    'Infantómetro', 'Soporte',
    'Instrumento de medición de talla para bebés en posición decúbito supino. Escala graduada de alta precisión.',
    'Rango: 0–100 cm',
    'Cotizar', 'infantometro_0', 'infantometro_1', cotizar=True
)

print("  ✓ PARTE 3: All card HTML built")

# ────────────────────────────────────────────────────────────────────────────
# PARTE 3: Insert cards into sections
# ────────────────────────────────────────────────────────────────────────────

# Helper: insert pcard(s) before closing prod-grid of a section
def insert_before_section(anchor_text, new_cards_html):
    """anchor_text = the start of next section; inserts cards before prod-grid closes"""
    global content
    idx = content.find(anchor_text)
    if idx == -1:
        print(f'  WARNING: anchor not found: {repr(anchor_text[:60])}')
        return
    # The anchor is at: </div>\n</div>\n<next-section>
    # We insert new cards before the 1st </div> of this pair
    content = content[:idx] + new_cards_html + content[idx:]
    print(f'  ✓ Cards inserted before: {repr(anchor_text[:50])}')

# Boundary anchors (exact strings found before each section)
BEFORE_CODO    = '</div>\n</div>\n<div class="cat-section alt" id="codo-sec">'
BEFORE_ABDOMEN = '</div>\n</div>\n<div class="cat-section alt" id="abdomen-sec">'
BEFORE_ORTESIS = '</div>\n</div>\n<div class="ortesis-sec" id="ortesis">'
BEFORE_SOPORTE = '</div>\n</div>\n<div class="soporte-sec" id="soporte">'
BEFORE_B2B     = '</div>\n</div>\n<section class="b2b-section"'

# Rodilla section HTML
RODILLA_SECTION = (
    '\n</div>\n'
    '<div class="cat-section" id="rodilla-sec">\n'
    '  <div class="cat-header"><div class="cat-icon-big">🦵</div>'
    '<div><h2>Rodilla</h2><p>Rodilleras y soportes para rehabilitación y actividad deportiva</p></div></div>\n'
    '  <div class="prod-grid">'
    + card5 + card6 +
    '</div>\n'
    '</div>'
)

# Card 1+2 → muneca-sec (before codo-sec)
insert_before_section(BEFORE_CODO, card1 + card2)

# Card 4 → postura-sec (before abdomen-sec)
insert_before_section(BEFORE_ABDOMEN, card4)

# Card 3 (hernia) → abdomen-sec + rodilla-sec section (before ortesis)
# We insert: hernia card INSIDE abdomen prod-grid, then new rodilla section
insert_before_section(BEFORE_ORTESIS, card3 + RODILLA_SECTION)

# Cards 7,9,10,11 → ortesis section (before soporte)
insert_before_section(BEFORE_SOPORTE, card7 + card9 + card10 + card11)

# Card 12 (Infantómetro) → soporte section (before b2b)
insert_before_section(BEFORE_B2B, card12)

# ────────────────────────────────────────────────────────────────────────────
# PARTE 4: Cat-nav update
# ────────────────────────────────────────────────────────────────────────────

OLD_NAV = '<a href="#ortesis">⚙️ Ortesis & Férulas</a>'
NEW_NAV = '<a href="#rodilla-sec">🦵 Rodilla</a>' + OLD_NAV

count_nav = content.count(OLD_NAV)
content = content.replace(OLD_NAV, NEW_NAV, 1)
print(f'  ✓ PARTE 4: cat-nav updated (found {count_nav} match(es))')

# ────────────────────────────────────────────────────────────────────────────
# Save
# ────────────────────────────────────────────────────────────────────────────

with open('/home/user/GlobalChay/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

new_len = len(content)
print(f'\n✅ Saved. {original_len:,} → {new_len:,} chars ({new_len-original_len:+,})')
