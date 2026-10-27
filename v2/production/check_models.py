"""Independently check representative rendered-model data against small oracles."""
import sys,json,itertools
from pathlib import Path
from collections import deque
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from script_text import scenes
from art import model
r=Path(__file__).resolve().parents[1]
def get(name,i):
 direction,text=scenes((r/name).read_text())[i];return model(dict(source=name,scene=i,direction=direction,text=text))
# BFS states from independently built queue traversal; adjacency order is part of trace.
g=[[1,2],[0,3],[0,4],[1,5],[2,5],[3,4],[]];dist=[-1]*7;dist[0]=0;q=deque([0]);checks=0
for scene in range(4,10):
 u=q.popleft()
 for v in g[u]:
  if dist[v]==-1:dist[v]=dist[u]+1;q.append(v)
 m=get('part3_bfs_script.txt',scene);assert m['dist']==dist and m['queue']==list(q);checks+=1
# Every visible coin table entry is checked by denomination-multiplicity enumeration.
for scene in [4,8,9,10,11,12,13]:
 m=get('part3_dynamic_programming_script.txt',scene);coins=[4,6] if scene==13 else [1,3,4]
 for amount,value in enumerate(m['values']):
  if value=='?':continue
  choices=[sum(c) for c in itertools.product(*(range(amount//x+1) for x in coins)) if sum(x*k for x,k in zip(coins,c))==amount]
  expected=min(choices) if choices else '∞';assert value==expected,(scene,amount,value,expected);checks+=1
# Fenwick blocks computed by direct original-array slices, with both updates explicit.
for scene in [2,3,5,6,7,8,13]:
 m=get('part4_fenwick_script.txt',scene);a=[3,1,4,1,5,9,2,6]
 if scene in [6,7,8,13]:a[4]+=3
 if scene==13:a[0]-=2
 assert m['values']==a
 for i in range(1,9):assert m['bit'][i]==sum(a[i-(i&-i):i]);checks+=1
# Knapsack rows: all subsets of available items at each capacity.
items=[(2,3),(3,4),(4,5)]
for scene in [3,4,5]:
 m=get('part4_knapsack_script.txt',scene)
 for row in m['rows']:
  count=row[0]
  for capacity,value in enumerate(row[1:]):
   best=max(sum(items[j][1] for j in range(count) if mask>>j&1) for mask in range(1<<count) if sum(items[j][0] for j in range(count) if mask>>j&1)<=capacity)
   assert value==best;checks+=1
# Prefix model counts original slices directly.
m=get('part2_prefix_script.txt',5);a=[2,1,3,1,2,1]
for k,*counts in m['rows']:assert counts==[a[:k].count(x) for x in [1,2,3]];checks+=1
# Casework diagrams use an independent booth-contents representation.
for scene,start in [(3,2),(4,1),(5,3)]:
 m=get('part1_casework_script.txt',scene);booths=[1,2,3];score=0
 expected=[['initial',start,0]]
 for event,(a,b,guess) in enumerate([(1,2,1),(2,3,3),(1,3,1)]):
  booths[a-1],booths[b-1]=booths[b-1],booths[a-1]
  score+=booths[guess-1]==start;expected.append([event+1,booths.index(start)+1,score])
 assert m['rows']==expected;checks+=len(expected)
# Feasibility rows: enumerate all contiguous partitions rather than greedy packing.
weights=[3,2,2,4,1,4]
for lo,hi,mid,days,works in get('part2_binary_search_script.txt',9)['rows']:
 possible=[]
 for mask in range(1<<(len(weights)-1)):
  groups=[];total=weights[0]
  for j,w in enumerate(weights[1:]):
   if mask>>j&1:groups.append(total);total=w
   else:total+=w
  groups.append(total)
  if max(groups)<=mid:possible.append(len(groups))
 assert min(possible)==days and (works=='yes')==(days<=3);checks+=1
# Transfer questions must have no model solution rows/code anywhere.
questions=0
for part in json.loads((r/'course_manifest.json').read_text())['parts']:
 for name in part['scripts']:
  for i,(direction,text) in enumerate(scenes((r/name).read_text())):
   m=model(dict(source=name,scene=i,direction=direction,text=text))
   if m['question']:assert m['kind']=='question' and not m['code'] and 'rows' not in m;questions+=1
report=dict(passed=True,independent_numeric_checks=checks,hidden_question_models=questions,scope='BFS queue/distance,coin DP,Fenwick blocks,knapsack,prefix tables; question models across all sections',limits='Not all narration or rendered media; complete decode and sampled-frame review are separate.')
(r/'verification/course-models.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
