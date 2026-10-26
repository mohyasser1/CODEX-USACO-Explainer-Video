"""Create the small offline companion bundle after final media checks pass."""
import json,time,zipfile,hashlib
from pathlib import Path
ROOT=Path('/workspace/usaco-film/output');REPO=Path(__file__).resolve().parents[1]
while True:
 try:
  qa=json.loads((ROOT/'final-QA.json').read_text());media=json.loads((ROOT/'verification.json').read_text())
  if qa['status']=='passed' and media['status']=='passed':break
 except (FileNotFoundError,json.JSONDecodeError):pass
 time.sleep(3)
start='''BESSIE VS. THE ALGORITHM — START HERE

Watch the separately delivered film in short sessions. Pause at each coding challenge.
Use chapter-index.txt to return to a topic. Bessie-USACO-captions.srt is an optional
external caption file; the MP4 includes visible captions for universal playback.

Read Bessie-USACO-workbook.pdf for the complete lessons, exercises, answer checkpoints,
complexity assumptions, and Wrong Answer Awards debugging exercises.

RUN THE C++ EXAMPLES (C++17 compiler):
g++ -std=c++17 -O2 -Wall -Wextra examples/main.cpp -o lesson
g++ -std=c++17 -O2 -Wall -Wextra examples/test.cpp -o tests
./tests
./lesson shipping

Then enter:
6 3
3 2 2 4 1 4
Expected answer: 6

The workbook explains other modes and input contracts. The header contains additional
selected algorithms; the tests exercise them against simpler independent oracles.

LEARNING SCOPE
C++ and Bronze foundations, Silver patterns, Gold algorithms, and Platinum extensions.
The advanced chapters introduce tools whose full mastery requires dedicated problems.
This film cannot replace practice or guarantee contest promotion. Check current event
rules and compiler support at the official USACO site before competing.

PRODUCTION
Original cartoon/motion graphics and procedural hip-hop instrumental. Synthetic stock
narration, with no artist-voice imitation or copied song recordings. Sentence boundaries
are measured; within-sentence caption timing is approximate and proportional to words.
See validation reports for the checks performed and their limits.
'''
(ROOT/'START-HERE.txt').write_text(start)
files=[]
for p in (REPO/'examples').glob('*'):
 if p.suffix in ['.cpp','.hpp']:files.append((p,'examples/'+p.name))
for p in (REPO/'production').glob('*'):
 if p.suffix in ['.py','.json','.txt'] and p.name!='delivery.json':files.append((p,'production/'+p.name))
files.append((REPO/'PRODUCTION.txt','PRODUCTION.txt'))
for name in ['START-HERE.txt','Bessie-USACO-workbook.pdf','complete-script.txt','Bessie-USACO-captions.srt','Bessie-USACO-captions.ass','chapter-index.txt','chapters.json']:
 files.append((ROOT/name,name))
for name in ['verification.json','final-QA.json','document-QA.json','code-test-results.txt']:
 files.append((ROOT/name,'validation/'+name))
target=ROOT/'Bessie-USACO-course-materials.zip'
with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED) as z:
 for p,name in files:z.write(p,name)
 assert z.testzip() is None
report={'file':str(target),'bytes':target.stat().st_size,'sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'entries':len(files)}
(ROOT/'package-manifest.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2),flush=True)
