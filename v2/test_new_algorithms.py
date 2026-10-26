"""Exhaustive small assignment and bit-mask oracles, independent of traversals."""
import itertools,json,random,subprocess
from pathlib import Path
OUT=Path('/workspace/usaco-film-v2')
rng=random.Random(7139)
def run(name,text):
    p=subprocess.run([str(OUT/name)],input=text,text=True,capture_output=True)
    assert p.returncode==0,p.stderr
    return p.stdout.strip()
parity_cases=0
for n in range(1,8):
    for trial in range(35):
        edges=[(rng.randrange(n),rng.randrange(n),rng.randrange(2)) for _ in range(rng.randrange(15))]
        count=sum(all((bits[u]^bits[v])==p for u,v,p in edges) for bits in itertools.product((0,1),repeat=n))
        text=f'{n} {len(edges)}\n'+''.join(f'{"D" if p else "S"} {u+1} {v+1}\n' for u,v,p in edges)
        assert run('parity',text)==bin(count)[2:],(n,edges,count)
        parity_cases+=1
subset_cases=0
for a,target in [([],0),([],1),([5,-3],2),([0]*20,0),([10**9]*20,20*10**9)]+[
    ([rng.randrange(-5,6) for _ in range(rng.randrange(10))],rng.randrange(-10,11)) for _ in range(80)]:
    expected=sum(sum(x for i,x in enumerate(a) if mask>>i&1)==target for mask in range(1<<len(a)))
    assert int(run('subsets',f'{len(a)} {target}\n'+ ' '.join(map(str,a))+'\n'))==expected
    subset_cases+=1
report=dict(parity_cases=parity_cases,subset_cases=subset_cases,seed=7139,passed=True,
            oracle='enumeration of all binary colorings and all index masks')
(OUT/'output/new-algorithm-tests.json').write_text(json.dumps(report,indent=2))
print(report)
