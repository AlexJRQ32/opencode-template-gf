# OpenCode Template — Academico

Template de configuracion OpenCode para trabajos universitarios, investigacion y documentos academicos.

## Que incluye

### Skills Academicas
- `apa7-docx` — Documentos APA 7ª edicion 100% compliant
- `undetectable-apa7` — Anti-deteccion IA + anti-plagio multi-fuente
- `fuentes-confiables` — Fuentes academicas verificadas (A1-A5)
- `presentation-designer` — Presentaciones profesionales
- `cursos-gratis` — Descubrimiento de cursos online

### Skills de Imagenes
- `image-viewer` — Analiza y describe imagenes existentes
- `image-prompt-creator` — Crea prompts optimizados para IA de imagenes externa

### Skills de Seguridad
- `install-auditor` — Audita skills/MCPs antes de instalarlos
- `gptzero` — Detecta si un texto fue escrito por IA

### Subagentes (4)
@oracle (qwen3.7-max), @fixer (glm-5.2), @explorer (deepseek-v4-flash), @librarian (deepseek-v4-flash)

### Plugins (9)
Minimales: oh-my-opencode, opencode-vibeguard, opencode-websearch-cited, opencode-pty, opencode-supermemory, opencode-snip, opencode-working-memory, opencode-orchestrator, opencode-dux

## Setup rapido
1. Lee SETUP.md para configurar el vault de Obsidian
2. Las skills se instalan con: `npx skills add <skill-name>`
3. Listo — ya podes generar documentos academicos

## Flujo de trabajo recomendado
1. Investigar con fuentes confiables
2. Redactar con undetectable-apa7
3. Formatear con apa7-docx
4. Verificar con check_detectability()
5. Para imagenes: image-prompt-creator ? IA externa ? image-viewer