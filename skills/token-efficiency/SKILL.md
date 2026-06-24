---
name: token-efficiency
description: Disciplina de fondo para minimizar tokens. No re-leer, leer quirúrgicamente, respuestas concisas, bachear tool calls, resumir contexto, priorizar retención.
---

# Token Efficiency (Consolidado)

Disciplina de fondo. **No es un skill que se invoca, se sigue siempre.**

## 1. No re-leer lo que ya tenés

```
Antes de Read/Grep/Glob:
  - ¿Ya tengo este archivo en contexto?
  - ¿Ya lo leí antes en la conversación?
  - Si sí → usá lo que tenés. NO re-leas.
```

## 2. Leer quirúrgicamente

```
  - Líneas específicas → offset/limit
  - Buscar algo → Grep primero, leer solo la sección relevante
  - NO leer 500 líneas para encontrar una función
```

## 3. Respuestas concisas

```
  - Respondé primero, explicación después si hace falta
  - Sin preámbulos, sin repetir lo que dijo el usuario
  - No expliques lo que vas a hacer → hacelo
  - Después de cambios: resumen breve, no el diff completo
```

## 4. Batch tool calls

Múltiples calls independientes en un solo mensaje. No uno por uno.

## 5. No sobre-explorar

Empezá por el archivo más probable, no por una búsqueda amplia.

## 6. No pedir permiso para cambios seguros

Si estás seguro, hacelo directamente.

## 7. Resumir contexto cuando se acerca al límite

Si el contexto está >70%, reemplazá historial viejo con:

```markdown
## Resumen de sesión
### Intención del usuario
[1-2 líneas]
### Archivos modificados
- `ruta`: [qué cambió]
### Decisiones clave
- [decisión]: [por qué]
### Estado actual
[qué funciona, qué falta, próximos pasos]
```

## 8. Priorizar retención por importancia

| Prioridad | Contenido | Acción |
|-----------|-----------|--------|
| P1 | Paths, errors, intent del user | NUNCA podar |
| P2 | Decisiones + cambios | Resumir |
| P3 | Logs de exploración, intentos fallidos | Solo mantener lección |
| P4 | Tool outputs duplicados | Podar completamente |

## 9. Partitioning

Tareas grandes → partir en sub-agentes con contextos aislados via `task()`.

## Qué NO sacrificar

Ser conciso no significa ser descuidado:
- Error handling, tests, decisiones complejas cuando el usuario las necesita
- No skipees pasos de skills solo para "ahorrar tokens"
