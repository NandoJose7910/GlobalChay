#!/usr/bin/env python3
import sys

with open('/home/user/GlobalChay/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

original_len = len(content)

# ── CORRECCIÓN 1: Textos redes sociales ─────────────────────────────────────
old_fb_sub = '<div class="sl-sub">Ortholines Colombia</div>'
new_fb_sub = '<div class="sl-sub">Ortholines S.A.S</div>'
if old_fb_sub not in content:
    print("WARN: FB sub text not found, skipping")
else:
    content = content.replace(old_fb_sub, new_fb_sub, 1)
    print('✓ Corrección 1a: Facebook subtitle → Ortholines S.A.S')

old_ig_sub = '<div class="sl-sub">@ortholines.oficial</div>'
new_ig_sub = '<div class="sl-sub">@ortholinesas</div>'
if old_ig_sub not in content:
    print("WARN: IG sub text not found, skipping")
else:
    content = content.replace(old_ig_sub, new_ig_sub, 1)
    print('✓ Corrección 1b: Instagram subtitle → @ortholinesas')

# ── CORRECCIÓN 3: cat-nav CSS mobile ────────────────────────────────────────
# Replace the existing @media (max-width: 768px) cat-nav block added previously
old_cat_css = '''
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
new_cat_css = '''
@media (max-width: 768px) {
  .cat-nav {
    position: sticky;
    top: 56px;
    z-index: 150;
    display: flex;
    flex-wrap: wrap;
    gap: 4px;
    padding: 6px 10px;
    background: #fff;
    border-bottom: 1px solid #e2e8f0;
    overflow-x: visible;
    white-space: normal;
  }
  .cat-nav a {
    font-size: 10.5px !important;
    padding: 4px 8px !important;
    white-space: nowrap;
  }
}
'''
if old_cat_css not in content:
    print("WARN: old cat-nav CSS not found — trying to replace before </style>")
    content = content.replace('</style>', new_cat_css + '</style>', 1)
else:
    content = content.replace(old_cat_css, new_cat_css, 1)
print('✓ Corrección 3: cat-nav mobile CSS actualizado')

# ── CORRECCIÓN 4a: EmailJS en <head> ────────────────────────────────────────
emailjs_script = '''<script src="https://cdn.jsdelivr.net/npm/@emailjs/browser@4/dist/email.min.js"></script>
<script>emailjs.init("SERVICE_PENDING");</script>
'''
if 'emailjs' not in content:
    content = content.replace('</head>', emailjs_script + '</head>', 1)
    print('✓ Corrección 4a: EmailJS script añadido al <head>')
else:
    print('✓ Corrección 4a: EmailJS ya presente')

# ── CORRECCIÓN 4b: Actualizar función submitB2B ─────────────────────────────
old_fn = '''function submitB2B(e) {
  e.preventDefault();
  var form = e.target;
  var inputs = form.querySelectorAll('input[type="text"]');
  var nombre   = inputs[0] ? inputs[0].value : '';
  var ciudad   = inputs[1] ? inputs[1].value : '';
  var whatsapp = form.querySelector('input[type="tel"]') ? form.querySelector('input[type="tel"]').value : '';
  var tipo     = form.querySelector('select') ? form.querySelector('select').value : '';
  var mensaje  = form.querySelector('textarea') ? form.querySelector('textarea').value : '';
  var subject  = encodeURIComponent('Solicitud Aliado Comercial — Ortholines S.A.S');
  var body     = encodeURIComponent('Nombre: ' + nombre + '\\nCiudad: ' + ciudad + '\\nWhatsApp: ' + whatsapp + '\\nTipo de negocio: ' + tipo + '\\nMensaje: ' + mensaje);
  window.location.href = 'mailto:ortholinesgerencia@gmail.com?subject=' + subject + '&body=' + body;
  document.getElementById('b2b-form-content').style.display = 'none';
  document.getElementById('b2b-success').style.display = 'block';
}'''

new_fn = """function submitB2B(e) {
  e.preventDefault();
  const form = e.target;
  const inputs = form.querySelectorAll('input[type="text"]');
  const nombre   = inputs[0]?.value || '';
  const ciudad   = inputs[1]?.value || '';
  const whatsapp = form.querySelector('input[type="tel"]')?.value || '';
  const tipo     = form.querySelector('select')?.value || '';
  const mensaje  = form.querySelector('textarea')?.value || '';
  const subject = encodeURIComponent('Solicitud Aliado Comercial — Ortholines S.A.S');
  const body = encodeURIComponent(
    'Nombre: ' + nombre +
    '\\nCiudad: ' + ciudad +
    '\\nWhatsApp: ' + whatsapp +
    '\\nTipo de negocio: ' + tipo +
    '\\nMensaje: ' + mensaje
  );
  window.open('mailto:ortholinesgerencia@gmail.com?subject=' + subject + '&body=' + body);
  document.getElementById('b2b-form-content').style.display = 'none';
  document.getElementById('b2b-success').style.display = 'block';
}"""

if old_fn in content:
    content = content.replace(old_fn, new_fn, 1)
    print('✓ Corrección 4b: submitB2B actualizado con window.open()')
else:
    print('WARN: submitB2B original no encontrado exacto — buscando alternativa')
    # Try to find and replace via simpler anchor
    old_anchor = "window.location.href = 'mailto:ortholinesgerencia@gmail.com?subject=' + subject + '&body=' + body;"
    new_anchor = "window.open('mailto:ortholinesgerencia@gmail.com?subject=' + subject + '&body=' + body);"
    if old_anchor in content:
        content = content.replace(old_anchor, new_anchor, 1)
        print('✓ Corrección 4b: window.location → window.open reemplazado')
    else:
        print('WARN: submitB2B anchor not found either')

# ── CORRECCIÓN 2: Reordenar secciones ───────────────────────────────────────
# Current: hero → trust → cat-nav+catalog → ortesis → soporte → aliados → nosotros → testimonios
# Desired: hero → nosotros → trust → cat-nav+catalog → ortesis → soporte → aliados → testimonios

# Extract nosotros block (depth-counting)
nos_anchor = '<section class="about" id="nosotros">'
if nos_anchor not in content:
    print('ERROR: nosotros section not found'); sys.exit(1)
nos_start = content.index(nos_anchor)
depth = 0
pos = nos_start
while pos < len(content):
    open_pos = content.find('<section', pos)
    close_pos = content.find('</section>', pos)
    if close_pos == -1: break
    if open_pos != -1 and open_pos < close_pos:
        depth += 1
        pos = open_pos + 8
    else:
        depth -= 1
        pos = close_pos + 10
        if depth == 0:
            nos_end = pos
            break

nosotros_block = content[nos_start:nos_end]
print(f'Nosotros extracted: {len(nosotros_block)} chars from pos {nos_start}')

# Remove nosotros (with its preceding newline if present)
if nos_start > 0 and content[nos_start-1] == '\n':
    content = content[:nos_start-1] + content[nos_end:]
else:
    content = content[:nos_start] + content[nos_end:]
print('Nosotros removed from current position')

# Insert nosotros AFTER hero section and BEFORE cat-nav
# Hero section closes at </section>, after which comes trust div, then cat-nav
# We insert BEFORE <div class="cat-nav"
catnav_anchor = '<div class="cat-nav" id="catalogo">'
if catnav_anchor not in content:
    print('ERROR: cat-nav anchor not found'); sys.exit(1)
catnav_pos = content.index(catnav_anchor)
content = content[:catnav_pos] + nosotros_block + '\n' + content[catnav_pos:]
print(f'✓ Corrección 2: Nosotros movido antes de cat-nav')

# ── CORRECCIÓN 5: Verificar correo ──────────────────────────────────────────
old_count = content.count('ortholinessasventas@gmail.com')
new_count = content.count('ortholinesgerencia@gmail.com')
if old_count > 0:
    content = content.replace('ortholinessasventas@gmail.com', 'ortholinesgerencia@gmail.com')
    print(f'✓ Corrección 5: {old_count} ocurrencias viejas reemplazadas')
else:
    print(f'✓ Corrección 5: correo ya actualizado ({new_count} ocurrencias de ortholinesgerencia)')

with open('/home/user/GlobalChay/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

new_len = len(content)
print(f'\n✅ Guardado. {original_len:,} → {new_len:,} bytes ({new_len - original_len:+,})')
