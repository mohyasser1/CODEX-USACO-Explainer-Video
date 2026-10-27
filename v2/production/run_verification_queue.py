"""Validate finished parts and extract frames without restarting active builds."""
import subprocess,time,json
from pathlib import Path
R=Path(__file__).resolve().parent;O=Path('/workspace/usaco-film-v2/output/course');done=set()
while len(done)<4:
 for n in range(1,5):
  f=O/f'part{n}'/'verification.json'
  if n in done or not f.exists():continue
  report=json.loads(f.read_text())
  if not report.get('manuscript_paragraphs_exact'):
   with (O/f'part{n}-final-check.log').open('w') as log:subprocess.run(['python',str(R/'verify_delivery.py'),str(n)],stdout=log,stderr=subprocess.STDOUT,check=True)
  print('READY FOR FRAME REVIEW',n,flush=True);done.add(n)
 time.sleep(15)
