#!/usr/bin/env python3
import sys
sys.path.insert(0, r"{{USER_DIR}}\.agents\skills\undetectable-apa7\scripts")
from humanize import Humanizer
h = Humanizer()
text = (
    "This study analyzes the impact of artificial intelligence on "
    "higher education. The results suggest that AI integration offers "
    "opportunities for improving educational experiences. "
    "The adoption of machine learning algorithms has increased significantly "
    "in academic settings. Researchers have identified several key factors "
    "that contribute to successful implementation. These include "
    "institutional support, faculty training, and infrastructure development. "
    "Understanding these factors is crucial for policymakers and educators. "
    "Furthermore, ethical considerations must be taken into account when "
    "deploying AI systems in educational environments. This research "
    "contributes to the growing body of knowledge on AI in education."
)
result = h.humanize(text, style="academic", intensity=0.7)
report = h.check_detectability(result)
print("INPUT LENGTH:", len(text), "chars")
print("OUTPUT LENGTH:", len(result), "chars")
print("DETECTABILITY SCORE:", report.get("detectability_score", "?"))
print()
import difflib
for i, line in enumerate(difflib.unified_diff(text.split(". "), result.split(". "), lineterm="")):
    print(line)
print()
print("=== REPORT ===")
for k, v in report.items():
    if isinstance(v, float):
        print(f"  {k}: {v:.4f}")
    else:
        print(f"  {k}: {v}")

