# Setup — OpenCode Template Academico

## 1. Prerrequisitos
- Node.js >= 20 instalado
- OpenCode instalado
- Suscripcion OpenCode Go ($10/mes) para modelos de calidad

## 2. Clonar el template
```bash
git clone <repo-url> ~/.config/opencode
```

## 3. Reemplazar variables
En `opencode.template.jsonc`, reemplazar:
- `{{MCPVAULT_CMD}}` — ruta al comando mcpvault (ej: `C:\Users\tu-user\.config\opencode\...\mcpvault.cmd`)
- `{{VAULT_PATH}}` — ruta a tu vault de Obsidian

## 4. Instalar skills
```bash
npx skills add --skill apa7-docx
npx skills add --skill undetectable-apa7
npx skills add --skill fuentes-confiables
npx skills add --skill presentation-designer
npx skills add --skill obsidian-vault
```

## 5. Configurar vault
- Crea tu vault en Obsidian
- Ejecuta el script gen-context-snapshot.ps1 para generar _context_.md
- Revisa AGENTS.md para las reglas de memoria persistente

## 6. Primer documento
```python
from apa7 import APA7Doc
doc = APA7Doc()
doc.add_title_page("Mi Trabajo", "Tu Nombre", "Universidad", curso="Curso", instructor="Prof.", date="Fecha")
doc.add_paragraph("Contenido...")
doc.save("trabajo.docx")
```