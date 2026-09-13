from pathlib import Path
import json
root=Path(__file__).resolve().parents[1]
for p in root.glob('contracts/jsonschema/*.json'): json.loads(p.read_text())
manifest=json.loads((root/'industry-packs/manufacturing/manifest.json').read_text())
assert manifest['packId']
required=['CONSTITUTION.md','ARCHITECTURE.md','docs/00-START-HERE.md','docs/20-HARDWARE-AND-CAPACITY.md']
for r in required: assert (root/r).exists(), r
print('repository validation: ok')
