"""Independent multiplicity-vector enumeration, plus reconstructed-choice checks."""
import itertools,json,random,subprocess
from pathlib import Path
rng=random.Random(610)
cases=[([1,3,4],6),([4,6],5),([4,6],0),([7],14),([1,1,3],6),([1000000],3)]
for _ in range(100):cases.append(([rng.randrange(1,9) for _ in range(rng.randrange(1,5))],rng.randrange(19)))
for coins,target in cases:
    possible=[sum(counts) for counts in itertools.product(*(range(target//c+1) for c in coins)) if sum(c*k for c,k in zip(coins,counts))==target]
    expected=min(possible) if possible else -1
    p=subprocess.run(['/workspace/usaco-film-v2/minimum-coins'],input=f'{len(coins)} {target}\n'+' '.join(map(str,coins))+'\n',text=True,capture_output=True)
    assert p.returncode==0,p.stderr
    lines=p.stdout.splitlines();assert int(lines[0])==expected,(coins,target,p.stdout,expected)
    if expected>=0:
        chosen=list(map(int,lines[1].split()))
        assert len(chosen)==expected and sum(chosen)==target and all(c in coins for c in chosen)
# Upper target boundary: expected count is known without using the recurrence.
p=subprocess.run(['/workspace/usaco-film-v2/minimum-coins'],input='1 100000\n1\n',text=True,capture_output=True)
assert p.returncode==0 and p.stdout.splitlines()[0]=='100000'
report=dict(cases=len(cases)+1,passed=True,seed=610,oracle='exhaustive denomination multiplicities; independent boundary formula')
Path('/workspace/usaco-film-v2/output/coin-tests.json').write_text(json.dumps(report,indent=2));print(report)
