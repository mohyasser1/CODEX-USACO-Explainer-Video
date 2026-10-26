"""Recompute authored trace data independently; no rendered-media validation."""
import json,itertools
from collections import deque
from pathlib import Path
root=Path(__file__).resolve().parent
examples=json.loads((root/'visual_contracts.json').read_text())['worked_examples']
checked=[]
for e in examples:
    lines=e['stdin'].splitlines(); data=list(map(int,lines[1].split())) if len(lines)>1 and not lines[1].startswith(('S','D')) else []
    expected={}
    if 'condition_states' in e:
        expected['condition_states']=[[i,sum(data[:i])] for i in range(len(data)+1)]
    if 'prefix_rows' in e:
        expected['prefix_rows']=[[data[:i].count(c) for c in (1,2,3)] for i in range(len(data)+1)]
    if 'search_rows' in e:
        n,limit=map(int,lines[0].split());lo=max(data);hi=sum(data);rows=[]
        while lo<hi:
            mid=(lo+hi)//2;days=1;load=0
            for w in data:
                if load+w>mid:days+=1;load=0
                load+=w
            rows.append(dict(lo=lo,hi=hi,mid=mid,days=days))
            if days<=limit:hi=mid
            else:lo=mid+1
        expected['search_rows']=rows
    if 'queues_after_processing' in e:
        n,m,s,t=map(int,lines[0].split());g=[[] for _ in range(n)]
        for line in lines[1:]:
            u,v=map(int,line.split());g[u].append(v);g[v].append(u)
        q=deque([s]);seen={s};rows=[]
        while q:
            u=q.popleft()
            for v in g[u]:
                if v not in seen:seen.add(v);q.append(v)
            rows.append(dict(vertex=u,queue=list(q)))
        expected['queues_after_processing']=rows
    if 'components' in e:
        n,m=map(int,lines[0].split());g=[[] for _ in range(n)];seen=set();count=0
        for line in lines[1:]:
            _,u,v=line.split();u=int(u)-1;v=int(v)-1;g[u].append(v);g[v].append(u)
        for s in range(n):
            if s in seen:continue
            count+=1;todo=[s];seen.add(s)
            for u in todo:
                for v in g[u]:
                    if v not in seen:seen.add(v);todo.append(v)
        expected['components']=count
    if 'dp' in e:
        _,target=map(int,lines[0].split());values=[]
        for amount in range(target+1):
            solutions=[sum(counts) for counts in itertools.product(*(range(amount//c+1) for c in data)) if sum(c*k for c,k in zip(data,counts))==amount]
            values.append(min(solutions) if solutions else -1)
        expected['dp']=values
    if 'rows' in e:
        n,capacity=map(int,lines[0].split());items=[tuple(map(int,l.split())) for l in lines[1:]];rows=[]
        for i in range(n+1):
            rows.append([max(sum(items[j][1] for j in range(i) if mask>>j&1) for mask in range(1<<i) if sum(items[j][0] for j in range(i) if mask>>j&1)<=c) for c in range(capacity+1)])
        expected['rows']=rows
    if 'bit_before' in e:
        def bit(a):return [0]+[sum(a[i-(i&-i):i]) for i in range(1,len(a)+1)]
        expected['bit_before']=bit(data)
        for line in lines[2:]:
            kind,i,x=line.split()
            if kind=='A':data[int(i)]+=int(x)
        expected['bit_after']=bit(data)
    fields=set(e)-{'id','program','stdin','stdout'}
    assert set(expected)==fields,(e['id'],'unchecked fields',fields-set(expected))
    for key,value in expected.items():
        assert e[key]==value,(e['id'],key,e[key],value)
        checked.append(e['id']+'.'+key)
report=dict(passed=True,checked_fields=checked,limitation='Authored data only; no animation, highlighting, audio or timing checked.')
(root/'verification/trace-state-tests.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
