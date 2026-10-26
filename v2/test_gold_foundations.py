"""Independent exhaustive/naive oracles for the standalone Part4 programs."""
import itertools,json,random,subprocess
from pathlib import Path
rng=random.Random(404);root=Path('/workspace/usaco-film-v2');counts={}
def run(name,text):
 p=subprocess.run([str(root/name)],input=text,text=True,capture_output=True)
 assert p.returncode==0,(name,p.stderr)
 counts[name]=counts.get(name,0)+1;return p.stdout
for _ in range(90):
 n=rng.randrange(11);items=[(rng.randrange(1,7),rng.randrange(13)) for _ in range(n)];capacity=rng.randrange(16)
 expected=max(sum(v for i,(w,v) in enumerate(items) if mask>>i&1) for mask in range(1<<n) if sum(w for i,(w,v) in enumerate(items) if mask>>i&1)<=capacity)
 assert int(run('knapsack01',f'{n} {capacity}\n'+''.join(f'{w} {v}\n' for w,v in items)))==expected
assert int(run('knapsack01','1 4\n2 3\n'))==3
assert int(run('knapsack01','100 100\n'+'1 1000000000\n'*100))==100000000000
for _ in range(90):
 n=rng.randrange(1,9);edges=[(rng.randrange(n),rng.randrange(n),rng.randrange(11)) for _ in range(rng.randrange(25))];start=rng.randrange(n);inf=10**18
 d=[[inf]*n for _ in range(n)]
 for i in range(n):d[i][i]=0
 for u,v,w in edges:d[u][v]=min(d[u][v],w)
 for k in range(n):
  for i in range(n):
   for j in range(n):d[i][j]=min(d[i][j],d[i][k]+d[k][j])
 text=f'{n} {len(edges)} {start}\n'+''.join(f'{u} {v} {w}\n' for u,v,w in edges)
 assert list(map(int,run('weighted_routes',text).split()))==[-1 if x==inf else x for x in d[start]]
for _ in range(75):
 n=rng.randrange(1,6);edges=[(rng.randrange(n),rng.randrange(n),rng.randrange(-4,10)) for _ in range(rng.randrange(9))];best=None
 for chosen in itertools.combinations(edges,n-1):
  g=[[] for _ in range(n)]
  for u,v,w in chosen:g[u].append(v);g[v].append(u)
  seen={0};todo=[0]
  for u in todo:
   for v in g[u]:
    if v not in seen:seen.add(v);todo.append(v)
  if len(seen)==n:
   weight=sum(w for u,v,w in chosen);best=weight if best is None else min(best,weight)
 out=run('minimum_network',f'{n} {len(edges)}\n'+''.join(f'{u} {v} {w}\n' for u,v,w in edges)).strip()
 assert out==('DISCONNECTED' if best is None else str(best))
for name,update in [('fenwick_queries','A'),('segment_queries','X')]:
 for _ in range(65):
  n=rng.randrange(25);initial=[rng.randrange(-15,16) for _ in range(n)];a=initial[:];ops=[];answers=[]
  for j in range(60):
   if n and rng.randrange(2):
    i=rng.randrange(n);x=rng.randrange(-15,16);ops.append(f'{update} {i} {x}');a[i]=a[i]+x if update=='A' else x
   else:
    l=rng.randrange(n+1);r=rng.randrange(l,n+1);ops.append(f'S {l} {r}');answers.append(sum(a[l:r]))
  text=f'{n} {len(ops)}\n'+' '.join(map(str,initial))+'\n'+'\n'.join(ops)+'\n'
  assert list(map(int,run(name,text).split()))==answers
for _ in range(65):
 n=rng.randrange(1,35);a=[rng.randrange(-50,51) for _ in range(n)];queries=[];answers=[]
 for j in range(30):
  l=rng.randrange(n);r=rng.randrange(l+1,n+1);queries.append((l,r));answers.append(min(a[l:r]))
 text=f'{n} {len(queries)}\n'+' '.join(map(str,a))+'\n'+''.join(f'{l} {r}\n' for l,r in queries)
 assert list(map(int,run('static_minimum',text).split()))==answers
# Large-integer boundary checks use direct formulas, not either tree algorithm.
initial=' '.join(['1000000000']*100000)
assert list(map(int,run('fenwick_queries','100000 3\n'+initial+'\nS 0 100000\nA 0 1000000000\nS 0 100000\n').split()))==[10**14,10**14+10**9]
assert list(map(int,run('segment_queries','100000 3\n'+initial+'\nS 0 100000\nX 0 -1000000000\nS 0 100000\n').split()))==[10**14,10**14-2*10**9]
report=dict(passed=True,seed=404,cases=counts,oracles=['all item subsets','Floyd-Warshall','all n-1 edge subsets with independent reachability','direct mutable-array sums','direct slice minima'])
(root/'output/gold-foundation-tests.json').write_text(json.dumps(report,indent=2));print(report)
