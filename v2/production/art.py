"""Authored paragraph-level models. They are result/trace panels, not word clocks."""
import re
BASE_BFS=[(0,1),(0,2),(1,3),(2,4),(3,5),(4,5)]
BFS_STATES={2:([-1]*7,[]),3:([0,-1,-1,-1,-1,-1,-1],[0]),4:([0,1,1,-1,-1,-1,-1],[1,2]),5:([0,1,1,2,-1,-1,-1],[2,3]),6:([0,1,1,2,2,-1,-1],[3,4]),7:([0,1,1,2,2,3,-1],[4,5]),8:([0,1,1,2,2,3,-1],[5]),9:([0,1,1,2,2,3,-1],[])}
SNIPPETS={
'loop_trace':['long long total = 0;','for (int i=0; i<n; ++i) {','    total += a[i];','}','cout << total << "\\n";'],
'string_lab':['// Inside main; s was read', 'array<int,26> frequency{};', "for (char c:s) ++frequency[c-'A'];", 'for (int i=0;i<(int)s.size();++i)', "  if (frequency[s[i]-'A']==1) {", "    cout << i << '\\n'; return 0;", '  }', "cout << -1 << '\\n';"],
'prefix':['prefix[i+1] = prefix[i];','++prefix[i+1][category-1];','// Inclusive positions l..r:','answer[c] = prefix[r][c]-prefix[l-1][c];'],
'binary_search':['while (lo < hi) {','    auto mid = lo + (hi-lo)/2;','    if (feasible(mid)) hi = mid;','    else lo = mid + 1;','}'],
'bfs':['int u = pending.front();','pending.pop();','for (int v : graph[u])','  if (distance[v] == -1) {','    distance[v] = distance[u] + 1;','    parent[v]=u; pending.push(v); }'],
'dynamic_programming':['dp[0] = 0;','for (int x=1; x<=target; ++x)','  for (int c : coins)','    if (c<=x && dp[x-c]!=INF)','      dp[x]=min(dp[x],1+dp[x-c]);'],
'knapsack':['for (auto [weight,value] : items)','  for (int c=capacity; c>=weight; --c)','    dp[c]=max(dp[c],','              dp[c-weight]+value);'],
'lis_lab':['auto it=lower_bound(tails.begin(),','                    tails.end(), x);','if (it==tails.end()) tails.push_back(x);','else *it=x;','// tails.size() is the LENGTH'],
'fenwick':['// add at external position p','for (int i=p+1; i<=n; i+=i&-i)','    bit[i] += delta;','// sum first r values','for (int i=r; i>0; i-=i&-i)','    answer += bit[i];'],
'dijkstra':['auto [du,u] = heap.top(); heap.pop();','if (du != distance[u]) continue;','// Relax each nonnegative edge u->v','if (du+w < distance[v]) {','    distance[v]=du+w;','    heap.push({distance[v],v}); }'],
'dashboard_lab':['diff[l] += delta; diff[r] -= delta;','active += diff[i];','a[i] += active;','prefix[i+1] = prefix[i] + a[i];','answer = prefix[r] - prefix[l];'],
'grid_lab':['nr=r+dr[k]; nc=c+dc[k];','if (nr<0 || nr>=h || nc<0 || nc>=w)','    continue;','if (grid[nr][nc]==\'#\') continue;','// Discover only if distance==-1'],
}
def topic(source):return re.sub(r'^part\d_','',source).replace('_script.txt','')
def is_question(text):return any(w in text.lower() for w in ['pause and','pause the video','pause for','transfer task:'])

def model(c):
 t=topic(c['source']);i=c['scene'];question=is_question(c['text']);d=dict(topic=t,kind='concept',label='MODEL / REASONING',notes='',question=question,code=SNIPPETS.get(t,[]))
 if question:
  d.update(kind='question',label='YOUR TURN · INPUT ONLY',notes='Pause the video to work through the question.\nThe next scene contains the answer.',code=[])
  inputs={'loop_trace':[-4,0,7,-3],'binary_search':[4,1,1],'prefix':[2,1,3,1,2,1],'two_pointers':[11,1,7,2,4],'functional_graph':[1,2,2],'fenwick':[3,1,4,1,8,9,2,6],'lis_lab':[4,2,3,1,5],'dashboard_lab':[1,0,2]}
  if t in inputs:d['question_model']=dict(kind='array',values=inputs[t],index_start=1 if t=='prefix' else 0)
  if t=='grid_lab':d['question_model']=dict(kind='grid',grid=['S#.','..T'],dist={})
  if t=='bfs':d['question_model']=dict(kind='graph',n=7,edges=BASE_BFS+[(5,6)],dist=[None]*7,queue=[])
  from learner_panels import apply
  return apply(d,c)
 if t=='foundations':
  if i==3:d.update(kind='rows',label='FIRST COMPLETE C++17 PROGRAM',rows=[['read','two long long integers'],['compute','their sum'],['print','answer and newline']],code=['#include <iostream>','int main() {','  long long a, b;','  std::cin >> a >> b;','  std::cout << a+b << "\\n";','}'])
  if i==6:d.update(kind='rows',rows=[['int count','0'],['long long price','3000000000'],['bool open','true']],label='NAME · TYPE · VALUE')
  if i==7:d.update(kind='rows',rows=[['old count','2'],['evaluate count+1','3'],['store in count','3']],code=['count = count + 1;','// Assignment changes state','bool same = (count == 3);','// Comparison produces a bool'])
  if i==8:d.update(kind='rows',rows=[['int operands','1500000000 + 1500000000'],['unsafe expression','int + int overflows'],['promote first','1LL*a + b = 3000000000']],code=['int a=1500000000, b=1500000000;','long long good = 1LL*a + b;','// WRONG: long long bad = a+b;'])
  if i==11:d.update(kind='table',headers=['x','x<0','x%2==0','both'],rows=[[-4,'true','true','true'],[-3,'true','false','false'],[0,'false','true','false']],label='AND REQUIRES BOTH CONDITIONS')
  if i==13:d.update(kind='array',values=list('BANANA'),label='STRING · SIX CHARACTERS',small='Length = 6; count of A = 3')
  if i==15:d.update(kind='rows',label='FIRST ATTEMPT · INCORRECT',rows=[['receipts','+3, -2, +5, -1'],['positive-only program','3 + 5 = 8'],['actual net total','3 - 2 + 5 - 1 = 5'],['mistake','refunds were discarded']],code=['// WRONG for a signed total','if (x > 0) total += x;'])
 elif t=='functions_cost':
  if i==1:d.update(kind='rows',rows=[['caller before','x = 7'],['local parameter','value: 7 → 8'],['caller after','x = 7']],code=['void bump(int value) {','  ++value;','}','int x=7;','bump(x); // x is still 7'])
  if i==2:d.update(kind='rows',rows=[['caller before','x = 7'],['reference parameter','alias of caller x'],['caller after','x = 8']],code=['void bump(int& value) {','  ++value;','}','int x=7;','bump(x); // x is now 8'])
 elif t=='loop_trace':
  d.update(kind='rows',label='SIGNED TOTAL · TRACE',rows=[['input','3, -2, 5, -1'],['count','4'],['answer','5']])
  if i in [1]:d['rows']=[['read count','n = 4'],['create slots','vector<int> a(n)'],['read values','for (int& x:a) cin >> x;']];d['code']=[]
  if i in [2,8]:d['rows']=[['index','0'],['total','0'],['processed prefix','empty']]
  if i==3:d['rows']=[['check','i=0, total=0; 0<4'],['add','0+3=3; i still0'],['increment','i becomes1']]
  if i==4:d['rows']=[['check','i=1, total=3; 1<4'],['add','3+(-2)=1'],['increment','i becomes2']]
  if i==5:d['rows']=[['index2','1+5=6'],['index3','6-1=5'],['final check','i=4; 4<4 false'],['output','5']]
  if i==6:d.update(code=[],rows=[['wrong condition','i <= n'],['extra index','i=4 with n=4'],['access a[4]','OUT OF BOUNDS'],['valid indices','0,1,2,3']],label='COUNTEREXAMPLE · INVALID EXTRA ITERATION')
  if i in [7,9,10]:d['rows']=[['invariant','total = sum of first i values'],['preserve','add a[i], then increment i'],['finish','i=n; whole input processed']]
  if i==11:d['rows']=[['new input','n=0; a=[]'],['initial state','i=0,total=0'],['condition','0<0 false'],['output','0']]
  if i==15:d['rows']=[['i','0  1  2  3  4'],['total','0 -4 -4  3  0']]
 elif t=='bfs':
  dist,q=BFS_STATES.get(i,([None]*7,[]));edges=list(BASE_BFS)
  if i==16:edges.append((5,6));dist=[0,1,1,2,2,3,4]
  d.update(kind='graph',n=7,edges=edges,dist=dist,queue=q,label='ROOM GRAPH · ONE STEP PER EDGE')
  if i==12:d['path']=[0,1,3,5]
  if i==16:d['label']='TRANSFER · AFTER ADDING EDGE 5–6'
 elif t=='dynamic_programming':
  values=[0]+['?']*6;upto={4:0,8:2,9:3,10:5,11:6,12:6}.get(i,0)
  for j in range(upto+1):values[j]=[0,1,2,1,1,2,2][j]
  d.update(kind='array',values=values,label='dp[x] · MINIMUM TOKEN COUNT',index_label='amount',small='Denominations: 1, 3, 4')
  if i==13:d.update(values=[0,'∞','∞','∞',1,'∞'],small='New denominations: 4, 6; target5')
  if i==17:d.update(kind='rows',rows=[['target7','2 + 5: two tokens'],['target3','unreachable'],['supply','unlimited copies']])
 elif t=='fenwick':
  a=[3,1,4,1,5,9,2,6]
  if i in [6,7,8,12,13]:a[4]+=3
  if i==13:a[0]-=2
  bit=[0]+[sum(a[j-(j&-j):j]) for j in range(1,9)]
  d.update(kind='fenwick',values=a,bit=bit,label='FENWICK BLOCKS · EXTERNAL INDICES',active=[5,6,8] if i==6 else [7,6,4] if i in [3,7] else [])
  if i==8:d.update(code=[],notes='Internal update path: 5 = 0101 → 6 = 0110 → 8 = 1000.\nSkipped 7 = 0111 covers only position7, not position5.\nEach visited block contains the updated point.')
  if i==9:d.update(kind='rows',rows=[['assignment','old5 → new8'],['delta','8-5=3'],['wrong add8','old5+8=13']])
 elif t=='prefix':
  a=[2,1,3,1,2,1];rows=[[k]+[a[:k].count(x) for x in [1,2,3]] for k in range(7)]
  d.update(kind='table',headers=['boundary','cat1','cat2','cat3'],rows=rows,label='PREFIX COUNTS · FIXED LINE')
  if i==4:d['rows']=rows[:4]+[['wrong P4',1,0,0]];d['label']='WRONG CANDIDATE · DOES NOT COPY PREFIX'
  if i==11:d.update(kind='array',values=[2,3,3,1,2,1],label='CHANGED INPUT · OLD PREFIX TABLE STALE',index_label='position',index_start=1)
 elif t=='knapsack':
  rows=[[0]*6,[0,0,3,3,3,3],[0,0,3,4,4,7],[0,0,3,4,5,7]]
  limit={3:2,4:3,5:4}.get(i,1)
  d.update(kind='table',headers=['items','c0','c1','c2','c3','c4','c5'],rows=[[j]+row for j,row in enumerate(rows[:limit])],label='0/1 KNAPSACK · AT MOST CAPACITY')
  if i==8:d.update(kind='rows',rows=[['one item','weight2,value3; capacity4'],['ascending wrong','dp2=3; dp4=6 (reuse!)'],['descending correct','dp4=3; dp2=3']])
  if i==10:d.update(kind='rows',rows=[['new capacity','4'],['density-first','take(3,5):value5'],['better pair','(2,3)+(2,3):value6']])
  if i==9:d.update(kind='concept',code=[])
  if i==13:d.update(kind='rows',rows=[['capacity3','best value5'],['capacity0 / no items','best value0']])
 elif t=='dijkstra':
  edges=[(0,1,10),(0,2,3),(2,1,4),(1,3,2),(2,3,12)];dist={1:[0,'∞','∞','∞'],2:[0,10,3,'∞'],3:[0,7,3,15],4:[0,7,3,9]}.get(i,[None]*4)
  if i==6:edges=[(0,1,2),(0,2,5),(2,1,-4)];dist=[0,1,5]
  d.update(kind='graph',n=3 if i==6 else 4,edges=edges,dist=dist,directed=True,label='WEIGHTED DIRECTED GRAPH',queue=[])
  if i==12:d.update(kind='rows',rows=[['new edge cost8','best route cost8'],['new edge cost12','old route cost9 wins']])
 elif t=='binary_search':
  rows=[[4,16,10,2,'yes'],[4,10,7,3,'yes'],[4,7,5,4,'no'],[6,7,6,3,'yes']]
  d.update(kind='array',values=[3,2,2,4,1,4],label='ORDERED BOXES · AT MOST THREE TRIPS',index_label='box')
  if 7<=i<=9:d.update(kind='table',headers=['lo','hi','mid','trips','works'],rows=rows[:{7:1,8:3,9:4}[i]],label='BINARY SEARCH TRACE')
  if i==13:d.update(kind='rows',rows=[['new weights','4,1,1'],['two trips','minimum capacity4'],['one / three trips','6 / 4'],['all zero weights','capacity0']])
 elif t=='two_pointers':
  a=[1,2,4,7,11] if i<7 else [2,1,1,3,1];d.update(kind='array',values=a,label='SORTED PAIR · TARGET9' if i<7 else 'CONTIGUOUS WINDOW · LIMIT4',index_label='index',active=[0,4] if i<2 else [1,3] if i<7 else [])
  if i==4:d.update(kind='rows',rows=[['two positions','[4,4] can make8'],['one position','[4] cannot use itself twice']])
  if i==11:d.update(values=[5,-2],label='NEGATIVE-INPUT COUNTEREXAMPLE · LIMIT3')
  if i==13:d.update(kind='rows',rows=[['pair original indices','2 and3; values7+2=9'],['zero window','length3']])
 elif t=='grid_lab':
  grid=['S..#','.#..','...T'];dist={0:0}
  if i>=4:dist.update({1:1,4:1})
  if i>=5:dist.update({2:2,8:2})
  if i>=6:dist.update({6:3,9:3,7:4,10:4,11:5})
  d.update(kind='grid',grid=grid,dist=dist,label='GRID BFS · COORDINATES (ROW,COLUMN)')
  if i==14:d.update(kind='grid_compare',grids=[['S#.','..T'],['S#.','.#T']],case_labels=['Original: distance 3','Block (1,1): unreachable'],code=[],label='TRANSFER · TWO SEPARATE CASES',notes='Original route: (0,0) → (1,0) → (1,1) → (1,2).\nAfter blocking (1,1), the target has no route from S.')
 elif t=='lis_lab':
  d.update(kind='array',values=[3,1,2,5,4,6],label='STRICT LIS · KEEP ORIGINAL ORDER',index_label='index')
  if i==3:d.update(kind='table',headers=['value',3,1,2,5,4,6],rows=[['DP length',1,1,2,3,3,4]],label='QUADRATIC ENDING-LENGTH DP')
  if i==7:d.update(kind='rows',rows=[['3 →1','[3] → [1]'],['then2,5','[1,2] → [1,2,5]'],['then4,6','[1,2,4] → [1,2,4,6]']],label='MINIMUM-TAIL TRACE')
  if i==9:d.update(values=[2,2,2],label='STRICT DUPLICATES · LENGTH1')
  if i==11:d.update(kind='rows',rows=[['input','2,3,1'],['tails','1,3'],['actual witness','2,3; tails is not a witness']])
  if i==14:d.update(kind='rows',rows=[['DP','1,1,2,1,3'],['tails','1,3,5 (not a witness)'],['real witness','2,3,5; length3'],['equal fives','strict1; nondecreasing3']])
 elif t=='dashboard_lab':
  d.update(kind='rows',rows=[['original','2,1,3,0,4'],['updates','+2 on[1,4); -1 on[2,5)'],['timeline','ALL updates before queries']],label='BATCH DASHBOARD')
  if i in [3,4,5,6,7,8,9]:d['rows']=[['events','0,2,-1,0,-2,1'],['active','0,2,1,1,-1'],['final','2,3,4,1,3'],['prefix','0,2,5,9,10,13']]
  if i==13:d['rows']=[['final','4,1,0'],['prefix','0,4,5,5'],['queries','5 and1']]
 elif t=='string_lab':
  d.update(kind='array',values=list('SWISS'),label='FIND FIRST GLOBALLY UNIQUE POSITION',index_label='index')
  if i in [4,5,6]:d.update(kind='rows',rows=[['counts','S:3  W:1  I:1'],['scan index0','S repeats →skip'],['scan index1','W occurs once →answer1']])
  if i==13:d.update(kind='rows',rows=[['new contract','first second occurrence'],['SWISS','second S arrives at index3'],['old contract','globally unique first position1']])
  if i==12:d.update(kind='rows',rows=[['empty / A / AAAA','-1 / 0 / -1'],['BANANA / ZYX','0 / 0'],['order','positions, not alphabet']])
 elif t=='functional_graph':
  d.update(kind='graph',n=5,edges=[(0,1),(1,2),(2,3),(3,1),(4,4)],directed=True,dist=[None]*5,queue=[],label='ONE SUCCESSOR PER VERTEX')
  if i==7:d.update(n=3,edges=[(0,1),(1,2),(2,2)],dist=[None]*3,label='TRANSFER · 0 → 1 → 2 → 2',notes='Start0: tail length2, cycle length1.\nStart2: tail length0, cycle length1.')
 elif t=='parity':
  edges=[(0,1,'S'),(1,2,'D')]+([(0,2,'S')] if i in [6,7] else [])
  d.update(kind='graph',n=4,edges=edges,dist=[0,0,1,'?'] if i>=3 else [None]*4,queue=[],label='SAME / DIFFERENT CONSTRAINTS · GROUPS1..4',node_offset=1)
  if i==14:d.update(kind='rows',rows=[['all-D triangle','impossible'],['path plus isolated','4 assignments = binary100']])
 elif t=='topological':
  d.update(kind='graph',n=5,edges=[(0,2),(1,2),(2,3),(1,4)]+([(3,1)] if i==4 else []),directed=True,dist=[None]*5,queue=[],label='PREREQUISITE → DEPENDENT')
  if i==6:d.update(kind='rows',rows=[['original edge 1→4','task4 waits for task1'],['remove edge 1→4','task4 is ready initially'],['valid output','every remaining edge respected'],['cost','O(n+m) time and space']],label='TRANSFER · REMOVE ONE PREREQUISITE')
 elif t=='dsu_mst':d.update(kind='graph',n=4,edges=[(0,1,1),(1,2,2),(0,2,3),(2,3,4),(0,3,10)],dist=[None]*4,queue=[],label='MINIMUM NETWORK · CHOOSE EDGES',path=[0,1,2,3] if i>=2 else [])
 elif t=='segment_sparse':
  d.update(kind='array',values=[3,1,10 if i in [4,5] else 4,1,5],label='RANGE SUM TREE · POINT ASSIGNMENT',index_label='index')
  if i==1:d.update(kind='rows',rows=[['leaves','3,1,4,1,5,0,0,0'],['pairs','4,5,5,0'],['halves','9,5'],['root','14']],label='SUM TREE · BOTTOM-UP LEVELS')
  if i==2:d.update(kind='rows',rows=[['query','[1,4)'],['first block','[1,2): sum1'],['second block','[2,4): sum5'],['combine','1+5=6']],label='DISJOINT QUERY BLOCKS')
  if i==4:d.update(kind='rows',rows=[['leaf index2','4 → 10'],['pair [2,4)','5 → 11'],['half [0,4)','9 → 15'],['root [0,8)','14 → 20']],label='ASSIGNMENT · RECOMPUTE ANCESTORS')
  if i==8:d.update(kind='rows',rows=[['input','3,1,4'],['overlap blocks','[3,1] and[1,4]'],['minimum','min(1,1)=1'],['sum fails','4+5=9, true sum8']])
 elif t=='ranges':
  if i<=4:d.update(kind='rows',rows=[['events','0,3,2,0,-3,-2'],['reconstructed','0,3,5,5,2']],label='DIFFERENCE EVENTS → VALUES')
  elif i<=9:d.update(kind='grid',grid=['123','456','789'],dist={},label='2D PREFIX · FOUR-REGION CANCELLATION')
  elif i==11:d.update(kind='rows',rows=[['updates','0,3,5,5,2'],['rectangle','2+3+5+6=16']])
 elif t=='sorting':
  d.update(kind='rows',rows=[['original','4,2,4,9,2'],['sorted','2,2,4,4,9'],['distinct','2,4,9']],label='SORTING CHANGES ORDER')
  if i==4:d['rows']=[['original pairs','(8,3),(8,1),(6,2)'],['lexicographic','(6,2),(8,1),(8,3)']]
  if i==6:d['rows']=[['new multiset','[2,2,4]'],['erase value2','[4]'],['erase one iterator','[2,4]']]
  if i==7:d['rows']=[['values','10,100,1000'],['ranks','0,1,2'],['original gaps','90 and900'],['rank gaps','1 and1: distance not preserved']]
 elif t=='backtracking':
  d.update(kind='tree',label='CALL STACK / BRANCH RESULTS',rows=[['input','5,-3; target2'],['decisions','exclude or include each INDEX']])
  if i in [2,3]:d['rows']=[['frame','i=0,sum=0'],['contract','count ways to finish at target2']]
  if i==4:d['rows']=[['caller','(i0,sum0)'],['exclude5','(i1,sum0)'],['exclude-3','(i2,sum0) →return0']]
  if i==5:d['rows']=[['caller','(i1,sum0)'],['include-3','(i2,sum-3) →return0'],['combine','0+0 →return0']]
  if i==6:d['rows']=[['include5','(i1,sum5)'],['exclude-3','(i2,sum5) →return0'],['include-3','(i2,sum2) →return1'],['combine','0+1 →return1']]
  if i==7:d['rows']=[['sum by value','child copy; caller unchanged'],['shared chosen vector','push →recurse →pop (undo)']]
  if i==11:d['rows']=[['[2,2],target2','two singleton subsets'],['[],target0','one empty subset'],['missing undo','shared choices leak into sibling']]
 elif t=='casework':
  d.update(kind='rows',rows=[['start1','simulate independently'],['start2','simulate independently'],['start3','simulate independently']],label='THREE COMPLETE CASES')
  if i in [3,4,5]:
   start={3:2,4:1,5:3}[i];pos=start;score=0;rows=[['initial',pos,score]]
   for j,(a,b,g) in enumerate([(1,2,1),(2,3,3),(1,3,1)]):
    pos=b if pos==a else a if pos==b else pos;score+=pos==g;rows.append([j+1,pos,score])
   d.update(kind='table',headers=['event','position','score'],rows=rows,label=f'CASE START={start} · SWAP THEN GUESS')
  if i==6:d.update(kind='concept',code=[])
  if i==10:d['rows']=[['fresh event','swap1,3; guess2'],['best score','1, starting at2'],['count optimal starts','count ties, not just maximum']]
 if any(word in c['direction'].lower() for word in ['proof','invariant','cost:','cost ','complexity','bounds','limits:','counterexample','state definition','key example']):d['code']=[]
 from learner_panels import apply
 return apply(d,c)
