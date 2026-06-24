---
name: undetectable-apa7
description: Genera documentos .docx en formato APA 7ª edición indetectables por GPTZero, Turnitin, Originality.ai, Copyleaks, ZeroGPT, QuillBot, Grammarly y Sapling. Extiende apa7-docx con técnicas de humanización, anti-plagio y citación automática desde fuentes web reales.
---

# undetectable-apa7 — Documentos APA 7 Indetectables

**Extiende el skill `apa7-docx`** añadiendo una capa de **humanización lingüística** que hace que el texto generado sea indistinguible de la escritura humana ante detectores de IA, **más** un sistema de **anti-plagio** basado en síntesis multi-fuente y citas verificadas.

---

## 1. Prerrequisitos

1. **`apa7-docx`** skill instalado en `~/.agents/skills/apa7-docx/`
2. **`fuentes-confiables`** skill instalado (para verificación de fuentes)
3. Python ≥ 3.10 con `python-docx` instalado:
   ```bash
   pip install python-docx
   ```

---

## 2. Metodología de 3 Pilares

### Pilar 1: Anti-Detección por IA

El motor de humanización ataca las **seis señales** que miden los detectores GPTZero, Turnitin, Originality.ai, Copyleaks, ZeroGPT, QuillBot, Grammarly y Sapling:

| Señal | Qué mide | Cómo la atacamos |
|-------|----------|------------------|
| **Perplexity** | Qué tan predecible es la elección de palabras | Rotación de vocabulario, sinónimos inesperados, términos de dominio específico |
| **Burstiness** | Variación en longitud y estructura de oraciones | Mezcla deliberada de oraciones cortas (8-12), medias (15-22) y largas (28-40+) |
| **Repetitividad** | Uniformidad de patrones sintácticos | Variación de aperturas de oración, alternancia de complejidad sintáctica |
| **N-gram Repetition** | Densidad de n-gramas idénticos o casi idénticos | Ruptura activa con ventana deslizante de 120 palabras |
| **Function Word Variance** | Variación en uso de artículos, preposiciones, conectores | Rotación de function words, reemplazo de frases preposicionales |
| **Syntactic Structure Consistency** | Uniformidad en estructura sintáctica de oraciones | 8 plantillas de variación sintáctica forzada |

### Pilar 2: Anti-Plagio (0% Copia)

| Regla | Descripción |
|-------|-------------|
| **Síntesis multi-fuente** | Cada párrafo combina ideas de ≥3 fuentes diferentes |
| **Paráfrasis estructural** | Reestructurar, no solo reemplazar sinónimos — cambiar orden de ideas, voz activa/pasiva, énfasis |
| **Atribución constante** | Cada afirmación factual tiene una cita APA 7 a una fuente real y verificable |
| **No recycling** | Nunca reusar la misma frase o estructura de un párrafo a otro |

### Pilar 3: Citas APA 7 desde Web

| Regla | Descripción |
|-------|-------------|
| **URLs reales** | Toda referencia debe tener una URL válida obtenida de búsqueda real |
| **Formato APA 7 estricto** | Usar los helpers de `apa7.py` para formato correcto |
| **Jerarquía de fuentes** | Oficiales > Google Scholar > arXiv > repositorios verificados (según `fuentes-confiables`) |
| **Fecha de acceso** | Incluir fecha de recuperación para fuentes web |

---

## 3. Flujo de Trabajo

```
┌─────────────────────────────────────────────────┐
│ 1. USUARIO solicita documento                   │
│    (tema, tipo, extensión, # fuentes)           │
└──────────────────┬──────────────────────────────┘
                   ▼
┌─────────────────────────────────────────────────┐
│ 2. INVESTIGAR fuentes confiables                 │
│    (Google Scholar, arXiv, repos oficiales)      │
│    Mínimo 5-10 fuentes por documento             │
└──────────────────┬──────────────────────────────┘
                   ▼
┌─────────────────────────────────────────────────┐
│ 3. REDACTAR con Humanizer                        │
│    Por cada párrafo:                             │
│    a) Sintetizar 3+ fuentes                     │
│    b) Aplicar humanize(texto, estilo, URLs)     │
│    c) Verificar burstiness y perplexity         │
│    d) Ajustar si score < 70                     │
└──────────────────┬──────────────────────────────┘
                   ▼
┌─────────────────────────────────────────────────┐
│ 4. ENSAMBLAR documento APA 7                    │
│    (portada → TOC → resumen → cuerpo → refs)    │
└──────────────────┬──────────────────────────────┘
                   ▼
┌─────────────────────────────────────────────────┐
│ 5. VERIFICACIÓN FINAL                            │
│    a) check_detectability() → score global      │
│    b) Verificar que todas las citas tienen URL  │
│    c) Verificar que no hay AI-trigger words     │
│    d) Si score < 70, re-humanizar secciones     │
└──────────────────┬──────────────────────────────┘
                   ▼
┌─────────────────────────────────────────────────┐
│ 6. GUARDAR .docx                                │
│    Output: Archivos OpenCode/Documentos/         │
└─────────────────────────────────────────────────┘
```

---

## 4. Palabras Gatillo de IA — EVITAR

Organizadas por era del modelo que las popularizó:

### 2023–mid2024 (GPT-3.5/4)
delieve, crucial, pivotal, intricate, tapestry, testament, meticulous, garner, vibrant, landscape, interplay, underscoring, multifaceted

### mid2024–mid2025 (GPT-4o/Claude)
bolster, foster, enhance, showcasing, highlighting, dynamic, align with, enduring

### 2025+ (Modelos actuales)
transformative, leverage, paradigm, actionable, synergy, nuanced understanding, rapid evolution, foster innovation, cutting-edge, game-changer

### Siempre de alta señal
- **Conectores excesivos**: Furthermore, Moreover, In addition, Consequently, Nevertheless (como inicio de párrafo)
- **Clichés académicos**: "In today's world", "In recent years", "It is important to note that", "It is worth mentioning that"
- **Adjetivos sobreusados**: significant, essential, vital, crucial
- **Estructura repetida**: "Not only... but also" usado múltiples veces

---

## 5. Técnicas de Humanización

| # | Técnica | Descripción | Frecuencia |
|---|---------|-------------|------------|
| 1 | **Variar longitud de oraciones** | Alternar cortas (8-12), medias (15-22), largas (28-40+) por párrafo | Siempre |
| 2 | **Hedging (matizadores)** | "perhaps", "arguably", "to some degree", "it could be argued that", "may suggest", "tends to", "often", "in many cases" | 30-40% de oraciones |
| 3 | **Variedad de transiciones** | No solo "Furthermore/Moreover". Usar: "That said,", "On a related note,", "Interestingly,", "A parallel argument is that,", "Looking beyond this," | Dentro y entre párrafos |
| 4 | **Ejemplos concretos** | Añadir referencias a estudios específicos, cifras, datos numéricos, casos | ≥1 por párrafo |
| 5 | **Variedad sintáctica** | Alternar aperturas: frases preposicionales, cláusulas dependientes, frases participiales, adverbios | 40-50% de oraciones |
| 6 | **Adaptación por género** | Tono diferente para: informativo, argumentativo, persuasivo, narrativo, descriptivo | Por documento |
| 7 | **"Imperfecciones" naturales** | Preguntas retóricas, incisos entre paréntesis, aposiciones. Evitar estructura perfecta TD→Evidencia→Conclusión siempre | Espaciado |
| 8 | **Vocabulario de dominio** | Reemplazar palabras genéricas con terminología específica del campo | Por sección |
| 9 | **Rotación de vocabulario** | No repetir la misma palabra en 2-3 párrafos. Usar sinónimos. | Siempre |
| 10 | **Longitud variable de párrafos** | Mezclar párrafos de 2 oraciones con otros de 6-8 oraciones | Por sección |
| 11 | **Inyección de perplejidad léxica** | Replace predictable words with uncommon alternatives | 25-35% of sentences |
| 12 | **Ruptura de n-gramas repetidos** | Detect and break repeated 3-4 word patterns | Sliding window of 120 words |
| 13 | **Variedad sintáctica forzada** | 8 templates: fronted adverbial, passive, appositive, participial phrase | 35% of sentences |
| 14 | **Variación de function words** | Replace verbose prepositional phrases, vary articles | By density |
| 15 | **Imperfecciones humanas** | Contractions, em-dash asides, rhetorical questions | 10-15% of sentences |
| 16 | **Estructura variable de párrafos** | Alternate openings: Although, While, Despite | 40% of paragraphs |
| 17 | **Vocabulario de dominio específico** | Auto-insert domain terms from title/keywords | Per document |

---

## 5b. 3-Pass Cascade

| Pass | Intensidad | Transformaciones |
|------|-----------|-----------------|
| 1 (aggressive) | x1.2 | 12 transformations in sequence |
| 2 (smoothing) | x0.5 | sentence length + hedging |
| 3 (corrective) | condicional | re-humanization if detectability score > 15 |

---

## 5c. Per-Detector Strategy

| Detector | Weakness | Counter-strategy |
|----------|----------|-----------------|
| GPTZero | Perplexity + Burstiness | Lexical rarity + std >= 8 length variance |
| Turnitin | Neural classifier | Maximum syntactic variation |
| Originality.ai | Sentence rhythm | Vary clause patterns |
| QuillBot | Per-sentence scoring | 3-pass cascade breaking per-sentence patterns |
| Copyleaks | Multi-model | Combined all-phase strategy |
| ZeroGPT | Pure perplexity | Maximum lexical surprise |
| Grammarly | Grammatical consistency | Natural human imperfections |

---

## 6. Reglas de Anti-Plagio

1. **FUENTES REALES**: Toda cita debe tener una URL obtenida de búsqueda real en Google Scholar, arXiv, sitio oficial o repositorio verificado
2. **SÍNTESIS OBLIGATORIA**: Cada párrafo debe combinar información de al menos 3 fuentes diferentes
3. **PARÁFRASIS ESTRUCTURAL**: Cambiar la estructura de la oración original (voz activa ↔ pasiva, orden de ideas, énfasis)
4. **ATRIBUCIÓN**: Cada afirmación factual debe tener una cita APA 7 explícita
5. **NO RECYCLING**: Prohibido reusar frases o estructuras entre párrafos
6. **VERIFICACIÓN**: Usar `check_detectability()` antes de guardar; score mínimo 90/100
7. **VARIEDAD DE REFERENCIAS**: No citar al mismo autor más de 2 veces en párrafos consecutivos

---

## 7. Uso del Código

```python
# Import directo
from humanize import Humanizer

h = Humanizer()

# Analizar texto existente
report = h.analyze_text("texto a analizar")
print(f"Score de detectabilidad: {report['score']}/100")

# Humanizar un párrafo
texto_humanizado = h.humanize(
    "texto original generado por IA",
    style="academic",
    genre="argumentative",
    domain_terms=["cognitive load", "working memory", "dual coding"]
)

# Verificación final
metrics = h.check_detectability(texto_humanizado)
# metrics = {"perplexity": 0.72, "burstiness": 0.68, "score": 78, ...}
```

### Integración con apa7-docx

```python
from apa7 import APA7Doc
from humanize import Humanizer

h = Humanizer()
doc = APA7Doc()

# Cada párrafo se humaniza antes de agregarlo
parrafo_original = "Este texto debe ser humanizado..."
parrafo_humanizado = h.humanize(parrafo_original, style="academic")
doc.add_paragraph(parrafo_humanizado)

doc.save("documento.docx")

# Verificación final
report = h.check_detectability(doc)
```

### Usando generar_trabajo.py (recomendado)

```python
from generar_trabajo import UndetectableAPA7Doc

doc = UndetectableAPA7Doc()
# add_paragraph y add_heading_* humanizan automáticamente
doc.add_paragraph(texto, style="academic")
doc.save("documento.docx")
print(doc.detectability_report)  # Score final
```

---

## 8. Output Path

Guardar en: `{{USER_DIR}}\OneDrive\Documentos\Archivos OpenCode\Documentos\`

---

## 9. Referencia de Estilos por Género

| Género | Tono | Características |
|--------|------|-----------------|
| `informative` | Neutral, objetivo | Menos hedging, más datos, estructura clara |
| `argumentative` | Persuasivo, firme | Más hedging, preguntas retóricas, contraargumentos |
| `persuasive` | Convincente, apasionado | Llamados a la acción, ejemplos vívidos, lenguaje emotivo medido |
| `narrative` | Descriptivo, fluido | Transiciones suaves, variación rítmica, incisos narrativos |
| `descriptive` | Detallado, sensorial | Imágenes concretas, analogías, vocabulario específico |

Si no se especifica, se usa `informative` por defecto.

---

## 10. Variedad Lingüística

Todo texto generado por este skill debe usar **español neutro** sin vocabulario ni expresiones de España.

- **EVITAR** vocabulario de España: "vale", "tío/tía", "coche", "ordenador", "mola", "guay", "chulo", "cojones", "joder", "gilipollas", "coño", "hostia", "mogollón", "currar".
- **EVITAR** conjugaciones propias del español de España: "habéis", "tenéis", "sois", "habéis hecho" (preterito perfecto compuesto excesivo).
- Usar **"usted"** como tratamiento formal (no "tú" genérico).
- Preferir **español latinoamericano neutro**, sin inclinación marcada hacia ningún país en específico.
- El objetivo es que el texto suene natural para un hablante de América Latina, sin resultar forzado ni caricaturesco.

