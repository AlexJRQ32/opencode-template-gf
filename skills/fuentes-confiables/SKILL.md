---
name: fuentes-confiables
description: Obliga a usar fuentes confiables (oficiales, Google Scholar, arXiv, repositorios verificados) para toda investigaciÃ³n e inferencia. Para implementaciones, exige paso a paso (step-by-step) con validaciÃ³n intermedia.
---

# Fuentes Confiables + Step by Step

Skill obligatoria cuando el usuario pida **informaciÃ³n, investigaciÃ³n, trabajos acadÃ©micos, tutoriales, guÃ­as, implementaciones, cÃ³digo, features, debugging, o cualquier tarea que requiera precisiÃ³n factual o ejecuciÃ³n tÃ©cnica**.

## Reglas de Fuentes (Research Mode)

### 1. JerarquÃ­a de fuentes (solo la A)

| Prioridad | Fuente | Ejemplos |
|-----------|--------|----------|
| **A1** | DocumentaciÃ³n oficial | docs.python.org, react.dev, supabase.com/docs, learn.microsoft.com, developer.mozilla.org |
| **A2** | Google Scholar / arXiv | scholar.google.com, arxiv.org |
| **A3** | Repositorios oficiales | github.com/org/repo (solo oficial), npm registry, crates.io, pypi.org |
| **A4** | Publicaciones revisadas | IEEE, ACM, Springer, Elsevier, Nature, Science |
| **A5** | Blogs tÃ©cnicos de ingenierÃ­a | engineering.fb.com, netflixtechblog.com, vercel.com/blog |

### 2. Fuentes NO aceptadas

| Fuente | RazÃ³n |
|--------|-------|
| Medium / Dev.to / Hashnode (salvo autor oficial) | Sin revisiÃ³n, contenido desactualizado |
| Stack Overflow sin respaldo oficial | Puede estar incorrecto |
| Blogs personales sin referencias | Sin autoridad |
| Foros, Reddit, Quora, YouTube (fuente primaria) | No verificables. Usar solo si NO existe fuente A1-A5 |
| IA generativa como fuente | Circular |
| W3Schools (para temas avanzados) | Simplifica en exceso, contiene errores |
| Wikipedia (como fuente primaria) | Usar solo para contexto general, citar fuentes originales |

### 3. Fuentes de ultimo recurso (solo si no existe A1-A5)

Si despues de agotar A1-A5 no hay informacion util:
- **YouTube**: Solo canales tecnicos reconocidos (Fireship, Theo, Web Dev Simplified, Academind, freeCodeCamp, Google Devs, Microsoft Learn)
- **Reddit**: Solo r/programming, r/webdev, r/reactjs, r/nextjs, y subreddits oficiales de tecnologias
- **Stack Overflow**: SOLO respuestas con score >10 o aceptadas por OP
- **GitHub Issues/Discussions**: Solo del repositorio oficial de la herramienta
- Reportar al usuario: No encontre fuentes A1-A5. Usando [fuente ultimo recurso]. Tomelo con precaucion.

### 4. Proceso obligatorio

```markdown
Cada vez que investigues algo:
1. Buscar en web con query orientada a docs oficiales ("official documentation", "docs")
2. Si no existe doc oficial clara â†’ buscar en Google Scholar ("site:scholar.google.com")
3. Si tampoco â†’ buscar en arXiv ("site:arxiv.org")
4. Ãšltimo recurso: blogs de ingenierÃ­a de empresas reconocidas
5. **Descartar explÃ­citamente** fuentes no confiables
6. Reportar al usuario: "SegÃºn [fuente oficial]..." o "No encontrÃ© fuente oficial, lo mÃ¡s cercano es [fuente A4/A5]"
```

### 5. Para trabajos academicos

- Citar **solo**: papers (Google Scholar, arXiv, IEEE, ACM, ScienceDirect)
- Incluir DOI o enlace permanente
- Si el usuario pide APA/MLA/Chicago, generarlo con formato correcto
- Si no hay paper sobre el tema exacto, informar al usuario: "No encontrÃ© literatura revisada sobre este tema. Las fuentes disponibles son [A3/A5]"

## Reglas de ImplementaciÃ³n (Step by Step Mode)

### 1. Toda implementaciÃ³n = paso a paso

Nunca dar una soluciÃ³n completa de golpe. Siempre estructurar en pasos secuenciales:

```markdown
## Paso 1: [nombre]
[quÃ© hacer, comando/snippet, explicaciÃ³n breve]

âœ… VerificaciÃ³n: [cÃ³mo confirmar que este paso funciona]

---

## Paso 2: [nombre]
...
```

### 2. Estructura de cada paso

| Elemento | Obligatorio |
|----------|-------------|
| **QuÃ© hacer** | SÃ­ â€” instrucciÃ³n clara |
| **CÃ³digo/comando** | SÃ­ â€” si aplica |
| **ExplicaciÃ³n breve** | SÃ­ â€” 1-3 lÃ­neas |
| **âœ… VerificaciÃ³n** | SÃ­ â€” cÃ³mo saber que funcionÃ³ ("deberÃ­as ver X", "corre Y comando") |
| **âš ï¸ Error comÃºn** | Si aplica â€” quÃ© podrÃ­a salir mal |

### 3. ProgresiÃ³n lÃ³gica

```
Paso 1: Setup/instalaciÃ³n
Paso 2: ConfiguraciÃ³n bÃ¡sica
Paso 3: Feature mÃ­nima funcional
Paso 4: Refinamiento
Paso 5: Testing/validaciÃ³n
```

Cada paso **debe funcionar por sÃ­ solo** antes de pasar al siguiente.

### 4. Si el usuario pide debuggear

```
1. Identificar el error exacto (logs, mensaje)
2. Buscar en docs oficiales la causa raÃ­z
3. Proponer 1 fix a la vez
4. âœ… VerificaciÃ³n: "corre X comando, deberÃ­as ver Y"
5. Si no funciona, diagnosticar antes de proponer otro fix
```

### 5. Restricciones

- NO asumir configuraciones que no se hayan verificado
- NO mezclar pasos â€” si un paso tiene 3 sub-tareas, dividirlo
- SIEMPRE preguntar al usuario antes de borrar/modificar archivos existentes que no forman parte del plan
- SIEMPRE verificar prerequisitos antes de empezar (versiones, dependencias instaladas)



