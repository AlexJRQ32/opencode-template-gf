---
name: image-maker
description: Crea imágenes, diagramas, logos, gráficos y visuales de alta resolución con Python/Pillow. Integra diseño UI/UX, tipografía, paletas y principios visuales de las skills de diseño. Úsala para "imagen", "diagrama", "logo", "banner", "infografía", "4K", "gráfico", o "visual".
---

# Image Maker

Skill para crear imágenes programáticas de alta calidad. Integra automáticamente las skills de diseño disponibles.

## Skills de diseño que debe usar en conjunto

| Skill | Propósito |
|-------|-----------|
| `impeccable` | Auditoría visual, jerarquía, espaciado, alineación, refinamiento |
| `frontend-design` | Dirección estética audaz, tipografía, paletas no genéricas |
| `ui-ux-pro-max` | Base de datos de estilos, paletas, fuentes, guías UX |
| `emil-design-eng` | Microdetalles, animación implícita, polish invisible |
| `presentation-designer` | Narrativa visual por slide, estructura de contenido |

**Siempre que crees una imagen, DEBES cargar estas skills y aplicar sus principios.** No son opcionales — son parte del pipeline de calidad.

## Flujo de trabajo

### 1. Brief → Dirección estética
Antes de escribir código, definir:
- **Propósito**: ¿diagrama técnico, logo, banner, infografía, slide, icono?
- **Resolución**: ¿web (72dpi), 4K (3840×2160), print (300dpi)?
- **Tono**: minimalista, corporativo, lúdico, técnico, oscuro, colorido
- **Paleta**: ¿marca existente o crear desde cero?
- **Formato de salida**: PNG, JPG, SVG, PDF

Usar `ui-ux-pro-max` para buscar paletas y tipografías, `frontend-design` para la dirección estética.

### 2. Configurar el canvas

```python
from PIL import Image, ImageDraw, ImageFont

# 4K estándar
W, H = 3840, 2160
img = Image.new('RGB', (W, H), color=(0x0D, 0x11, 0x17))
draw = ImageDraw.Draw(img)

# Print quality
# W, H = 4961, 3508  # A3 a 300dpi
# img = Image.new('RGB', (W, H), color='white')
```

### 3. Tipografía
Cargar fuentes del sistema:
```python
# Windows
font_bold = ImageFont.truetype("C:/Windows/Fonts/Inter-Bold.ttf", size=120)
font_regular = ImageFont.truetype("C:/Windows/Fonts/Inter-Regular.ttf", size=60)
font_light = ImageFont.truetype("C:/Windows/Fonts/Inter-Light.ttf", size=40)

# También buscar en: C:/Windows/Fonts/, ~/AppData/Local/Microsoft/Windows/Fonts/
# Fuentes recomendadas: Inter, Manrope, Plus Jakarta Sans, DM Sans, Space Grotesk
```

Usar `ui-ux-pro-max search.py` para encontrar font pairings. Usar `emil-design-eng` para kerning y jerarquía visual.

### 4. Diagramas técnicos (flechas, cajas, conexiones)

```python
def draw_arrow(draw, x1, y1, x2, y2, color, width=6):
    """Dibuja flecha entre dos puntos."""
    draw.line([(x1, y1), (x2, y2)], fill=color, width=width)
    # Punta de flecha
    import math
    angle = math.atan2(y2 - y1, x2 - x1)
    arrow_len = 30
    ax1 = x2 - arrow_len * math.cos(angle - 0.4)
    ay1 = y2 - arrow_len * math.sin(angle - 0.4)
    ax2 = x2 - arrow_len * math.cos(angle + 0.4)
    ay2 = y2 - arrow_len * math.sin(angle + 0.4)
    draw.polygon([(x2, y2), (ax1, ay1), (ax2, ay2)], fill=color)

def draw_rounded_box(draw, x1, y1, x2, y2, radius=20, fill=None, outline=None, width=1):
    """Caja con esquinas redondeadas."""
    draw.rounded_rectangle([(x1, y1), (x2, y2)], radius=radius, fill=fill, outline=outline, width=width)
```

### 5. Iconos y formas básicas
```python
# Círculo
draw.ellipse([(x-r, y-r), (x+r, y+r)], fill=color)

# Triángulo (para flechas, play buttons, etc)
draw.polygon([(cx, cy-h), (cx-w, cy+h), (cx+w, cy+h)], fill=color)

# Gradiente lineal
for i in range(H):
    ratio = i / H
    r = int(c1[0] * (1-ratio) + c2[0] * ratio)
    g = int(c1[1] * (1-ratio) + c2[1] * ratio)
    b = int(c1[2] * (1-ratio) + c2[2] * ratio)
    draw.line([(0, i), (W, i)], fill=(r, g, b))
```

### 6. Procesamiento de imágenes existentes
```python
# Abrir, redimensionar, recortar
logo = Image.open("logo.png").resize((300, 300), Image.LANCZOS)

# Pegar con máscara (transparencia)
img.paste(logo, (x, y), logo if logo.mode == 'RGBA' else None)

# Cambiar color de píxeles específicos (útil para logos)
pixels = img.load()
for y in range(y1, y2):
    for x in range(x1, x2):
        if pixels[x, y] == (255, 255, 255):  # blanco → nuevo color
            pixels[x, y] = nuevo_color

# Fondo redondeado
mask = Image.new('L', (w, h), 0)
draw_mask = ImageDraw.Draw(mask)
draw_mask.rounded_rectangle([(0, 0), (w, h)], radius=r, fill=255)
result = Image.composite(overlay, img, mask)
```

### 7. Guardado
```python
# PNG (lossless, con transparencia)
img.save("output.png", format="PNG")

# JPEG (con calidad controlada)
img = img.convert('RGB')
img.save("output.jpg", format="JPEG", quality=95)

# WebP (buena compresión)
img.save("output.webp", format="WEBP", quality=90)

# PDF (una página)
img.save("output.pdf", format="PDF", resolution=300)
```

## Reglas de diseño visual

Aplicar principios de `impeccable` y `emil-design-eng`:

- **Jerarquía clara**: un elemento domina visualmente por slide/imagen
- **Espaciado consistente**: usar una grilla base de 8px o 16px
- **Alineación**: nada está "casi" alineado. Usar coordenadas exactas
- **Color**: paleta de 3-4 colores máximo. Usar `ui-ux-pro-max` para buscar combinaciones
- **Blur/transparencia**: solo con propósito (profundidad, enfoque)
- **Sombras**: suaves, dirección de luz consistente
- **Bordes**: 1-2px para UI, 3-6px para diagramas

## Resoluciones estándar

| Formato | Dimensiones | PPI | Uso |
|---------|-------------|-----|-----|
| Web | 1920×1080 | 72 | Slides digitales |
| 4K | 3840×2160 | 72 | Diagramas, banners grandes |
| HD+ | 2560×1440 | 72 | Wallpapers, presentaciones |
| Print A4 | 2480×3508 | 300 | Documentos impresos |
| Print A3 | 3508×4961 | 300 | Posters |
| Instagram | 1080×1080 | 72 | Redes sociales |
| LinkedIn banner | 1584×396 | 72 | Banners perfil |

## Pipelines típicos

### Diagrama técnico 4K
`brief → ui-ux-pro-max palette → frontend-design direction → Pillow render → impeccable audit → save`

### Procesar logo
`extract from PDF → Pillow color fix → impeccable polish → re-embed → export`

### Infografía
`content structure → presentation-designer narrative → ui-ux-pro-max fonts → Pillow layout → emil-design-eng polish → 4K export`
