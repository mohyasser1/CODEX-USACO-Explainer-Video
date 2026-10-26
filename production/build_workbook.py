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
