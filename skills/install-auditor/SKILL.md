---
name: install-auditor
description: Audita skills, MCPs y plugins antes de instalarlos. Verifica código fuente, dependencias, conexiones externas, reputación y malware. Instala usando pnpm en vez de npx. Actívala cuando el usuario pida "instalar", "descargar", "auditar antes de instalar", o cualquier solicitud de instalación de skills/MCPs/plugins.
---

# Install Auditor

Skill que audita TODO lo que se instala en OpenCode (skills, MCPs, plugins) **antes** de instalarlo, y ejecuta la instalación con `pnpm dlx` en vez de `npx`.

## Metodología de Auditoría

Cada instalación debe pasar por estas 6 verificaciones **ANTES** de ejecutarse:

### Fase 1: Origen
| Check | Qué buscar |
|-------|-----------|
| Repositorio | ¿Es oficial del equipo de OpenCode? ¿De una empresa conocida (Vercel, Anthropic, Supabase)? ¿De un dev comunitario? |
| Estrellas | ¿Tiene tracción? >100 ⭐ = buena señal. 0 ⭐ = precaución |
| Instalaciones | ¿Cuántos downloads/installs tiene en skills.sh o npm? |

### Fase 2: Código fuente
| Check | Qué buscar |
|-------|-----------|
| Ofuscación | ¿Hay código minimizado/obfuscado sin source maps? |
| eval() | ¿Hay `eval()`, `Function()`, `new Function()` que ejecuten strings construidos dinámicamente? |
| Base64 | ¿Hay payloads base64 largos que podrían ser código oculto? |
| Descargas externas | ¿Hay fetch/wget/curl a URLs no documentadas? |

### Fase 3: Conexiones externas
| Check | Qué buscar |
|-------|-----------|
| URLs hardcodeadas | Listar TODAS las URLs en el código |
| Telemetría | ¿Hay analytics, trackers, beacons? |
| APIs | ¿A qué servicios se conecta? ¿Son los esperados? |

### Fase 4: Dependencias
| Check | Qué buscar |
|-------|-----------|
| package.json | Listar dependencias runtime. ¿Son conocidas? |
| npm audit | ¿Hay vulnerabilidades conocidas? |

### Fase 5: Permisos
| Check | Qué buscar |
|-------|-----------|
| Filesystem | ¿Lee/escribe en qué rutas? |
| Red | ¿A qué dominios se conecta? |
| Ejecución | ¿Ejecuta comandos? ¿Cuáles? |

### Fase 6: Veredicto
| Resultado | Acción |
|-----------|--------|
| 🟢 **SEGURO** | Proceder con instalación vía `pnpm dlx` |
| 🟡 **PRECAUCIÓN** | Preguntar al usuario antes de continuar |
| 🔴 **NO INSTALAR** | Bloquear y explicar por qué |

## Instalación con pnpm

Siempre usar `pnpm dlx` en vez de `npx` para instalar skills:

```bash
# En vez de:
# npx skills add <repo> --skill <name> -g -a opencode -y

# Usar:
pnpm dlx skills add <repo> --skill <name> -g -a opencode -y
```

Para MCPs y plugins, usar `pnpm add -g` o `pnpm dlx` según corresponda.

## Script de auditoría

El script `scripts/audit.py` automatiza las verificaciones de las Fases 1-5 para skills ya descargadas a `~/.agents/skills/`. Úsalo cuando el skill ya esté en disco pero quieras verificar antes de habilitarlo.

```bash
python scripts/audit.py --path ~/.agents/skills/<skill-name>
```

## Flujo completo recomendado

```
1. Usuario pide instalar [X]
2. BUSCAR X en skills.sh o npm
3. AUDITAR: origen → código → conexiones → dependencias → permisos
4. PRESENTAR veredicto al usuario
5. Si acepta → INSTALAR con pnpm dlx
6. VERIFICAR instalación exitosa
```
