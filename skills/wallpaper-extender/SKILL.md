---
name: wallpaper-extender
description: Convierte cualquier imagen en wallpaper 4K (3840×2160) alargando solo los fondos y manteniendo la imagen original centrada e intacta. Úsala cuando pidan "wallpaper", "4K wallpaper", "fondo de pantalla", "extender imagen a 4K", "alargar imagen para fondo", "wallpaper sin recortar", o "imagen para fondo de escritorio".
---

# Wallpaper Extender

Skill para convertir cualquier imagen en un wallpaper 4K sin recortar ni deformar el contenido principal. La imagen original se mantiene centrada con su relación de aspecto original, mientras el fondo se extiende inteligentemente para llenar los 3840×2160.

## ⚙️ Cómo funciona

```
INPUT: imagen de cualquier tamaño/relación de aspecto
                         │
            ┌────────────┴────────────┐
            │  0. AUTO-DETECCIÓN      │
            │  ┌──────────────────┐   │
            │  │ ¿Bordes          │   │
            │  │ uniformes?       │──┼──→ EXTEND
            │  │ (std dev < 20)   │   │
            │  ├──────────────────┤   │
            │  │ ¿Aspecto 16:9?   │   │
            │  │ + bordes         │──┼──→ FULL
            │  │ variados         │   │
            │  ├──────────────────┤   │
            │  │ ¿Transparencia?  │──┼──→ EXTEND
            │  ├──────────────────┤   │
            │  │ Default seguro   │──┼──→ EXTEND
            │  └──────────────────┘   │
            └────────────┬────────────┘
                         │
    ┌────────────────────┴────────────────────┐
    │                                         │
    ▼                                         ▼
  EXTEND                                    FULL
    │                                         │
    ├─ 1. Escalar imagen                     ├─ 1. Escalar (cover)
    │   (manteniendo aspecto)                │    max scale para
    │   para que quepa en 4K                 │    llenar canvas
    │                                         │
    ├─ 2. Generar fondo                      ├─ 2. Recorte centrado
    │   ┌──────────────────┐                  │
    │   │ blur  → estirar  │                  │
    │   │         + blur   │                  │
    │   ├──────────────────┤                  │
    │   │ edge  → reflejar │                  │
    │   │         bordes   │                  │
    │   ├──────────────────┤                  │
    │   │ solid → color    │                  │
    │   │         promedio │                  │
    │   ├──────────────────┤                  │
    │   │ grad  → degradé  │                  │
    │   │         desde    │                  │
    │   │         bordes   │                  │
    │   └──────────────────┘                  │
    │                                         │
    ├─ 3. Componer: fondo +                   │
    │   imagen centrada encima               │
    │                                         │
    ├─ 4. (Opcional) Feather                  │
    │   sutil en la costura                   │
    │                                         │
    ▼                                         ▼
  wallpaper-{metodo}-...jpg               wallpaper-full-...jpg
```

## 🚀 Uso rápido

```powershell
python "$env:USERPROFILE\.agents\skills\wallpaper-extender\scripts\wallpaper-extender.py" "C:\ruta\a\mi-imagen.jpg"
```

Por defecto:
- Método: `blur` (estirar + blurrear para fondo tipo macOS/Windows)
- Sin feather
- Output: `{{USER_DIR}}\OneDrive\Documentos\Archivos OpenCode\Imágenes\wallpapers\`

### Ejemplos

```powershell
# Modo auto (default) — detecta si extender o solo upscalar
python "$env:USERPROFILE\.agents\skills\wallpaper-extender\scripts\wallpaper-extender.py" "foto.jpg"

# Forzar modo FULL — upscale directo a 4K con cover crop (para fotos full-frame)
python "$env:USERPROFILE\.agents\skills\wallpaper-extender\scripts\wallpaper-extender.py" "foto.jpg" --mode full

# Forzar modo EXTEND — siempre extiende fondo (para imágenes con fondo)
python "$env:USERPROFILE\.agents\skills\wallpaper-extender\scripts\wallpaper-extender.py" "foto.jpg" --mode extend

# Método blur (default) — el más versátil, queda como fondo profesional
python "$env:USERPROFILE\.agents\skills\wallpaper-extender\scripts\wallpaper-extender.py" "foto.jpg"

# Método edge — refleja los bordes, ideal para ilustraciones con fondo sólido
python "$env:USERPROFILE\.agents\skills\wallpaper-extender\scripts\wallpaper-extender.py" "ilustracion.png" --method edge

# Método solid — color sólido del borde, ideal para arte minimalista
python "$env:USERPROFILE\.agents\skills\wallpaper-extender\scripts\wallpaper-extender.py" "logo.png" --method solid

# Método gradient — degradado desde los bordes hacia afuera
python "$env:USERPROFILE\.agents\skills\wallpaper-extender\scripts\wallpaper-extender.py" "paisaje.jpg" --method grad

# Con feather para transición más suave
python "$env:USERPROFILE\.agents\skills\wallpaper-extender\scripts\wallpaper-extender.py" "foto.jpg" --feather 30

# Blur personalizado
python "$env:USERPROFILE\.agents\skills\wallpaper-extender\scripts\wallpaper-extender.py" "foto.jpg" --blur 80

# Output personalizado
python "$env:USERPROFILE\.agents\skills\wallpaper-extender\scripts\wallpaper-extender.py" "foto.jpg" -o "{{USER_DIR}}\Pictures\wallpaper-4k.jpg"
```

## 🎯 Modos de procesamiento

| Modo | Flag | Descripción |
|------|------|-------------|
| **Auto** | `--mode auto` (default) | Detecta automáticamente si la imagen tiene fondo (→ EXTEND) o es full-frame (→ FULL). Usa heurísticos de uniformidad de bordes + aspecto ratio. |
| **Extend** | `--mode extend` | Comportamiento clásico: escala la imagen manteniendo aspecto y extiende el fondo con el método elegido. |
| **Full** | `--mode full` | Upscale directo a 4K con cover-crop centrado. Ideal para fotos que ya cubren toda la pantalla. |

### Algoritmo de auto-detección

1. **Transparencia** — Si la imagen tiene RGBA con píxeles transparentes → EXTEND
2. **Uniformidad de bordes** — Muestrea 100+ píxeles por borde, calcula std dev por canal RGB
3. Si **std dev promedio < 20** (bordes casi idénticos) → EXTEND (tiene fondo)
4. Si **aspecto ratio cercano a 16:9 (±10%)** + bordes variados → FULL
5. **Default seguro** → EXTEND (en caso de duda)

## 🎯 Métodos de extensión de fondo (solo modo EXTEND)

| Método | Flag | Mejor para | Descripción |
|--------|------|-----------|-------------|
| **Blur** | `--method blur` | Fotos, paisajes, cualquier imagen | Escala la imagen para llenar 4K (estirada) y aplica Gaussian blur. El resultado es un fondo suave que conserva los colores generales de la imagen. **El más recomendado.** |
| **Edge** | `--method edge` | Ilustraciones, logos, UI | Toma los píxeles del borde de la imagen y los refleja hacia afuera como un espejo. Ideal cuando el fondo es uniforme o tiene un patrón simple. |
| **Solid** | `--method solid` | Minimalista, gráficos planos | Calcula el color promedio de todos los bordes y crea un fondo de color sólido. |
| **Gradient** | `--method grad` | Arte conceptual, fondos degradados | Crea un degradado radial/cuadrado desde el centro de la imagen hacia las esquinas basado en los colores de los bordes. |

## 📋 Parámetros del script

```
wallpaper-extender.py <input_path> [opciones]

Argumentos:
  input_path               Ruta a la imagen a convertir

Opciones:
  -o, --output PATH        Ruta de salida (default: Archivos OpenCode/Imágenes/wallpapers/)
  -m, --method {blur,edge,solid,grad}
                           Método de extensión de fondo (default: blur)
  -b, --blur RADIUS        Radio del blur para método 'blur' (default: 50)
  -f, --feather PX         Píxeles de transición suave en la costura (default: 0)
  -q, --quality 1-100      Calidad JPEG (default: 95)
  --canvas WxH             Dimensiones del canvas (default: 3840x2160)
  --mode {auto,extend,full}
                           Modo de procesamiento (default: auto)
  --no-center              No centrar la imagen (esquina superior izquierda)
  --offset X,Y             Desplazamiento de la imagen desde el centro
  --scale FACTOR           Escala forzada (ej: 1.5 para 150%)
  --list-methods           Listar métodos disponibles y salir
```

## 📁 Output

Por defecto las imágenes se guardan en:
```
{{USER_DIR}}\OneDrive\Documentos\Archivos OpenCode\Imágenes\wallpapers\
```

El nombre de archivo sigue el formato:
```
wallpaper-{metodo}-{nombre-original}-{timestamp}.jpg   (modo EXTEND)
wallpaper-full-{nombre-original}-{timestamp}.jpg       (modo FULL)
```

## 🧠 Algoritmo detallado

### Método Blur (recomendado)

```python
from PIL import Image, ImageFilter

def method_blur(img, canvas_w, canvas_h, blur_radius):
    """Estira la imagen a 4K y aplica blur para crear fondo."""
    bg = img.resize((canvas_w, canvas_h), Image.LANCZOS)
    bg = bg.filter(ImageFilter.GaussianBlur(radius=blur_radius))
    return bg
```

### Método Edge

```python
import numpy as np

def method_edge(img, canvas_w, canvas_h):
    """Refleja los bordes de la imagen hacia afuera."""
    # Crea un canvas más grande que la imagen
    # Tira de los bordes hacia afuera como espejo
    # El resultado se recorta a 4K
```

### Método Solid

```python
def method_solid(img, canvas_w, canvas_h):
    """Usa el color promedio de los bordes como fondo sólido."""
    import numpy as np
    arr = np.array(img)
    top = arr[0, :, :].mean(axis=0)
    bottom = arr[-1, :, :].mean(axis=0)
    left = arr[:, 0, :].mean(axis=0)
    right = arr[:, -1, :].mean(axis=0)
    avg = (top + bottom + left + right) / 4
    bg = Image.new('RGB', (canvas_w, canvas_h),
                   tuple(int(x) for x in avg))
    return bg
```

### Método Gradient

```python
from PIL import Image, ImageDraw

def method_grad(img, canvas_w, canvas_h):
    """Crea degradado cuadrado desde bordes hacia afuera."""
    # Extrae colores de los bordes
    # Crea degradado radial/lineal
    # Guarda como fondo
```

## 🔧 Edge cases manejados

| Caso | Comportamiento |
|------|---------------|
| Imagen más grande que 4K | Se escala hacia abajo para caber |
| Imagen cuadrada | Se centra con fondo a los lados |
| Imagen vertical (retrato) | Se centra con fondo arriba/abajo |
| Imagen panorámica | Se centra con fondo a los lados |
| Imagen con transparencia (RGBA) | Se preserva sobre fondo generado |
| Archivo no encontrado | Error claro con sugerencias |
| Formato no soportado | Intenta abrir igual, error si falla |

## 🔗 Skills relacionadas

- `image-maker` — Para crear imágenes desde cero
- `visual-creator` — Templates generales de imagen
- `image-viewer` — Para analizar y depurar resultados

