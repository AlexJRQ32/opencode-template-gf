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
1. Al iniciar cada interaccion, leer _context_.md del vault de Obsidian
2. Para trabajos academicos: usar apa7-docx + fuentes-confiables para citas reales
3. Para evitar deteccion IA: usar undetectable-apa7 siempre antes de entregar
4. Para imagenes: usar image-prompt-creator para generar prompts, image-viewer para analizar
5. Verificar con check_detectability() antes de guardar documento final
6. Guardar automaticamente: sessions/, decisions/, learnings/, preferences/, activity/
7. Cierre obligatorio por nota con wikilinks y extension .md