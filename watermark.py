from PIL import Image, ImageDraw, ImageFont
import math, os, glob

def add_watermark(input_path, output_path):
    img = Image.open(input_path).convert('RGBA')
    W, H = img.size
    diag = math.sqrt(W**2 + H**2)
    angle = math.degrees(math.atan2(H, W))

    try:
        font_size = int(diag * 0.07)
        font = ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf', font_size)
    except:
        try:
            font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', font_size)
        except:
            font = ImageFont.load_default()

    text = "Ortholines S.A.S."
    test_draw = ImageDraw.Draw(Image.new('RGBA', (1, 1)))
    bbox = test_draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    scale = diag * 0.85 / tw
    font_size = int(font_size * scale)

    try:
        font = ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf', font_size)
    except:
        try:
            font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', font_size)
        except:
            font = ImageFont.load_default()

    bbox = test_draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]

    size = int(diag * 1.5)
    txt_layer = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    tdraw = ImageDraw.Draw(txt_layer)
    cx = (size - tw) // 2
    cy = (size - th) // 2
    tdraw.text((cx, cy), text, font=font, fill=(26, 58, 143, 45))

    txt_rot = txt_layer.rotate(angle, resample=Image.BICUBIC, center=(size//2, size//2))
    ox = (size - W) // 2
    oy = (size - H) // 2
    txt_crop = txt_rot.crop((ox, oy, ox + W, oy + H))

    result = Image.alpha_composite(img, txt_crop)

    # Preservar transparencia si la imagen original tenia canal alfa
    tiene_alfa = img.getchannel('A').getextrema()[0] < 255

    if output_path.endswith('.webp'):
        if tiene_alfa:
            result.save(output_path, 'WEBP', quality=85)
        else:
            result.convert('RGB').save(output_path, 'WEBP', quality=85)
    else:
        if tiene_alfa:
            result.save(output_path, quality=90)
        else:
            result.convert('RGB').save(output_path, quality=90)

# Imágenes a excluir (iconos y assets de marca)
EXCLUIR = [
    'icono-whatsapp',
    'logo',
    'favicon',
    'cruz',
    'og-image',
    'ortholines-s-a-s',
]

def debe_excluir(nombre):
    nombre_lower = nombre.lower()
    return any(ex in nombre_lower for ex in EXCLUIR)

# Procesar todas las imágenes en /img/
img_dir = os.path.join(os.path.dirname(__file__), 'img')
archivos = glob.glob(os.path.join(img_dir, '*.webp')) + \
           glob.glob(os.path.join(img_dir, '*.jpg')) + \
           glob.glob(os.path.join(img_dir, '*.png'))

procesados = 0
omitidos = 0

for archivo in sorted(archivos):
    nombre = os.path.basename(archivo)
    if debe_excluir(nombre):
        print(f"  OMITIDO: {nombre}")
        omitidos += 1
        continue
    add_watermark(archivo, archivo)
    print(f"  OK: {nombre}")
    procesados += 1

print(f"\nTotal: {procesados} procesadas, {omitidos} omitidas")
