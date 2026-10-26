"""Independent Python integer-sum oracle, boundary and invalid-input checks."""
import json, random, subprocess
from pathlib import Path
exe = '/workspace/usaco-film-v2/signed-total'
rng = random.Random(20261026)
cases = [[], [3,-2,5,-1], [-4,0,7,-3], [1000000000]*100000,
         [-1000000000]*100000, [0], [-1000000000,1000000000]]
cases += [[rng.randrange(-10**9,10**9+1) for _ in range(rng.randrange(101))] for _ in range(100)]
for a in cases:
    p = subprocess.run([exe], input=str(len(a))+'\n'+' '.join(map(str,a))+'\n', text=True, capture_output=True)
    assert p.returncode == 0 and p.stdout.strip() == str(sum(a)), (a[:10],p.stderr)
for text in ['-1\n', '100001\n', '1\n1000000001\n', '2\n3\n', '']:
    p = subprocess.run([exe], input=text, text=True, capture_output=True)
    assert p.returncode == 1, p.stderr
report = dict(valid_cases=len(cases), invalid_cases=5, seed=20261026,
              oracle='Python arbitrary-precision sum', sanitizers='address,undefined', passed=True)
Path('/workspace/usaco-film-v2/output/pilot-code-tests.json').write_text(json.dumps(report, indent=2))
print(report)
