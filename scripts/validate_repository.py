#!/usr/bin/env python3
from pathlib import Path
import csv
import hashlib
import json
import sys

root = Path(__file__).resolve().parents[1]

required = [
    "README.md",
    "README_IT.md",
    "CITATION.cff",
    "pyproject.toml",
    "src/acs/model.py",
    "tests/test_model.py",
    "data/simulation_summary.json",
    "data/monte_carlo_unoptimized.csv",
    "data/monte_carlo_design_envelope.csv",
    "figures/fig_00_system_architecture.png",
    "figures/fig_06_cooling_prediction.png",
    "media/adaptive_capillary_skin_virtual_prototype.mp4",
    "paper/Adaptive_Capillary_Skin_Journal_Manuscript_v0.1.pdf",
    "paper/Adaptive_Capillary_Skin_Supplementary_Information_v0.1.pdf",
    "paper/Adaptive_Capillary_Skin_Zenodo_Technical_Disclosure_v0.1.pdf",
    "docs/falsification_protocol.md",
    "docs/physical_validation_protocol.md",
    "provenance/contribution_matrix.csv",
    "SHA256SUMS.txt",
]

missing = [p for p in required if not (root / p).exists()]
if missing:
    print("Missing required files:", *missing, sep="\n - ")
    sys.exit(1)

json.loads((root / "data/simulation_summary.json").read_text(encoding="utf-8"))
json.loads((root / "metadata/zenodo_metadata_draft.json").read_text(encoding="utf-8"))

with open(root / "provenance/contribution_matrix.csv", newline="", encoding="utf-8") as f:
    rows = list(csv.reader(f))
assert len(rows) >= 2

manifest = root / "SHA256SUMS.txt"
errors = []
for line in manifest.read_text(encoding="utf-8").splitlines():
    if not line.strip():
        continue
    expected, rel = line.split(maxsplit=1)
    path = root / rel
    if not path.is_file():
        errors.append(f"Manifest path missing: {rel}")
        continue
    actual = hashlib.sha256(path.read_bytes()).hexdigest()
    if actual != expected:
        errors.append(f"Checksum mismatch: {rel}")

if errors:
    print("Repository integrity validation failed:")
    for error in errors:
        print(" -", error)
    sys.exit(1)

print("Repository structure, JSON metadata, provenance table and SHA-256 manifest OK")
