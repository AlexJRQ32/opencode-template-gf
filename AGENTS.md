# Memoria Persistente con Obsidian

Vault: {{VAULT_PATH}} (MCP root para Obsidian)

## Skills Instaladas
Academicas: apa7-docx, undetectable-apa7, fuentes-confiables, presentation-designer, cursos-gratis
Imagenes: image-viewer (analizar), image-prompt-creator (crear prompts para IA externa)
Utilerias: obsidian-vault, model-router, token-efficiency, install-auditor

## Subagentes (4 - todos gratis)
| Subagente | Modelo (Zen Free) | Rol |
|---|---|---|
| `@oracle` | `opencode/nemotron-3-ultra-free` | Analisis, debugging, arquitectura (1M ctx) |
| `@fixer` | `opencode/glm-5-free` | Implementacion de codigo y documentos |
| `@explorer` | `opencode/deepseek-v4-flash-free` | Busqueda de codigo/simbolos |
| `@librarian` | `opencode/deepseek-v4-flash-free` | Documentacion externa e investigacion |

## Plugins (9)
oh-my-opencode, opencode-vibeguard, opencode-websearch-cited, opencode-pty, opencode-supermemory, opencode-snip, opencode-working-memory, opencode-orchestrator, opencode-dux

## Reglas Obligatorias

### Regla 1: Investigacion y citas
Para trabajos academicos: usar apa7-docx + fuentes-confiables para citas reales.

### Regla 2: Anti-deteccion
Para evitar deteccion IA: usar undetectable-apa7 siempre antes de entregar. Verificar con check_detectability() antes de guardar.

### Regla 3: Imagenes
Usar image-prompt-creator para generar prompts, image-viewer para analizar imagenes existentes.

### Regla 4: Explicar cada herramienta antes de usarla
Antes de ejecutar cualquier skill, MCP o plugin, el agente DEBE explicar brevemente que hace, para que sirve y que va a hacer con ella.

### Regla 5: Modo Facil - Preguntar antes de generar
Siempre que la usuaria pida generar un documento academico, el agente debe hacer estas 3 preguntas ANTES de comenzar:
1. "De que tema exacto quieres que trate?"
2. "Que extension necesitas? (corta / mediana / larga)"
   - Corta = 3-5 paginas (ensayo)
   - Mediana = 8-12 paginas (informe)
   - Larga = 15+ paginas (investigacion)
3. "Cuantas fuentes quieres que incluya? (3-5 / 5-10 / 10+)"

No comenzar a escribir hasta que la usuaria responda las 3 preguntas.

### Regla 6: Memoria persistente
Guardar automaticamente en Obsidian: sessions/, decisions/, learnings/, preferences/, activity/. Cierre obligatorio con wikilinks y extension .md.

### Regla 7: Contexto inicial
Al iniciar cada interaccion, leer _context_.md del vault de Obsidian.