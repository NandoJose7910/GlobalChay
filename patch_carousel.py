#!/usr/bin/env python3
"""
PARTE 1: Carousel on ALL cards (pcard + ocard)
PARTE 2: Specific corrections
PARTE 3: Extra images per card (from /tmp/ortho_imgs/)
"""
import re, os

# ── Load images ───────────────────────────────────────────────────────────────
imgs = {}
for f in sorted(os.listdir('/tmp/ortho_imgs/')):
    key = f.replace('.b64', '')
    with open(f'/tmp/ortho_imgs/{f}', 'r') as fh:
        imgs[key] = fh.read().strip()
print(f"Loaded {len(imgs)} images")

with open('/home/user/GlobalChay/index.html', 'r', encoding='utf-8') as f:
    content = f.read()
print(f"HTML: {len(content):,} chars")

# ── CSS ───────────────────────────────────────────────────────────────────────
CAROUSEL_CSS = '''
.carousel-wrap{position:relative;background:#f8f9fc;aspect-ratio:1/1;overflow:hidden;}
.carousel-track{display:flex;height:100%;transition:transform 0.3s ease;}
.carousel-slide{min-width:100%;height:100%;display:flex;align-items:center;justify-content:center;overflow:hidden;}
.carousel-slide img{width:100%;height:100%;object-fit:contain;}
.carousel-btn{position:absolute;top:50%;transform:translateY(-50%);width:28px;height:28px;background:rgba(255,255,255,0.92);border:0.5px solid #dde3f0;border-radius:50%;display:flex;align-items:center;justify-content:center;cursor:pointer;z-index:10;transition:background 0.15s;font-size:14px;color:#1a3a8f;padding:0;line-height:1;}
.carousel-btn:hover{background:#fff;}
.carousel-btn.prev{left:8px;}
.carousel-btn.next{right:8px;}
.carousel-dots{position:absolute;bottom:8px;left:50%;transform:translateX(-50%);display:flex;gap:5px;z-index:10;}
.cdot{width:6px;height:6px;border-radius:50%;background:rgba(255,255,255,0.5);border:0.5px solid rgba(26,58,143,0.3);cursor:pointer;transition:background 0.2s;}
.cdot.active{background:#1a3a8f;}
.foto-count{position:absolute;top:8px;right:8px;background:rgba(26,58,143,0.75);color:#fff;font-size:10px;padding:2px 7px;border-radius:20px;z-index:10;}
.video-slot{width:100%;height:100%;display:flex;align-items:center;justify-content:center;background:#1a1a2e;cursor:pointer;flex-direction:column;gap:8px;color:rgba(255,255,255,0.7);font-size:12px;}
.video-slot .play-icon{width:48px;height:48px;background:rgba(244,124,26,0.9);border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:20px;color:#fff;}
@media(max-width:768px){.carousel-btn{width:24px;height:24px;font-size:12px;}}
'''

# ── JS ────────────────────────────────────────────────────────────────────────
CAROUSEL_JS = '''<script>
(function(){
  var pos={};
  window.carMove=function(id,dir){
    var t=document.getElementById(id);if(!t)return;
    var n=t.querySelectorAll('.carousel-slide').length;
    if(pos[id]==null)pos[id]=0;
    pos[id]=(pos[id]+dir+n)%n; carUp(id);
  };
  window.carGoTo=function(id,i){pos[id]=i;carUp(id);};
  function carUp(id){
    var t=document.getElementById(id),i=pos[id];
    var n=t.querySelectorAll('.carousel-slide').length;
    t.style.transform='translateX(-'+(i*100)+'%)';
    var w=t.closest('.carousel-wrap');if(!w)return;
    var c=w.querySelector('.foto-count');if(c)c.textContent=(i+1)+' / '+n;
    w.querySelectorAll('.cdot').forEach(function(d,j){d.classList.toggle('active',j===i);});
  }
})();
</script>'''

# ── Helpers ───────────────────────────────────────────────────────────────────
def find_div_end(s, start):
    pos = start + 4; depth = 1
    while depth > 0 and pos < len(s):
        op = s.find('<div', pos); cl = s.find('</div>', pos)
        if cl == -1: break
        if op != -1 and op < cl: depth += 1; pos = op + 4
        else: depth -= 1; pos = cl + 6
    return pos

def build_carousel(car_id, name, b64_list, badge=None):
    n = len(b64_list) + 1
    slides = ''
    for b64 in b64_list:
        slides += (f'<div class="carousel-slide">'
                   f'<img src="data:image/png;base64,{b64}" alt="{name}" loading="lazy">'
                   f'</div>')
    slides += (f'<div class="carousel-slide">'
               f'<div class="video-slot" data-video-url="" '
               f'onclick="if(this.dataset.videoUrl)window.open(this.dataset.videoUrl)">'
               f'<div class="play-icon">▶</div><span>Video próximamente</span>'
               f'</div></div>')
    dots = ''.join(
        f'<div class="cdot{" active" if i==0 else ""}" onclick="carGoTo(\'{car_id}\',{i})"></div>'
        for i in range(n)
    )
    badge_html = f'<div class="pcard-badge">{badge}</div>' if badge else ''
    return (f'<div class="carousel-wrap">'
            f'<div class="carousel-track" id="{car_id}">{slides}</div>'
            f'<span class="foto-count">1 / {n}</span>'
            f'<button class="carousel-btn prev" onclick="carMove(\'{car_id}\',-1)" aria-label="Anterior">&#8249;</button>'
            f'<button class="carousel-btn next" onclick="carMove(\'{car_id}\',1)" aria-label="Siguiente">&#8250;</button>'
            f'<div class="carousel-dots">{dots}</div>'
            f'{badge_html}</div>')

# Images to use per card (overrides what's in HTML)
CARD_IMGS = {
    'Brace Túnel del Carpo':               ['tunel_carpo'],
    'Muñequera de Inmovilización Flexible': ['munequera_inm_orig_0','munequera_inm_orig_1'],
    'Muñequera Sencilla':                   ['munequera_s0','munequera_s1','munequera_s2'],
    'Soporte de Muñeca':                    ['soporte_muneca_0','soporte_muneca_1','soporte_muneca_2','soporte_muneca_3'],
    'Faja Abdominal 30cm':                  ['faja_abd30cm_0','faja_abd30cm_1','faja_abd30cm_2'],
    'Faja para Hernia Inguinal':            ['hernia_0','hernia_1','hernia_2','hernia_3'],
    'Costillero Elástico':                  ['costillero_0','costillero_1','costillero_2','costillero_3'],
    'Cabestrillo Acolchado Adulto':         ['cabestrillo_0','cabestrillo_1'],
    'Rodillera Universal Ajustable':        ['rodilla_univ_0','rodilla_univ_1','rodilla_univ_2','rodilla_univ_3'],
    'Rodillera Rótula Abierta':             ['rodilla_rotula_0','rodilla_rotula_1','rodilla_rotula_2','rodilla_rotula_3'],
    'Infantómetro':                         ['infantometro_0','infantometro_1'],
    'Férula para Pie Caído':               ['pie_caido_0','pie_caido_1','pie_caido_2'],
    'Férula de Milgram':                   ['milgram_0','milgram_1','milgram_2','milgram_3','milgram_4'],
    'Ponseti':                             ['ponseti_0'],
    'Corset Jewett':                       ['corset_jewett_0','corset_jewett_1','corset_jewett_2',
                                            'corset_jewett_3','corset_jewett_4','corset_jewett_5','corset_jewett_6'],
    'Arnés de Paulik':                     ['arnes_paulik_0'],
}

# ── Step 1: Collect all card image sections with proper names ─────────────────
print("\n── Scanning cards...")
slots = []  # (img_section_start, img_section_end, card_name, card_type)

# PCARDs: anchor on <div class="pcard">
pcard_pos = [m.start() for m in re.finditer(r'<div class="pcard">', content)]
for i, ps in enumerate(pcard_pos):
    pe = pcard_pos[i+1] if i+1 < len(pcard_pos) else len(content)
    # Find pcard-name: search from ps to pe (cards span big because of base64)
    nm = re.search(r'<div class="pcard-name">([^<]+)</div>', content[ps:pe])
    name = nm.group(1).strip() if nm else f'pcard_{i+1}'
    # Find pcard-imgs within this card
    istart = content.find('<div class="pcard-imgs">', ps, pe)
    if istart == -1:
        print(f'  SKIP pcard "{name}": no pcard-imgs found')
        continue
    iend = find_div_end(content, istart)
    # Verify pcard-name exists after iend (sanity check)
    slots.append((istart, iend, name, 'pcard'))
    print(f'  pcard "{name}": imgs [{istart},{iend}) → {iend-istart:,} chars')

# OCARDs: anchor on <div class="ocard">
ocard_pos = [m.start() for m in re.finditer(r'<div class="ocard">', content)]
for i, os_ in enumerate(ocard_pos):
    oe = ocard_pos[i+1] if i+1 < len(ocard_pos) else len(content)
    nm = re.search(r'<div class="ocard-name">([^<]+)</div>', content[os_:oe])
    name = nm.group(1).strip() if nm else f'ocard_{i+1}'
    # ocard-img: single div with no nested divs
    istart = content.find('<div class="ocard-img">', os_, oe)
    if istart == -1:
        print(f'  SKIP ocard "{name}": no ocard-img found')
        continue
    iend = content.find('</div>', istart) + len('</div>')
    slots.append((istart, iend, name, 'ocard'))
    print(f'  ocard "{name}": img [{istart},{iend}) → {iend-istart:,} chars')

# Sort by position (document order) → assign car IDs
slots.sort(key=lambda x: x[0])
print(f"\nTotal: {len(slots)} card slots")

# ── Step 2: Build replacement list ───────────────────────────────────────────
print("\n── Building carousels...")

WS_GIF_M = re.search(r'"(data:image/gif;base64,[^"]+)"[^>]*alt="WS"', content)
WS_GIF = WS_GIF_M.group(1) if WS_GIF_M else 'data:image/gif;base64,'

pie_caido_car = None
replacements = []

for idx, (istart, iend, name, ctype) in enumerate(slots):
    car_id = f'car{idx+1}'
    segment = content[istart:iend]

    if name in CARD_IMGS:
        keys = CARD_IMGS[name]
        b64s = [imgs[k] for k in keys if k in imgs]
    else:
        # Extract existing PNG images from current HTML
        b64s = re.findall(r'src="data:image/png;base64,([^"]+)"', segment)

    if not b64s:
        print(f'  WARNING: no images for "{name}" (car={car_id})')
        b64s = re.findall(r'src="data:image/png;base64,([^"]+)"', segment)

    badge = None
    if '<div class="pcard-badge">' in segment:
        bm = re.search(r'<div class="pcard-badge">([^<]+)</div>', segment)
        badge = bm.group(1) if bm else '⭐ Popular'

    new_html = build_carousel(car_id, name, b64s, badge=badge)
    replacements.append((istart, iend, new_html))
    print(f'  ✓ {name!r}: {car_id}, {len(b64s)} img(s)+video ({ctype})')

    if name == 'Férula para Pie Caído':
        pie_caido_car = car_id

# ── Step 3: Apply in REVERSE order ───────────────────────────────────────────
print("\n── Applying...")
for istart, iend, new_html in sorted(replacements, key=lambda x: x[0], reverse=True):
    content = content[:istart] + new_html + content[iend:]
print(f"  Applied {len(replacements)} replacements")

# ── Step 4: PARTE 2B — Soporte de Muñeca description ─────────────────────────
old_d = 'Soporte con barras laterales para mayor estabilización de la muñeca. Ideal post-lesión y actividad deportiva.'
new_d = 'Soporte ergonómico de muñeca. Compresión graduada para uso prolongado. Ideal para deporte y actividad diaria.'
if old_d in content:
    content = content.replace(old_d, new_d, 1)
    print('\n✓ PARTE 2B: Soporte de Muñeca desc updated')
else:
    print(f'\n  WARNING: Soporte desc not found')

# ── Step 5: PARTE 2C — Move Pie Caído → tobillo-sec ──────────────────────────
print("\n── PARTE 2C: tobillo-sec...")

# Build the pcard version of Pie Caído for tobillo-sec
pie_b64s = [imgs[k] for k in ['pie_caido_0','pie_caido_1','pie_caido_2'] if k in imgs]
pie_carousel = build_carousel(pie_caido_car or 'car_pie', 'Férula para Pie Caído', pie_b64s, badge='⭐ Popular')
pie_pcard = (
    f'<div class="pcard">'
    f'{pie_carousel}'
    f'<div class="pcard-body">'
    f'<div class="pcard-cat">Tobillo &amp; Pie</div>'
    f'<div class="pcard-name">Férula para Pie Caído</div>'
    f'<div class="pcard-desc">Ortesis de tobillo-pie (AFO) para corrección del pie caído. Termoplástico ultraligero y transpirable.</div>'
    f'<div class="pcard-specs"><strong>Métricas: Sobre medidas del paciente</strong></div>'
    f'<div class="pcard-price">Cotizar</div>'
    f'<a href="https://wa.me/573222236174?text=Hola!%20Me%20interesa%20F%C3%A9rula%20para%20Pie%20Ca%C3%ADdo" target="_blank" class="btn-ws">'
    f'<img src="{WS_GIF}" alt="WS"> Consultar disponibilidad</a>'
    f'</div></div>'
)

# Remove the old Pie Caído ocard from ortesis
pie_name_idx = content.find('>Férula para Pie Caído<')
if pie_name_idx != -1:
    pie_ocard_start = content.rfind('<div class="ocard">', 0, pie_name_idx)
    pie_ocard_end = find_div_end(content, pie_ocard_start)
    content = content[:pie_ocard_start] + content[pie_ocard_end:]
    print(f'  ✓ Removed Pie Caído ocard from ortesis')
else:
    print(f'  WARNING: Pie Caído not found in HTML for removal')

# Insert tobillo-sec between rodilla-sec and ortesis
RODILLA_END = '</div>\n</div>\n<div class="ortesis-sec" id="ortesis">'
TOBILLO_SEC = (
    '\n<div class="cat-section alt" id="tobillo-sec">\n'
    '  <div class="cat-header"><div class="cat-icon-big">🦶</div>'
    '<div><h2>Tobillo &amp; Pie</h2>'
    '<p>Férulas y soportes de tobillo para rehabilitación y corrección postural</p></div></div>\n'
    '  <div class="prod-grid">' + pie_pcard + '</div>\n</div>'
)
if RODILLA_END in content:
    content = content.replace(RODILLA_END,
                              f'{TOBILLO_SEC}\n<div class="ortesis-sec" id="ortesis">', 1)
    print('  ✓ tobillo-sec created')
else:
    print(f'  WARNING: rodilla/ortesis boundary not found')

# ── Step 6: cat-nav — add tobillo-sec ─────────────────────────────────────────
OLD_NAV = '<a href="#rodilla-sec">🦵 Rodilla</a><a href="#ortesis">'
NEW_NAV = '<a href="#rodilla-sec">🦵 Rodilla</a><a href="#tobillo-sec">🦶 Tobillo & Pie</a><a href="#ortesis">'
if OLD_NAV in content:
    content = content.replace(OLD_NAV, NEW_NAV, 1)
    print('\n✓ cat-nav: tobillo-sec added')
else:
    print(f'\n  WARNING: cat-nav anchor not found')

# ── Step 7: CSS + JS ──────────────────────────────────────────────────────────
content = content.replace('</style>', CAROUSEL_CSS + '</style>', 1)
content = content.replace('</body>', CAROUSEL_JS + '\n</body>', 1)
print('✓ CSS + JS added')

# ── Step 8: Price verification ────────────────────────────────────────────────
print('\n── Price checks:')
checks = [('Brace Túnel del Carpo','$26.500'),('Muñequera de Inmovilización Flexible','$20.600'),
          ('Costillero Elástico','$29.800'),('Faja Abdominal 30cm','Desde $56.300')]
for cn, ep in checks:
    i = content.find(f'>{cn}<')
    if i < 0: print(f'  {cn}: CARD NOT FOUND'); continue
    found = ep in content[i:i+2000000]
    print(f'  {cn}: {ep} → {"✓" if found else "MISSING"}')

# ── Verify all card names present ────────────────────────────────────────────
pcard_names = re.findall(r'<div class="pcard-name">([^<]+)</div>', content)
ocard_names = re.findall(r'<div class="ocard-name">([^<]+)</div>', content)
print(f'\n── Cards in HTML: {len(pcard_names)} pcards, {len(ocard_names)} ocards')
print('PCARDs:', pcard_names)
print('OCARDs:', ocard_names)

# ── Verify car IDs are unique ─────────────────────────────────────────────────
car_ids = re.findall(r'id="(car\d+)"', content)
unique_ids = set(car_ids)
print(f'\nCarousel IDs: {len(car_ids)} total, {len(unique_ids)} unique')
if len(car_ids) != len(unique_ids):
    from collections import Counter
    dups = [k for k,v in Counter(car_ids).items() if v > 1]
    print(f'  DUPLICATE IDs: {dups}')

# ── Save ──────────────────────────────────────────────────────────────────────
orig = 22740146
with open('/home/user/GlobalChay/index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print(f'\n✅ Saved: {orig:,} → {len(content):,} chars ({len(content)-orig:+,})')
