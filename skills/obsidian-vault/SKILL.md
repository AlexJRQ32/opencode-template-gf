# Obsidian Vault Management

## Estructura

```
Obsidian Vault/
└── opencode/
    ├── activity/        # Feed visible (un archivo por día)
    ├── decisions/       # Decisiones técnicas
    ├── learnings/       # Cosas aprendidas
    ├── sessions/        # Resúmenes de sesiones
    ├── preferences/     # Preferencias del usuario
    └── context/         # Contexto de proyectos activos
```

## File naming

Un archivo por día por carpeta, con nombre descriptivo:
- `YYYY-MM-DD-descripcion-breve.md`

Convenciones por carpeta:
| Carpeta | Sufijo |
|---------|--------|
| `sessions/` | `-setup` o tema |
| `decisions/` | `-decisiones` o `-decisiones-tema` |
| `learnings/` | `-aprendizajes` o `-aprendizajes-tema` |
| `preferences/` | `-preferencias` |
| `activity/` | `-activity` |
| `context/` | `-nombre-proyecto` |

Ejemplo (válido): `sessions/2026-06-06-setup-completo.md`

## activity/ — Feed visible

Carpeta con un archivo por día: `activity/YYYY-MM-DD-activity.md`.

Formato estricto (solo título + tags, sin descripciones):

```markdown
### HH:MM - Título breve
- Tags: `#tag1` `#tag2`
```

- Orden descendente (nuevo arriba)
- Sin líneas de descripción entre título y tags
- Sin líneas `- Relacionado:`
- Horas en 24h, corregidas a hora real (12:xx → 00:xx, 13:xx → 01:xx)

## Cross-linking

Toda nota DEBE incluir `- Relacionado:` con wikilinks al final. No en activity/. Los wikilinks usan `[[activity/YYYY-MM-DD-activity#Sección]]`.

Formato:
```markdown
- Relacionado: [[carpeta/nota#Sección]] | [[carpeta/otra-nota]]
```

## Append strategy

1. Leer archivo del día con `mcpvault_read_note(path="carpeta/YYYY-MM-DD-descripcion.md")`
2. Si existe → añadir nueva entrada al final
3. Si no existe → crearlo con frontmatter y formato inicial
4. Guardar con `mcpvault_write_note()`
5. Insertar nueva entrada al inicio del archivo del día en `opencode/activity/YYYY-MM-DD-activity.md`

## Auto-save

Guardar SIEMPRE después de cada interacción:
- **Sesiones**: siempre que haya interacción
- **Decisiones**: si se tomó una decisión técnica
- **Aprendizajes**: si se aprendió algo nuevo
- **Preferencias**: si se detectó una preferencia del usuario
- **activity/**: siempre

## Herramientas MCP

Usar herramientas `mcpvault_*` para operaciones en el vault:
- `mcpvault_search(query)` — buscar contenido
- `mcpvault_read_note(path)` — leer nota
- `mcpvault_write_note(path, content)` — crear/sobrescribir
- `mcpvault_list_files(path)` — listar archivos
- `mcpvault_list_all_tags()` — listar todos los tags
- `mcpvault_get_vault_stats()` — estadísticas

## Rotación mensual activity/

Cuando un archivo del día en `activity/` supere ~100 entradas, archivar en `archived/activity-YYYY-MM-DD.md` y empezar uno nuevo.

## Inline links en activity/

Cada entrada puede incluir UN wikilink inline al final del título si hay una nota relevante:

```markdown
### HH:MM - Título [[carpeta/nota]]
- Tags: `#tag1`
```

No es obligatorio, pero mejora la navegabilidad del feed.

## Tags estándar

| Tipo | Tag |
|------|-----|
| Sesión | `#sesion` |
| Decisión | `#decision` |
| Aprendizaje | `#aprendizaje` |
| Contexto proyecto | `#contexto` |
| Preferencias | `#preferencia` |
| MCP/Obsidian | `#mcp` `#obsidian` |
| Skills | `#skill` |
| Organización | `#organizacion` |
