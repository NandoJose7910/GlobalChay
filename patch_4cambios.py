#!/usr/bin/env python3
import re, sys

with open('/home/user/GlobalChay/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

original_len = len(content)

# ── CAMBIO 3: Actualizar correo ──────────────────────────────────────────────
old_email = 'ortholinessasventas@gmail.com'
new_email = 'ortholinesgerencia@gmail.com'
count_email = content.count(old_email)
content = content.replace(old_email, new_email)
print(f'✓ Cambio 3: correo reemplazado {count_email} veces')

# ── CAMBIO 4: Actualizar redes sociales ─────────────────────────────────────
old_fb = 'https://www.facebook.com/profile.php?id=61578304701096'
new_fb = 'https://www.facebook.com/profile.php?id=61589489687876'
count_fb = content.count(old_fb)
content = content.replace(old_fb, new_fb)
print(f'✓ Cambio 4a: Facebook reemplazado {count_fb} veces')

old_ig = 'https://www.instagram.com/ortholines.oficial/'
new_ig = 'https://www.instagram.com/ortholinessas/'
count_ig = content.count(old_ig)
content = content.replace(old_ig, new_ig)
print(f'✓ Cambio 4b: Instagram reemplazado {count_ig} veces')

# ── CAMBIO 1: Mover sección aliados ─────────────────────────────────────────
# Find aliados block boundaries (depth-counting for nested sections)
start = content.index('<section class="b2b-section" id="aliados">')
depth = 0
pos = start
while pos < len(content):
    open_pos = content.find('<section', pos)
    close_pos = content.find('</section>', pos)
    if close_pos == -1:
        break
    if open_pos != -1 and open_pos < close_pos:
        depth += 1
        pos = open_pos + 8
    else:
        depth -= 1
        pos = close_pos + 10
        if depth == 0:
            aliados_end = pos
            break

aliados_block = content[start:aliados_end]

# Remove aliados from current position (includes leading \n before next section)
content = content[:start] + content[aliados_end:]
print(f'✓ Cambio 1a: aliados removido de posición {start}')

# Find insertion point: before <section class="testimonios"
testi_anchor = '<section class="testimonios" id="testimonios">'
testi_pos = content.index(testi_anchor)
content = content[:testi_pos] + aliados_block + '\n' + content[testi_pos:]
print(f'✓ Cambio 1b: aliados insertado antes de testimonios (pos {testi_pos})')

# ── CAMBIO 2: cat-nav responsive CSS ────────────────────────────────────────
cat_css = '''
@media (max-width: 768px) {
  .cat-nav {
    display: flex !important;
    flex-wrap: wrap !important;
    overflow-x: visible !important;
    white-space: normal !important;
    padding: 6px 12px !important;
  }
  .cat-nav a {
    font-size: 11px !important;
    padding: 4px 8px !important;
    white-space: nowrap;
  }
}
'''
if '</style>' not in content:
    print('ERROR: </style> no encontrado'); sys.exit(1)
content = content.replace('</style>', cat_css + '</style>', 1)
print('✓ Cambio 2: CSS cat-nav mobile insertado')

with open('/home/user/GlobalChay/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

new_len = len(content)
print(f'\n✅ Guardado. {original_len:,} → {new_len:,} bytes ({new_len - original_len:+,})')
