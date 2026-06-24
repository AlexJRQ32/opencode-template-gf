from PIL import Image, ImageDraw, ImageFont
import os, math

W, H = 3840, 2160
img = Image.new('RGB', (W, H), color=(0x10, 0x14, 0x1A))
draw = ImageDraw.Draw(img)

BG = (0x10, 0x14, 0x1A)
CARD = (0x25, 0x2B, 0x36)
ACCENT = (0x4A, 0x8C, 0xC7)
ACCENT_DIM = (0x36, 0x6E, 0x9A)
WHITE = (240, 242, 245)
GRAY = (0x8A, 0x92, 0x9E)
TAG_BG = (0x2D, 0x34, 0x40)
BORDER = (0x34, 0x3D, 0x4C)
SHADOW = (0x08, 0x0A, 0x0E)

def load_font(name, size):
    path = f"C:/Windows/Fonts/{name}"
    if os.path.exists(path):
        return ImageFont.truetype(path, size)
    return ImageFont.load_default()

f_title = load_font("segoeuib.ttf", 100)
f_step = load_font("segoeuib.ttf", 60)
f_desc = load_font("segoeui.ttf", 34)
f_small = load_font("segoeui.ttf", 28)
f_label = load_font("segoeuib.ttf", 36)
f_num = load_font("segoeuib.ttf", 48)

def ctext(draw, text, font, x, y, color=WHITE):
    draw.text((x, y), text, font=font, fill=color, anchor="mm")

def draw_arrow(draw, x1, y1, x2, y2, color, width=4, head_size=18):
    mid_x = (x1 + x2) // 2
    draw.line([(x1, y1), (mid_x, y2)], fill=color, width=width)
    angle = 0.5
    pts = [(x2, y2),
           (x2 - head_size * math.cos(angle), y2 - head_size * math.sin(angle)),
           (x2 - head_size * math.cos(angle), y2 + head_size * math.sin(angle))]
    draw.polygon(pts, fill=color)

# Title
ctext(draw, "Pipeline de Datos", f_title, W//2, 120, WHITE)
draw.rounded_rectangle([(W//2 - 340, 202), (W//2 + 340, 206)], radius=2, fill=ACCENT_DIM)
draw.rounded_rectangle([(W//2 - 280, 212), (W//2 + 280, 214)], radius=2, fill=ACCENT)

B, G, BH = 720, 180, 440
TW = 3*B + 2*G
SX = (W - TW)//2
CY = H//2 - 30

labels = ["INGESTA", "TRANSFORMACIÓN", "VISUALIZACIÓN"]
titles = ["Datos Crudos", "Procesamiento", "Reporte"]
descs = [
    "Fuentes: CSV  ·  APIs  ·  SQL",
    "Limpieza  ·  Validación  ·  Transformación",
    "Dashboards  ·  PDFs  ·  Alertas",
]
tags_arr = [["CSV","API","SQL"], ["LIMPIEZA","VALIDA","TRANSFOR"], ["DASHBOARD","PDF","ALERTAS"]]

for i in range(3):
    x1 = SX + i*(B + G)
    y1 = CY
    x2 = x1 + B
    y2 = y1 + BH

    for s in range(6, 0, -1):
        draw.rounded_rectangle(
            [(x1+6-s, y1+10-s), (x2+6+s, y2+10+s)],
            radius=28, fill=SHADOW)

    draw.rounded_rectangle([(x1, y1), (x2, y2)], radius=20, fill=CARD, outline=BORDER, width=1)

    cx, cyc = x1 + 55, y1 + 48
    r = 26
    draw.ellipse([(cx-r-2, cyc-r-2), (cx+r+2, cyc+r+2)], fill=ACCENT_DIM)
    draw.ellipse([(cx-r, cyc-r), (cx+r, cyc+r)], fill=ACCENT)
    ctext(draw, str(i+1), f_num, cx, cyc, WHITE)

    ctext(draw, labels[i], f_label, x1 + B//2, y1 + 95, ACCENT)

    ctext(draw, titles[i], f_step, x1 + B//2, y1 + 155, WHITE)

    draw.rounded_rectangle([(x1 + 55, y1 + 205), (x2 - 55, y1 + 207)], radius=1, fill=TAG_BG)

    ctext(draw, descs[i], f_desc, x1 + B//2, y1 + 258, GRAY)

    tags = tags_arr[i]
    tw, tg = 185, 14
    ttw = 3*tw + 2*tg
    tsx = x1 + (B - ttw)//2
    ty = y1 + 330
    for j, tag in enumerate(tags):
        tx = tsx + j*(tw + tg)
        draw.rounded_rectangle([(tx, ty), (tx+tw, ty+30)], radius=5, fill=TAG_BG)
        ctext(draw, tag, f_small, tx+tw//2, ty+15, (0xAA, 0xCC, 0xEE))

    if i < 2:
        ax1 = x2 + 8
        ay = CY + BH//2
        ax2 = x1 + B + G - 8
        draw.line([(ax1, ay), (ax2-18, ay)], fill=TAG_BG, width=4)
        al = 18
        angle = 0.5
        pts = [(ax2, ay),
               (ax2 - al*math.cos(angle), ay - al*math.sin(angle)),
               (ax2 - al*math.cos(angle), ay + al*math.sin(angle))]
        draw.polygon(pts, fill=ACCENT_DIM)

ctext(draw, "Extremo a extremo  ·  Automatizado  ·  Escalable",
      f_small, W//2, CY + BH + 100, GRAY)
draw.rounded_rectangle([(W//2 - 180, CY + BH + 145), (W//2 + 180, CY + BH + 147)],
                        radius=1, fill=ACCENT_DIM)

out_dir = os.path.expanduser("~/OneDrive/Documentos/Archivos OpenCode/Imágenes/diagrams")
os.makedirs(out_dir, exist_ok=True)
out_path = os.path.join(out_dir, "pipeline-datos-3-pasos.png")
img.save(out_path)
print(f"OK: {out_path}")
