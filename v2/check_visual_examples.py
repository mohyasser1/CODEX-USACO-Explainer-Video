"""Check exact scripted examples against previously oracle-tested programs."""
import json,subprocess
from pathlib import Path
root=Path(__file__).resolve().parent
examples=json.loads((root/'visual_contracts.json').read_text())['worked_examples']
for e in examples:
    p=subprocess.run(['/workspace/usaco-film-v2/'+e['program']],input=e['stdin'],text=True,capture_output=True)
    assert p.returncode==0 and p.stdout==e['stdout'],(e['id'],p.stdout,p.stderr)
print(f'PASS: {len(examples)} scripted input/output fixtures match runnable programs; intermediate states and media are not checked here.')
