#!/usr/bin/env python3
from pathlib import Path
import csv
import json
import math
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
    "data/key_results.csv",
    "data/nominal_timeseries.csv",
    "data/monte_carlo_unoptimized.csv",
    "data/monte_carlo_design_envelope.csv",
    "figures/fig_00_system_architecture.png",
    "figures/fig_01_nominal_flow.png",
    "figures/fig_02_sensor_signal.png",
    "figures/fig_03_monte_carlo.png",
    "figures/fig_04_falsification_map.png",
    "figures/fig_05_hygromorphic_gate.png",
    "figures/fig_06_cooling_prediction.png",
    "media/adaptive_capillary_skin_virtual_prototype.mp4",
    "paper/Adaptive_Capillary_Skin_Journal_Manuscript_v0.1.pdf",
    "paper/Adaptive_Capillary_Skin_Supplementary_Information_v0.1.pdf",
    "paper/Adaptive_Capillary_Skin_Zenodo_Technical_Disclosure_v0.1.pdf",
    "docs/falsification_protocol.md",
    "docs/physical_validation_protocol.md",
    "docs/limitations.md",
    "provenance/contribution_matrix.csv",
    "provenance/curated_trace_2026-08-19.md",
    "metadata/zenodo_metadata_draft.json",
]

missing = [p for p in required if not (root / p).is_file()]
if missing:
    print("Missing required files:", *missing, sep="\n - ")
    sys.exit(1)

# Basic non-empty checks for binary/research assets.
for rel in required:
    if (root / rel).stat().st_size == 0:
        print(f"Empty required file: {rel}")
        sys.exit(1)

summary = json.loads((root / "data/simulation_summary.json").read_text(encoding="utf-8"))
json.loads((root / "metadata/zenodo_metadata_draft.json").read_text(encoding="utf-8"))

with open(root / "provenance/contribution_matrix.csv", newline="", encoding="utf-8") as f:
    provenance_rows = list(csv.reader(f))
if len(provenance_rows) < 2:
    print("Provenance contribution matrix has no data rows")
    sys.exit(1)


def read_dict_rows(rel):
    with open(root / rel, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

nominal = read_dict_rows("data/nominal_timeseries.csv")
broad = read_dict_rows("data/monte_carlo_unoptimized.csv")
design = read_dict_rows("data/monte_carlo_design_envelope.csv")

errors = []

if len(nominal) != 901:
    errors.append(f"nominal_timeseries.csv has {len(nominal)} rows; expected 901")
if len(broad) != 1000:
    errors.append(f"monte_carlo_unoptimized.csv has {len(broad)} rows; expected 1000")
if len(design) != 1000:
    errors.append(f"monte_carlo_design_envelope.csv has {len(design)} rows; expected 1000")

required_mc_columns = {
    "seed", "leak_reduction_pct", "flow_retention_pct",
    "isolation_time_s", "expected_sensor_effect_sigma", "pass_all"
}
for name, rows in (("broad", broad), ("design", design)):
    if not rows:
        errors.append(f"{name} Monte Carlo table is empty")
        continue
    missing_cols = required_mc_columns - set(rows[0].keys())
    if missing_cols:
        errors.append(f"{name} Monte Carlo missing columns: {sorted(missing_cols)}")


def truthy(value):
    return str(value).strip().lower() in {"true", "1", "yes"}

if broad:
    broad_rate = sum(truthy(r.get("pass_all")) for r in broad) / len(broad)
    expected = float(summary["broad_prior_pass_rate"])
    if not math.isclose(broad_rate, expected, abs_tol=1e-12):
        errors.append(f"broad pass rate {broad_rate:.6f} != summary {expected:.6f}")

if design:
    design_rate = sum(truthy(r.get("pass_all")) for r in design) / len(design)
    expected = float(summary["design_envelope_pass_rate"])
    if not math.isclose(design_rate, expected, abs_tol=1e-12):
        errors.append(f"design pass rate {design_rate:.6f} != summary {expected:.6f}")

status = str(summary.get("status", ""))
if "COMPUTATIONAL" not in status.upper() or "NOT PHYSICAL" not in status.upper():
    errors.append("simulation_summary.json must explicitly identify results as computational and not physical experiments")

if errors:
    print("Repository scientific-consistency validation failed:")
    for error in errors:
        print(" -", error)
    sys.exit(1)

print("Repository structure and scientific data consistency OK")
print(f"Nominal rows: {len(nominal)}")
print(f"Broad Monte Carlo: {len(broad)} trials, pass rate = {broad_rate:.3f}")
print(f"Design envelope: {len(design)} trials, pass rate = {design_rate:.3f}")
