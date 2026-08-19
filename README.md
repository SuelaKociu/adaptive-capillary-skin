# Adaptive Capillary Skin (ACS)

**Open computational research package · v0.1.0 · 19 August 2026**

> **Scientific status:** computational / virtual design study only. No fabricated ACS prototype and no physical experimental measurements are claimed in this repository.

![ACS system architecture](figures/fig_00_system_architecture.png)

Adaptive Capillary Skin (ACS) is a biomimetic material-system concept in which a **single distributed capillary network** is proposed to couple environmental water transport, passive humidity response, evaporative heat transfer, electrokinetic state sensing, and damage-triggered local hydraulic isolation.

The central engineering hypothesis is deliberately narrow and falsifiable:

> **A local damage event can create the hydraulic perturbation that passively drives its own local isolation while redundant neighboring paths preserve useful flow.**

The repository also documents the **human–AI collaborative research process** that produced the project: an initial human analogy from natural liquid transport was iteratively expanded, criticized, formalized, simulated, exposed to failure, and converted into an open research package with explicit falsification gates.

## Why this repository exists

ACS is published as an open scientific design, not as a finished device. The goals are to:

- make the idea technically inspectable rather than rhetorical;
- expose the model assumptions and failure regions;
- make computational results reproducible;
- preregister conditions that would reject or force revision of the hypothesis;
- enable independent physical replication;
- preserve transparent provenance of human and AI contributions;
- provide a citable public technical record.

## Current computational result

The supplied v0.1 model translates the damage-isolation hypothesis into a low-order redundant hydraulic network. Under broad parameter sampling, the model frequently fails the complete gate. A refined design envelope derived from those failures performs far more robustly. These outputs define **candidate engineering requirements**, not measured device performance.

**Important model boundary:** v0.1 imposes the inlet-to-outlet pressure difference. It tests damage isolation and rerouting under a supplied hydraulic driving force; it does not yet simulate how a pump-free physical ACS would establish that pressure through capillarity, wetting, evaporation, gravity or atmospheric-water capture.

The numerical tables used in the manuscripts are available in [`data/`](data/). The decisive next step is a physical transparent-flow prototype tested under the preregistered protocol in [`docs/physical_validation_protocol.md`](docs/physical_validation_protocol.md).

## Repository map

| Path | Contents |
|---|---|
| [`src/acs/`](src/acs/) | Reproducible low-order computational model |
| [`tests/`](tests/) | Model smoke tests and invariants |
| [`data/`](data/) | Raw computational outputs, summary JSON and workbook |
| [`figures/`](figures/) | Publication figures |
| [`media/`](media/) | Virtual prototype explainer |
| [`paper/`](paper/) | Technical disclosure, manuscript and supplement |
| [`docs/`](docs/) | Architecture, falsification, physical validation, limitations and roadmap |
| [`hardware/`](hardware/) | V1 physical-prototype specification and candidate bill of materials |
| [`experiments/`](experiments/) | Preregistered physical-test templates |
| [`provenance/`](provenance/) | Human–AI contribution trace and contribution matrix |
| [`metadata/`](metadata/) | Zenodo metadata drafts |

## Reproduce the computational model

```bash
python -m venv .venv
# Linux/macOS
source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1

python -m pip install --upgrade pip setuptools wheel
python -m pip install -e '.[dev]'
python -m pip check
python scripts/validate_repository.py
python -m pytest -q
python scripts/run_model.py --trials 1000 --output reproduced_outputs
```

Random seeds are retained in the Monte Carlo tables. Reproduction should be judged against the stored output distributions, not against a claim of physical validation.

## Continuous verification

The normal GitHub Actions workflow checks repository structure, metadata, stored-data consistency, unit tests and a short reproduction run on every push and pull request. It can also be started manually with `workflow_dispatch`.

A separate `release-integrity` workflow is reserved for manual/tagged releases. It performs a full 1000 + 1000 trial reproduction and generates a SHA-256 manifest from the **exact frozen revision**. This avoids treating stale checksums from an evolving branch as evidence of integrity. See [`docs/release_process.md`](docs/release_process.md).

## Falsification gate

The v0.1 computational gate requires all of the following:

- late leak reduction **≥ 80%**;
- time to reach 80% leak reduction **≤ 600 s** after damage;
- useful outlet-flow retention **≥ 70%**;
- idealized sensing effect **≥ 5 assumed readout-noise standard deviations**.

The physical experiment adds controls for passive drainage, reservoir depletion, evaporation, false electrical signals and hydrogel-free geometry. See [`docs/falsification_protocol.md`](docs/falsification_protocol.md).

## Human–AI collaborative cognition study

ACS is also being used as a process-traced case study of scientific co-creation. The repository does **not** claim machine consciousness or biological human–machine evolution. It tests a narrower question: whether iterative coupling between heterogeneous human and artificial capabilities can transform an intuitive analogy into a more explicit, falsifiable and reproducible research object.

Start here:

- [`docs/human_ai_collaboration_study.md`](docs/human_ai_collaboration_study.md)
- [`provenance/curated_trace_2026-08-19.md`](provenance/curated_trace_2026-08-19.md)
- [`provenance/contribution_matrix.csv`](provenance/contribution_matrix.csv)

## Citation

Use [`CITATION.cff`](CITATION.cff). Once a Zenodo DOI is assigned, add it to this README, `CITATION.cff`, the final Zenodo metadata and the PDF title pages.

Suggested citation before DOI assignment:

> Kociu, S. (2026). *Adaptive Capillary Skin (ACS): Open Computational Design, Falsification Framework, and Human–AI Collaborative Research Record*, v0.1.0.

### Zenodo note

This repository intentionally uses **mixed file-level licenses**: MIT for code and CC BY 4.0 for non-code research content. For the first archival record, a **manual Zenodo deposit** is recommended so both licenses can be declared accurately. The working metadata is in [`metadata/zenodo_metadata_draft.json`](metadata/zenodo_metadata_draft.json). A GitHub-integration draft is retained only as reference in [`metadata/zenodo_github_integration_draft.json`](metadata/zenodo_github_integration_draft.json).

## Authorship and AI disclosure

**Concept and research responsibility:** Suela Kociu, Independent Researcher.

OpenAI ChatGPT (GPT-5.6 Sol) assisted with literature orientation, computational implementation, model construction, falsification design, visualization, repository preparation and manuscript drafting. The AI system is not listed as an author. Scientific responsibility, interpretation, decisions to publish, and future physical claims remain with the human author and any future human collaborators.

See [`provenance/README.md`](provenance/README.md) for the provenance policy.

## Licensing

- **Code** (`src/`, `scripts/`, `tests/`, GitHub workflows): MIT License.
- **Text, figures, data, video and reports**: Creative Commons Attribution 4.0 International (CC BY 4.0).

See [`LICENSE`](LICENSE) and [`LICENSES/`](LICENSES/).

## Patent / prior-art notice

This repository is intended as an **open technical disclosure**. Publication can be relevant to later patentability analyses, but this repository makes **no legal representation** that any specific claim is novel, patentable, non-patentable, or free to operate. The project has not received a professional patentability or freedom-to-operate opinion.

## Contributing

Physical replications, negative results, material-characterization data, model criticism and prior-art corrections are explicitly welcome. Please read [`CONTRIBUTING.md`](CONTRIBUTING.md) before opening an issue or pull request.
