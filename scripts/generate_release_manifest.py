#!/usr/bin/env python3
"""Generate SHA-256 checksums for a frozen ACS release.

This script is intentionally separate from normal CI. The main branch is a
living research record, so checksums are generated only when a revision is
being frozen for a tag/archival release.
"""

from pathlib import Path
import argparse
import hashlib

ROOT = Path(__file__).resolve().parents[1]

RELEASE_PATHS = [
    "data/Adaptive_Capillary_Skin_Simulation_Data.xlsx",
    "data/evaporative_cooling_prediction.csv",
    "data/falsification_parameter_grid.csv",
    "data/fog_collection_bounding_predictions.csv",
    "data/hygromorphic_gate_prediction.csv",
    "data/key_results.csv",
    "data/monte_carlo_design_envelope.csv",
    "data/monte_carlo_unoptimized.csv",
    "data/nominal_timeseries.csv",
    "data/simulation_summary.json",
    "docs/architecture.md",
    "docs/falsification_protocol.md",
    "docs/human_ai_collaboration_study.md",
    "docs/limitations.md",
    "docs/open_science_and_defensive_publication.md",
    "docs/physical_validation_protocol.md",
    "docs/prior_art_scope.md",
    "docs/research_roadmap.md",
    "experiments/templates/physical_run_template.csv",
    "experiments/templates/specimen_metadata.json",
    "figures/fig_00_system_architecture.png",
    "figures/fig_01_nominal_flow.png",
    "figures/fig_02_sensor_signal.png",
    "figures/fig_03_monte_carlo.png",
    "figures/fig_04_falsification_map.png",
    "figures/fig_05_hygromorphic_gate.png",
    "figures/fig_06_cooling_prediction.png",
    "hardware/BOM_V1.csv",
    "hardware/PROTOTYPE_SPEC_V1.md",
    "media/adaptive_capillary_skin_virtual_prototype.mp4",
    "paper/Adaptive_Capillary_Skin_Journal_Manuscript_v0.1.pdf",
    "paper/Adaptive_Capillary_Skin_Supplementary_Information_v0.1.pdf",
    "paper/Adaptive_Capillary_Skin_Zenodo_Technical_Disclosure_v0.1.pdf",
    "provenance/README.md",
    "provenance/contribution_matrix.csv",
    "provenance/curated_trace_2026-08-19.md",
    "scripts/run_model.py",
    "scripts/validate_repository.py",
    "src/acs/model.py",
    "tests/test_model.py",
]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="SHA256SUMS.txt")
    args = parser.parse_args()

    missing = [rel for rel in RELEASE_PATHS if not (ROOT / rel).is_file()]
    if missing:
        raise SystemExit("Missing release files:\n - " + "\n - ".join(missing))

    lines = [f"{sha256(ROOT / rel)}  {rel}" for rel in sorted(RELEASE_PATHS)]
    output = ROOT / args.output
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {len(lines)} SHA-256 entries to {output.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
