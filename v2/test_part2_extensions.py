import itertools,json,random,subprocess
from pathlib import Path
rng=random.Random(216);root=Path('/workspace/usaco-film-v2');counts={}
def run(name,text):
 p=subprocess.run([str(root/name)],input=text,text=True,capture_output=True)
 assert p.returncode==0,(name,p.stderr)
 counts[name]=counts.get(name,0)+1
 return p.stdout
for a,target in [([],0),([1500000000]*2,3000000000),([-1500000000]*2,-3000000000),([4],8),([4,4],8)]+[([rng.randrange(-20,21) for _ in range(rng.randrange(16))],rng.randrange(-40,41)) for _ in range(100)]:
 out=run('two-sum',f'{len(a)} {target}\n'+' '.join(map(str,a))+'\n').strip()
 pairs=[(i,j) for i in range(len(a)) for j in range(i+1,len(a)) if a[i]+a[j]==target]
 if out=='NONE':assert not pairs
 else:
  i,j=map(int,out.split());assert i!=j and 0<=i<len(a) and 0<=j<len(a) and a[i]+a[j]==target
for _ in range(100):
 a=[rng.randrange(8) for _ in range(rng.randrange(20))];limit=rng.randrange(20)
 expected=max([r-l for l in range(len(a)+1) for r in range(l,len(a)+1) if sum(a[l:r])<=limit])
 assert int(run('window',f'{len(a)} {limit}\n'+' '.join(map(str,a))+'\n'))==expected
for _ in range(100):
 n=rng.randrange(20);a=[0]*n;updates=[]
 for j in range(rng.randrange(20)):
  l=rng.randrange(n+1);r=rng.randrange(l,n+1);x=rng.randrange(-10,11);updates.append((l,r,x))
  for i in range(l,r):a[i]+=x
 out=run('differences',f'{n} {len(updates)}\n'+''.join(f'{l} {r} {x}\n' for l,r,x in updates))
 assert list(map(int,out.split()))==a
for _ in range(60):
 rows=rng.randrange(1,7);cols=rng.randrange(1,7);a=[[rng.randrange(-9,10) for _ in range(cols)] for _ in range(rows)];queries=[];answers=[]
 for j in range(15):
  r1=rng.randrange(rows+1);r2=rng.randrange(r1,rows+1);c1=rng.randrange(cols+1);c2=rng.randrange(c1,cols+1)
  queries.append((r1,c1,r2,c2));answers.append(sum(a[r][c] for r in range(r1,r2) for c in range(c1,c2)))
 text=f'{rows} {cols} {len(queries)}\n'+'\n'.join(' '.join(map(str,row)) for row in a)+'\n'+'\n'.join(' '.join(map(str,q)) for q in queries)+'\n'
 assert list(map(int,run('rectangles',text).split()))==answers
for _ in range(80):
 events=[]
 for j in range(rng.randrange(10)):
  start=rng.randrange(10);events.append((start,start+rng.randrange(1,8)))
 best=0
 for mask in range(1<<len(events)):
  chosen=sorted(events[i] for i in range(len(events)) if mask>>i&1)
  if all(a[1]<=b[0] for a,b in zip(chosen,chosen[1:])):best=max(best,len(chosen))
 out=run('intervals',str(len(events))+'\n'+''.join(f'{a} {b}\n' for a,b in events)).splitlines()
 ids=list(map(int,out[1].split()));assert int(out[0])==best==len(ids)==len(set(ids))
 assert all(0<=i<len(events) for i in ids)
 assert all(events[a][1]<=events[b][0] for a,b in zip(ids,ids[1:]))
report=dict(passed=True,seed=216,cases=counts,oracles='all pairs; all subarrays; direct updates; direct rectangles; all interval subsets')
(root/'output/part2-extension-tests.json').write_text(json.dumps(report,indent=2));print(report)
