import html,json,sys
from pathlib import Path
from curriculum import lessons
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Preformatted,PageBreak,KeepTogether
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_CENTER
ROOT=Path('/workspace/usaco-film/output');ROOT.mkdir(exist_ok=True)
esc=html.escape
styles=getSampleStyleSheet();styles.add(ParagraphStyle(name='CodeBlock',fontName='Courier',fontSize=8.2,leading=10.8,backColor=HexColor('#eef3f7'),spaceBefore=8,spaceAfter=10));styles['BodyText'].fontSize=10.5;styles['BodyText'].leading=15;styles['BodyText'].spaceAfter=9
story=[]
def p(s,style='BodyText'):story.append(Paragraph(s,styles[style]))
def code(s):story.append(Preformatted(s,styles['CodeBlock']))
p('BESSIE VS. THE ALGORITHM','Title');p('The companion workbook','Heading1')
p('C++ foundations • Bronze • Silver • Gold • Platinum extensions')
p('Use this film in short sessions. Pause at each challenge, implement independently, then compare the answer. This is a broad course map with worked examples, not a guarantee of promotion or an exhaustive treatment of every advanced algorithm.')
p('The film uses original procedural music, an original cartoon character, and synthetic narration. No artist voice imitation or copyrighted song recordings are used.')
p('How to work with the course','Heading2')
p('1. Watch one chapter. 2. Explain its state and invariant. 3. Solve the challenge without notes. 4. Implement a related problem. 5. Record a counterexample or mistake. 6. Re-solve later from a blank file.')
p('Division labels describe a learning sequence, not an official immutable syllabus. Advanced topics overlap divisions. Check current USACO contest rules, compiler support, scoring, and assistance restrictions on the official site.')
p('Reference destinations','Heading2')
p('<link href="https://usaco.org/">USACO: official contest information and problem archive</link><br/><link href="https://usaco.guide/">USACO Guide: structured topics and practice</link><br/><link href="https://en.cppreference.com/">cppreference: C++ library and language reference</link>')
p('These are recommended reference destinations. Their current pages were not fetched or audited for this production; do not infer current contest policy from the film.')
p('Scope and mastery gates','Heading2')
for s in ['C++: compile, read/write input, choose numeric types, use loops, vectors, strings and functions safely.','Bronze: simulate precisely, enumerate small search spaces, sort and reason about complexity.','Silver: prove prefix-sum, two-pointer, binary-search and traversal solutions.','Gold: define DP states, distinguish graph objectives, implement dynamic range structures and tree reasoning.','Platinum extensions: recognize advanced structures and the conditions they require; study full implementations and solve dedicated problems afterward.']:p(s)
story.append(PageBreak());p('Runnable code: quick start','Heading1')
p('The source bundle contains examples/algorithms.hpp, examples/main.cpp and examples/test.cpp. The library contains selected teaching implementations, not a template for every topic mentioned in the film. Read preconditions before reuse. Inputs in main.cpp are assumed to follow the chosen mode’s format.')
code('g++ -std=c++17 -O2 -Wall -Wextra examples/main.cpp -o lesson\ng++ -std=c++17 -O2 -Wall -Wextra examples/test.cpp -o tests\n./tests\n./lesson shipping')
p('Shipping mode input: number of packages, number of days, then nonnegative weights in order.');code('6 3\n3 2 2 4 1 4\n\nExpected output: 6')
p('Range mode input: n, q, then n values, then q half-open ranges [l,r).');code('5 3\n3 1 4 1 5\n1 4\n2 5\n0 5\n\nExpected output:\n6\n10\n14')
p('Other modes: sum reads two integers; coins reads number of denominations and target, then positive denominations; lis reads n then n values; bfs reads n m source then m undirected zero-based edges; dijkstra reads n m source then m directed edges u v nonnegative_weight. Unreachable vertices print -1.')
p('Validation','Heading2');p('The bundled test program uses fixed cases and seeded differential tests against simpler independent methods. This validates the included implementations on those cases; it is not a proof of every statement in the film. Preconditions and proof reasoning remain necessary.')
p('Useful C++ reminders','Heading2')
for s in ['Use == to compare and = to assign. Parentheses help make mixed logical expressions unambiguous.','Integer division truncates toward zero. The nonnegative ceiling-division shortcut needs its stated domain.','Use long long for potentially large sums. Promote before multiplying; long long does not prevent all possible overflow.','A reference can refer to an existing object; avoid returning references to local variables. Vector reallocation can invalidate pointers and iterators.','Functions need declarations before calls unless their definition is already visible. Keep variable scope narrow.','Recursive functions need a base case and progress toward it. Deep recursion can overflow the stack; iterative graph traversals avoid this risk.','Use explicit standard headers. The examples target C++17.']:p(s)
story.append(PageBreak());p('Chapter index','Heading1')
for i,l in enumerate(lessons):p(f'{i+1:02d}. {esc(l["title"])} — {l["level"]}')
for i,l in enumerate(lessons):
 story.append(PageBreak());p(f'{i+1:02d} / {l["level"]}','Heading2');p(esc(l['title']),'Heading1');p('<i>'+esc(l['hook'])+'</i>')
 p('Learning objectives','Heading2');p('; '.join(esc(h) for h,t in l['beats'])+'.')
 for h,t in l['beats']:p(esc(h),'Heading2');p(esc(t))
 if l['code']:p('On-screen code excerpt','Heading2');code(l['code']);p('Excerpts may depend on surrounding declarations. Use the full companion examples for runnable programs.')
 p('Pause and solve','Heading2');p(esc(l['challenge']));p('Answer and reasoning checkpoint','Heading2');p(esc(l['answer']))
 p('Transfer task','Heading2');p('Find or create a related problem with different numbers or constraints. Before coding, write the input contract, state meaning, correctness argument, time complexity, memory use, and one condition under which this method would fail.')
story.append(PageBreak());p('Complexity and assumption reference','Heading1')
rows=[
('Prefix sums','O(n) build; O(1) query; O(n) space','Static additive range queries.'),
('Difference array','O(1) per range addition; O(n) reconstruction','Batch updates before final values are needed.'),
('Two pointers','O(n) scan after any sorting','A monotonic discard argument must hold.'),
('Binary search on answer','O(check cost * log(answer range))','Monotone predicate and valid bounds.'),
('Sort / ordered set / map','O(n log n) sort; O(log n) tree operation','Strict comparator; ordered-container semantics.'),
('DFS / BFS','O(V+E) time; O(V+E) graph storage','BFS shortest paths require equal edge costs.'),
('Dijkstra with binary heap','O((V+E) log V) for a simple graph','Nonnegative edge weights; safe distance arithmetic.'),
('Bellman-Ford / Floyd-Warshall','O(VE) / O(V^3)','Negative cycles require explicit handling.'),
('0-1 BFS','O(V+E)','Every edge weight is exactly 0 or 1.'),
('Coin / capacity DP','O(number of items * numeric target)','Pseudo-polynomial; loop order changes semantics.'),
('LIS','O(n log n) with tails','lower_bound for strictly increasing subsequences.'),
('Generic interval split DP','Often O(n^3) time; O(n^2) space','Recurrence and dependency order must be proved.'),
('DSU','O(alpha(n)) amortized per operation','Union by size/rank plus path compression; ordinary DSU does not delete edges.'),
('Kruskal','O(E log E)','Undirected graph; disconnected input yields a forest.'),
('Fenwick / segment tree','O(log n) update and query; O(n) space','Choose summaries and operations appropriate to the structure.'),
('Binary lifting LCA','O(n log n) build; O(log n) query','Rooted tree with consistent ancestor conventions.'),
('Reroot distance sums','O(n)','Connected unweighted tree for the shown n-2s formula.'),
('Monotonic stack / deque','O(n) total','Each index enters and leaves a bounded number of times.'),
('Meet in the middle','About O(n * 2^(n/2)) with sorting','Exponential, but often feasible for modest n.'),
('Mo ordering','O((n+q) sqrt(n)) endpoint moves','Static/offline ranges; constant-time add/remove for this bound.'),
('HLD + segment tree','Typically O(log^2 n) per path operation','Tree paths; preserve direction for noncommutative summaries.'),
('KMP / Z','O(n) for the relevant combined string length','Exact deterministic string processing.'),
('Persistent point-update segment tree','O(log n) new nodes per update','Unchanged subtrees are shared; total memory grows with versions.'),
('General Dinic bound','O(V^2 E)','Special networks admit better bounds; advanced implementation required.'),
('Convex hull by sorting','O(n log n)','Correct orientation predicates and collinearity policy.')]
for name,cost,condition in rows:p(esc(name),'Heading2');p(esc(cost)+'<br/><i>'+esc(condition)+'</i>')
story.append(PageBreak());p('The Wrong Answer Awards: spot the bug','Heading1')
traps=[
('The overflow remix','long long area = a*b, where a and b are int and both 100000.','The multiplication happens as int before assignment. Promote an operand first: 1LL*a*b. Signed overflow has undefined behavior.'),
('The disappearing window','Use the nonnegative sliding-window rule on [4,-3,1] with sum limit 2.','It may discard the initial 4, missing the full length-3 window whose sum is 2. Negative values invalidate the standard monotonic argument.'),
('The fake monotone predicate','Truth values F,T,F,F,T,T. Apply first-true binary search without checking monotonicity.','The search can return 4 while the first true index is 1. A monotonic predicate is a proof requirement.'),
('The VIP bonus index','Read a[a.size()] to inspect the last element.','That is one past the end. For a nonempty vector the last index is size()-1.'),
('The infinite encore','A one-based Fenwick update starts internally at i=0 and repeatedly adds i&-i.','The index stays zero forever. The public zero-based wrapper must increment before entering the internal loop.'),
('The duplication glitch','One item: weight 2, value 3; capacity 4. Update zero-one knapsack capacities upward.','The same item can be reused, incorrectly producing 6 instead of 3. Iterate downward for this one-dimensional zero-one formulation.'),
('The route with fewer turns','S->A costs 10; S->B and B->A cost 1 each. Use ordinary BFS to minimize travel cost.','BFS minimizes the number of equal-cost edges. The cheapest weighted route costs 2 via B, even though it has more edges.'),
('The cheapest network is not every shortest route','Undirected edges S-A=2, A-B=2, S-B=3.','The MST costs 4 but gives an S-to-B route of cost 4; the actual shortest route costs 3. Objectives differ.'),
('The shrinking geography','Compress coordinates 7 and 100 into ranks 0 and 1, then use rank difference as distance.','Ranks preserve order, not gaps. The actual distance is 93.'),
('The impossible inverse','Divide by 2 modulo 6 using a supposed multiplicative inverse.','No inverse exists because gcd(2,6)=2, not 1.'),
('The comparator where everyone wins','Return a<=b from the sort comparator.','An element would compare before itself. The comparator must define a strict weak ordering.'),
('The overconfident visited flag','In a directed graph, declare a cycle whenever DFS sees any visited neighbor.','A finished vertex can be reached by a cross edge without a cycle. Use an active recursion-stack state for the cycle witness.')]
for name,q,a in traps:p(esc(name),'Heading2');p('<b>Challenge:</b> '+esc(q));p('<b>Reasoning:</b> '+esc(a))
def footer(canvas,doc):
 canvas.setFont('Helvetica',8);canvas.setFillColor(HexColor('#65738a'));canvas.drawString(42,24,'Bessie vs. the Algorithm • Companion workbook');canvas.drawRightString(570,24,str(doc.page))
SimpleDocTemplate(str(ROOT/'Bessie-USACO-workbook.pdf'),pagesize=(612,792),rightMargin=42,leftMargin=42,topMargin=42,bottomMargin=42,title='Bessie vs. the Algorithm — USACO Workbook').build(story,onFirstPage=footer,onLaterPages=footer)
# Searchable plain-text transcript is deliberately not a Markdown artifact.
parts=['BESSIE VS. THE ALGORITHM — COMPLETE SCRIPT\n']
for i,l in enumerate(lessons):
 parts.append(f'\nCHAPTER {i+1:02d}: {l["title"]} [{l["level"]}]\n{l["hook"]}\n')
 for h,t in l['beats']:parts.append(h+'\n'+t+'\n')
 parts.extend(['CHALLENGE: '+l['challenge'],'ANSWER: '+l['answer']])
(ROOT/'complete-script.txt').write_text('\n'.join(parts))
print('Built workbook PDF and complete script.')
