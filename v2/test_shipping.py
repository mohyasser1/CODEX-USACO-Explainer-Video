"""Optimal-capacity oracle enumerates contiguous partitions, not greedy search."""
import random,subprocess,json
from pathlib import Path
rng=random.Random(902)
cases=[([3,2,2,4,1,4],3),([0],1),([0,0,0],2),([10**9]*8,1),([10**9]*8,8)]
cases += [([rng.randrange(10) for _ in range(n)],rng.randrange(1,n+1)) for n in range(1,9) for _ in range(15)]
for a,d in cases:
    best=sum(a)
    for cuts in range(1<<(len(a)-1)):
        if cuts.bit_count()+1>d:continue
        groups=[];load=a[0]
        for i,w in enumerate(a[1:]):
            if cuts>>i&1:groups.append(load);load=w
            else:load+=w
        groups.append(load);best=min(best,max(groups))
    p=subprocess.run(['/workspace/usaco-film-v2/shipping'],input=f'{len(a)} {d}\n'+' '.join(map(str,a))+'\n',text=True,capture_output=True)
    assert p.returncode==0 and int(p.stdout)==best,(a,d,best,p.stderr)
r=dict(cases=len(cases),passed=True,seed=902,oracle='all contiguous partitions using at most d groups')
Path('/workspace/usaco-film-v2/output/shipping-tests.json').write_text(json.dumps(r,indent=2));print(r)
