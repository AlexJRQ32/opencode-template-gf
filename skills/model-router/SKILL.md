---
name: model-router
description: >
  big-pickle elige dinámicamente el mejor modelo gratis.
  Actívate cuando detectes keywords de programación, planificación,
  creatividad o comparación de modelos. No lo actives para preguntas
  simples o conversación casual. Todos los modelos son GRATIS.
license: MIT
---

# Model Router — big-pickle Director de Orquesta

**big-pickle analiza la tarea y elige el mejor modelo gratis.** Solo 5 agentes, el resto lo cubre `openrouter-free`.

## Agentes

| Agente | Modelo | Cuándo usarlo |
|--------|--------|---------------|
| `qwen3-coder` | `qwen/qwen3-coder:free` | Código, features, refactors (262K ctx) |
| `nemotron-reasoning` | `nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free` | Razonamiento, debugging |
| `llama` | `meta-llama/llama-3.3-70b-instruct:free` | Creatividad, copy, brainstorming |
| `opencode-nemotron` | `opencode/nemotron-3-ultra-free` | Contexto gigante (1M), documentos grandes |
| `kimi-ui` | `moonshotai/kimi-k2.6:free` | UI/UX, CSS, frontend, interfaces visuales |
| `openrouter-free` | `openrouter/free` | **CATCH-ALL**: todo lo demás, elige automágicamente |

## Flujo

1. **Analizá** la tarea
2. **Elegí** el agente: código → `qwen3-coder`, razonamiento → `deepseek-r1`, creativo → `llama`, UI/CSS → `kimi-ui`, contexto enorme → `opencode-nemotron`, cualquier otra cosa → `openrouter-free`
3. **Dispatch async** via `task(subagent_type="<agente>", prompt="...")`
4. **Devolvé** la respuesta del modelo elegido

> **IMPORTANTE:** El agente que ejecute la tarea DEBE indicar explícitamente al inicio de su respuesta qué modelo lo realizó, con el formato: `**Modelo:** <nombre>`. Ejemplo: `**Modelo:** Qwen3 Coder 480B` o `**Modelo:** Llama 3.3 70B`.

### Competencia
Si pide comparar → dispatch paralelo a varios y compará.

### Tareas simples
Procesalas directo con big-pickle.

## Notas

- Todos gratis. Rate limits ~20 req/min.
- `openrouter-free` cubre ~27 modelos gratis de respaldo.
- Si falla un modelo, reintentá con otro o con `openrouter-free`.
