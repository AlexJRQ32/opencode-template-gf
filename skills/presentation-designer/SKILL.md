---
name: presentation-designer
description: Crea presentaciones profesionales (PPTX, PDF, slides) con narrativa, diseño visual y estructura por diapositiva. Cubre python-pptx, guion por slide, transiciones, y exportación. Úsala cuando el usuario pida "crea una presentación", "haz slides", "powerpoint", "diapositivas", "elevator pitch", o "presentación".
---

# Presentation Designer

Skill para crear presentaciones profesionales. Combina narrativa, diseño visual y generación programática.

## Flujo de trabajo

### 1. Entender el contexto
Antes de escribir código:
- **Audiencia**: ¿quién ve esto? (directivos, clientes, academia, público general)
- **Propósito**: ¿informar, persuadir, vender, enseñar?
- **Formato**: PPTX, PDF, Google Slides, markdown slides
- **Duración**: ¿cuántos minutos? → calcular número de diapositivas (~1 min por diapo)

### 2. Estructurar la narrativa
Toda presentación necesita un arco narrativo:

| Fase | % del tiempo | Qué hacer |
|------|-------------|-----------|
| **Gancho** | 10% | Problema/pregunta que engancha |
| **Contexto** | 20% | Marco, datos, antecedentes |
| **Conflicto** | 25% | El reto, la dificultad, el "pero" |
| **Solución** | 30% | Propuesta, cómo se resuelve |
| **Cierre** | 15% | Conclusión, llamado a la acción |

### 3. Diseñar cada diapositiva
Reglas por diapositiva:
- **1 idea por slide** — si hay dos ideas, son dos slides
- **Texto mínimo** — el público lee o escucha, no ambos
- **La diapo apoya al orador**, no al revés
- **Contraste** — título grande, cuerpo pequeño. Una cosa domina visualmente

### 4. Crear el guion por slide
Cada diapositiva debe tener:
- **Qué se ve** (contenido visual)
- **Qué se dice** (texto del orador)
- **Cuándo avanzar** (transición)

Formato recomendado en el documento:
```
### Diapositiva N — Título
🎬 Qué se ve: [descripción visual]
🎙 Qué se dice: "[texto del guion]"
⏭ Avanzar cuando: [condición para pasar a la siguiente]
```

### 5. Generar el PPTX con python-pptx

```python
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

prs = Presentation()
prs.slide_width = Inches(13.333)  # 16:9 widescreen
prs.slide_height = Inches(7.5)

# Slide layout: blank (6) for full control
blank_layout = prs.slide_layouts[6]

slide = prs.slides.add_slide(blank_layout)

# Fondo personalizado
background = slide.background
fill = background.fill
fill.solid()
fill.fore_color.rgb = RGBColor(0x0D, 0x11, 0x17)

# Texto
txBox = slide.shapes.add_textbox(Inches(1), Inches(2), Inches(10), Inches(3))
tf = txBox.text_frame
p = tf.paragraphs[0]
p.text = "Título de la diapositiva"
p.font.size = Pt(44)
p.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
p.font.bold = True
p.alignment = PP_ALIGN.LEFT
```

### 6. Exportar a PDF
```python
from pptx import Presentation
import comtypes.client  # Windows only, requires PowerPoint installed

def pptx_to_pdf(pptx_path, pdf_path):
    powerpoint = comtypes.client.CreateObject("PowerPoint.Application")
    powerpoint.Visible = 1
    deck = powerpoint.Presentations.Open(pptx_path)
    deck.SaveAs(pdf_path, 32)  # 32 = ppSaveAsPDF
    deck.Close()
    powerpoint.Quit()
```

Alternativa sin PowerPoint: convertir con `fitz` (PyMuPDF) renderizando cada slide como imagen.

## Estilos de presentación

| Estilo | Cuándo usarlo | Paleta | Tipografía |
|--------|--------------|--------|------------|
| **Corporativo** | Clientes, juntas directivas | Azul marino + blanco + acento | Sans-serif (Calibri, Inter) |
| **Académico** | Conferencias, defensas | Blanco + texto oscuro + acento sutil | Serif (Garamond, Noto) |
| **Moderno oscuro** | Producto, tech, startups | Fondo oscuro (#0d1117) + acentos vivos | Sans-serif bold headlines |
| **Creativo** | Portafolio, diseño | Fondos con gradiente, tipografía expresiva | Display + sans-serif |
| **Mínimo** | Pitch decks, ejecutivo | Blanco + mucho espacio negativo | Una sola familia tipográfica |

## Reglas de diseño visual

- **Contraste suficiente**: texto sobre fondo → ratio 4.5:1 mínimo (WCAG AA)
- **Una paleta de 3 colores**: primario + secundario + acento. No más.
- **Máximo 2 tipografías**: una para títulos, otra para cuerpo
- **Regla de los tercios**: no centrar todo. Usar asimetría intencional
- **Imágenes > texto**: una imagen bien elegida reemplaza 100 palabras
- **Animaciones con propósito**: entrar/ salir para guiar la atención, no por decoración

## Herramientas disponibles

- **python-pptx**: generación programática de PowerPoint
- **python-docx**: scripts/guiones en Word
- **PyMuPDF (fitz)**: manipulación de PDFs, extracción de slides
- **Pillow**: procesamiento de imágenes para slides
- **VSCode + Markdown**: slides rápidos con Marp (`.md` → PDF/PPTX)
