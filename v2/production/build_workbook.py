"""Student workbook with questions before solutions and complete C++ companions."""
import sys,json,re,math
from pathlib import Path
from xml.sax.saxutils import escape
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from script_text import scenes
from art import is_question,topic
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,PageBreak,KeepTogether,Preformatted,CondPageBreak
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
R=Path(__file__).resolve().parents[1];OUT=Path('/workspace/usaco-film-v2/output/course');OUT.mkdir(exist_ok=True)
for name,file in [('Body','DejaVuSans.ttf'),('Bold','DejaVuSans-Bold.ttf'),('Mono','DejaVuSansMono.ttf')]:pdfmetrics.registerFont(TTFont(name,'/usr/share/fonts/truetype/dejavu/'+file))
style=getSampleStyleSheet();style.add(ParagraphStyle('Text',fontName='Body',fontSize=10,leading=15,spaceAfter=9,allowWidows=0,allowOrphans=0));style.add(ParagraphStyle('Heading',fontName='Bold',fontSize=16,leading=21,spaceBefore=14,spaceAfter=9,keepWithNext=True,textColor=HexColor('#17354b')));style.add(ParagraphStyle('Small',parent=style['Text'],fontSize=8,leading=11));style.add(ParagraphStyle('CodeBlock',fontName='Mono',fontSize=7.5,leading=10,spaceAfter=8));story=[]
def p(t,s='Text'):return Paragraph(escape(t).replace('\n','<br/>'),style[s])
def heading(t):story.append(p(t,'Heading'))
manifest=json.loads((R/'course_manifest.json').read_text());progress=json.loads((R/'draft-progress.json').read_text())
heading("Rohail’s School Music Night")
story.extend([p('USACO Foundations and Beyond — V2 student workbook'),p('Four lessons · C++17 programs · worked reasoning · independent practice'),p('This course develops C++ and Bronze foundations, selected Silver techniques and selected Gold foundations. Platinum-level techniques are largely a prerequisite roadmap, not a claim of mastery. No single course covers every possible USACO problem or replaces sustained practice.'),p('Delivery uses the requested 1.25× tempo of Voice A. Final video chapter times come from measured audio. Manuscript-based estimates are provisional.'),p('Use the video for guided explanations, this workbook for attempts and the source package for complete runnable code. Pause the video when prompted. The brief cue before an answer is not intended to supply all the time needed to solve the exercise.'),p('The students and school event are fictional. Supplied clean lyric hooks are educational reinterpretations; no artist voice, recording, melody or endorsement is used. Source headings supplied by the user are not independently verified release metadata.')])
heading('How to study')
story.append(p('For each problem: state the input/output contract; draw a small example; define every state variable; justify the algorithm; estimate time and memory; implement; test boundaries; then solve a changed problem without copying. Keep a notebook of failed ideas and the counterexamples that explain their failure.'))
heading('Build and run the companions')
story.append(Preformatted('g++ -std=c++17 -O2 -Wall -Wextra program.cpp -o program\n./program < input.txt',style['CodeBlock']))
story.append(p('Programs use standard input/output. Historical official problems may specify named files; adapt only as their current practice/submission instructions require. Each companion validates its teaching bounds. Do not assume a different problem has identical constraints.'))
story.append(PageBreak());heading('Course map')
for part,row in zip(manifest['parts'],progress['parts']):
 group=[p(f"Part {part['number']}: {part['title']}",'Heading')]
 report_path=OUT/f"part{part['number']}"/'verification.json'
 if report_path.exists():
  report=json.loads(report_path.read_text());seconds=round(report['duration'])
  group.append(p(f"Measured video runtime: {seconds//60}:{seconds%60:02d}; {row['spoken_words']:,} narrated words."))
  for ch in json.loads((report_path.parent/'chapters.json').read_text()):
   sec=round(ch['start']);group.append(p(f"{sec//60:02d}:{sec%60:02d} — {ch['title'].title()}",'Small'))
 else:
  group.append(p(f"{row['spoken_words']:,} narrated words; provisional {row['estimated_minutes']:.1f} minutes at the current measured sample pace."))
  for name in part['scripts']:group.append(p('• '+topic(name).replace('_',' ').title()))
 story.append(KeepTogether(group))
custom={
'foundations':('Two int operands are each1,500,000,000. Why is assigning their sum to long long insufficient? Also explain why reserve(100) on an empty vector does not make index0 valid.','Promote before addition, for example1LL*a+b. Assignment happens after the expression is evaluated. Reserve changes capacity, not size; construct elements or push_back before indexing.'),
'sorting':('For4,2,4,9,2, give the sorted sequence and distinct count. Why would sorting be invalid if a query asks about the people originally at positions2 through4?','Sorted:2,2,4,4,9; three distinct values. Sorting changes positions, so an original-position interval must preserve order or retain an appropriate separate mapping.'),
'topological':('For edges0→2,1→2,2→3,1→4, give one valid order. Then add3→1. Why is task4 blocked even though it is not on the new cycle?','One order is0,1,2,4,3. The new cycle1→2→3→1 prevents those prerequisites from being completed. Task4 depends on1 and is therefore blocked downstream; being unprocessed does not imply every such vertex lies on a cycle.'),
'dsu_mst':('For edges0–1 cost1,1–2 cost2,0–2 cost3,2–3 cost4,0–3 cost10, find an MST. Why are DSU parent links not necessarily selected network edges?','Choose0–1,1–2,2–3 for total7. DSU parents represent component bookkeeping and can change under compression; record accepted original edges separately.'),
'segment_sparse':('Start with3,1,4,1,5. Assign index2 to10. Give the new whole sum and sum on[1,4). Explain why overlapping sparse-table blocks work for minimum but not ordinary sum.','The whole sum is20 and[1,4) sums to12. Minimum is idempotent: seeing a value twice changes nothing. Sum double-counts overlapped values.'),
'advanced_roadmap':('Choose one advanced topic, name its prerequisite and write a concrete problem that motivates it. Explain what you still cannot implement from this roadmap alone.','One valid choice is subtree sums: learn rooted DFS and entry-only subtree intervals, then combine with range-sum queries. The roadmap names the connection; a full traversal implementation, correctness argument and transfer practice still need study.')}
givens={
'loop_trace':'Algorithm: initialize total=0, then for i=0 while i<n add a[i] to total and increment i. Indices are zero-based. ',
'string_lab':'Return the zero-based position of the first character occurring exactly once in the entire uppercase string, or -1 if none. ',
'casework':'There are three possible starting positions, 1, 2 and 3. A hidden token moves with each swap; a correct guess after the swap earns one point. ',
'backtracking':'Each input position can be selected at most once; equal values at distinct positions are distinct choices. Count subsets whose values sum to the target. ',
'prefix':'Given category sequence [2,1,3,1,2,1], with one-based positions and categories 1, 2 and 3. P[k] counts categories in the first k positions, with P[0]=[0,0,0]. ',
'ranges':'Start with five zeros at indices 0..4. Add 3 on [1,4), then add 2 on [2,5); half-open intervals exclude the right endpoint. The separate 3×3 grid has rows [1,2,3], [4,5,6], [7,8,9]. ',
'dashboard_lab':'All indices are zero-based; intervals are half-open and all updates precede queries. ',
'two_pointers':'Use zero-based original positions, distinct indices for a pair, and contiguous windows. ',
'binary_search':'Boxes must retain their order and cannot be split. Each trip carries one consecutive block with total weight at most the capacity. ',
'greedy':'Requests are half-open intervals: touching endpoints are allowed. Maximize the number of accepted requests in one room. ',
'bfs':'Original undirected unit-edge graph: vertices 0..6; edges (0,1),(0,2),(1,3),(2,4),(3,5),(4,5). Source is 0; visit neighbors in increasing order. Vertex 6 is originally isolated. ',
'grid_lab':'Coordinates are zero-based (row,column); legal moves are up/down/left/right through open cells, each costing one. Thus row one column one means (1,1), the bottom-middle cell. ',
'functional_graph':'Array indices are zero-based; entry at index u is the unique successor of u. ',
'dynamic_programming':'Each denomination has unlimited copies; minimize token count for an exact target, or report impossible. ',
'knapsack':'Each item is available once, weights are positive, and total weight may be at most capacity. For the loop-order question, use one item of weight 2 and value 3 with capacity 4. ',
'dijkstra':'Directed graph on vertices 0..3, source 0: 0→1 cost 10, 0→2 cost 3, 2→1 cost 4, 1→3 cost 2, 2→3 cost 12. ',
'fenwick':'Current length-eight array is [3,1,4,1,8,9,2,6]. External indices are 0..7; Fenwick internal indices are 1..8. Prefix(r) sums external [0,r). ',
'segment_sparse':'Array indices are zero-based; intervals exclude their right boundary. ',
}
questions=[];number=0
for part in manifest['parts']:
 story.append(PageBreak() if part['number']==1 else CondPageBreak(220));heading(f"Part {part['number']} — Practice before answers")
 for name in part['scripts']:
  seq=scenes((R/name).read_text());pairs=[]
  for i,(direction,text) in enumerate(seq):
   if is_question(text):pairs.append((text,seq[i+1][1]))
  if not pairs and topic(name) in custom:pairs=[custom[topic(name)]]
  for question,answer in pairs:
   question=givens.get(topic(name),'')+question
   if topic(name)=='knapsack':answer='With capacity 3, choose the weight-3, value-5 item: answer 5. Capacity zero or no items gives 0. For one weight-2, value-3 item and capacity 4, an ascending loop sets dp[2]=3, then computes dp[4]=dp[2]+3=6, reusing the same item. Descending capacities evaluate dp[4] while dp[2] still belongs to the previous item layer, so dp[4]=3; only afterward does dp[2] become 3. Descending order therefore enforces single use.'
   if topic(name)=='grid_lab':answer='All coordinates below are zero-based; the changed cell is (1,1). '+answer
   number+=1;questions.append(dict(number=number,source=name,question=question,answer=answer))
   block=[p(f"{number}. {topic(name).replace('_',' ').title()}",'Heading'),p(question),p('Your contract / trace / argument:'),Spacer(1,55)]
   story.append(KeepTogether(block))
story.append(PageBreak());heading('Solutions and reasoning — consult after attempting')
story.append(p('An answer is not a substitute for the state meaning and proof. Where multiple routes/orders/witnesses are valid, compare the required properties rather than demanding the same tie choice.'))
for q in questions:story.append(KeepTogether([p(f"{q['number']}. {topic(q['source']).replace('_',' ').title()}",'Heading'),p(q['answer'])]))
story.append(PageBreak());heading('Complete standalone C++17 companions')
story.append(p('Each file is a separate program with its own main function. Compile one file at a time. The downloadable source package preserves exact files; PDF line wrapping is for reading. The algorithm library from V1 is additional reference, not evidence that every advanced algorithm is fully taught in V2.'))
for f in sorted(R.glob('*.cpp')):
 lines=f.read_text().splitlines();chunks=max(1,math.ceil(len(lines)/48))
 for j in range(chunks):
  block=lines[len(lines)*j//chunks:len(lines)*(j+1)//chunks]
  # Wrap at whitespace for readable complete code; source archive is authoritative.
  import textwrap
  wrapped=[]
  for line in block:wrapped.extend(textwrap.wrap(line,100,replace_whitespace=False,drop_whitespace=False) or [''])
  block=[Preformatted('\n'.join(wrapped),style['CodeBlock'])]
  if j==0:block.insert(0,p(f.name,'Heading'))
  story.append(KeepTogether(block))
story.append(PageBreak());heading('Practice links and attribution')
for text in ['Official archive/training: https://usaco.org/index.php?page=training','Shell Game (Bronze): https://usaco.org/index.php?page=viewproblem2&cpid=891','Breed Counting (Silver): https://usaco.org/index.php?page=viewproblem2&cpid=572','The Great Revegetation (Silver): https://usaco.org/index.php?page=viewproblem2&cpid=920','Official resources: https://usaco.org/index.php?page=resources','Community learning guide (not an official syllabus): https://usaco.guide/']:story.append(p(text))
story.append(p('Consult current official rules for compiler versions and contest policies. Division groupings here are learning guidance, not an exhaustive official list.'))
heading('Supplied musical references')
credits=[
('SICKO MODE','Boolean on/off and resetting a hypothetical case.'),
('In My Feelings','Include/exclude choices in backtracking.'),
('Toosie Slide','Pointer movement; each discard still requires proof.'),
("Hold On, We’re Going Home",'Visited state and the parent route back to the start.'),
('Work / Started From the Bottom','Repeated subproblems and dependency-ordered DP.'),
('Runaway','Look for concrete counterexamples in the string lab.'),
('Reborn','Move forward through subsequence indices while checking value order.'),
('Too Much','Deliberate tracing in the integrated review segment.')]
for title,use in credits:story.append(p(title+' — '+use))
story.append(p('Hooks are selected educational adaptations from text supplied by the user, including four distinct Drake/Kanye excerpt collections and pasted song passages. Song headings are credited as supplied. Original classroom jokes and all algorithm explanations are newly written. The artists did not narrate or endorse this course.'))
def footer(c,doc):
 c.setFont('Body',8);c.setFillColor(HexColor('#567365'));c.drawString(45,25,'Rohail · USACO V2 · questions precede solutions');c.drawRightString(567,25,str(doc.page))
path=OUT/'Rohail-USACO-V2-Workbook.pdf';SimpleDocTemplate(str(path),pagesize=(612,792),rightMargin=45,leftMargin=45,topMargin=42,bottomMargin=44).build(story,onFirstPage=footer,onLaterPages=footer)
(OUT/'workbook-exercises.json').write_text(json.dumps(questions,indent=2))
print(path,len(questions),'exercises',path.stat().st_size,'bytes')
