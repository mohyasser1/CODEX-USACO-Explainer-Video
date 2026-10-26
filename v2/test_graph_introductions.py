import itertools,json,random,subprocess
from pathlib import Path
rng=random.Random(612);root=Path('/workspace/usaco-film-v2');functional_cases=0;topo_cases=0
for n in range(1,9):
    for _ in range(8):
        nxt=[rng.randrange(n) for _ in range(n)]
        # Independently classify nodes by whether a positive number <=n of
        # successor steps returns to that node, then locate first cycle node.
        lengths={}
        for v in range(n):
            u=v
            for k in range(1,n+1):
                u=nxt[u]
                if u==v:lengths[v]=k;break
        for start in range(n):
            entry=start;tail=0
            while entry not in lengths:entry=nxt[entry];tail+=1
            p=subprocess.run([str(root/'functional-walk')],input=f'{n} {start}\n'+' '.join(map(str,nxt))+'\n',text=True,capture_output=True)
            assert p.returncode==0,p.stderr
            assert list(map(int,p.stdout.splitlines()[0].split()))==[tail,lengths[entry],entry]
            walk=list(map(int,p.stdout.splitlines()[1].split()))
            assert len(walk)==len(set(walk))==tail+lengths[entry] and walk[0]==start
            assert all(nxt[u]==v for u,v in zip(walk,walk[1:])) and nxt[walk[-1]]==entry
            functional_cases+=1
for n in range(1,7):
    for _ in range(12):
        edges=[(rng.randrange(n),rng.randrange(n)) for _ in range(rng.randrange(12))]
        def valid(order):
            pos={v:i for i,v in enumerate(order)}
            return all(pos[u]<pos[v] for u,v in edges)
        exists=any(valid(p) for p in itertools.permutations(range(n)))
        p=subprocess.run([str(root/'topological-order')],input=f'{n} {len(edges)}\n'+''.join(f'{u} {v}\n' for u,v in edges),text=True,capture_output=True)
        assert p.returncode==0,p.stderr
        if p.stdout.strip()=='IMPOSSIBLE':assert not exists
        else:
            order=list(map(int,p.stdout.split()));assert exists and sorted(order)==list(range(n)) and valid(order)
        topo_cases+=1
report=dict(functional_cases=functional_cases,topological_cases=topo_cases,passed=True,seed=612,
            oracles=['independent cycle-membership/self-return checks','exhaustive vertex permutations'])
(root/'output/graph-introduction-tests.json').write_text(json.dumps(report,indent=2));print(report)
