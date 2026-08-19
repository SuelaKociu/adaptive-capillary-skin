# ACS release and archival process

This document separates the **living GitHub repository** from a **frozen archival release**.

## Before a release

1. `main` must pass the `reproducibility-smoke-test` workflow.
2. Run `python scripts/validate_repository.py` and `python -m pytest -q` locally when possible.
3. Review `docs/limitations.md` and confirm no computational result is described as a physical measurement.
4. Confirm the final author metadata, ORCID if used, title, version and licensing information.
5. For Zenodo, reserve/obtain the DOI before freezing the final PDFs if the DOI is to appear on their title pages.

## Freeze the archival revision

1. Update README, CITATION metadata, Zenodo metadata and PDFs with the final DOI/version information.
2. Commit the frozen revision.
3. Create the version tag (for example `v0.1.0`).
4. The `release-integrity` workflow then:
   - validates repository structure and stored scientific data;
   - runs unit tests;
   - performs a fresh 1000 + 1000 Monte Carlo reproduction;
   - compares reproduced pass rates with the archived summary;
   - generates a fresh `SHA256SUMS.txt` from the exact tagged bytes;
   - stores the reproduction outputs and checksum manifest as a GitHub Actions artifact.

## Zenodo deposit

The repository uses mixed file-level licensing: MIT for code and CC BY 4.0 for non-code research content. The first Zenodo record should therefore be reviewed manually before publication so the archival object, licenses and metadata are represented accurately.

## Rule for checksums

Do not keep an old checksum file as an integrity gate on the moving `main` branch. A SHA-256 manifest is meaningful only for the exact frozen revision whose bytes it describes. Generate it at the tag/release stage with:

```bash
python scripts/generate_release_manifest.py --output SHA256SUMS.txt
```

The manifest is an integrity record, not evidence that the scientific model or a physical ACS device is valid.
