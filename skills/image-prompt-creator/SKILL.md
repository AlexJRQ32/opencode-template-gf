---
name: image-prompt-creator
description: Crea prompts optimizados para generacion de imagenes con IA y recomienda el mejor servicio externo segun el tipo de imagen que se necesita. No genera imagenes — solo crea el prompt. Usarla cuando pidan "imagen", "logo", "banner", "ilustracion", "dibujo", "arte", "grafico", "prompt para imagen", "crea una imagen de...".
---

# Image Prompt Creator

Skill que toma una descripcion de lo que necesitas y te devuelve:

1. **Un prompt optimizado** listo para copiar y pegar en cualquier generador de imagenes IA
2. **Recomendacion del mejor servicio** segun el tipo de imagen

## Como funciona

```
Tu descripcion → Prompt optimizado → Recomendacion de IA externa
```

## Servicios recomendados segun tipo

| Tipo de imagen | Servicio recomendado | Donde usarlo |
|---|---|---|
| **Arte conceptual / ilustraciones** | Midjourney (via Discord) | midjourney.com |
| **Fotos realistas / personas** | DALL-E 3 | chatgpt.com (con GPT-4) |
| **Logos / branding** | Adobe Firefly | firefly.adobe.com |
| **Diseno grafico / marketing** | Canva AI | canva.com |
| **Anime / estilo cartoon** | Niji Journey | nijijourney.com (Midjourney sub) |
| **Fotos de stock personalizadas** | Stable Diffusion 3 | stability.ai |
| **Arte conceptual gratis** | Leonardo AI | leonardo.ai |
| **Generacion rapida sin cuenta** | Perchance AI | perchance.org/ai-png | 
| **Iconos / SVGs** | Recraft AI | recraft.ai |
| **Editar fotos existentes** | Clipdrop | clipdrop.co |

## Estructura del prompt

Siempre generar prompts con esta estructura:

```
[SUJETO/ESCENA], [DETALLES], [ESTILO], [ILUMINACION], [COLOR], [COMPOSICION], [MOOD]
```

### Elementos clave para prompts de calidad

1. **Sujeto**: Que o quien aparece en la imagen (especifico)
2. **Accion**: Que esta haciendo el sujeto
3. **Entorno**: Donde ocurre la escena
4. **Estilo**: Realista, cartoon, acuarela, 3D, minimalista, etc.
5. **Iluminacion**: Natural, dramatica, de estudio, dorada, etc.
6. **Paleta de colores**: Colores especificos o tono general
7. **Composicion**: Primer plano, gran angular, vista aerea, etc.
8. **Estado de animo**: Alegre, misterioso, calmado, epico, etc.

### Ejemplos de prompts completos

**Para logo:**
> "Minimalist logo design for a brand called 'Luna Books', elegant open book silhouette with crescent moon, navy blue and gold color scheme, clean lines, vector style, white background, professional, memorable"

**Para banner de curso:**
> "Wide banner 16:9 for an online course called 'Introduction to Psychology', brain with colorful neural networks floating above an open book, soft blue and purple gradient background, clean modern design, educational, inspiring, detailed, 8k quality"

**Para ilustracion academica:**
> "Scientific illustration of the water cycle, evaporation condensation precipitation, labeled diagram, clean white background, educational style, blue and green color palette, clear typography, vector quality"

## Como usar con image-viewer

Si ya tenes una imagen y quieres analizarla o mejorarla:
1. Usa `image-viewer` para analizar la imagen existente
2. Usa `image-prompt-creator` para generar un prompt mejorado
3. Lleva el prompt a la IA recomendada y genera la nueva version

## Nota importante

Este skill NO genera imagenes. Solo crea prompts para que los uses en servicios externos de IA generativa.
