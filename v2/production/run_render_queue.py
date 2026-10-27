"""Render each complete extended part once, preserving checkpoints."""
import json,time,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];OUT=Path('/workspace/usaco-film-v2/output/course');done=set()
while len(done)<4:
 manifest=json.loads((ROOT/'course_manifest.json').read_text());started=False
 for part in manifest['parts']:
  n=part['number'];dest=OUT/f'part{n}';timing=dest/'timing.json'
  if n in done or not timing.exists():continue
  data=json.loads(timing.read_text())
  if set(part['scripts'])!=set(c['source'] for c in data['cues']):continue
  if (dest/'verification.json').exists():done.add(n);continue
  print('RENDER START',n,flush=True)
  with (OUT/f'part{n}-render.log').open('w') as log:subprocess.run(['python',str(ROOT/'production/render_course.py'),str(n)],stdout=log,stderr=subprocess.STDOUT,check=True)
  done.add(n);print('RENDER COMPLETE',n,flush=True);started=True;break
 if not started:time.sleep(15)
