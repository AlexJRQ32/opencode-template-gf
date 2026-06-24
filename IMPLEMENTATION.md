# Implementacion - Template OpenCode

## Requisitos
1. Tener Node.js instalado
2. Tener Obsidian instalado con un vault creado
3. Tener OpenCode instalado

## Pasos

### 1. Configurar Obsidian
1. Abre Obsidian y crea/abre tu vault
2. Copia la ruta de tu vault (ej: \C:\Users\TU_USUARIO\Documents\Mi Vault\)
3. Instala el plugin \"MCP Vault\" en Obsidian si no lo tienes

### 2. Configurar el template
1. Copia \opencode.template.jsonc\ como \opencode.jsonc\
2. Edita \opencode.jsonc\ y reemplaza los placeholders:
   - \{{MCPVAULT_CMD}}\ → ruta al comando mcpvault (normalmente \
px @bitbonsai/mcpvault\)
   - \{{VAULT_PATH}}\ → ruta completa de tu vault de Obsidian
3. En \AGENTS.md\, actualiza \{{VAULT_PATH}}\ con tu ruta

### 3. Instalar plugins
Ejecuta en terminal:
\\\
npx opencode-marketplace install oh-my-opencode opencode-vibeguard opencode-websearch-cited opencode-pty opencode-wakatime opencode-worktree opencode-background-agents opencode-supermemory opencode-goal-plugin opencode-conductor opencode-quota opencode-snip opencode-claude-memory opencode-working-memory opencode-swarm opencode-orchestrator opencode-hive opencode-lazy opencode-codeindex opencode-models-discovery opencode-copilot-plugin @openspoon/subtask2 @plannotator/opencode @hueyexe/opencode-ensemble @capybearista/opencode-agents-loader opencode-dux opencode-agent-trace-plugin opencode-mem
\\\

### 4. Configurar skills
Las skills ya estan en la carpeta \skills/\. Copialas a \~/.agents/skills/\:
\\\
xcopy /E /I skills %USERPROFILE%\.agents\skills\
\\\

### 5. Configurar MCP servers
1. Navega a la carpeta \mcp-servers/\
2. Ejecuta \
pm install\ para instalar dependencias
3. El MCP de Obsidian ya deberia funcionar tras configurar \opencode.jsonc\

### 6. Listo!
Abre OpenCode en cualquier carpeta y empieza a usar la configuracion.
