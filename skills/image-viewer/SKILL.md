---
name: image-viewer
description: "Analiza imágenes del usuario y pule automáticamente las que fueron creadas por opencode (en Imágenes/). Cuando el usuario pide 'mira esta imagen', 've esta', 'qué se ve en', 'analiza', 'abre imagen', 'pule esta imagen', 'arregla la imagen', 'mejórala', o pasa una ruta de imagen (.png, .jpg, .jpeg, .gif, .bmp, .webp). RESTRICCION: Solo aceptar rutas bajo OneDrive\\Documentos\\Archivos OpenCode\\Imágenes\\ o OneDrive\\Documentos\\Screenshots\\. Si está fuera, rechazar con mensaje claro."
---

# Image Viewer + Image Polisher

## Directorios permitidos

| Tipo | Ruta | Acción |
|------|------|--------|
| ✅ Creadas por opencode | `OneDrive\Documentos\Archivos OpenCode\Imágenes\` | Analizar + pulir |
| ✅ Capturas de pantalla | `OneDrive\Documentos\Screenshots\` | Solo analizar |
| ❌ Cualquier otra ruta | — | Rechazar |

## Flujo

### 1. Validar ruta
Si la ruta NO está dentro de los directorios permitidos, responder:
> "Ruta no permitida. Solo acepto imágenes en `Archivos OpenCode/Imágenes/` o `Screenshots/`."

### 2. Leer imagen
Usar `read` tool con la ruta absoluta para intentar mostrar la imagen visualmente.

### 3. Analizar + Auditar
Ejecutar:
```powershell
python "$env:USERPROFILE\.agents\skills\image-viewer\image_view.py" "<ruta_absoluta>" --audit
```

Procesar el JSON de salida:
- Reportar dimensiones, formato, brillo, paleta, texto
- Si `audit` tiene issues, listarlos

### 4. Pulir (solo imágenes en `Imágenes\`)
Si el directorio es `Archivos OpenCode\Imágenes\` y el audit encontró issues:

**a. Buscar script fuente.** Revisar en este orden:
1. `$env:TEMP\opencode\` — scripts recientes
2. `~\.agents\skills\image-maker\scripts\`
3. `~\.agents\skills\visual-creator\`
4. Preguntar al usuario si no se encuentra

**b. Leer el script fuente**

**c. Corregir issues.** Tipos de issues y correcciones típicas:
| Issue | Corrección |
|-------|-----------|
| `text_invisible` | Aumentar contraste texto/fondo (colores claros sobre oscuro), agrandar fuente |
| `low_contrast` | Usar colores acento más brillantes, fondo más oscuro |
| `too_dark` | Reducir opacidad fondo, elementos más brillantes |
| `content_small` | Escalar contenido para que ocupe >50% del área |
| `faint_colors` | Saturar o agrandar elementos poco visibles |
| `many_dead_rows` | Reducir padding, distribuir contenido verticalmente |

**d. Regenerar**
Ejecutar el script corregido. Guardar en la MISMA ruta.

**e. Verificar**
Ejecutar `image_view.py <ruta> --audit` de nuevo. Si el audit ya no tiene issues → ✅.
Si quedan issues, iterar hasta que esté limpio.

### 5. Reporte final
Incluir:
- ✅/❌ Resultado del análisis
- Issues encontrados y corregidos (si aplica)
- Si se regeneró: ruta del archivo pulido
