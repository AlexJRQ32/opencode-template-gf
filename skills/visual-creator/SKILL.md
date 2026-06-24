---
name: visual-creator
description: Crea imágenes, gráficos, diagramas, logos, infografías, banners, collages, procesamiento de fotos y visuales para documentos y presentaciones. Usa Python/Pillow con templates reutilizables. Úsala cuando pidan "imagen", "visual", "gráfico", "logo", "banner", "infografía", "diagrama", "collage", "procesar imagen", "edit foto", "generar visual".
---

# Visual Creator

Skill especializada en crear imágenes y visuales con Python/Pillow. Ofrece templates prácticos para los casos más comunes.

## 📁 Reglas de salida

Toda imagen generada se guarda en:
**`{{USER_DIR}}\OneDrive\Documentos\Archivos OpenCode\Imágenes\`**

Con subcarpetas según tipo:
- `logos/` — logos y variantes
- `diagrams/` — diagramas técnicos
- `banners/` — banners y headers
- `infographics/` — infografías
- `processed/` — imágenes procesadas/editadas
- `generated/` — imágenes generadas desde cero

## 🧰 Templates reutilizables

### Template 1: Canvas base 4K
```python
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 3840, 2160
img = Image.new('RGB', (W, H), color=(0x0F, 0x12, 0x16))
draw = ImageDraw.Draw(img)

def load_font(name, size):
    path = f"C:/Windows/Fonts/{name}"
    if os.path.exists(path):
        return ImageFont.truetype(path, size)
    return ImageFont.load_default()
```

### Template 2: Caja redondeada con sombra
```python
def box_with_shadow(draw, x1, y1, x2, y2, radius=20, fill=(0x17, 0x1C, 0x22), shadow=True):
    if shadow:
        for i in range(8, 0, -1):
            a = int(20 / (i + 1))
            draw.rounded_rectangle(
                [(x1-i, y1-i), (x2+i, y2+i)], radius=radius,
                fill=(0x0A, 0x0D, 0x12) if a > 10 else (0x0F, 0x12, 0x16))
    draw.rounded_rectangle([(x1, y1), (x2, y2)], radius=radius, fill=fill)
```

### Template 3: Texto centrado
```python
def centered_text(draw, text, font, x, y, color=(255,255,255)):
    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text((x - tw//2, y - th//2), text, font=font, fill=color)
```

### Template 4: Paleta de 3 colores (estilo presentación)
```python
BG = (0x0F, 0x12, 0x16)     # fondo oscuro
CARD = (0x17, 0x1C, 0x22)    # tarjeta
ACCENT = (0x5B, 0x9B, 0xD5)  # acento azul acero
WHITE = (255, 255, 255)
GRAY = (0x9B, 0xA2, 0xAB)
```

### Template 5: Diagrama con flechas
```python
import math

def arrow(draw, x1, y1, x2, y2, color=ACCENT, width=4):
    draw.line([(x1, y1), (x2, y2)], fill=color, width=width)
    angle = math.atan2(y2 - y1, x2 - x1)
    a_len = 20
    pts = [(x2, y2),
           (x2 - a_len * math.cos(angle - 0.4), y2 - a_len * math.sin(angle - 0.4)),
           (x2 - a_len * math.cos(angle + 0.4), y2 - a_len * math.sin(angle + 0.4))]
    draw.polygon(pts, fill=color)
```

## 📋 Flujos comunes

### Crear banner o header
```
brief → elegir dimensiones → paleta → template canvas → texto + formas → guardar en banners/
```

### Hacer diagrama técnico
```
brief → paleta → template canvas → cajas → flechas → labels → guardar en diagrams/
```

### Procesar logo (cambiar color, fondo)
```
abrir imagen → recorrer píxeles → reemplazar color → pegar sobre fondo nuevo → guardar en logos/
```

### Hacer infografía paso a paso
```
brief → estructura en secciones → títulos → métricas/viñetas → líneas divisorias → guardar en infographics/
```

## 📐 Resoluciones rápidas

| Tipo | Dimensiones |
|------|------------|
| Banner horizontal | 3840×1080 |
| Infografía | 2160×3840 |
| Logo cuadrado | 1024×1024 |
| Diagrama | 3840×2160 |
| Post redes | 1080×1080 |
| Slide | 1920×1080 |

## 🎨 Diseño simple

- **Un solo acento de color** (no más de 2 colores + blanco/gris)
- **Texto grande y claro** (título 80-120px, cuerpo 30-50px)
- **Espacio negativo** (no llenar todo, dejar aire)
- **Consistencia** (misma fuente, mismo radio de esquina, mismo espaciado)

