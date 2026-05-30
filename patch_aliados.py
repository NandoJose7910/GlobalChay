#!/usr/bin/env python3
import sys

with open('/home/user/GlobalChay/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

original_len = len(content)

# ── PASO 4: Navbar — agregar Aliados después de Soporte
old_nav = '<li><a href="#soporte">Soporte</a></li>'
new_nav = '<li><a href="#soporte">Soporte</a></li><li><a href="#aliados">Aliados</a></li>'
if old_nav not in content:
    print("ERROR: nav Soporte no encontrado"); sys.exit(1)
content = content.replace(old_nav, new_nav, 1)
print("✓ Paso 4: link Aliados en navbar")

# ── PASO 2: CSS — insertar antes de </style>
css_block = '''
.b2b-section { font-family: 'Segoe UI', system-ui, sans-serif; background: #1a3a8f; padding: 64px 20px 56px; position: relative; overflow: hidden; }
.b2b-bg-deco { position: absolute; top: -80px; right: -80px; width: 400px; height: 400px; border-radius: 50%; background: rgba(255,255,255,0.04); pointer-events: none; }
.b2b-bg-deco2 { position: absolute; bottom: -60px; left: -60px; width: 280px; height: 280px; border-radius: 50%; background: rgba(244,124,26,0.08); pointer-events: none; }
.b2b-inner { max-width: 960px; margin: 0 auto; position: relative; z-index: 2; }
.b2b-eyebrow { display: inline-flex; align-items: center; gap: 8px; background: rgba(244,124,26,0.18); color: #f5a25a; font-size: 11px; font-weight: 600; letter-spacing: 1.2px; text-transform: uppercase; padding: 6px 16px; border-radius: 100px; margin-bottom: 20px; border: 1px solid rgba(244,124,26,0.3); }
.b2b-title { font-size: clamp(24px, 4vw, 40px); font-weight: 700; color: #fff; line-height: 1.2; margin: 0 0 12px; }
.b2b-title em { color: #f47c1a; font-style: normal; }
.b2b-sub { font-size: 15px; color: rgba(255,255,255,0.7); max-width: 540px; line-height: 1.6; margin: 0 0 40px; }
.b2b-perfiles { display: flex; flex-wrap: wrap; gap: 10px; margin-bottom: 40px; }
.b2b-perfil { background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.15); color: #fff; font-size: 13px; font-weight: 500; padding: 8px 18px; border-radius: 100px; display: flex; align-items: center; gap: 8px; }
.b2b-beneficios { display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 14px; margin-bottom: 44px; }
.b2b-ben { background: rgba(255,255,255,0.07); border: 1px solid rgba(255,255,255,0.12); border-radius: 16px; padding: 22px 18px; transition: background 0.25s, transform 0.25s; }
.b2b-ben:hover { background: rgba(255,255,255,0.13); transform: translateY(-3px); }
.b2b-ben-icon { width: 42px; height: 42px; background: rgba(244,124,26,0.2); border-radius: 11px; display: flex; align-items: center; justify-content: center; font-size: 20px; margin-bottom: 12px; }
.b2b-ben-title { font-size: 13px; font-weight: 600; color: #fff; margin: 0 0 5px; }
.b2b-ben-desc { font-size: 12px; color: rgba(255,255,255,0.58); line-height: 1.5; margin: 0; }
.b2b-bottom { display: grid; grid-template-columns: 1fr 1fr; gap: 28px; align-items: start; }
.b2b-credito { background: rgba(244,124,26,0.12); border: 1px solid rgba(244,124,26,0.3); border-radius: 14px; padding: 22px; margin-bottom: 16px; }
.b2b-credito-title { font-size: 15px; font-weight: 700; color: #f5a25a; margin: 0 0 8px; display: flex; align-items: center; gap: 8px; }
.b2b-credito-text { font-size: 13px; color: rgba(255,255,255,0.65); line-height: 1.55; margin: 0; }
.b2b-tc { font-size: 11px; color: rgba(255,255,255,0.45); margin-top: 10px; display: block; text-decoration: underline; text-underline-offset: 3px; text-decoration-color: rgba(255,255,255,0.25); }
.col-flag { width: 40px; height: 28px; border-radius: 4px; overflow: hidden; flex-shrink: 0; display: flex; flex-direction: column; border: 1px solid rgba(255,255,255,0.2); }
.col-flag .f-y { background: #FCD116; flex: 2; }
.col-flag .f-b { background: #003087; flex: 1; }
.col-flag .f-r { background: #CE1126; flex: 1; }
.b2b-cobertura { background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 14px; padding: 16px 20px; display: flex; align-items: center; gap: 14px; }
.b2b-cob-text { font-size: 13px; color: rgba(255,255,255,0.7); line-height: 1.5; }
.b2b-cob-text strong { color: #fff; font-size: 14px; display: block; margin-bottom: 2px; }
.b2b-form-wrap { background: #ffffff; border-radius: 20px; padding: 28px 24px; box-shadow: 0 20px 60px rgba(0,0,0,0.3); }
.b2b-form-title { font-size: 17px; font-weight: 700; color: #1a3a8f; margin: 0 0 3px; }
.b2b-form-sub { font-size: 13px; color: #5a6480; margin: 0 0 20px; }
.b2b-fg { margin-bottom: 12px; }
.b2b-fg label { display: block; font-size: 11px; font-weight: 600; color: #5a6480; margin-bottom: 4px; text-transform: uppercase; letter-spacing: 0.5px; }
.b2b-fg input, .b2b-fg select, .b2b-fg textarea { width: 100%; box-sizing: border-box; border: 1.5px solid #dde3f0; border-radius: 10px; padding: 10px 13px; font-size: 14px; color: #1a1a2e !important; background: #f5f7fc !important; outline: none; font-family: inherit; transition: border-color 0.2s, background 0.2s; -webkit-appearance: none; appearance: none; }
.b2b-fg input:focus, .b2b-fg select:focus, .b2b-fg textarea:focus { border-color: #1a3a8f; background: #fff !important; }
.b2b-fg select { background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='8' viewBox='0 0 12 8'%3E%3Cpath d='M1 1l5 5 5-5' stroke='%235a6480' stroke-width='1.5' fill='none' stroke-linecap='round'/%3E%3C/svg%3E") !important; background-repeat: no-repeat !important; background-position: right 12px center !important; padding-right: 36px !important; cursor: pointer; }
.b2b-fg option { color: #1a1a2e !important; background: #ffffff !important; }
.b2b-fg textarea { resize: vertical; min-height: 68px; }
.b2b-form-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
.b2b-btn { width: 100%; box-sizing: border-box; background: #1a3a8f !important; color: #ffffff !important; border: none; border-radius: 12px; padding: 13px 20px; font-size: 15px; font-weight: 700; cursor: pointer; margin-top: 8px; font-family: inherit; display: flex; align-items: center; justify-content: center; gap: 8px; transition: background 0.2s, transform 0.15s; -webkit-appearance: none; appearance: none; }
.b2b-btn:hover { background: #2d52b8 !important; transform: translateY(-1px); }
.b2b-btn:active { transform: scale(0.98); }
.b2b-disclaimer { font-size: 11px; color: #8a94b0; text-align: center; margin-top: 10px; line-height: 1.45; }
.b2b-success { display: none; text-align: center; padding: 20px 0; }
.b2b-success-icon { font-size: 44px; margin-bottom: 10px; }
.b2b-success-title { font-size: 17px; font-weight: 700; color: #1a3a8f; margin: 0 0 6px; }
.b2b-success-text { font-size: 13px; color: #5a6480; line-height: 1.5; }
@media (max-width: 640px) { .b2b-bottom { grid-template-columns: 1fr; } .b2b-beneficios { grid-template-columns: 1fr 1fr; } }
@media (max-width: 380px) { .b2b-beneficios { grid-template-columns: 1fr; } .b2b-form-grid { grid-template-columns: 1fr; } }
'''

if '</style>' not in content:
    print("ERROR: </style> no encontrado"); sys.exit(1)
content = content.replace('</style>', css_block + '</style>', 1)
print("✓ Paso 2: CSS insertado")

# ── PASO 1: HTML — insertar antes de <section class="about" id="nosotros">
b2b_html = '''<section class="b2b-section" id="aliados">
  <div class="b2b-bg-deco"></div>
  <div class="b2b-bg-deco2"></div>
  <div class="b2b-inner">
    <div class="b2b-eyebrow">🤝 Aliados Comerciales</div>
    <h2 class="b2b-title">Crezcamos juntos.<br><em>Tú vendes, nosotros te respaldamos.</em></h2>
    <p class="b2b-sub">Sé parte de la red de distribución de Ortholines S.A.S. Accede a catálogo completo, precios especiales y respaldo comercial para tu negocio — en todo el país.</p>
    <div class="b2b-perfiles">
      <div class="b2b-perfil">💼 Emprendedores</div>
      <div class="b2b-perfil">🏪 Almacenes y tiendas</div>
      <div class="b2b-perfil">🏥 Clínicas y consultorios</div>
      <div class="b2b-perfil">🏢 Empresas y distribuidores</div>
    </div>
    <div class="b2b-beneficios">
      <div class="b2b-ben">
        <div class="b2b-ben-icon">🏷️</div>
        <p class="b2b-ben-title">Precios especiales</p>
        <p class="b2b-ben-desc">Tarifas de distribuidor sobre todo el catálogo. Mayor volumen, mejor precio.</p>
      </div>
      <div class="b2b-ben">
        <div class="b2b-ben-icon">📦</div>
        <p class="b2b-ben-title">Catálogo completo</p>
        <p class="b2b-ben-desc">Línea ortopédica y deportiva, ortesis a medida y ayudas para la movilidad. Todo disponible.</p>
      </div>
      <div class="b2b-ben">
        <div class="b2b-ben-icon">🎓</div>
        <p class="b2b-ben-title">Capacitación</p>
        <p class="b2b-ben-desc">Te enseñamos los productos para que puedas venderlos con confianza y conocimiento.</p>
      </div>
      <div class="b2b-ben">
        <div class="b2b-ben-icon">📊</div>
        <p class="b2b-ben-title">Asesoría comercial</p>
        <p class="b2b-ben-desc">Acompañamiento directo de nuestro equipo para impulsar tus ventas.</p>
      </div>
    </div>
    <div class="b2b-bottom">
      <div>
        <div class="b2b-credito">
          <div class="b2b-credito-title">💳 Crédito disponible</div>
          <p class="b2b-credito-text">Ofrecemos líneas de crédito para aliados comerciales calificados. Potencia tu inventario sin comprometer todo tu capital.</p>
          <span class="b2b-tc">* Aplican términos y condiciones. Sujeto a evaluación comercial.</span>
        </div>
        <div class="b2b-cobertura">
          <div class="col-flag">
            <div class="f-y"></div>
            <div class="f-b"></div>
            <div class="f-r"></div>
          </div>
          <div class="b2b-cob-text">
            <strong>Cobertura nacional</strong>
            Despachamos a todo el territorio colombiano. Bogotá con entrega express disponible.
          </div>
        </div>
      </div>
      <div class="b2b-form-wrap">
        <div id="b2b-form-content">
          <p class="b2b-form-title">Quiero ser aliado</p>
          <p class="b2b-form-sub">Cuéntanos sobre tu negocio y te contactamos en menos de 24 horas.</p>
          <form id="b2bForm" onsubmit="submitB2B(event)">
            <div class="b2b-fg">
              <label>Nombre completo</label>
              <input type="text" placeholder="Tu nombre" required />
            </div>
            <div class="b2b-form-grid">
              <div class="b2b-fg">
                <label>Ciudad</label>
                <input type="text" placeholder="Ciudad" required />
              </div>
              <div class="b2b-fg">
                <label>WhatsApp</label>
                <input type="tel" placeholder="+57 300..." required />
              </div>
            </div>
            <div class="b2b-fg">
              <label>Tipo de negocio</label>
              <select required>
                <option value="" disabled selected>Selecciona...</option>
                <option value="emp">Emprendedor independiente</option>
                <option value="alm">Almacén / Tienda física</option>
                <option value="cli">Clínica o consultorio</option>
                <option value="dis">Empresa / Distribuidor</option>
                <option value="otro">Otro</option>
              </select>
            </div>
            <div class="b2b-fg">
              <label>¿Qué buscas? (opcional)</label>
              <textarea placeholder="Cuéntanos brevemente qué productos te interesan o qué necesitas..."></textarea>
            </div>
            <button type="submit" class="b2b-btn">Enviar solicitud ✉️</button>
          </form>
          <p class="b2b-disclaimer">Nos comunicaremos por WhatsApp o correo.<br>Tu información es confidencial.</p>
        </div>
        <div class="b2b-success" id="b2b-success">
          <div class="b2b-success-icon">✅</div>
          <p class="b2b-success-title">¡Solicitud enviada!</p>
          <p class="b2b-success-text">Te contactaremos en menos de 24 horas. ¡Bienvenido a la familia Ortholines!</p>
        </div>
      </div>
    </div>
  </div>
</section>
'''

anchor = '<section class="about" id="nosotros">'
if anchor not in content:
    print("ERROR: sección nosotros no encontrada"); sys.exit(1)
content = content.replace(anchor, b2b_html + anchor, 1)
print("✓ Paso 1: HTML sección Aliados insertado")

# ── PASO 3: JavaScript — insertar antes de </body>
js_block = '''<script>
function submitB2B(e) {
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
  window.location.href = 'mailto:ortholinessasventas@gmail.com?subject=' + subject + '&body=' + body;
  document.getElementById('b2b-form-content').style.display = 'none';
  document.getElementById('b2b-success').style.display = 'block';
}
</script>
'''

if '</body>' not in content:
    print("ERROR: </body> no encontrado"); sys.exit(1)
content = content.replace('</body>', js_block + '</body>', 1)
print("✓ Paso 3: JS submitB2B insertado")

with open('/home/user/GlobalChay/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

new_len = len(content)
print(f"✓ Archivo guardado. Tamaño: {original_len:,} → {new_len:,} bytes (+{new_len - original_len:,})")
