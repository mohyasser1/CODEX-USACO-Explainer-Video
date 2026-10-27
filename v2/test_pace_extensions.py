"""Independent brute-force/oracle tests for faster-course substantive additions."""
import json,random,subprocess,itertools
from pathlib import Path
rng=random.Random(2727);binroot=Path('/workspace/usaco-film-v2');counts={}
def run(name,text):
 p=subprocess.run([str(binroot/name)],input=text,text=True,capture_output=True);assert p.returncode==0,(name,text,p.stderr)
 counts[name]=counts.get(name,0)+1;return p.stdout
for s in ['', 'SWISS','BANANA','ZYX','AAAA','A']+[''.join(rng.choice('ABCDE') for _ in range(rng.randrange(35))) for _ in range(120)]:
 expected=next((i for i,c in enumerate(s) if s.count(c)==1),-1)
 assert int(run('first_unique',s+'\n'))==expected
for _ in range(100):
 n=rng.randrange(15);a=[rng.randrange(-10,11) for _ in range(n)];updated=a[:];updates=[];queries=[]
 for __ in range(rng.randrange(15)):
  l=rng.randrange(n+1);r=rng.randrange(l,n+1);d=rng.randrange(-5,6);updates.append((l,r,d))
  for i in range(l,r):updated[i]+=d
 for __ in range(10):
  l=rng.randrange(n+1);r=rng.randrange(l,n+1);queries.append((l,r))
 text=f'{n} {len(updates)} {len(queries)}\n'+' '.join(map(str,a))+'\n'+''.join(f'{l} {r} {d}\n' for l,r,d in updates)+''.join(f'{l} {r}\n' for l,r in queries)
 assert list(map(int,run('batch_dashboard',text).split()))==[sum(updated[l:r]) for l,r in queries]
text='100000 10000 1\n'+'1000000000 '*100000+'\n'+'0 100000 1000000\n'*10000+'0 100000\n'
assert int(run('batch_dashboard',text))==1100000000000000
for _ in range(100):
 h=rng.randrange(1,5);w=rng.randrange(2,5);n=h*w;s,t=rng.sample(range(n),2)
 grid=[['#' if rng.random()<.3 else '.' for c in range(w)] for r in range(h)]
 grid[s//w][s%w]='S';grid[t//w][t%w]='T';dist=[[999]*n for _ in range(n)]
 for u in range(n):
  if grid[u//w][u%w]=='#':continue
  dist[u][u]=0
  for v in range(n):
   if grid[v//w][v%w]!='#' and abs(u//w-v//w)+abs(u%w-v%w)==1:dist[u][v]=1
 for k in range(n):
  for i in range(n):
   for j in range(n):dist[i][j]=min(dist[i][j],dist[i][k]+dist[k][j])
 text=f'{h} {w}\n'+'\n'.join(''.join(row) for row in grid)+'\n';lines=run('grid_routes',text).splitlines();expected=dist[s][t] if dist[s][t]<999 else -1;assert int(lines[0])==expected
 if expected<0:assert len(lines)==1
 else:
  path=[tuple(map(int,l.split())) for l in lines[1:]];assert len(path)==expected+1 and path[0]==(s//w,s%w) and path[-1]==(t//w,t%w)
  assert all(0<=r<h and 0<=c<w and grid[r][c]!='#' for r,c in path)
  assert all(abs(a-c)+abs(b-d)==1 for (a,b),(c,d) in zip(path,path[1:]))
for a in [[],[2,2,2],[3,1,2,5,4,6],[2,3,1],[4,2,3,1,5]]+[[rng.randrange(-4,5) for _ in range(rng.randrange(12))] for _ in range(100)]:
 best=0
 for mask in range(1<<len(a)):
  seq=[x for i,x in enumerate(a) if mask>>i&1]
  if all(x<y for x,y in zip(seq,seq[1:])):best=max(best,len(seq))
 assert int(run('lis_length',str(len(a))+'\n'+' '.join(map(str,a))+'\n'))==best
assert int(run('lis_length','200000\n'+' '.join(map(str,range(200000)))+'\n'))==200000
report=dict(passed=True,seed=2727,cases=counts,oracles=['direct character count per position','direct element updates and interval sums','Floyd-Warshall plus path witness checks','all subsequences with strict-comparison check'],boundary_tests=['dashboard maximum stated positive accumulation1.1e15','LIS200000 increasing elements'])
Path('v2/verification/pace-extension-tests.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
