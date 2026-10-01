---
name: ortholines-product-launch
description: Workflow completo para publicar, actualizar o corregir product cards en ortholinessas.com — pipeline de imágenes con marca de agua, estructura .ocard (desktop + mobile), categorías y tags, formato de precios, WhatsApp 50/50, datos estructurados JSON-LD (ItemList + Product/Offer) y deploy a Hostinger. Usar SIEMPRE que se vaya a agregar un producto nuevo, agregar fotos a una card existente, cambiar precios, renombrar un producto, o tocar cualquier cosa dentro de las product cards de index.html — tanto si el pedido menciona "card", "carrusel", "catálogo" como si solo dice "sube estas fotos" o "cambia este precio".
---

# Ortholines — Lanzamiento y Actualización de Productos

Consolida el estándar `.ocard`, el pipeline de imágenes, las reglas de SEO/JSON-LD y el proceso de deploy — todo aprendido a punta de errores reales en producción (imágenes rotas, JSON-LD inválido). Seguir esto evita repetirlos.

## 0. Antes de tocar nada

1. Leer el HTML actual — nunca asumir la estructura de memoria. Inspeccionar una card funcional real (Infantómetro o Bastón Canadiense) como referencia exacta de clases/JS antes de crear o modificar cualquier otra.
2. Replicar, nunca inventar. Ninguna card nueva introduce una estructura, clase o lógica JS distinta a las que ya existen.
3. Si la tarea es grande (varios productos), dividir en batches pequeños (ej. 2 cards a la vez) y confirmar cada paso antes de seguir — así se ha trabajado siempre este proyecto.

## 1. Pipeline de imágenes (obligatorio para toda foto nueva)

1. **Origen**: las fotos viven en Google Drive, carpeta "Articulos nuevos". Buscar por `parentId`, no por título — es más confiable.
2. **Formato de entrada**: 800×800px, fondo blanco limpio. Nunca redimensionar ni recortar.
3. **Marca de agua obligatoria**: procesar con `watermark.py` (ya existe en la raíz del repo) — alpha=45, texto "Ortholines S.A.S.", diagonal, azul `#1a3a8f`. Ninguna imagen nueva se inserta en el HTML sin pasar por este paso.
4. **Conversión**: a WebP, guardada en `/img/`.
5. **Nombrado**: descriptivo y consistente con el producto (ej. `faja-dorsolumbar-nuevo.webp`, `faja-dorsolumbar-nuevo-0.webp` para la siguiente). Cuidado con mayúsculas/minúsculas — Windows (entorno local) no distingue case, pero Hostinger (Linux) sí. Un mismatch de case pasa desapercibido en local y rompe en producción.

## 2. Estructura de card — spec `.ocard` (bloqueado, no se reinventa)

1. Carrusel de fotos arriba con flechas, dots, y contador "X/Y" — el último slot del contador SIEMPRE se reserva para un video futuro (ej. 4 fotos → contador llega a "1/5").
2. Fondo de la card: claro (blanco/beige) — nunca un color sólido de categoría; el color de categoría es solo acento en badge, precio y bordes.
3. Nombre del producto: azul `#1a3a8f`, mayúsculas, bold.
4. Precio ("Desde $XXX.000 COP" o "Cotizar"): azul `#1a3a8f`, tamaño moderado, una sola línea — igual que la card de referencia. Nunca grande, nunca partido en dos líneas.
5. Botón WhatsApp "Consultar disponibilidad": verde, estandarizado — no modificar su estilo.
6. **Mobile**: descripción truncada con "..." + link "Toca para ver más" en azul `#1a3a8f`; al tocar abre un bottom-sheet con el carrusel completo y la descripción completa — misma clase/JS que las cards de referencia, nunca una estructura nueva.
7. **Desktop**: carrusel funcional con flechas, dots y contador visibles y sincronizados.

### Al agregar fotos a una card existente

- La(s) foto(s) nueva(s) van como primer(os) slide(s) (portada), empujando las existentes al final en el mismo orden relativo que ya tenían.
- El contador sube exactamente en +N (N = fotos agregadas).
- Verificar SIEMPRE que la cantidad de dots coincide exactamente con la cantidad de slides — esta es la causa más común de bugs de carrusel.

### Al convertir una card de emoji/placeholder a carrusel completo

- Reemplazar el emoji por el carrusel completo, mismo patrón que las demás.
- Mantener descripción, precio y botón WhatsApp existentes sin tocar.
- Fondo claro, precio azul, badge del color de su categoría — igual que las cards vecinas de esa misma sección.

## 3. Categorías, subcategorías y color de badge

Categorías del menú superior: Muñeca & Mano · Codo · Postura & Espalda · Abdomen & Tórax · Rodilla · Tobillo & Pie · Ortesis & Férulas (a medida) · Soporte & Movilidad.

- Dentro de una categoría puede haber un **tag** de subgrupo (ej. "Hombro & Brazo" dentro de Postura & Espalda, junto a Cabestrillo Acolchado Adulto). Al ubicar un producto nuevo, no asumir la categoría por el nombre del producto — comparar contra un producto ya existente y similar en la web viva y usar el mismo tag.
- Color de acento por categoría: Soporte = naranja `#f47c1a`. Las demás categorías se van definiendo según se trabajan — si no está documentado el color de una categoría, revisar una card real de esa sección antes de inventar uno.

## 4. Precios

- Producto con precio variable/desde: `"Desde $XXX.000 COP"`.
- Producto con precio fijo: `"$XXX.000 COP"`.
- Producto bespoke/a medida sin precio de catálogo: `"Cotizar"` — **nunca inventar un número** solo para llenar el campo, ni siquiera basado en competencia, salvo que el dueño del negocio lo confirme explícitamente.
- Referencias de mercado reales y públicas para investigar precios de competencia en Bogotá: biosmedic.com y santeyconfort.com (tienen catálogo público con precios — la mayoría de competidores locales no).

## 5. WhatsApp — distribución 50/50

Los botones de WhatsApp alternan entre dos líneas (Asesor / Gerencia) para repartir la carga comercial. Al agregar una card nueva, revisar qué línea usó la card vecina más cercana en esa misma sección y alternar a la otra — nunca repetir la misma línea dos veces seguidas dentro de una sección.

## 6. Datos estructurados (JSON-LD) — dos capas distintas, no confundir

### Capa A — ItemList en el `<head>`
Es el listado general de navegación/SEO de todo el catálogo. Toda card visible en la página debe tener su entrada ahí (mismo `name` que el título de la card). Al agregar o renombrar un producto:
- Agregar/actualizar su entrada en el ItemList.
- Mantener el `position` secuencial coherente con el orden real de aparición en la página — si insertar en medio desordena la numeración, renumerar todo de principio a fin.
- Verificar con una comparación explícita: extraer todos los `name` del ItemList Y todos los títulos (h3) de las cards, y compararlos uno a uno. No asumir que "ya debe estar" — varias cards históricas no tenían entrada y pasó desapercibido durante meses.

### Capa B — Product/Offer por card
Es el schema que le permite a Google mostrar precio y estrellas directo en resultados de búsqueda (Fichas de comerciante / Fragmentos de productos en Search Console).

- **Producto con precio fijo o "Desde $X"**: usar `Offer` simple (NO `AggregateOffer`) con `price` numérico plano (sin puntos ni símbolo), `priceCurrency: "COP"`, `availability: "https://schema.org/InStock"`, y `priceValidUntil` (~6 meses adelante — dejar nota de que hay que refrescar esa fecha periódicamente, no hay mecanismo automático).
- **Producto "Cotizar" sin precio real**: regla dura de Google — todo `Product` necesita AL MENOS UNO de `offers`, `review` o `aggregateRating`. Si no tiene precio y tampoco tiene un testimonio real, **no crear el bloque `Product` para ese producto en absoluto** (ni siquiera con `offers` vacío o ausente pero el resto del schema presente) — eso es justo lo que genera error crítico en Search Console. Sin bloque, Google simplemente no intenta el rich result para ese producto, que es lo correcto.
- **`review`/`aggregateRating`**: solo se agregan a un producto si tiene un testimonio REAL y visible en la sección "Clientes que Confían" de la página, amarrado explícitamente a ese producto (ej. "Faja Lumbosacra · Bogotá"). Nunca inventar reseñas. Un testimonio genérico sin producto amarrado (ej. de un fisioterapeuta hablando en general) no cuenta para ningún producto puntual.

## 7. Checklist de verificación antes de dar por terminado

- [ ] Todas las imágenes nuevas tienen marca de agua (alpha=45) y están en WebP en `/img/`
- [ ] Ningún carrusel tiene desincronización entre cantidad de slides y cantidad de dots
- [ ] Mobile: descripción truncada + "Toca para ver más" funcionando en las cards tocadas
- [ ] Desktop: carrusel con flechas, dots y contador correctos
- [ ] ItemList del `<head>` actualizado y comparado 1:1 contra los títulos reales de las cards
- [ ] Cada Product con precio tiene `Offer` completo (no `AggregateOffer`); cada "Cotizar" sin review real NO tiene bloque Product
- [ ] JSON-LD completo parsea sin errores (comas colgantes, comillas rotas)
- [ ] Correr la prueba de resultados enriquecidos de Google (search.google.com/test/rich-results) contra la URL en producción — 0 errores críticos antes de cerrar la tarea

## 8. Deploy

1. `git pull` SIEMPRE antes de `git add . && git commit && git push` (Code auto-commitea seguido; hace falta el pull para evitar rechazo).
2. **Code NO tiene acceso a Hostinger** (ni hPanel ni FTP) — la subida a producción es 100% manual, la hace el dueño del proyecto arrastrando archivos en el Administrador de Archivos de hPanel.
3. **Error histórico real a evitar**: subir solo `index.html` sin las imágenes nuevas de `/img/` rompe todas las fotos nuevas en producción (el navegador muestra el alt-text en vez de la imagen porque el archivo no existe en el servidor — funciona perfecto en local porque ahí sí están los archivos en disco). Recordar explícitamente en cada entrega: "sube `/img/` (archivos nuevos) + `index.html`", no solo el segundo.
4. Después del deploy, purgar caché si el hosting tiene LiteSpeed Cache o similar, y hacer hard refresh antes de dar el visto bueno.
