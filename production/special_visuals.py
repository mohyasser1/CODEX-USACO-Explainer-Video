"""Topic-specific visual labs. Examples are labeled and do not imply full proofs."""
import math

def draw_special(d,t,lesson,api):
 text,box,arrow,cells,wrap=api
 title=lesson['title'];step=int(t/1.8); MINT='#62f2bc';PINK='#ff77b7';YELLOW='#ffdb72';BLUE='#75adff';MUTED='#aeb9d4';WHITE='#f2f4ff';BG='#0b1020'
 def node(x,y,label,on=False):
  d.ellipse((x-27,y-27,x+27,y+27),fill=MINT if on else '#283651',outline=WHITE,width=2);text(d,(x-9,y-15),str(label),23,BG if on else WHITE,True)
 if title.startswith('DIJKSTRA'):
  pts=[(160,360),(470,260),(470,450)];a,b,c=pts
  arrow(d,(188,350),(440,268),MUTED);arrow(d,(187,370),(440,443),MUTED);arrow(d,(470,420),(470,292),MINT)
  text(d,(290,280),'10',26,YELLOW);text(d,(290,415),'2',26,YELLOW);text(d,(490,345),'3',26,YELLOW)
  for p,label in zip(pts,['S','A','B']):node(*p,label)
  states=['dist: S=0, A=INF, B=INF','relax S: A=10, B=2','settle B: improve A to 2+3=5','settle A: shortest distance is 5']
  text(d,(90,520),states[step%4],25,MINT,True);return True
 if title.startswith('FLOW,'):
  xs=[150,350,560,770];pts=[(xs[0],365),(xs[1],280),(xs[1],450),(xs[2],365),(xs[3],365)]
  for u,v in [(0,1),(0,2),(1,3),(2,3),(3,4)]:
   a,b=pts[u],pts[v];dx,dy=b[0]-a[0],b[1]-a[1];ln=math.hypot(dx,dy);a=(a[0]+dx/ln*30,a[1]+dy/ln*30);b=(b[0]-dx/ln*30,b[1]-dy/ln*30)
   active=(u,v) in [(0,1),(1,3),(3,4)] and step%3>0;arrow(d,a,b,MINT if active else MUTED)
   text(d,((a[0]+b[0])/2-15,(a[1]+b[1])/2-30),'1/1' if active else '0/1',19,YELLOW)
  for p,l in zip(pts,['S','A','B','X','T']):node(*p,l)
  text(d,(90,225),'Two fans, one slot. Labels = flow / capacity.',25,MINT,True)
  text(d,(90,525),'The slot-to-sink capacity limits total flow to 1.',24,MUTED);return True
 if title.startswith('EULER') or title.startswith('TREES,') or title.startswith('TREE DP') or title.startswith('ADVANCED TREE'):
  pts=[(430,260),(250,350),(650,350),(150,450),(350,450)];edges=[(0,1),(0,2),(1,3),(1,4)]
  for u,v in edges:d.line((pts[u],pts[v]),fill='#405475',width=4)
  order=[0,1,3,4,2];active=set(order[:step%6]);labels=list(range(5))
  if title.startswith('TREE DP'):active={0,3,4} if step%2 else {1,2}
  for j,p in enumerate(pts):node(*p,labels[j],j in active)
  if title.startswith('EULER'):
   text(d,(90,515),'Entry order: [0, 1, 3, 4, 2]',24,MINT,True);text(d,(90,550),'Subtree(1) occupies positions [1,4).',22,YELLOW)
  elif title.startswith('TREE DP'):
   text(d,(90,515),'Green = selected. Adjacent vertices cannot both be green.',24,MINT,True)
  elif title.startswith('ADVANCED'):
   text(d,(90,515),'A light edge enters a substantially smaller subtree.',23,MINT,True)
  else:text(d,(90,515),'Subtree sizes: node 0 = 5; node 1 = 3.',24,MINT,True)
  return True
 if title.startswith('KNAPSACK'):
  cells(d,[0,0,3,3,3],330,170,(4-step%3,))
  text(d,(90,240),'ONE item: weight 2, value 3. Capacity 4.',26,MINT,True)
  text(d,(90,470),'Update capacities 4 -> 3 -> 2. Each item used once.',23,YELLOW)
  text(d,(90,520),'Correct best value: 3. Forward reuse can invent 6.',23,MUTED);return True
 if title.startswith('SEQUENCE DP'):
  cells(d,[3,1,2,5,4],330,170,(1,2,4));text(d,(90,245),'Strictly increasing subsequence: 1, 2, 4',26,MINT,True)
  text(d,(90,490),'Keep original order. Skipping elements is allowed.',24,MUTED);return True
 if title.startswith('MODULAR'):
  text(d,(100,255),'3 x 5 = 15 = 1 (mod 7)',38,MINT,True)
  for j in range(7):
   ang=2*math.pi*j/7;x=660+100*math.cos(ang);y=415+100*math.sin(ang);node(x,y,j,j==step%7)
  text(d,(100,355),'Multiplicative inverse of 3:',24,MUTED);text(d,(100,400),'5, because the product leaves 1.',25,YELLOW)
  text(d,(100,530),'An inverse exists iff gcd(a, modulus) = 1.',23,MUTED);return True
 if title.startswith('OFFLINE'):
  text(d,(100,255),'Standard Mo ordering: O((n + q) sqrt(n))',29,MINT,True)
  text(d,(100,320),'Endpoint moves; assume O(1) add/remove operations.',24,MUTED)
  cells(d,[2,7,1,8,2,8],395,130,tuple(range(step%3,step%3+3)))
  text(d,(100,520),'Know all queries -> reorder -> restore answer order.',23,YELLOW)
  return True
 if title.startswith('STRING'):
  cells(d,list('ababa'),325,180,(0,1,2));text(d,(100,240),'A border is both a prefix and a suffix.',26,MINT,True)
  text(d,(100,465),'ababa: longest proper border = aba (length 3)',24,YELLOW)
  text(d,(100,520),'Reuse the matching border when extending a pattern.',22,MUTED);return True
 if title.startswith('DISJOINT'):
  joined=step%3
  for j in range(5):node(160+j*150,350,j,j<=joined)
  if joined>=1:arrow(d,(280,350),(190,350),MINT)
  if joined>=2:arrow(d,(430,350),(190,350),MINT)
  text(d,(100,250),'Union(0,1), union(1,2): representatives merge.',25,MINT,True)
  text(d,(100,490),'A redundant union does not increase component size.',23,YELLOW);return True
 if title.startswith('MINIMUM SPANNING'):
  pts=[(250,300),(620,300),(440,470)]
  for u,v,w in [(0,1,10),(0,2,2),(1,2,3)]:
   a,b=pts[u],pts[v];d.line((a,b),fill=MINT if w<10 else '#405475',width=5);text(d,((a[0]+b[0])/2,(a[1]+b[1])/2-28),str(w),25,YELLOW)
  for j,p in enumerate(pts):node(*p,j)
  text(d,(100,530),'Cheapest connected tree: edges 2 + 3 = 5.',25,MINT,True);return True
 if title.startswith('DAGs'):
  pts=[(200,280),(200,450),(600,365)]
  arrow(d,(230,287),(565,355),MINT);arrow(d,(230,442),(565,375),MINT)
  for p,l in zip(pts,['A','B','C']):node(*p,l)
  text(d,(100,520),'A,B,C or B,A,C: both prerequisites precede C.',24,YELLOW);return True
 if title.startswith('STRONG COMPONENTS'):
  pts=[(180,350),(340,260),(460,430),(740,430)]
  for u,v in [(0,1),(1,2),(2,0),(2,3)]:d.line((pts[u],pts[v]),fill=PINK if (u,v)==(2,3) else MINT,width=5)
  for j,p in enumerate(pts):node(*p,j)
  text(d,(100,520),'Undirected example: the leaf edge is the only bridge.',23,YELLOW);return True
 return False
