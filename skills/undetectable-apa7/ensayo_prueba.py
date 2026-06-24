#!/usr/bin/env python3
import sys
sys.path.insert(0, r"{{USER_DIR}}\.agents\skills\undetectable-apa7\scripts")
from humanize import Humanizer

h = Humanizer()

# Ensayo original (estilo académico formal, como lo escribiría un estudiante)
ensayo_original = """
The distinction between left-wing and right-wing politics represents one of the most fundamental frameworks for understanding political ideology. This classification emerged during the French Revolution when members of the National Assembly sat to the left of the president's chair if they supported revolutionary change, and to the right if they favored the monarchy and traditional institutions. Since then, the left-right spectrum has evolved significantly across different historical contexts and geographical regions.

Left-wing politics generally emphasizes social equality, collective responsibility, and government intervention in the economy. Leftist ideologies advocate for progressive taxation, social welfare programs, public ownership of essential services, and labor rights. The core principle underlying left-wing thought is the belief that inequality is structurally produced by capitalism and that the state has a moral obligation to reduce these disparities through redistributive policies. Socialism, social democracy, and communism are traditionally classified as left-wing ideologies.

Right-wing politics typically prioritizes individual liberty, free markets, traditional values, and limited government intervention. Rightist ideologies support private property rights, free enterprise, low taxation, and personal responsibility. The fundamental premise of right-wing philosophy is that inequality is natural and often productive, as it incentivizes hard work and innovation. Conservatism, libertarianism, and classical liberalism are commonly associated with the right side of the political spectrum.

However, the left-right dichotomy has limitations in the contemporary political landscape. Modern political issues often cut across traditional ideological boundaries. For example, globalization has created strange alliances where both left-wing anti-globalists and right-wing nationalists oppose free trade agreements, albeit for different reasons. Environmental politics also challenges the traditional spectrum, as issues of climate change and sustainability require collective action that transcends ideological divisions.

Populism has further complicated the left-right framework in recent decades. Populist movements can emerge on both the left and the right, typically characterized by anti-establishment rhetoric and appeals to the common people against an elite class. Left-wing populism tends to frame the conflict in economic terms, pitting the working class against corporate elites and financial institutions. Right-wing populism often emphasizes cultural and national identity, opposing immigration and supranational institutions.

In conclusion, the left-right political spectrum remains a useful heuristic for understanding general ideological tendencies, but it cannot capture the full complexity of modern political thought. The most accurate understanding of contemporary politics requires analyzing multiple dimensions of ideology, including economic policy, social values, and attitudes toward governance and authority. Political actors today increasingly draw from diverse ideological traditions, creating hybrid positions that resist simple classification.
"""

print("=" * 65)
print("  ORIGINAL (antes de humanizar)")
print("=" * 65)
print(ensayo_original.strip())
print()

# --- Análisis del original ---
analisis_original = h.analyze_text(ensayo_original)
print("=" * 65)
print("  ANÁLISIS DEL ORIGINAL")
print("=" * 65)
for k, v in analisis_original.items():
    if isinstance(v, float):
        print(f"  {k}: {v:.4f}")
    else:
        print(f"  {k}: {v}")
print()

# --- Humanizar ---
ensayo_humanizado = h.humanize(ensayo_original, style="academic", intensity=0.8)

print("=" * 65)
print("  HUMANIZADO (intensity=0.8)")
print("=" * 65)
print(ensayo_humanizado.strip())
print()

# --- Reporte de detectabilidad ---
reporte = h.check_detectability(ensayo_humanizado)
print("=" * 65)
print("  REPORTE DE DETECTABILIDAD")
print("=" * 65)
for k, v in reporte.items():
    if isinstance(v, float):
        print(f"  {k}: {v:.4f}")
    else:
        print(f"  {k}: {v}")

# Veredicto final
print()
score = reporte.get("detectability_score", 0)
if score >= 60:
    print("⚠️  ALERTA: Detectabilidad alta.")
elif score >= 35:
    print("📊  Detectabilidad MODERADA.")
else:
    print("✅  Detectabilidad BAJA. Parece humano.")

