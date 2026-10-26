"""Direct interval scan oracle independent of prefix preprocessing."""
import json,random,subprocess
from pathlib import Path
root=Path('/workspace/usaco-film-v2')
rng=random.Random(304)
cases=[([2,1,3,1,2,1],[(1,6),(2,5),(3,3)]),([1],[(1,1)]),([3]*100000,[(1,100000),(100000,100000)]),([2],[])]
for _ in range(100):
    a=[rng.randrange(1,4) for _ in range(rng.randrange(1,70))]
    queries=[]
    for _ in range(30):
        l=rng.randrange(1,len(a)+1);r=rng.randrange(l,len(a)+1);queries.append((l,r))
    cases.append((a,queries))
for a,queries in cases:
    text=f'{len(a)} {len(queries)}\n'+' '.join(map(str,a))+'\n'+''.join(f'{l} {r}\n' for l,r in queries)
    p=subprocess.run([str(root/'prefix-counts')],input=text,text=True,capture_output=True)
    expected=[' '.join(str(a[l-1:r].count(c)) for c in (1,2,3)) for l,r in queries]
    assert p.returncode==0 and p.stdout.splitlines()==expected,(a[:10],queries[:3],p.stderr)
report=dict(cases=len(cases),queries=sum(len(q) for _,q in cases),oracle='direct Python slice counts',seed=304,passed=True)
(root/'output/prefix-tests.json').write_text(json.dumps(report,indent=2));print(report)
