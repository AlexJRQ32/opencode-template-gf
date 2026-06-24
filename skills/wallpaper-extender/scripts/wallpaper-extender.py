#!/usr/bin/env python3
"""
Wallpaper Extender -- Convierte cualquier imagen en wallpaper 4K (3840x2160)
alargando solo los fondos y manteniendo la imagen original centrada e intacta.

Metodos:
  blur    -> Escala la imagen para llenar 4K + Gaussian blur (default, recomendado)
  edge    -> Refleja los pixeles del borde hacia afuera
  solid   -> Color solido promedio de los bordes
  grad    -> Degradado desde los bordes hacia afuera

Uso:
  python wallpaper-extender.py "imagen.jpg"
  python wallpaper-extender.py "imagen.png" --method edge --feather 20
  python wallpaper-extender.py "imagen.jpg" -o "mi-wallpaper.jpg" --blur 80
"""

import argparse
import os
import sys
import time
from pathlib import Path

try:
    from PIL import Image, ImageFilter, ImageDraw
except ImportError:
    print("ERROR: Pillow no esta instalado. Ejecuta: pip install Pillow")
    sys.exit(1)

try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False
    print("!! numpy no disponible - algunos modos usan fallback mas lento.")
    print("   Para instalarlo: pip install numpy\n")

# -- Constantes ----------------------------------------------------------------

DEFAULT_CANVAS_W = 3840
DEFAULT_CANVAS_H = 2160
DEFAULT_BLUR_RADIUS = 50
DEFAULT_OUTPUT_DIR = Path.home() / "OneDrive" / "Documentos" / "Archivos OpenCode" / "Imágenes" / "wallpapers"
DEFAULT_QUALITY = 95

VALID_METHODS = ("blur", "edge", "solid", "grad")
VALID_MODES = ("auto", "extend", "full")

# -- Utilidades ----------------------------------------------------------------

def timestamp():
    return time.strftime("%Y%m%d-%H%M%S")


def ensure_dir(path):
    Path(path).mkdir(parents=True, exist_ok=True)


def slug_from_path(path):
    return Path(path).stem.replace(" ", "-").lower()[:40] or "image"


def compute_fit_rect(img_w, img_h, canvas_w, canvas_h, scale=None, no_center=False, offset_x=0, offset_y=0):
    if scale:
        new_w = int(img_w * scale)
        new_h = int(img_h * scale)
    else:
        fit_scale = min(canvas_w / img_w, canvas_h / img_h)
        new_w = int(img_w * fit_scale)
        new_h = int(img_h * fit_scale)

    if no_center:
        x, y = 0, 0
    else:
        x = (canvas_w - new_w) // 2 + offset_x
        y = (canvas_h - new_h) // 2 + offset_y

    return x, y, x + new_w, y + new_h, new_w, new_h


# -- Metodos de extension de fondo -------------------------------------------

def method_blur(img, canvas_w, canvas_h, blur_radius):
    """Escala la imagen PARA LLENAR 4K (ignorando aspecto, estirandola)
    y aplica Gaussian blur. Efecto wallpaper tipo macOS/Windows."""
    bg = img.resize((canvas_w, canvas_h), Image.LANCZOS)
    bg = bg.filter(ImageFilter.GaussianBlur(radius=blur_radius))
    return bg


def method_edge(img, canvas_w, canvas_h):
    """Refleja los bordes de la imagen hacia afuera como un espejo."""
    if not HAS_NUMPY:
        return _method_edge_fallback(img, canvas_w, canvas_h)

    img_w, img_h = img.size
    arr = np.array(img, dtype=np.uint8)

    strip_w = max(img_w // 10, 1)
    strip_h = max(img_h // 10, 1)

    top_strip = arr[:strip_h, :, :]
    bottom_strip = arr[-strip_h:, :, :]
    left_strip = arr[:, :strip_w, :]
    right_strip = arr[:, -strip_w:, :]

    top_reflected = np.flip(top_strip, axis=0)
    bottom_reflected = np.flip(bottom_strip, axis=0)
    left_reflected = np.flip(left_strip, axis=1)
    right_reflected = np.flip(right_strip, axis=1)

    extend_top = max((canvas_h - img_h) // 2, 0)
    extend_bottom = max(canvas_h - img_h - extend_top, 0)
    extend_left = max((canvas_w - img_w) // 2, 0)
    extend_right = max(canvas_w - img_w - extend_left, 0)

    bg_arr = np.zeros((canvas_h, canvas_w, 3), dtype=np.uint8)

    # Llenar areas superior e inferior
    if extend_top > 0:
        for y in range(extend_top):
            src_row = top_reflected[min(y, top_reflected.shape[0] - 1)]
            tiled = np.tile(src_row, (canvas_w // img_w + 2, 1))[:canvas_w]
            bg_arr[y, :, :] = tiled

    if extend_bottom > 0:
        for y in range(extend_bottom):
            src_row = bottom_reflected[min(y, bottom_reflected.shape[0] - 1)]
            tiled = np.tile(src_row, (canvas_w // img_w + 2, 1))[:canvas_w]
            bg_arr[canvas_h - 1 - y, :, :] = tiled

    # Llenar areas izquierda y derecha (donde no hay top/bottom)
    if extend_left > 0:
        for x in range(extend_left):
            src_col = left_reflected[:, min(x, left_reflected.shape[1] - 1), :]
            for y in range(canvas_h):
                if y < extend_top or y >= canvas_h - extend_bottom:
                    bg_arr[y, x, :] = src_col[min(y, src_col.shape[0] - 1)]

    if extend_right > 0:
        for x in range(extend_right):
            src_col = right_reflected[:, min(x, right_reflected.shape[1] - 1), :]
            cx = canvas_w - 1 - x
            for y in range(canvas_h):
                if y < extend_top or y >= canvas_h - extend_bottom:
                    bg_arr[y, cx, :] = src_col[min(y, src_col.shape[0] - 1)]

    # Llenar esquinas restantes con color del pixel mas cercano de la imagen
    for y in range(canvas_h):
        for x in range(canvas_w):
            if (y < extend_top or y >= canvas_h - extend_bottom or
                x < extend_left or x >= canvas_w - extend_right):
                if np.all(bg_arr[y, x] == 0):
                    orig_x = max(0, min(x - extend_left, img_w - 1))
                    orig_y = max(0, min(y - extend_top, img_h - 1))
                    bg_arr[y, x] = arr[orig_y, orig_x]

    return Image.fromarray(bg_arr, mode='RGB')


def _method_edge_fallback(img, canvas_w, canvas_h):
    """Fallback para method_edge sin numpy (mas lento, pixel por pixel)."""
    img_w, img_h = img.size
    bg = Image.new('RGB', (canvas_w, canvas_h))
    pixels_img = img.load()
    pixels_bg = bg.load()

    extend_top = max((canvas_h - img_h) // 2, 0)
    extend_left = max((canvas_w - img_w) // 2, 0)

    for y in range(canvas_h):
        for x in range(canvas_w):
            img_x = x - extend_left
            img_y = y - extend_top

            if 0 <= img_x < img_w and 0 <= img_y < img_h:
                continue

            # Reflect pixel to nearest edge
            if img_x < 0:
                ref_x = -img_x
            elif img_x >= img_w:
                ref_x = 2 * img_w - img_x - 1
            else:
                ref_x = img_x
            if img_y < 0:
                ref_y = -img_y
            elif img_y >= img_h:
                ref_y = 2 * img_h - img_y - 1
            else:
                ref_y = img_y
            ref_x = max(0, min(ref_x, img_w - 1))
            ref_y = max(0, min(ref_y, img_h - 1))
            pixels_bg[x, y] = pixels_img[ref_x, ref_y]

    return bg


def method_solid(img, canvas_w, canvas_h):
    """Color solido promedio de todos los bordes."""
    img_w, img_h = img.size

    if HAS_NUMPY:
        arr = np.array(img, dtype=np.float64)
        top = arr[0, :, :].mean(axis=0)
        bottom = arr[-1, :, :].mean(axis=0)
        left = arr[:, 0, :].mean(axis=0)
        right = arr[:, -1, :].mean(axis=0)
        avg_color = (top + bottom + left + right) / 4
        color = tuple(int(x) for x in avg_color)
    else:
        pixels = img.load()
        r_sum, g_sum, b_sum, count = 0, 0, 0, 0
        for x in range(img_w):
            r_sum += pixels[x, 0][0]
            g_sum += pixels[x, 0][1]
            b_sum += pixels[x, 0][2]
            r_sum += pixels[x, img_h - 1][0]
            g_sum += pixels[x, img_h - 1][1]
            b_sum += pixels[x, img_h - 1][2]
            count += 2
        for y in range(1, img_h - 1):
            r_sum += pixels[0, y][0]
            g_sum += pixels[0, y][1]
            b_sum += pixels[0, y][2]
            r_sum += pixels[img_w - 1, y][0]
            g_sum += pixels[img_w - 1, y][1]
            b_sum += pixels[img_w - 1, y][2]
            count += 2
        color = (r_sum // count, g_sum // count, b_sum // count)

    return Image.new('RGB', (canvas_w, canvas_h), color=color)


def method_grad(img, canvas_w, canvas_h):
    """Degradado desde los bordes de la imagen hacia afuera."""
    if HAS_NUMPY:
        arr = np.array(img, dtype=np.float64)
        top_color = tuple(int(x) for x in arr[0, :, :].mean(axis=0))
        bottom_color = tuple(int(x) for x in arr[-1, :, :].mean(axis=0))
        left_color = tuple(int(x) for x in arr[:, 0, :].mean(axis=0))
        right_color = tuple(int(x) for x in arr[:, -1, :].mean(axis=0))
    else:
        samples = 50
        top_color = _sample_edge_color(img, 'top', samples)
        bottom_color = _sample_edge_color(img, 'bottom', samples)
        left_color = _sample_edge_color(img, 'left', samples)
        right_color = _sample_edge_color(img, 'right', samples)

    bg = Image.new('RGB', (canvas_w, canvas_h))
    draw = ImageDraw.Draw(bg)

    for y in range(canvas_h):
        ny = y / canvas_h if canvas_h > 1 else 0.5
        for x in range(canvas_w):
            nx = x / canvas_w if canvas_w > 1 else 0.5

            w_top = 1 - ny
            w_bottom = ny
            w_left = 1 - nx
            w_right = nx

            r = int(
                top_color[0] * w_top * 0.5 +
                bottom_color[0] * w_bottom * 0.5 +
                left_color[0] * w_left * 0.5 +
                right_color[0] * w_right * 0.5
            )
            g = int(
                top_color[1] * w_top * 0.5 +
                bottom_color[1] * w_bottom * 0.5 +
                left_color[1] * w_left * 0.5 +
                right_color[1] * w_right * 0.5
            )
            b = int(
                top_color[2] * w_top * 0.5 +
                bottom_color[2] * w_bottom * 0.5 +
                left_color[2] * w_left * 0.5 +
                right_color[2] * w_right * 0.5
            )

            draw.point((x, y), fill=(r, g, b))

    return bg


def _sample_edge_color(img, side, samples=50):
    w, h = img.size
    pixels = img.load()
    r_sum, g_sum, b_sum = 0, 0, 0
    count = 0

    for i in range(samples):
        if side == 'top':
            x = int(w * i / samples)
            y = 0
        elif side == 'bottom':
            x = int(w * i / samples)
            y = h - 1
        elif side == 'left':
            x = 0
            y = int(h * i / samples)
        elif side == 'right':
            x = w - 1
            y = int(h * i / samples)

        if 0 <= x < w and 0 <= y < h:
            px = pixels[x, y]
            r_sum += px[0]
            g_sum += px[1]
            b_sum += px[2]
            count += 1

    if count == 0:
        return (0, 0, 0)
    return (r_sum // count, g_sum // count, b_sum // count)


# -- Quality Enhancement -----------------------------------------------------

def compute_scale_factor(img_w, img_h, canvas_w, canvas_h, mode='full'):
    """Compute the effective upscale factor for source-to-canvas sizing."""
    if mode == 'full':
        return max(canvas_w / img_w, canvas_h / img_h)
    else:
        return min(canvas_w / img_w, canvas_h / img_h)


def multi_step_upscale(img, target_w, target_h, resample=Image.LANCZOS):
    """
    Upscale in multiple incremental steps (max ~2x per step) to reduce
    interpolation artifacts compared to a single large upscale jump.
    """
    current = img
    cw, ch = current.size

    while cw < target_w or ch < target_h:
        next_w = min(cw * 2, target_w)
        next_h = min(ch * 2, target_h)
        current = current.resize((next_w, next_h), resample)
        cw, ch = next_w, next_h

    return current


def enhance_quality(img, level=50):
    """
    Post-upscale quality enhancement via UnsharpMask.

    Maps level (0-100) to tuned UnsharpMask parameters:
      level=35 -> radius=1.2, percent=76,  threshold=5  (clean)
      level=50 -> radius=1.5, percent=100, threshold=3 (balanced)
      level=75 -> radius=2.0, percent=150, threshold=1 (aggressive)
    """
    if level <= 0:
        return img

    level = max(0, min(100, level))

    radius = 0.5 + (level / 100) * 2.5
    percent = int(10 + (level / 100) * 100)
    threshold = int(max(0, 10 - (level / 100) * 10))

    return img.filter(ImageFilter.UnsharpMask(radius, percent, threshold))


# -- Auto-detection: EXTEND vs FULL ----------------------------------------

def detect_mode(img, canvas_w, canvas_h):
    """Detecta si la imagen necesita EXTEND (tiene fondo) o FULL (full-frame).
    
    Heuristicos:
    1. Si tiene transparencia real (RGBA con alpha==0) -> EXTEND
    2. Evalua uniformidad de bordes (std dev por canal)
    3. Si bordes uniformes (std dev < 20) -> EXTEND (tiene fondo)
    4. Si bordes variados Y aspecto cercano a 16:9 -> FULL
    5. Default -> EXTEND (seguro)
    """
    # 1. Verificar transparencia
    if img.mode == 'RGBA':
        alpha = img.split()[3]
        ext = alpha.getextrema()
        if ext[0] < 255:
            print("[DETECT] Transparencia detectada -> EXTEND")
            return "extend"

    # Convertir a RGB para analisis
    if img.mode != 'RGB':
        img_rgb = img.convert('RGB')
    else:
        img_rgb = img.copy()

    # 2. Muestrear uniformidad de bordes
    w, h = img_rgb.size
    edge_pixels = []
    samples_per_side = max(100, min(w, h) // 2)

    # Borde superior
    for i in range(samples_per_side):
        x = int(w * i / samples_per_side)
        edge_pixels.append(img_rgb.getpixel((x, 0)))
    # Borde inferior
    for i in range(samples_per_side):
        x = int(w * i / samples_per_side)
        edge_pixels.append(img_rgb.getpixel((x, h - 1)))
    # Borde izquierdo
    for i in range(samples_per_side):
        y = int(h * i / samples_per_side)
        edge_pixels.append(img_rgb.getpixel((0, y)))
    # Borde derecho
    for i in range(samples_per_side):
        y = int(h * i / samples_per_side)
        edge_pixels.append(img_rgb.getpixel((w - 1, y)))

    # Calcular std dev por canal
    n = len(edge_pixels)
    mean_r = sum(p[0] for p in edge_pixels) / n
    mean_g = sum(p[1] for p in edge_pixels) / n
    mean_b = sum(p[2] for p in edge_pixels) / n

    var_r = sum((p[0] - mean_r) ** 2 for p in edge_pixels) / n
    var_g = sum((p[1] - mean_g) ** 2 for p in edge_pixels) / n
    var_b = sum((p[2] - mean_b) ** 2 for p in edge_pixels) / n

    std_r = var_r ** 0.5
    std_g = var_g ** 0.5
    std_b = var_b ** 0.5

    mean_std = (std_r + std_g + std_b) / 3
    print(f"[DETECT] Edge std dev: R={std_r:.1f} G={std_g:.1f} B={std_b:.1f} | mean={mean_std:.1f}")

    # 3. Si bordes uniformes -> EXTEND
    UNIFORM_THRESHOLD = 20
    if mean_std < UNIFORM_THRESHOLD:
        print(f"[DETECT] Bordes uniformes (std<{UNIFORM_THRESHOLD}) -> EXTEND")
        return "extend"

    # 4. Verificar relacion de aspecto vs 16:9
    target_ratio = canvas_w / canvas_h  # ~1.778
    img_ratio = w / h
    ratio_diff = abs(img_ratio - target_ratio) / target_ratio

    ASPECT_TOLERANCE = 0.10  # 10%
    if ratio_diff <= ASPECT_TOLERANCE:
        print(f"[DETECT] Aspecto cercano a 16:9 (diff={ratio_diff:.1%}) + bordes variados -> FULL")
        return "full"

    print(f"[DETECT] Default seguro -> EXTEND")
    return "extend"


def mode_full(img, canvas_w, canvas_h, sharpen=0, multistep=False):
    """Modo FULL: upscale la imagen a 4K con cover-crop centrado.
    Mantiene la maxima calidad posible con LANCZOS.

    Args:
        sharpen: 0-100 nivel de enfoque post-escalado (0=off)
        multistep: si True, usa upscale progresivo (max 2x por paso)
    """
    w, h = img.size

    # Cover: escala para que el menor lado llene el canvas
    scale = max(canvas_w / w, canvas_h / h)
    new_w = int(w * scale)
    new_h = int(h * scale)

    # Escalar (multi-step si el factor es grande)
    if multistep and scale > 2.0:
        img_scaled = multi_step_upscale(img, new_w, new_h)
    else:
        img_scaled = img.resize((new_w, new_h), Image.LANCZOS)

    # Recorte centrado
    x = (new_w - canvas_w) // 2
    y = (new_h - canvas_h) // 2
    img_cropped = img_scaled.crop((x, y, x + canvas_w, y + canvas_h))

    # Post-sharpen
    if sharpen > 0:
        img_cropped = enhance_quality(img_cropped, sharpen)

    print(f"[FULL] Escalado: {w}x{h} -> {new_w}x{new_h}, recorte centrado a {canvas_w}x{canvas_h}")
    return img_cropped


# -- Feather (transicion suave) ---------------------------------------------

def apply_feather(bg, fg, fg_rect, feather_px):
    """Transicion suave entre foreground y background."""
    x1, y1, x2, y2 = fg_rect
    fw = x2 - x1
    fh = y2 - y1

    mask = Image.new('L', (fw, fh), 255)
    mask_draw = ImageDraw.Draw(mask)

    inner_margin = feather_px
    inner_x1 = inner_margin
    inner_y1 = inner_margin
    inner_x2 = fw - inner_margin
    inner_y2 = fh - inner_margin

    mask_draw.rectangle([(inner_x1, inner_y1), (inner_x2, inner_y2)], fill=255)

    for i in range(feather_px):
        alpha = int(255 * (i / feather_px))
        mask_draw.rectangle([(i, i), (fw - 1 - i, i)], fill=alpha)
        mask_draw.rectangle([(i, fh - 1 - i), (fw - 1 - i, fh - 1 - i)], fill=alpha)
        mask_draw.rectangle([(i, i), (i, fh - 1 - i)], fill=alpha)
        mask_draw.rectangle([(fw - 1 - i, i), (fw - 1 - i, fh - 1 - i)], fill=alpha)

    mask = mask.filter(ImageFilter.GaussianBlur(radius=feather_px // 2))
    bg.paste(fg, (x1, y1), mask)
    return bg


# -- Procesamiento principal -------------------------------------------------

def extend_to_wallpaper(
    input_path,
    output_path=None,
    method="blur",
    canvas_w=DEFAULT_CANVAS_W,
    canvas_h=DEFAULT_CANVAS_H,
    blur_radius=DEFAULT_BLUR_RADIUS,
    feather_px=0,
    quality=DEFAULT_QUALITY,
    no_center=False,
    offset_x=0,
    offset_y=0,
    scale=None,
    mode="auto",
    force_method=None,
    sharpen=None,
    multistep=False,
    denoise=0,
):
    """Pipeline principal:
    - auto: detecta si es EXTEND (background) o FULL (full-frame)
    - extend: comportamiento clasico (escalar + extender fondo)
    - full: upscale directo con cover-crop
    """
    # 1. Abrir imagen
    if not os.path.isfile(input_path):
        raise FileNotFoundError(f"No se encuentra: {input_path}")

    img_original = Image.open(input_path)

    # 2. Determinar modo
    if mode == "auto":
        mode = detect_mode(img_original, canvas_w, canvas_h)

    print(f"[MODE] {mode.upper()}")
    print(f"[DIM] Canvas: {canvas_w}x{canvas_h}")

    # Auto-detect quality enhancement from scale factor
    if sharpen is None:
        if mode == 'full':
            sf = max(canvas_w / img_original.width, canvas_h / img_original.height)
        else:
            sf = min(canvas_w / img_original.width, canvas_h / img_original.height)

        # Scale warning for extreme upscales
        if sf > 3.0:
            print(f"[WARN] Scale {sf:.1f}x from {img_original.width}x{img_original.height}. "
                  f"Quality is limited by source resolution. "
                  f"Optimal results require source >= 1920x1080.")

        if sf > 5.0:
            sharpen = 12
            multistep = True
            print(f"[ENHANCE] Factor {sf:.1f}x > 5x -> auto: sharpen={sharpen}, multistep=ON")
        elif sf > 3.0:
            sharpen = 20
            print(f"[ENHANCE] Factor {sf:.1f}x > 3x -> auto: sharpen={sharpen}")
        elif sf > 1.5:
            sharpen = 30
            print(f"[ENHANCE] Factor {sf:.1f}x > 1.5x -> auto: sharpen={sharpen}")
        else:
            sharpen = 0

        # Auto-detect denoise for extreme upscales
        if denoise == 0 and sf > 4.0:
            denoise = 1
    elif sharpen > 0 or multistep:
        print(f"[ENHANCE] sharpen={sharpen}, multistep={multistep}")

    # 3. Ejecutar segun modo
    if mode == "full":
        # Convertir a RGB si necesario
        if img_original.mode not in ('RGB', 'RGBA'):
            img_rgb = img_original.convert('RGB')
        else:
            img_rgb = img_original.copy()

        # Pre-denoise before upscale
        if denoise > 0:
            img_rgb = img_rgb.filter(ImageFilter.MedianFilter(size=denoise*2+1))
            print(f"[DENOISE] Pre-denoise applied (radius={denoise})")

        result = mode_full(img_rgb, canvas_w, canvas_h, sharpen=sharpen, multistep=multistep)

        if output_path is None:
            ensure_dir(DEFAULT_OUTPUT_DIR)
            slug = slug_from_path(input_path)
            output_path = DEFAULT_OUTPUT_DIR / f"wallpaper-full-{slug}-{timestamp()}.jpg"

    else:  # mode == "extend"
        # Convertir a RGB si es necesario
        if img_original.mode == 'RGBA':
            img_rgb = Image.new('RGB', img_original.size, (0, 0, 0))
            img_rgb.paste(img_original, mask=img_original.split()[3])
        elif img_original.mode != 'RGB':
            img_rgb = img_original.convert('RGB')
        else:
            img_rgb = img_original.copy()

        # Pre-denoise before upscale
        if denoise > 0:
            img_rgb = img_rgb.filter(ImageFilter.MedianFilter(size=denoise*2+1))
            print(f"[DENOISE] Pre-denoise applied (radius={denoise})")

        # Usar force_method si se especifico (via --method)
        actual_method = force_method or method

        # Calcular rectangulo del foreground
        fg_x1, fg_y1, fg_x2, fg_y2, fg_w, fg_h = compute_fit_rect(
            img_rgb.width, img_rgb.height,
            canvas_w, canvas_h,
            scale=scale, no_center=no_center,
            offset_x=offset_x, offset_y=offset_y
        )

        # Escalar foreground (multi-step si >2x)
        fg_scale_factor = max(fg_w / img_rgb.width, fg_h / img_rgb.height)
        if multistep and fg_scale_factor > 2.0:
            fg_scaled = multi_step_upscale(img_rgb, fg_w, fg_h)
        else:
            fg_scaled = img_rgb.resize((fg_w, fg_h), Image.LANCZOS)

        # Post-sharpen foreground (solo el sujeto, no el fondo)
        if sharpen > 0:
            fg_scaled = enhance_quality(fg_scaled, sharpen)

        print(f"[IMG] Foreground: {fg_w}x{fg_h} en ({fg_x1}, {fg_y1})")
        print(f"[METHOD] {actual_method}")

        # Generar fondo
        if actual_method == "blur":
            bg = method_blur(img_rgb, canvas_w, canvas_h, blur_radius)
        elif actual_method == "edge":
            bg = method_edge(img_rgb, canvas_w, canvas_h)
        elif actual_method == "solid":
            bg = method_solid(img_rgb, canvas_w, canvas_h)
        elif actual_method == "grad":
            bg = method_grad(img_rgb, canvas_w, canvas_h)
        else:
            raise ValueError(f"Metodo invalido: {actual_method}. Validos: {', '.join(VALID_METHODS)}")

        # Componer
        result = bg.copy()
        result.paste(fg_scaled, (fg_x1, fg_y1))

        # Feather opcional
        if feather_px > 0:
            print(f"[FEATHER] {feather_px}px")
            result = apply_feather(result, fg_scaled, (fg_x1, fg_y1, fg_x2, fg_y2), feather_px)

        if output_path is None:
            ensure_dir(DEFAULT_OUTPUT_DIR)
            slug = slug_from_path(input_path)
            output_path = DEFAULT_OUTPUT_DIR / f"wallpaper-{actual_method}-{slug}-{timestamp()}.jpg"

    # 4. Guardar
    ext = Path(output_path).suffix.lower()
    save_kwargs = {}
    if ext in ('.jpg', '.jpeg'):
        save_kwargs['quality'] = quality
        save_kwargs['subsampling'] = 0
    elif ext == '.png':
        save_kwargs['compress_level'] = 3

    result.save(output_path, **save_kwargs)
    print(f"[OK] Guardado: {output_path}")
    print(f"     Dimensions: {result.width}x{result.height}")

    return str(output_path)


# -- CLI --------------------------------------------------------------------

def parse_canvas(val):
    parts = val.lower().split('x')
    if len(parts) != 2:
        raise ValueError(f"Formato invalido para canvas: {val}. Usa WxH (ej: 3840x2160)")
    return int(parts[0]), int(parts[1])


def parse_offset(val):
    parts = val.split(',')
    if len(parts) != 2:
        raise ValueError(f"Formato invalido para offset: {val}. Usa X,Y (ej: 100,50)")
    return int(parts[0]), int(parts[1])


def main():
    parser = argparse.ArgumentParser(
        description="Convierte imagenes en wallpaper 4K alargando solo los fondos",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Ejemplos:
  %(prog)s foto.jpg
  %(prog)s ilustracion.png --method edge
  %(prog)s paisaje.jpg --method blur --blur 80 --feather 30
  %(prog)s logo.png --method solid -o wallpaper-personalizado.jpg
  %(prog)s retrato.jpg --canvas 2560x1440 --method grad
  %(prog)s panoramica.jpg --scale 1.5 --offset 0,-100"""
    )
    parser.add_argument("input_path", nargs="?", help="Ruta a la imagen a convertir")
    parser.add_argument("-o", "--output", help="Ruta de salida (default: subcarpeta wallpapers/)")
    parser.add_argument("-m", "--method", choices=VALID_METHODS, default="blur",
                        help="Metodo de extension de fondo (default: blur)")
    parser.add_argument("-b", "--blur", type=int, default=DEFAULT_BLUR_RADIUS,
                        help=f"Radio del blur para metodo 'blur' (default: {DEFAULT_BLUR_RADIUS})")
    parser.add_argument("-f", "--feather", type=int, default=0,
                        help=" Pixeles de transicion suave en la costura (default: 0)")
    parser.add_argument("-q", "--quality", type=int, default=DEFAULT_QUALITY,
                        help=f"Calidad JPEG 1-100 (default: {DEFAULT_QUALITY})")
    parser.add_argument("--canvas", default=f"{DEFAULT_CANVAS_W}x{DEFAULT_CANVAS_H}",
                        help=f"Dimensiones del canvas WxH (default: {DEFAULT_CANVAS_W}x{DEFAULT_CANVAS_H})")
    parser.add_argument("--mode", choices=VALID_MODES, default="auto",
                        help="Modo de procesamiento: auto (detecta), extend (fondo), full (upscale directo) (default: auto)")
    parser.add_argument("--no-center", action="store_true",
                        help="No centrar la imagen (esquina superior izquierda)")
    parser.add_argument("--offset", default=None,
                        help="Desplazamiento X,Y desde el centro (ej: 100,-50)")
    parser.add_argument("--scale", type=float, default=None,
                        help="Escala forzada (ej: 1.5 para 150%%)")
    parser.add_argument("--sharpen", type=int, default=None, metavar="0-100",
                        help="Nivel de enfoque post-escalado 0-100 (default: auto segun factor de escala)")
    parser.add_argument("--multistep", action="store_true",
                        help="Upscale progresivo (max 2x por paso) para mejor calidad en escalados >2x")
    parser.add_argument("--denoise", type=int, default=0, metavar="0-5",
                        help="Radio de MedianFilter pre-upscale (0-5). Auto-activado si la fuente es muy pequena.")
    parser.add_argument("--list-methods", action="store_true",
                        help="Listar metodos disponibles y salir")

    args = parser.parse_args()

    if args.list_methods or not args.input_path:
        print("Metodos disponibles para --method:")
        print("  blur   -> Estira la imagen a 4K + Gaussian blur (recomendado)")
        print("  edge   -> Refleja los bordes hacia afuera")
        print("  solid  -> Color solido promedio de los bordes")
        print("  grad   -> Degradado desde los bordes hacia afuera")
        return

    canvas_w, canvas_h = parse_canvas(args.canvas)
    offset = parse_offset(args.offset) if args.offset else (0, 0)

    try:
        extend_to_wallpaper(
            input_path=args.input_path,
            output_path=args.output,
            method=args.method,
            canvas_w=canvas_w,
            canvas_h=canvas_h,
            blur_radius=args.blur,
            feather_px=args.feather,
            quality=args.quality,
            no_center=args.no_center,
            offset_x=offset[0],
            offset_y=offset[1],
            scale=args.scale,
            mode=args.mode,
            force_method=args.method,
            sharpen=args.sharpen,
            multistep=args.multistep,
            denoise=args.denoise,
        )
    except FileNotFoundError as e:
        print(f"[ERR] {e}")
        print(f"   La ruta existe? Verifica: {os.path.abspath(args.input_path)}")
        sys.exit(1)
    except ValueError as e:
        print(f"[ERR] {e}")
        sys.exit(1)
    except Exception as e:
        print(f"[ERR] Inesperado: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
