#!/usr/bin/env python3
from pathlib import Path
import json, csv, sys

root=Path(__file__).resolve().parents[1]
required=[
 'README.md','CITATION.cff','.zenodo.json','pyproject.toml',
 'src/acs/model.py','data/simulation_summary.json',
 'docs/falsification_protocol.md','provenance/contribution_matrix.csv'
]
missing=[p for p in required if not (root/p).exists()]
if missing:
    print('Missing required files:', *missing, sep='\n - '); sys.exit(1)
json.loads((root/'.zenodo.json').read_text(encoding='utf-8'))
json.loads((root/'data/simulation_summary.json').read_text(encoding='utf-8'))
with open(root/'provenance/contribution_matrix.csv',newline='',encoding='utf-8') as f:
    rows=list(csv.reader(f))
assert len(rows) >= 2
print('Repository structure OK')
