"""
install-auditor: Audit script for OpenCode skills/MCPs/plugins.

Scans a skill directory and reports:
- Origen
- Archivos y tamano
- URLs/external connections found
- eval() or obfuscated code
- Dependencies (package.json)
- Overall risk verdict

Usage:
    python audit.py --path ~/.agents/skills/<skill-name>
    python audit.py --path .  (current directory)
"""

import os
import re
import json
import argparse
from pathlib import Path


# =============================================================================
# PATTERNS
# =============================================================================

URL_PATTERN = re.compile(r'https?://[^\s"\'\]\)>]+', re.IGNORECASE)

SUSPICIOUS_PATTERNS = {
    "eval()": re.compile(r'\beval\s*\('),
    "new Function()": re.compile(r'\bnew\s+Function\s*\('),
    "Base64 long string": re.compile(r'[A-Za-z0-9+/]{200,}={0,2}'),
    "fetch/wget/curl to unknown URL": re.compile(r'\b(fetch|wget|curl)\s*\('),
    "require('child_process')": re.compile(r"require\s*\(\s*['\"]child_process['\"]\s*\)"),
    
    "exec/spawn": re.compile(r'\b(exec|execSync|spawn|spawnSync)\s*\('),
}

ALLOWED_DOMAINS = {
    "opencode.ai", "api.github.com", "api.gptzero.me", "gptzero.me", "api.deepseek.com",
    "api.chutes.ai", "bigmodel.cn", "models.dev", "kroki.io",
    "mcp.context7.com", "mcp.vercel.com", "stitch.googleapis.com",
    "nexgendata--academic-research-mcp-server.apify.actor",
    "api.humanizerai.com", "apify.com", "nexgendata.com",
    "arxiv.org", "scholar.google.com", "wikipedia.org",
    "api.openai.com", "api.anthropic.com",
}

HIGH_REPUTATION_ORGS = {
    "vercel", "vercel-labs", "anthropic", "anthropics", "supabase",
    "github", "openai", "langchain-ai", "huggingface", "obra",
    "opencode", "opencode-ai",
}


# =============================================================================
# AUDIT FUNCTIONS
# =============================================================================

def get_file_tree(path, max_depth=4):
    files = []
    for root, dirs, fnames in os.walk(path):
        depth = root.replace(str(path), "").count(os.sep)
        if depth >= max_depth:
            dirs.clear()
            continue
        rel = Path(root).relative_to(path)
        for f in fnames:
            files.append(str(rel / f))
    return sorted(files)


def get_total_size(path):
    total = 0
    for root, dirs, fnames in os.walk(path):
        for f in fnames:
            fp = os.path.join(root, f)
            try:
                total += os.path.getsize(fp)
            except OSError:
                pass
    return total


def read_file_content(path, fname, max_bytes=100000):
    fp = path / fname
    if not fp.exists():
        return ""
    try:
        return fp.read_text(encoding="utf-8", errors="replace")[:max_bytes]
    except Exception:
        return ""


def check_source_reputation(path):
    result = {"org": "unknown", "verdict": "unknown"}
    skill_md = path / "SKILL.md"
    if skill_md.exists():
        content = skill_md.read_text(encoding="utf-8", errors="replace")
        for org in HIGH_REPUTATION_ORGS:
            if org.lower() in content.lower():
                result["org"] = org
                result["verdict"] = "high_reputation"
                break
    scores_json = path / "_scores.json"
    if scores_json.exists():
        try:
            data = json.loads(scores_json.read_text(encoding="utf-8"))
            result["install_count"] = data.get("install_count", "unknown")
        except Exception:
            pass
    return result


def scan_urls(content):
    urls = URL_PATTERN.findall(content)
    clean = []
    for u in urls:
        u = u.rstrip(".,;:)'\"")
        if u not in clean:
            clean.append(u)
    return clean


def scan_suspicious(content):
    findings = []
    for name, pattern in SUSPICIOUS_PATTERNS.items():
        matches = pattern.findall(content)
        if matches:
            findings.append({"pattern": name, "count": len(matches)})
    return findings


def check_dependencies(path):
    pkg_json = path / "package.json"
    if not pkg_json.exists():
        return {"has_deps": False, "deps": []}
    try:
        data = json.loads(pkg_json.read_text(encoding="utf-8"))
        deps = list(data.get("dependencies", {}).keys())
        dev_deps = list(data.get("devDependencies", {}).keys())
        return {"has_deps": True, "deps": deps, "dev_deps": dev_deps, "total": len(deps) + len(dev_deps)}
    except Exception:
        return {"has_deps": False, "deps": [], "error": "parse_error"}


def audit_skill(skill_path):
    path = Path(skill_path).expanduser().resolve()
    if not path.exists() or not path.is_dir():
        return {"error": "Directory not found: " + str(path)}

    source_info = check_source_reputation(path)
    files = get_file_tree(path)
    total_size = get_total_size(path)

    all_content = ""
    suspicious_findings = []
    all_urls = []
    for f in files:
        ext = Path(f).suffix.lower()
        if ext in (".md", ".py", ".js", ".ts", ".mjs", ".json", ".html", ".css", ".yaml", ".yml", ".sh", ".ps1", ".vbs"):
            content = read_file_content(path, f)
            all_content += content + "\n"
            suspicious_findings.extend(scan_suspicious(content))
            all_urls.extend(scan_urls(content))

    unique_urls = list(set(all_urls))
    unknown_urls = [u for u in unique_urls if not any(d in u for d in ALLOWED_DOMAINS)]
    deps_info = check_dependencies(path)

    risk_score = 0
    risk_factors = []

    if len(suspicious_findings) > 0:
        risk_score += 3
        risk_factors.append("Patrones sospechosos: " + str(len(suspicious_findings)))

    if unknown_urls:
        risk_score += 2
        risk_factors.append("URLs no verificadas: " + str(len(unknown_urls)))

    if deps_info.get("total", 0) > 10:
        risk_score += 1
        risk_factors.append("Muchas dependencias: " + str(deps_info['total']))

    if source_info.get("verdict") == "high_reputation":
        risk_score -= 1

    if total_size > 5000000:
        risk_score += 1
        risk_factors.append("Gran tamano: " + str(round(total_size / 1000000, 1)) + "MB")

    if risk_score <= 0:
        verdict = "[SEGURO]"
    elif risk_score <= 2:
        verdict = "[PRECAUCION]"
    else:
        verdict = "[NO INSTALAR]"

    return {
        "path": str(path),
        "files_count": len(files),
        "size_mb": round(total_size / 1000000, 1),
        "source": source_info,
        "suspicious_findings": suspicious_findings,
        "external_urls": unique_urls,
        "unknown_urls": unknown_urls,
        "dependencies": deps_info,
        "risk_score": risk_score,
        "risk_factors": risk_factors,
        "verdict": verdict,
    }


def print_report(report):
    if "error" in report:
        print("\n[ERRO] " + report['error'])
        return

    print("\n" + "=" * 60)
    print("  INSTALL AUDITOR - REPORTE")
    print("=" * 60)
    print("\n[DIR] " + report['path'])
    print("   Archivos: " + str(report['files_count']) + " | Tamano: " + str(report['size_mb']) + "MB")

    print("\n--- FASE 1: Origen ---")
    src = report["source"]
    print("   Organizacion: " + src.get('org', 'Desconocida'))
    print("   Reputacion: " + src.get('verdict', 'No evaluada'))

    print("\n--- FASE 2: Codigo Fuente ---")
    if report["suspicious_findings"]:
        for f in report["suspicious_findings"]:
            print("   [!] " + f['pattern'] + " (" + str(f['count']) + " ocurrencias)")
    else:
        print("   [OK] Sin patrones sospechosos")

    print("\n--- FASE 3: Conexiones Externas ---")
    print("   URLs encontradas: " + str(len(report['external_urls'])))
    for u in report.get("unknown_urls", []):
        print("   [?] No verificada: " + u)

    print("\n--- FASE 4: Dependencias ---")
    deps = report["dependencies"]
    if deps.get("has_deps"):
        print("   Total: " + str(deps.get('total', 0)))
        if deps.get("deps"):
            print("   Runtime: " + ', '.join(deps['deps'][:10]))
    else:
        print("   [OK] Sin dependencias externas")

    print("\n--- VEREDICTO ---")
    print("   Score de riesgo: " + str(report['risk_score']))
    for rf in report.get("risk_factors", []):
        print("   * " + rf)
    print("   Resultado: " + report['verdict'])
    print("=" * 60 + "\n")


def install_with_pnpm(skill_name, repo="", skill_ref=""):
    if repo and skill_ref:
        return 'pnpm dlx skills add ' + repo + ' --skill ' + skill_ref + ' -g -a opencode -y'
    elif skill_name:
        return 'pnpm dlx skills add ' + skill_name + ' -g -a opencode -y'
    return ""


def main():
    parser = argparse.ArgumentParser(description="Audit an OpenCode skill before installing")
    parser.add_argument("--path", type=str, required=True, help="Path to the skill directory")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    report = audit_skill(args.path)

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print_report(report)


if __name__ == "__main__":
    main()
