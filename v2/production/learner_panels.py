"""Learner-facing facts and models. Production directions are NEVER display text."""
PRINCIPLES={
'foundations':'A program executes instructions on typed values. Read the contract, define the state, then justify each step.',
'loop_trace':'Before each condition check: total is the sum of the first i transactions. The index and the total have different meanings.',
'functions_cost':'A function has an input contract, an output contract and local state. Count operations and stored data separately.',
'string_lab':'Count every character first. Then scan original positions to find the earliest character with final frequency one.',
'casework':'For each possible start, reset position and score. Swap first, then compare the new position with the guess.',
'backtracking':'Each input INDEX has two choices: exclude or include. A leaf counts only when its sum equals the target.',
'sorting':'Sorting preserves values but changes positions. Keep original indices when the answer must refer to original positions.',
'prefix':'P[k] counts the first k elements. One-based inclusive query l..r uses P[r] − P[l−1].',
'ranges':'A start event adds a contribution; its stop event cancels it. Prefix reconstruction combines overlapping contributions.',
'dashboard_lab':'All corrections happen before queries. Reconstruct final values first; build query prefixes from those final values.',
' two_pointers':'',
'two_pointers':'A pointer may discard a candidate only after a proof. Pair search uses sorted values; contiguous windows preserve original order.',
'binary_search':'feasible(C) means all ordered boxes fit in at most the allowed trips. If C works, every larger capacity works.',
'greedy':'For unweighted interval count, accept the earliest compatible finish. Touching endpoints are allowed.',
 'transfer':'Choose from the operation contract: input order, update timing, query meaning and numeric bounds.',
'graph_models':'Define the vertices, edges, direction, weights and requested result before selecting a graph algorithm.',
'bfs':'For unit edges, the queue processes distance layers in order. Mark a vertex when enqueuing it, once.',
'grid_lab':'Vertices are open cells. Legal edges are in-bounds, non-wall, four-direction moves, each costing one.',
'parity':'For edge parity p: neighbor = current XOR p. Every existing assignment must agree with every constraint.',
'functional_graph':'Exactly one successor per vertex makes the walk deterministic. A finite walk has a tail followed by a cycle.',
'dynamic_programming':'dp[x] is the fewest tokens for EXACT amount x, with unlimited copies. The amount and token count are different units.',
 'topological':'A ready task has no unprocessed prerequisites. Removing it releases its outgoing dependencies.',
'knapsack':'dp[c] is the best value with weight AT MOST c, using processed items once. Descending capacities preserve the previous item layer.',
'lis_lab':'Strict LIS preserves input order. Ending-length DP and minimum tails summarize different facts; tails is not necessarily a witness.',
'dijkstra':'For nonnegative weights, relax edges from the smallest current distance. Skip stale heap entries.',
'dsu_mst':'Kruskal accepts the cheapest edge joining different components. DSU tracks connectivity; accepted original edges form the network.',
'fenwick':'Internal block i covers positions i−lowbit(i)+1 through i. External array indices are zero-based; internal indices are one-based.',
'segment_sparse':'A segment tree merges disjoint ranges. A sparse minimum table may overlap blocks because minimum is idempotent.',
'debug_clinic':'A reusable routine is correct only when the caller preserves its contract and state bookkeeping.',
'advanced_roadmap':'INTRODUCTION / NEXT STUDY: these topics require further implementation, proofs and independent practice.',
'practice':'State the contract, attempt a solution, find counterexamples, justify it, implement, then solve a changed problem.'}

def rows(m,label,items):
 m.update(kind='rows',label=label,rows=[x.split('|',1) for x in items],code=[])
def flow(m,label,steps):m.update(kind='flow',label=label,steps=steps,code=[])

def apply(m,c):
 t=m['topic'];i=c['scene']
 # No brackets/directions or auto-generated summaries enter this renderer.
 m['notes']=PRINCIPLES[t]
 if m['question']:
  m['notes']='Work out the contract, trace and reason. Pause here; resume when ready for the answer.'
  return m
 if t=='foundations':
  if i==0:flow(m,'ROHAIL’S THREE JOBS',['Read the contract','Model the state','Justify the steps'])
  if i==1:flow(m,'COURSE PREREQUISITES',['C++ / Bronze','Repeated work','Graphs / DP','Structures / roadmap'])
  if i==2:flow(m,'FROM SOURCE TO RUNNING PROGRAM',['main.cpp','compiler','executable','running process']);m['notes']='Changing source does not change an old executable. Recompile, then run the newly built program.'
  if i==4:
   rows(m,'COMPILE, RUN, CHECK',['compile|g++ -std=c++17 -Wall -Wextra main.cpp -o main','run|./main','input → output|3 4 → 7; −5 8 → 3; 0 0 → 0']);m['notes']='Compiler warnings help locate mistakes. Print only the output the problem requests.'
  if i==5:rows(m,'THREE DIFFERENT FAILURES',['compile error|Source cannot be translated','runtime failure|Execution fails','wrong answer|Execution finishes; result is wrong'])
  if i==9:rows(m,'INTEGER DIVISION / REMAINDER',['integer|7 / 2 = 3','remainder|7 % 2 = 1','check|7 = 2 × 3 + 1','real division|7.0 / 2 = 3.5']);m['notes']='C++ signed integer division truncates toward zero. Converting only the destination cannot restore a discarded fraction.'
  if i==10:m.update(kind='table',headers=['condition','value','branch'],rows=[['0 < 4','true','enter'],['4 < 4','false','stop']],label='BOOLEAN · TWO POSSIBLE VALUES');m['notes']='A condition evaluates to true or false. The result controls which branch executes.'
  if i==12:rows(m,'SIZE IS NOT CAPACITY',['vector<int> a(4)|Four existing elements: indices 0..3','empty v; v.reserve(100)|Size 0, capacity at least 100','v[0] after reserve only|INVALID: no element exists','v.push_back(7)|Size becomes 1; v[0] is 7'])
  if i==14:flow(m,'FOR-LOOP CONTROL',['initialize once','check condition','body if true','increment → check']);m['notes']='A false condition leaves the loop. The increment happens after the body, not during assignment.'
 elif t=='loop_trace':
  n={0:'Input: count n, then n signed values. Output: their net sum. Refunds are negative values.',1:'Read n first, allocate n slots, then read each value. Creating a vector does not read input.',2:'Initialize total=0 and i=0. Assignment changes total; the loop increment changes i.',3:'Order: check 0<4 → add 3 → store total=3 → increment i to 1.',4:'Order: check 1<4 → add −2 → store total=1 → increment i to 2.',5:'The final check is 4<4, false. No access to a[4] occurs. Print total=5.',6:'Indices 0..n−1 exist. The condition i<=n would attempt the invalid index n.',7:'Invariant point: immediately BEFORE each condition check, total=sum(a[0..i)).',8:'Base case: i=0 and total=0. The empty processed prefix has sum zero.',9:'Symbolic state: before body, total=sum(a[0..i)). After adding a[i] and incrementing i, the same invariant holds for the longer prefix.',10:'i increases toward n. At termination i=n, so the processed prefix is the whole input.',11:'A valid empty list is input n=0. A missing input stream is a different, invalid input.',12:'n≤100000 and |a[i]|≤10^9 imply every prefix has magnitude at most 10^14, within long long.',13:'n additions: O(n) time. Stored input: O(n) space. Loop-only extra state: O(1).',15:'Condition states: (0,0), (1,−4), (2,−4), (3,3), (4,0). Zero changes the index even when the total stays unchanged.',16:'Two invariants: total sums the processed prefix; refund_count counts its negative values.'}
  m['notes']=n.get(i,PRINCIPLES[t])
  if i==1:m['code']=['int n; cin >> n;','vector<int> a(n);','for (int& x : a) cin >> x;']
  if i==9:rows(m,'SYMBOLIC PRESERVATION',['before body|total = sum of first i values','assignment|total += a[i]','increment|i becomes old i + 1','next condition|total = sum of first new i values']);m['notes']=n[i]
  if i==12:rows(m,'ARITHMETIC BOUND',['count bound|n ≤ 100000','element bound|absolute value ≤ 10^9','prefix magnitude|≤ 100000 × 10^9 = 10^14','storage type|long long']);m['notes']=n[i]
  if i==13:rows(m,'COUNT THE WORK AND SPACE',['loop iterations|n','additions|n','stored values|n','extra loop variables|constant count']);m['notes']=n[i]
  if i==16:rows(m,'TWO STATES, TWO MEANINGS',['processed values|3, −2, 5, −1','net total|5','negative-value count|2','zero transaction|Changes neither result, but is processed']);m['notes']=n[i]
 elif t=='functions_cost':
  if i==0:flow(m,'FUNCTION CALL',['arguments','local parameters','function body','return to caller'])
  if i==3:rows(m,'VECTOR OBJECT AND ELEMENT STORAGE',['vector object|Tracks size, capacity and buffer','element buffer|Stores the actual values','growth|May allocate a new buffer','old element references|May be invalid after reallocation'])
  if i==4:flow(m,'LOCAL OBJECT LIFETIME',['enter scope','create local object','use object','leave scope: lifetime ends']);m['notes']='Do not return a reference to a local object whose lifetime has ended. A returned value is a different contract.'
  if i==5:m.update(kind='table',label='GROWTH COMPARISON · n = 16',headers=['growth','illustrative count'],rows=[['n',16],['n log2 n',64],['n²',256],['2^n',65536]],code=[]);m['notes']='These are operation-count models, not measured seconds. Constants, memory access and implementation still matter.'
  if i==6:m.update(kind='work_grids',label='NESTED LOOPS · EXAMPLE n = 4',code=[]);m['notes']='Three outer iterations times n inner iterations gives 3n: linear. n outer times n inner gives n²: quadratic. Nesting alone does not determine complexity.'
  if i==7:rows(m,'SPACE COUNTS',['input vector|n elements','prefix vector|n+1 elements','five scalar variables|constant space','combined storage|O(n), not O(1)'])
  if i==8:flow(m,'WHY THE PROGRAM IS CORRECT',['contract','initial state','preserved invariant','termination / result'])
  if i==10:rows(m,'TRANSFER ANSWERS',['sum n values|O(n)','three cases × n events|O(n)','all pairs|O(n²)','copy then read one|Copy may cost O(n)'])
 elif t=='string_lab':
  if i==1:rows(m,'WHY “FIRST UNSEEN” FAILS',['first S|Unseen so far','later S values|The same letter repeats','global frequency of S|3','conclusion|An early unseen test is insufficient'])
  if i==2:rows(m,'UPPERCASE COUNTER INDEX',['A|0','B|1','Z|25','initial state|26 zero counters'])
  if i==3:rows(m,'TWO DIFFERENT REPRESENTATIONS',['s = SWISS|Preserves order','frequency[S] = 3|Preserves multiplicity','frequency[W] = 1|Does not record W’s position','need both|Earliest qualifying original position'])
  if i==4:rows(m,'COUNTING TRACE',['read S, W, I|S:1, W:1, I:1','read next S|S:2','read final S|S:3','final counts|I:1, S:3, W:1'])
  if i==5:rows(m,'ALPHABET ORDER IS THE WRONG ORDER',['alphabetic unique choice|I, original position 2','earliest original choice|W, original position 1','required order|Scan s from left to right'])
  if i in [7,8]:
   m['notes']='Counting invariant: after k characters, each counter equals its occurrences in s[0..k).' if i==7 else 'Search invariant: all positions before i failed the frequency-one test. Therefore the first successful position is earliest.'
  if i==9:m['notes']='This excerpt is inside main. The successful branch prints i, then returns exit status 0. If no position qualifies, the final cout prints −1 once.'
  if i==9:
   m['code']=['string s; getline(cin,s);','array<int,26> frequency{};',"for (char c:s) {", "  if(c<'A'||c>'Z') return 1;", "  ++frequency[c-'A'];",'}','for(int i=0;i<(int)s.size();++i)',"  if(frequency[s[i]-'A']==1) {", "    cout << i << '\\n'; return 0;",'  }',"cout << -1 << '\\n';"]
   m['code_heading']='INSIDE MAIN · INPUT / COUNT / OUTPUT'
  if i==10:rows(m,'TWO SCANS',['count pass|n characters','position pass|at most n characters','counter initialization|26 entries','time / stored data|O(n) / O(n) string + 26 counters'])
  if i==13:m['code']=[];m['notes']='The new request is a different problem: first second occurrence, not first globally unique position.'
 elif t=='casework':
  if i==1:flow(m,'ONE EVENT',['old position','apply swap','compare with guess','update score'])
  if i==6:
   rows(m,'ONE SWAP, AT MOST ONE MOVE',['position == a|Move to b','otherwise position == b|Move to a','neither endpoint|Stay in place'])
   m['code']=['if (position == a) position = b;','else if (position == b) position = a;','// Then score the post-swap guess.'];m['notes']='else if prevents the token from moving to b and immediately moving back during the same event.'
  if i==7:m['notes']='After k events, position is the simulated token location and score counts correct guesses for THIS assumed start.'
  if i==8:rows(m,'THREE CASES',['event visits|3n','time|O(n)','stored event triples|n','state per case|position and score, reset each time'])
  if i==10:m['notes']='For counting optimal starts, find the best score, then count how many starts attain it.'
 elif t=='backtracking':
  if i==0:m['notes']='Choose or skip each position. Equal values at different indices still define different subsets.'
  if i==2:m['notes']='count(i,sum) returns the number of ways to decide remaining indices and reach the target.'
  if i==7:m['notes']='Passing sum by value gives each call its own copy. A shared chosen vector needs push, recurse, then pop.'
  if i==8:m.update(kind='decision_tree',label='ONE ROOT-TO-LEAF PATH PER SUBSET',code=[]);m['notes']='Each subset determines exactly one include/exclude choice per index. The four leaves are distinct subsets.'
  if i==9:rows(m,'ENUMERATION COST',['leaf count|2^n','binary recursion tree|O(2^n) nodes','maximum active stack|n+1 frames','printing every subset|May add O(n) work per leaf'])
  if i==11:m['notes']='Duplicate values remain distinct positions. The empty subset is one valid subset with sum zero.'
 elif t=='sorting':
  if i==2:m['notes']='std::sort(a.begin(), a.end()) sorts [begin,end). Use a strict weak ordering comparator; <= is not a valid replacement for <.'
  if i==3:rows(m,'DISTINCT-COUNT SCAN',['sorted sequence|2, 2, 4, 4, 9','count after each element|1, 1, 2, 2, 3','first position|No previous element to inspect','result|3 distinct values'])
  if i==5:rows(m,'CONTAINER CONTRACTS',['set|Unique ordered keys','multiset|Ordered keys, duplicates allowed','map|Key → associated value'])
  if i==8:m['notes']='Comparison sorting: O(n log n); distinct scan: O(n). Preserve original order when positions define the query.'
 elif t=='prefix':
  n={2:'Boundary k means the first k fans. P[0]=(0,0,0).',4:'The candidate P[4]=(1,0,0) loses earlier fans. Copy the previous prefix before adding the next fan.',5:'P[5]−P[1]=(2,2,1)−(0,1,0)=(2,1,1).',6:'Positions 2..5 inclusive are zero-based indices [1,5). Both use prefix boundaries 1 and 5.',7:'One-fan check: P[3]−P[2]=(0,0,1). The whole line uses P[6]−P[0].',10:'Build O(n); each three-count query O(1); storage 3(n+1) counters = O(n).',11:'Changing position 2 invalidates all prefixes ending at or after that position. Static prefixes do not update themselves.',13:'P[6]−P[3]=(3,2,1)−(1,1,1)=(2,1,0).',14:'An independent oracle scans each requested interval directly and counts its categories.'};m['notes']=n.get(i,PRINCIPLES[t])
  if i==9:m['code']=['int l,r; cin >> l >> r;','for (int c=0;c<3;++c)','  cout << prefix[r][c]-prefix[l-1][c]',"       << (c==2 ? '\\n' : ' ');"]
 elif t=='ranges':
  if i in [5,6,7,8]:
   m['notes']={5:'P[r][c] sums cells in rows [0,r) and columns [0,c). Leading row and column are zero.',6:'Bottom-right build: 9 + 21 + 27 − 12 = 45. The overlap must be subtracted once.',7:'Query rows [1,3), columns [1,3): 45 − 6 − 12 + 1 = 28, matching 5+6+8+9.',8:'Rectangle = P[r2][c2] − P[r1][c2] − P[r2][c1] + P[r1][c1].'}[i]
  if i==6:rows(m,'BUILD THE BOTTOM-RIGHT PREFIX',['current cell|9','prefix above + left|21 + 27','subtract overlap|−12','result|45']);m['notes']='The above and left rectangles both include their overlap, so subtract it once.'
  if i==7:m.update(kind='grid_regions',grid=['123','456','789'],label='QUERY [1,3) × [1,3)',selected=[(1,1),(1,2),(2,1),(2,2)],code=[])
  if i==8:rows(m,'FOUR PREFIX TERMS',['bottom-right prefix|+P[r2][c2]','remove top|−P[r1][c2]','remove left|−P[r2][c1]','restore overlap|+P[r1][c1]'])
  if i==9:m['notes']='Dense grid preprocessing and storage are O(rows×columns). A rectangle query uses four table lookups.'
 elif t=='dashboard_lab':
  n={5:'Independent total check: original 10 + first correction 6 − second correction 3 = final 13.',7:'[1,4): 10−2=8. [0,5): 13−0=13. Empty [3,3): 9−9=0.',9:'active = sum of corrections covering i. prefix[i] = sum of final values before i. These are different quantities.',10:'Safe teaching bounds give absolute totals ≤ 1.1×10^15. Assuming n=u=10^5 and delta=10^9 could instead reach 10^19.',11:'u corrections, n reconstructed values and q queries: O(n+u+q) time, O(n) space.',13:'Events [3,−2,−3,2] → corrections [3,1,−2] → final [4,1,0]. Queries return 5 and 1.'};m['notes']=n.get(i,PRINCIPLES[t])
 elif t=='two_pointers':
  n={1:'1+11=12>9. Every remaining partner for 11 is at least 1, so 11 can be discarded.',2:'1+7=8<9: discard 1. Then 2+7=9: a valid pair.',3:'Every still-possible pair remains between the pointers; each discarded endpoint has been ruled out.',5:'Promote BEFORE addition: long long sum = 1LL*a[left].first + a[right].first;',6:'The scan moves pointers inward at most n−1 times. Sorting costs O(n log n).',7:'New contract: longest contiguous interval with sum≤4 and nonnegative values. Sorting would destroy contiguity.',8:'Windows [0,1), [0,2), [0,3) have sums 2,3,4 and lengths 1,2,3.',9:'Adding 3 makes 7; remove 2 then 1 to reach 4. Adding final 1 requires another left removal. Best length stays 3.',10:'Nonnegative values make extending right unable to decrease a sum. This justifies permanently discarding invalid left boundaries.',11:'With [5,−2], limit 3, the whole length-two interval is valid. Discarding 5 immediately misses it.'};m['notes']=n.get(i,PRINCIPLES[t])
 elif t=='binary_search':
  n={1:'Capacity 6: trips [3,2], [2,4], [1,4]. Three trips fit.',2:'Capacity 5: [3,2], [2], [4,1], [4]. Four trips do not fit the three-trip limit.',3:'A box heavier than capacity must fail; a new trip cannot make that box lighter.',4:'After each trip, greedy has carried at least as long a prefix as any packing using that many trips.',5:'Capacities 4,5 fail; 6,7,8,9 work. Once true, feasibility stays true.',6:'Largest box=4 is a lower bound. Total weight=16 is a feasible upper bound.',10:'mid = lo + (hi−lo)/2; arithmetic bounds justify the long long range.',11:'Each check scans n boxes. Binary search halves the capacity interval: O(n log W) time.'};m['notes']=n.get(i,PRINCIPLES[t])
 elif t=='greedy':
  if i in [0,1,2]:m.update(kind='intervals',label='ONE ROOM · MAXIMIZE REQUEST COUNT',intervals=[('A',0,6),('B',1,3),('C',3,5),('D',5,7)],selected=[] if i==0 else ['A'] if i==1 else ['B','C','D'],code=[])
  if i==1:m['notes']='Earliest-start A gives only one request. Compatible B,C,D give three: the first-start rule fails.'
  if i==2:m['notes']='End-time order B,C,A,D. Accept B and C, reject overlapping A, then accept D.'
  if i==3:rows(m,'EXCHANGE ARGUMENT',['greedy first G|Ends no later than optimal first O','replace O with G|No later request loses feasibility','remaining requests|Apply the same argument again'])
  if i==4:m.update(kind='intervals',label='SHORTEST-DURATION COUNTEREXAMPLE',intervals=[('short',3,5),('left',0,4),('right',4,8)],selected=['short'],code=[]);m['notes']='The shortest interval blocks both others. Taking [0,4) and [4,8) yields two requests instead of one.'
  if i==5:rows(m,'SELECTION STATE',['stored tuple|(end,start,original ID)','accept condition|start ≥ last accepted end','on acceptance|Update last end','on rejection|Keep last end unchanged'])
  if i==6:rows(m,'SCOPE AND COST',['sort|O(n log n)','scan|O(n)','objective|Maximum COUNT, not value','weighted requests|Need a different justification'])
  if i==8:m.update(kind='intervals',label='TRANSFER ANSWER · TWO REQUESTS',intervals=[('first',0,2),('overlap',1,3),('last',2,4)],selected=['first','last'],code=[])
 elif t=='transfer':
  data={1:('BATCH CORRECTIONS → STATIC QUERIES',['difference events|+2 at 1; −2 at 3','corrections|0,2,2,0','final values|2,3,5,0','query prefixes|0,2,5,10,10']),2:('TOTAL WORK',['n values|One reconstruction scan','u updates|Two events each','q queries|Two prefix lookups each','total|O(n+u+q)']),3:('A DIFFERENT TIMELINE',['old contract|All updates, then all queries','new contract|Update → query → update → query','stale prefixes|No longer describe current values','needed property|Support changes between queries']),4:('MATCH THE PROOF TO THE METHOD',['prefix sums|Unwanted prefix cancels','difference events|Start adds; stop cancels','binary search|Monotone feasibility','two pointers|Discarded candidates cannot work'])}
  if i in data:rows(m,*data[i])
 elif t=='graph_models':
  if i==0:rows(m,'ONE NOTATION, THREE CONTRACTS',['room graph|Allowed movement','constraint graph|Relationships between assignments','dependency graph|Prerequisites before tasks'])
  if i in [1,4]:m.update(kind='graph',n=4,edges=[(0,1),(0,2),(1,3)],dist=[None]*4,queue=[],label='ROOMS AND ALLOWED MOVES',code=[]);m['notes']='Adjacency lists: 0:[1,2], 1:[0,3], 2:[0], 3:[1]. Undirected edges appear at both endpoints.'
  if i==2:rows(m,'DIRECTION CHANGES MEANING',['A → B|A permits or precedes B','reverse B → A|Not implied','A — B|Both movement directions allowed'])
  if i==3:rows(m,'GRAPH REPRESENTATIONS',['edge list|Store endpoint pairs','adjacency list|Store each vertex’s neighbors','matrix|Store all possible pairs','implicit grid|Generate legal neighbors on demand'])
  if i==5:m.update(kind='graph',n=6,edges=[(0,1),(1,2),(3,4)],dist=[None]*6,queue=[],label='THREE CONNECTED COMPONENTS',code=[]);m['notes']='Components are {0,1,2}, {3,4}, and {5}. An isolated vertex is a component too.'
  if i==6:rows(m,'FOUR GRID NEIGHBORS',['up / down|(r−1,c), (r+1,c)','left / right|(r,c−1), (r,c+1)','before indexing|Check bounds','before traversal|Reject walls'])
  if i==7:rows(m,'LOCATION MAY NOT BE ENOUGH',['state A|(room, no key)','state B|(same room, key held)','possible moves|Can differ between A and B','visited state|Must include the key bit'])
  if i==8:rows(m,'MODEL BEFORE TRAVERSAL',['objects|What is a vertex?','relationships|What creates an edge?','edge rules|Direction and weight?','result|What answer is requested?'])
  if i==10:flow(m,'PREREQUISITE DIRECTION',['microphone test','sound check']);m['notes']='The test precedes the sound check. No reverse prerequisite is implied.'
 elif t=='bfs':
  if i in [10,11,12,14]:m['dist']=[0,1,1,2,2,3,-1]
  n={1:'Each undirected connection is stored in both adjacency lists.',2:'distance=-1 means undiscovered. parent=-1 means no predecessor yet. The queue starts empty.',3:'Initialize distance[0]=0, then enqueue 0. FIFO means first in, first out.',10:'Layers: {0}, then {1,2}, then {3,4}, then {5}. A shorter predecessor layer would already have discovered a shorter route.',11:'Mark on ENQUEUE, not dequeue. Otherwise two parents may enqueue the same undiscovered vertex.',12:'Backward parents: 5→3→1→0. Reverse to obtain route 0→1→3→5.',14:'Each vertex enters the queue at most once; each undirected edge is examined twice. O(n+m) time and space.',16:'After adding 5–6: distance[6]=4, parent[6]=5. In the ORIGINAL graph without that edge, 6 remains unreachable.'};m['notes']=n.get(i,PRINCIPLES[t])
 elif t=='grid_lab':
  n={1:'Zero-based coordinates: S=(0,0), T=(2,3).',2:'ID=r×width+c. Recover row=ID/width and column=ID%width. Here width=4.',3:'From (0,0), candidates (−1,0) and (0,−1) are out of bounds. Check BEFORE indexing.',7:'Route (0,0)→(0,1)→(0,2)→(1,2)→(1,3)→(2,3): five moves, six cells.',8:'Check endpoints, bounds, walls and Manhattan distance one between consecutive route cells.',10:'At most H×W cells, four candidate moves per processed cell. O(HW) time and space.',11:'Diagonal moves change edges. Terrain costs change weights. A key can change the state.',12:'With one reusable key, visited[row][column][key_bit] distinguishes two states at one cell.',14:'Left: distance 3. Right: blocking zero-based cell (1,1) separates S from T.'};m['notes']=n.get(i,PRINCIPLES[t])
 elif t=='parity':
  if i==4:m['dist']=[1,1,0,'?'];m['notes']='Flipping every bit in a component preserves same/different relationships: (0,0,1) ↔ (1,1,0).'
  n={2:'S has parity 0: keep the bit. D has parity 1: flip the bit.',5:'The isolated fourth group is an independent component. Two consistent components give 2²=4 assignments.',6:'Existing constraints force groups 1 and 3 to differ. A new S edge requiring equality is a contradiction.',7:'Recoloring group 3 to satisfy the new S edge breaks the existing D edge. Recheck ALL constraints, not only the newest one.'};m['notes']=n.get(i,m['notes'])
 elif t=='functional_graph':
  n={1:'Walk from 0: 0,1,2,3,1,… . A repeated vertex has the same deterministic successor.',2:'Tail [0] has length 1. Cycle [1,2,3] has length 3. Starting from 2 gives no tail.',3:'Store the first visit index of each vertex. Stop at the first repeat; its stored index splits tail from cycle.',4:'Starting at 4 follows 4→4: tail length 0, cycle length 1.',5:'After the tail, a far-future position depends on remaining steps modulo cycle length. Binary jumping is later study.',7:'Start 0: tail length 2, cycle length 1. Start 2: tail length 0, cycle length 1.'};m['notes']=n.get(i,PRINCIPLES[t])
 elif t=='dynamic_programming':
  if i==9:m['notes']='Denomination 3 chooses predecessor amount 0. The count candidate is 1+dp[0]=1, not 3+dp[0].'
  if i==13:m['notes']='With denominations 4 and 6, exact target 5 is unreachable. Infinity means no valid construction.'
 elif t=='topological':
  if i==1:m['queue']=[1];m['notes']='Initial indegrees [0,0,2,1,1]. After processing 0, task2 still has one prerequisite; queue=[1].'
  if i==2:m['notes']='After processing 1, enqueue 2 and 4. Processing 2 releases 3. One valid order: 0,1,2,4,3.'
  if i==4:m['notes']='Cycle 1→2→3→1 prevents a full order. Task4 can be blocked downstream without lying on the cycle.'
 elif t=='knapsack':
  if i==8:m['notes']='Ascending capacity reuses the just-updated dp[2], counting one item twice. Descending capacity reads the previous item layer.'
  if i==9:rows(m,'SIMILAR INPUTS, DIFFERENT STATES',['0/1, at most capacity|Each item once; zero is a valid empty choice','unlimited items|Reuse is allowed; different update logic','exact weight|Unreachable weights need −∞','contract first|Do not copy initialization blindly'])
  if i==10:m['notes']='Capacity 4: density-first takes (weight3,value5). Two (weight2,value3) items give value6 and are better.'
 elif t=='lis_lab':
  if i in [2,3,4]:m['code']=['vector<int> dp(n, 1);','for (int i=0; i<n; ++i)','  for (int j=0; j<i; ++j)','    if (a[j] < a[i])','      dp[i]=max(dp[i],dp[j]+1);']
  if i==3:m['notes']='dp[i] is the best strict increasing subsequence ending AT i. Extend only earlier j with a[j]<a[i].'
  if i==9:m['notes']='lower_bound finds the first tail ≥ x. Equal values replace a tail, so [2,2,2] has strict LIS length 1.'
  if i==11:m['notes']='For input [2,3,1], final tails [1,3] is not in input order. The true length-two witness is [2,3].'
 elif t=='dijkstra':
  if i==6:m['notes']='Negative-edge counterexample: 0→1 costs2, 0→2 costs5, 2→1 costs−4. Finalizing 1 at distance2 would be wrong; its optimum is1.'
  if i==12:m['notes']='Add direct 0→3 cost8: new optimum8. If its cost is12 instead, the old route of cost9 remains best.'
 elif t=='dsu_mst':m['notes']='Accepted edges 0–1 cost1, 1–2 cost2, 2–3 cost4 give total7. DSU parent pointers are bookkeeping, not necessarily those network edges.'
 elif t=='fenwick':
  n={3:'prefix(7) takes blocks 7,6,4. Their covered ranges are disjoint and together cover the first seven positions.',6:'External index4 is internal position5. Adding3 updates internal blocks5,6,8.',7:'A range [l,r) equals prefix(r)−prefix(l). Overlapping unwanted prefixes cancel.',8:'5=0101 → 6=0110 → 8=1000. Skipped7=0111 covers only position7, so it excludes updated position5.',9:'Assignment requires delta=new−old. Changing5 to8 means add3, not add8.',13:'Subtracting2 at external0 updates internal1,2,4,8. Range[2,7) is unchanged because it excludes external0.'};m['notes']=n.get(i,PRINCIPLES[t])
 elif t=='segment_sparse':
  n={1:'Zero-padded leaves preserve sums. Internal nodes store the sum of their children.',2:'Query[1,4) uses disjoint blocks[1,2) and[2,4): 1+5=6.',4:'Assign index2 from4 to10. Recompute its ancestors: whole sum14→20; query[1,4) becomes12.',6:'Range updates need additional state such as lazy tags. This companion supports point assignment only.',7:'Static sparse minima store power-of-two blocks. No updates are supported by this query contract.',8:'min(3,1) and min(1,4) overlap safely. Sums4+5=9 incorrectly double-count the middle1; true sum8.'};m['notes']=n.get(i,PRINCIPLES[t])
  if i==7:m['label']='STATIC RANGE MINIMUM · FIXED ARRAY'
  if i==8:m['label']='OVERLAPPING BLOCKS · MINIMUM VS SUM'
  if i==9:rows(m,'OPERATION CONTRACTS',['static minimum|Sparse table: O(1) query after preprocessing','assignment + sum|Segment tree: O(log n) query/update','sparse-table storage|O(n log n)','segment-tree storage|O(n)'])
 elif t=='debug_clinic':
  data={1:('SHORTEST-DISTANCE ANSWER',['distance[0]|0','distance[1]|2 via cheaper parallel edge','distance[2]|2 via zero-cost edge','stale heap entries|Costs9 and7 must be skipped']),3:('ASSIGNMENT ADAPTER',['first assignment|old−1 → new3; delta4; sum9','second assignment|old3 → new3; delta0; sum9','stale old value|Would add4 again: wrong sum13']),4:('EXACT WEIGHT IS A DIFFERENT CONTRACT',['one item|weight3, value8','at most capacity2|Empty selection gives0','exact weight2|Impossible','required state|Unreachable marker, not default0']),5:('BEFORE REUSING A ROUTINE',['operation|Addition or assignment?','objective|At most or exactly?','edge weights|Nonnegative or arbitrary?','state invariant|Does caller bookkeeping agree?'])}
  if i in data:rows(m,*data[i])
 elif t=='advanced_roadmap':
  data=[('NEXT COURSES · NOT MASTERY BADGES',['graphs|Trees and graph structure','DP|Richer states and proof-based optimizations','ranges|More operations and offline methods','arithmetic|Number-theoretic tools']),('TREES → SUBTREE QUERIES',['tree|Connected and acyclic; unique simple paths','rooted DFS|Define parent and depth','entry-only tour|Subtree becomes [tin,tout)','range structure|Query or update the subtree interval']),('BINARY JUMPING / LCA',['precompute|Ancestors after 1,2,4,8,… steps','query|Combine jumps to climb','LCA|Lowest shared ancestor','tree distance|depth[u]+depth[v]−2depth[LCA]']),('GRAPH STRUCTURE',['SCC|Mutually reachable directed vertices','condensation|SCCs form a DAG','bridges|Removal disconnects an undirected graph','Eulerian vs Hamiltonian|Edges once vs vertices once']),('ARITHMETIC PREREQUISITES',['GCD|Euclidean remainders','sieve|Prime information for many integers','binary exponentiation|Square and combine powers','modular multiplication|Check intermediate overflow bounds']),('STATE-SPACE METHODS',['bitmask|Represents a small subset','subset DP|State includes a selected set','meet in the middle|Split 40 choices into two groups of20','proof obligation|Combine halves without losing solutions']),('DEEPER DP',['interval DP|State is an interval','weighted scheduling|Profit changes the objective','optimization|Requires extra structure','next step|Derive state and transition first']),('STRINGS',['prefix function / KMP|Reuse matched-prefix information','Z algorithm|Prefix match at each position','trie|Shared prefix paths','hashing|Collisions require reasoning']),('FLOW AND MATCHING',['capacity|Maximum allowed edge flow','residual graph|Remaining and reversible flow choices','augmenting path|Improves a feasible flow','matching|Often modeled with unit capacities']),('MORE STRUCTURES AND GEOMETRY',['lazy propagation|Compose deferred range operations','offline processing|Reorder queries when the contract allows','geometry|Exact orientation and boundary cases','advanced structures|Select for a concrete operation workload']),('CHOOSE ONE NEXT TOPIC',['motivation|Name a problem it solves','prerequisite|Learn the needed foundations','implementation|Write and test it yourself','transfer|Solve a changed problem'])]
  rows(m,*data[i])
 elif t=='practice':
  data={1:('MATCH OPERATIONS TO STRUCTURES',['static sums|Prefix sums','addition + sum|Fenwick','assignment + sum|Segment tree or delta adapter','static minima|Sparse table']),3:('DISTINGUISH THE OBJECTIVES',['cheapest route|Dijkstra with nonnegative weights','cheapest whole network|Minimum spanning tree','unlimited exact amount|Coin DP','single-use items|0/1 knapsack']),4:('PRACTICE CYCLE',['attempt|Try before reading a solution','counterexample|Explain a failed assumption','implementation|Make the proof executable','transfer|Solve a meaningfully changed task']),5:('TESTING HABITS',['boundaries|Use contract-valid extremes','oracle|Check by an independent simple method','random cases|Save the seed','failure|Keep the exact reproducing input']),6:('CONTEST WORKFLOW',['read|Extract contract and bounds','plan|Prove correctness and estimate cost','test|Check boundaries and counterexamples','official rules|Consult current USACO instructions']),7:('ROHAIL’S CORRECTED LEDGER',['receipts|+3, −2, +5, −1','wrong positive-only total|8','correct signed total|5','next step|Practice a new problem independently'])}
  if i in data:rows(m,*data[i])
 # Every non-question scene must have a concrete typed panel, never a direction placeholder.
 assert m['kind']!='concept',(t,i,'missing learner panel')
 return m
