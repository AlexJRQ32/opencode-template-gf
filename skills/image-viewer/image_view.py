"""image_view.py — Analyze + audit images for quality issues.
Usage: python image_view.py <path> [--audit]
"""
import sys, os, json
from PIL import Image

def dominant_colors(img, n=6, skip_bg=True):
    w, h = img.size
    step = max(1, min(w, h) // 50)
    freq = {}
    for y in range(0, h, step):
        for x in range(0, w, step):
            r, g_, b = img.getpixel((x, y))[:3]
            key = ((r // 16) * 16, (g_ // 16) * 16, (b // 16) * 16)
            hex_c = "#{:02X}{:02X}{:02X}".format(*key)
            freq[hex_c] = freq.get(hex_c, 0) + 1
    sorted_c = sorted(freq.items(), key=lambda kv: -kv[1])
    bg_color = sorted_c[0][0] if skip_bg else None
    top = [(c, cnt) for c, cnt in sorted_c if c != bg_color][:n]
    total_excl = sum(cnt for c, cnt in sorted_c if c != bg_color) if skip_bg else sum(freq.values())
    if total_excl == 0:
        top = sorted_c[:n]
        total_excl = sum(freq.values())
    return [(c, round(cnt / total_excl * 100)) for c, cnt in top]

def _get_pixels_1d(img):
    if hasattr(img, "get_flattened_data"):
        return list(img.get_flattened_data())
    return list(img.getdata())

def avg_brightness(img):
    g = img.convert("L")
    pixels = _get_pixels_1d(g)
    return round(sum(pixels) / len(pixels), 1)

def brightness_range(img):
    g = img.convert("L")
    pixels = _get_pixels_1d(g)
    mn, mx = min(pixels), max(pixels)
    return {"min": mn, "max": mx, "range": mx - mn}

def sample_regions(img):
    w, h = img.size
    bg = img.getpixel((0, 0))[:3] if w > 0 and h > 0 else (0, 0, 0)
    pts = {
        "top": (w // 2, h // 8),
        "center": (w // 2, h // 2),
        "bottom": (w // 2, 7 * h // 8),
        "left": (w // 8, h // 2),
        "right": (7 * w // 8, h // 2),
    }
    result = {}
    for name, (x, y) in pts.items():
        px = img.getpixel((x, y))[:3]
        result[name] = "#{:02X}{:02X}{:02X}".format(*px)
        result[name + "_diff_bg"] = abs(px[0] - bg[0]) + abs(px[1] - bg[1]) + abs(px[2] - bg[2])
    return result

def detect_text_regions(img):
    g = img.convert("L")
    w, h = g.size
    if w == 0 or h == 0:
        return "Imagen vacía"
    step = max(1, h // 200)
    sx = max(0, w // 4)
    ex = min(w, 3 * w // 4)
    text_rows = 0
    for y in range(0, h, step):
        contrast_pairs = 0
        for x in range(sx + 4, ex - 4, 2):
            c = g.getpixel((x, y))
            l = g.getpixel((x - 4, y))
            r = g.getpixel((x + 4, y))
            if abs(c - l) > 60 or abs(c - r) > 60:
                contrast_pairs += 1
        if contrast_pairs > max(5, (ex - sx) // 50):
            text_rows += 1
    ratio = text_rows / (h / step) if step else 0
    if ratio > 0.05:
        return "Probable texto presente ({:.0f}% del alto)".format(ratio * 100)
    return "No se detectaron regiones de texto significativas"

def find_content_bounds(img, bg_tolerance=30):
    w, h = img.size
    bg = img.getpixel((0, 0))[:3]
    step = 4
    y_start, y_end = h, 0
    x_start, x_end = w, 0
    for y in range(0, h, step):
        for x in range(0, w, step):
            px = img.getpixel((x, y))[:3]
            d = abs(px[0] - bg[0]) + abs(px[1] - bg[1]) + abs(px[2] - bg[2])
            if d > bg_tolerance:
                y_start = min(y_start, y)
                y_end = max(y_end, y)
                x_start = min(x_start, x)
                x_end = max(x_end, x)
    if y_end < y_start:
        return None
    return {"x": x_start, "y": y_start, "w": x_end - x_start, "h": y_end - y_start}

def check_invisible_elements(img):
    """Count rows with zero contrast (potential invisible elements)."""
    g = img.convert("L")
    w, h = g.size
    step = max(1, h // 80)
    sx, ex = w // 4, 3 * w // 4
    dead_rows = 0
    total_rows = 0
    for y in range(0, h, step):
        has_contrast = False
        for x in range(sx, ex, 4):
            c = g.getpixel((x, y))
            l = g.getpixel((max(x - 8, 0), y))
            r = g.getpixel((min(x + 8, w - 1), y))
            if abs(c - l) > 15 or abs(c - r) > 15:
                has_contrast = True
                break
        if not has_contrast:
            dead_rows += 1
        total_rows += 1
    return {"dead_row_pct": round(dead_rows / total_rows * 100, 1)}

def audit(img):
    """Return a list of quality issues found."""
    w, h = img.size
    issues = []
    avg = avg_brightness(img)
    br = brightness_range(img)
    text_ratio = detect_text_regions(img)
    content = find_content_bounds(img)
    colors = dominant_colors(img, n=8, skip_bg=True)

    if "No se detectaron" in text_ratio:
        issues.append({"severity": "high", "type": "text_invisible",
                       "detail": "No se detecta texto — posible texto invisible o contraste insuficiente"})

    if avg < 20:
        issues.append({"severity": "medium", "type": "too_dark",
                       "detail": "Brillo promedio muy bajo ({:.1f}/255)".format(avg)})

    if br["range"] < 100:
        issues.append({"severity": "high", "type": "low_contrast",
                       "detail": "Rango de contraste bajo ({})".format(br["range"])})

    if content and content["w"] < w * 0.2:
        issues.append({"severity": "low", "type": "content_small",
                       "detail": "Contenido ocupa solo {:.0f}% del ancho".format(content["w"]/w*100)})

    if content and content["h"] < h * 0.2:
        issues.append({"severity": "low", "type": "content_small",
                       "detail": "Contenido ocupa solo {:.0f}% del alto".format(content["h"]/h*100)})

    low_contrast_colors = [(c, p) for c, p in colors if p < 1]
    if low_contrast_colors:
        faint = [c for c, p in colors if p < 2]
        if len(faint) >= 3:
            issues.append({"severity": "low", "type": "faint_colors",
                           "detail": "{} colores con poca presencia (<2%) — pueden ser elementos apenas visibles".format(len(faint))})

    dead = check_invisible_elements(img)
    if dead["dead_row_pct"] > 80:
        issues.append({"severity": "medium", "type": "many_dead_rows",
                       "detail": "{:.0f}% del alto sin contraste — posible fondo vacío dominante".format(dead["dead_row_pct"])})

    return issues

def analyze(path):
    if not os.path.exists(path):
        return {"error": "File not found: " + path}
    try:
        img = Image.open(path)
    except Exception as e:
        return {"error": str(e)}

    info = {
        "file": os.path.basename(path),
        "dir": os.path.dirname(path),
        "size_kb": round(os.path.getsize(path) / 1024, 1),
        "dims": "{}x{}".format(img.width, img.height),
        "format": img.format,
        "mode": img.mode,
        "brightness": avg_brightness(img),
        "brightness_range": brightness_range(img),
        "content_bounds": find_content_bounds(img),
        "colors_excl_bg": dominant_colors(img, n=6, skip_bg=True),
        "regions": sample_regions(img),
        "text_detection": detect_text_regions(img),
    }
    if "--audit" in sys.argv:
        info["audit"] = audit(img)
    return info

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: image_view.py <path> [--audit]"}))
        sys.exit(1)
    result = analyze(sys.argv[1])
    print(json.dumps(result, indent=2))
