# Integracion Obsidian + OpenCode (Guia Completa)

Esta guia explica **exactamente como esta configurado** el OpenCode de Alex para que tenga memoria persistente via Obsidian. Sigue estos pasos para tener la misma configuracion.

---

## Las 4 Capas de la Integracion

`
┌─────────────────────────────────────────────┐
│  1. MCP Server (@bitbonsai/mcpvault)         │  ← conexion al vault
├─────────────────────────────────────────────┤
│  2. AGENTS.md (reglas del sistema)           │  ← el cerebro
├─────────────────────────────────────────────┤
│  3. Skill obsidian-vault (comportamiento)    │  ← como escribir notas
├─────────────────────────────────────────────┤
│  4. Plugins de memoria (persistencia)        │  ← recuerda entre sesiones
└─────────────────────────────────────────────┘
`

---

## Capa 1: MCP Server de Obsidian

Es el puente entre OpenCode y tu vault de Obsidian.

### Instalacion

El paquete se llama @bitbonsai/mcpvault. Ya esta incluido en mcp-servers/package.json.

Solo ejecuta en la carpeta mcp-servers/:

`powershell
npm install
`

### Configuracion en opencode.jsonc

`json
"mcp": {
  "obsidian": {
    "type": "local",
    "command": [
      "npx",
      "-y",
      "@bitbonsai/mcpvault",
      "C:/Users/TU_USUARIO/Documents/Tu Vault"
    ],
    "enabled": true
  }
}
`

**Importante:** La ruta del vault usa / (no \), y apunta a la carpeta raiz de tu vault de Obsidian.

### Herramientas que expone

Una vez configurado, OpenCode tendra estos comandos disponibles:

| Herramienta | Para que sirve |
|-------------|----------------|
| obsidian_read_note(path) | Leer una nota del vault |
| obsidian_write_note(path, content) | Crear o sobrescribir una nota |
| obsidian_search_notes(query) | Buscar notas por contenido |
| obsidian_list_directory(path) | Listar archivos en una carpeta |
| obsidian_get_vault_stats() | Ver estadisticas del vault |
| obsidian_list_all_tags() | Ver todos los tags |
| obsidian_patch_note(path, old, new) | Editar parte de una nota |
| obsidian_move_note(old, new) | Mover o renombrar una nota |
| obsidian_delete_note(path) | Eliminar una nota |
| obsidian_update_frontmatter() | Editar metadatos |
| obsidian_manage_tags() | Gestionar tags |

---

## Capa 2: AGENTS.md (El Cerebro)

Este archivo en ~/.config/opencode/AGENTS.md le dice a OpenCode **como** debe usar Obsidian. Es lo mas importante.

Copia este contenido completo (ajustando TU_USUARIO por tu nombre de usuario de Windows):

`markdown
# Memoria Persistente con Obsidian

Vault: C:\Users\TU_USUARIO\Documents\TU_VAULT (MCP root: C:\Users\TU_USUARIO → prefijar Documents/TU_VAULT/)

─────────────────────────────────────────────────
## DATOS DEL SISTEMA
─────────────────────────────────────────────────

| Variable | Valor |
|----------|-------|
| **Usuario Windows** | TU_USUARIO |
| **Vault Obsidian** | C:\Users\TU_USUARIO\Documents\TU_VAULT |
| **Config OpenCode** | C:\Users\TU_USUARIO\.config\opencode |
| **Skills locales** | C:\Users\TU_USUARIO\.agents\skills\ |
| **Output archivos** | C:\Users\TU_USUARIO\Documents\Archivos OpenCode\ |
| **Python** | (ruta de tu Python si lo tienes) |
| **MCP vault root** | C:\Users\TU_USUARIO (prefijar Documents/TU_VAULT/) |

─────────────────────────────────────────────────
## REGLAS OBLIGATORIAS
─────────────────────────────────────────────────

### Al iniciar cada interaccion
1. obsidian_read_note(path="opencode/_context_.md")
2. Solo si el tema es conocido: obsidian_search_notes(query="<tema>")

### Guardado automatico
| Carpeta | Cuando |
|---------|--------|
| sessions/ | Siempre |
| decisions/ | Si hay decision tecnica |
| learnings/ | Si hay algo nuevo |
| preferences/ | Si se detecta preferencia |
| ctivity/ | Siempre (solo titulo+tags) |

### CIERRE OBLIGATORIO por nota
1. Incluir - Relacionado: [[YYYY-MM]] desde el inicio
2. Actualizar indice mensual
3. Activity: ### HH:MM - Titulo
4. Wikilinks con /, sin \\, sin trailing slash
5. Extension .md obligatoria
`

---

## Capa 3: Skill obsidian-vault

El skill esta en ~/.agents/skills/obsidian-vault/SKILL.md. OpenCode lo detecta automaticamente porque escanea ~/.agents/skills/.

### Instalacion

Copia la carpeta skills/obsidian-vault/ del template a tu maquina:

`powershell
xcopy /E /I skills\obsidian-vault %USERPROFILE%\.agents\skills\obsidian-vault\
`

### Estructura del vault que espera

`
Tu Vault Obsidian/
└── opencode/
    ├── activity/        # Feed visible (un archivo por dia)
    ├── decisions/       # Decisiones tecnicas
    ├── learnings/       # Cosas aprendidas
    ├── sessions/        # Resumenes de sesiones
    ├── preferences/     # Preferencias del usuario
    └── context/         # Contexto de proyectos activos
`

Crea esta estructura dentro de tu vault de Obsidian.

### Formato de archivos

Cada nota sigue el patron: YYYY-MM-DD-descripcion-breve.md

| Carpeta | Sufijo |
|---------|--------|
| sessions/ | -setup o el tema |
| decisions/ | -decisiones o -decisiones-tema |
| learnings/ | -aprendizajes o -aprendizajes-tema |
| preferences/ | -preferencias |
| ctivity/ | -activity |
| context/ | -nombre-proyecto |

Ejemplo: sessions/2026-06-24-setup-completo.md

### Formato de activity/

Cada entrada en ctivity/ sigue este formato estricto:

`markdown
### HH:MM - Titulo breve
- Tags: #tag1 #tag2
`

- Orden descendente (nuevo arriba)
- Sin descripciones entre titulo y tags
- Solo un wikilink opcional al final del titulo
- Horas en formato 24h

### Tags estandar

| Tipo | Tag |
|------|-----|
| Sesion | #sesion |
| Decision | #decision |
| Aprendizaje | #aprendizaje |
| Contexto proyecto | #contexto |
| Preferencias | #preferencia |
| MCP/Obsidian | #mcp #obsidian |
| Skills | #skill |

---

## Capa 4: Plugins de Memoria

Estos plugins trabajan con Obsidian para que OpenCode recuerde entre sesiones.

Ya estan en plugin: del opencode.template.jsonc. Solo asegurate de instalarlos:

`powershell
npx opencode-marketplace install opencode-supermemory opencode-claude-memory opencode-working-memory opencode-mem
`

- **opencode-supermemory**: Memoria persistente (recuerda preferencias, proyectos, errores)
- **opencode-claude-memory**: Memoria tipo claude-code
- **opencode-working-memory**: Memoria de trabajo en la sesion actual
- **opencode-mem**: Memoria adicional

---

## Checklist Completa de Configuracion

- [ ] Tener Node.js instalado
- [ ] Tener Obsidian instalado con un vault creado
- [ ] Tener OpenCode instalado
- [ ] Crear estructura opencode/ dentro del vault (sessions, activity, etc.)
- [ ] Copiar opencode.template.jsonc como opencode.jsonc
- [ ] Editar opencode.jsonc: poner ruta del vault en MCP obsidian
- [ ] Editar AGENTS.md: poner TU_USUARIO y ruta del vault
- [ ] Ejecutar 
pm install en mcp-servers/
- [ ] Instalar plugins con opencode-marketplace
- [ ] Copiar skills a ~/.agents/skills/
- [ ] Crear opencode/_context_.md en el vault (puede estar vacio inicialmente)
- [ ] Reiniciar OpenCode
- [ ] Probar: preguntar "puedes escribir una nota de prueba en Obsidian?"

---

## Notas Importantes

### Rutas en Windows
- En opencode.jsonc las rutas usan / (no \)
- El MCP root es C:\Users\TU_USUARIO y las rutas dentro del vault se prefijan como Documents/TU_VAULT/...

### Tokens y API Keys
Este template NO incluye tokens de GitHub, Azure DevOps, ni Supabase por seguridad. Si los necesitas, agregalos manualmente en opencode.jsonc.

### Output de archivos
OpenCode guardara archivos generados (documentos, imagenes) en C:\Users\TU_USUARIO\Documents\Archivos OpenCode\, organizados por tipo:
| Tipo | Subcarpeta |
|------|-----------|
| .docx .pdf .txt | Documentos/ |
| .png .jpg | Imagenes/ |
| .md | Markdown/ |

### Scripts Python (.py)
Los scripts Python **no deben guardarse** en Archivos OpenCode. Usa %TEMP% o la carpeta del proyecto correspondiente.
