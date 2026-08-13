#!/usr/bin/env python3
"""
Integra tracking CRM Ortholines: agrega onclick="crmTrack({...})" a cada
boton de contacto (WhatsApp, mailto, redes sociales) sin tocar href/target/rel.
"""
import re

PATH = 'index.html'
PHONE_DIEGO = '573103015391'
PHONE_NANDO = '573118834901'

with open(PATH, encoding='utf-8') as f:
    content = f.read()

# ── Secciones de catalogo (id -> nombre) ────────────────────────────────────
SECTION_IDS = {
    'muneca-sec': 'Muñeca & Mano',
    'codo-sec': 'Codo',
    'postura-sec': 'Postura & Espalda',
    'abdomen-sec': 'Abdomen & Tórax',
    'rodilla-sec': 'Rodilla',
    'tobillo-sec': 'Tobillo & Pie',
    'ortesis': 'Ortesis & Férulas',
    'soporte': 'Soporte',
}
section_starts = []
for m in re.finditer(r'<div class="[^"]*"\s+id="(' + '|'.join(SECTION_IDS) + r')"', content):
    section_starts.append((m.start(), SECTION_IDS[m.group(1)]))
section_starts.sort()

def section_for(pos):
    name = None
    for start, sec in section_starts:
        if start <= pos:
            name = sec
        else:
            break
    return name or '—'

# ── Nombres y precios de producto (pcard/ocard/scard) ───────────────────────
name_matches = list(re.finditer(r'<h3 class="(?:pcard-name|ocard-name|scard-name)">(.*?)</h3>', content))
price_matches = list(re.finditer(r'<div class="(?:pcard-price|ocard-price|scard-price)">(.*?)</div>', content))

def strip_tags(s):
    return re.sub(r'<[^>]+>', '', s).strip()

def last_before(matches, pos):
    val = None
    for m in matches:
        if m.start() < pos:
            val = strip_tags(m.group(1))
        else:
            break
    return val or '—'

def js_escape(s):
    return s.replace('\\', '\\\\').replace("'", "\\'").replace('&', '&amp;').replace('"', '&quot;')

def canal_producto(href):
    return 'Diego' if PHONE_DIEGO in href else 'Nando'

def canal_contacto(href):
    return 'Diego/Gerencia' if PHONE_DIEGO in href else 'Nando'

count = {'producto': 0, 'flotante': 0, 'hero': 0, 'contacto_ws': 0, 'correo': 0, 'red_social': 0}

ANCHOR_RE = re.compile(r'<a\s+href="([^"]*)"((?:\s+[\w-]+(?:="[^"]*")?)*)\s*>')

def build_onclick(tipo, canal, seccion, producto, precio_web, url_wa_literal=None):
    url_wa = url_wa_literal if url_wa_literal else 'this.href'
    return (f"onclick=\"crmTrack({{tipo:'{tipo}', canal:'{js_escape(canal)}', "
            f"seccion:'{js_escape(seccion)}', producto:'{js_escape(producto)}', "
            f"precio_web:'{js_escape(precio_web)}', url_wa:{url_wa}}})\"")

def replacer(m):
    href = m.group(1)
    attrs = m.group(2)
    full = m.group(0)
    pos = m.start()

    if 'class="ws-float-btn"' in attrs:
        count['flotante'] += 1
        oc = build_onclick('flotante_ws', 'Nando', 'Flotante', '—', '—')
    elif 'class="btn-ghost"' in attrs and href.startswith('https://wa.me/'):
        count['hero'] += 1
        oc = build_onclick('asesoria_gratuita', 'Nando', 'Hero', '—', '—')
    elif 'class="btn-ws"' in attrs and href.startswith('https://wa.me/'):
        count['producto'] += 1
        seccion = section_for(pos)
        producto = last_before(name_matches, pos)
        precio = last_before(price_matches, pos)
        oc = build_onclick('consulta_producto', canal_producto(href), seccion, producto, precio)
    elif 'class="cta-ws"' in attrs and href.startswith('https://wa.me/'):
        count['contacto_ws'] += 1
        oc = build_onclick('contacto_ws', canal_contacto(href), 'Contacto', '—', '—')
    elif re.search(r'class="social-link\s+sl-(fb|ig|maps)"', attrs):
        count['red_social'] += 1
        producto = {'sl-fb': 'Facebook', 'sl-ig': 'Instagram', 'sl-maps': 'Google Maps'}[re.search(r'sl-(fb|ig|maps)', attrs).group(0)]
        oc = build_onclick('red_social', '—', 'Contacto', producto, '—')
    elif href.startswith('mailto:') and 'class=' not in attrs:
        count['correo'] += 1
        seccion = 'Topbar' if pos < 200000 else 'Footer'
        oc = build_onclick('correo', 'Gerencia', seccion, '—', '—', url_wa_literal="'mailto:ortholinesgerencia@gmail.com'")
    elif href in (f'https://wa.me/{PHONE_DIEGO}', f'https://wa.me/{PHONE_NANDO}') and 'class=' not in attrs:
        count['contacto_ws'] += 1
        seccion = 'Topbar' if pos < 200000 else 'Footer'
        oc = build_onclick('contacto_ws', canal_contacto(href), seccion, '—', '—')
    elif re.match(r'https://(?:www\.)?(?:facebook|instagram)\.com/', href) and 'class=' not in attrs:
        count['red_social'] += 1
        producto = 'Facebook' if 'facebook.com' in href else 'Instagram'
        oc = build_onclick('red_social', '—', 'Footer', producto, '—')
    else:
        return full

    return full[:-1].rstrip() + ' ' + oc + '>'

new_content, n_subs = ANCHOR_RE.subn(replacer, content)
print('Anchors scanned & replaced:', n_subs)
print('Counts:', count)

# ── Inyectar funcion crmTrack antes de </body> ──────────────────────────────
CRM_JS = """
<script>
// ── CRM ORTHOLINES ──────────────────────────────────────
function crmTrack(datos) {
  const CRM_URL = 'https://script.google.com/macros/s/AKfycbxbjwaBUsIuEJhBi_UfV-uewXB2lVe40I3UwLTn6pz54ZAbCF1EASN5nKY2aCtZcUDE/exec';
  fetch(CRM_URL, {
    method: 'POST',
    mode: 'no-cors',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      ...datos,
      dispositivo: /Mobi|Android/i.test(navigator.userAgent) ? 'Móvil' : 'Desktop',
      fecha: new Date().toLocaleString('es-CO', { timeZone: 'America/Bogota' })
    })
  }).catch(() => {});
}
// ────────────────────────────────────────────────────────
</script>
</body>"""

assert new_content.count('</body>') == 1, 'expected exactly one </body>'
new_content = new_content.replace('</body>', CRM_JS)

with open(PATH, 'w', encoding='utf-8') as f:
    f.write(new_content)

print('Done. Total onclick insertions:', sum(count.values()))
