"""Floyd-Warshall oracle plus path validity; independent of queue traversal."""
import random,subprocess,json
from pathlib import Path
rng=random.Random(815)
cases=[(7,[(0,1),(0,2),(1,3),(2,4),(3,5),(4,5)],0,5),(1,[],0,0),(2,[],0,1)]
for _ in range(100):
    n=rng.randrange(1,12)
    edges=[(rng.randrange(n),rng.randrange(n)) for _ in range(rng.randrange(30))]
    cases.append((n,edges,rng.randrange(n),rng.randrange(n)))
for n,edges,start,target in cases:
    inf=n+1;dist=[[inf]*n for _ in range(n)]
    for i in range(n):dist[i][i]=0
    for u,v in edges:
        if u!=v:dist[u][v]=dist[v][u]=1
    for k in range(n):
        for i in range(n):
            for j in range(n):dist[i][j]=min(dist[i][j],dist[i][k]+dist[k][j])
    inp=f'{n} {len(edges)} {start} {target}\n'+''.join(f'{u} {v}\n' for u,v in edges)
    p=subprocess.run(['/workspace/usaco-film-v2/bfs-routes'],input=inp,text=True,capture_output=True)
    assert p.returncode==0,p.stderr
    lines=p.stdout.splitlines();expected=[-1 if d==inf else d for d in dist[start]]
    assert list(map(int,lines[0].split()))==expected
    if expected[target]==-1:assert lines[1]=='UNREACHABLE'
    else:
        path=list(map(int,lines[1].split()));assert path[0]==start and path[-1]==target and len(path)-1==expected[target]
        undirected=set(edges)|{(v,u) for u,v in edges}
        assert all((u,v) in undirected for u,v in zip(path,path[1:]))
report=dict(cases=len(cases),passed=True,seed=815,oracle='Floyd-Warshall distances plus edge/path validation')
Path('/workspace/usaco-film-v2/output/bfs-tests.json').write_text(json.dumps(report,indent=2));print(report)
