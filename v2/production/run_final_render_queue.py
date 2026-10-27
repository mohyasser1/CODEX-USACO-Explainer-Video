"""Final renderer queue. Starts only after the renderer review release marker."""
import json,time,subprocess,shutil,hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[1];O=Path('/workspace/usaco-film-v2/output/course')
while not (O/'renderer-release.json').exists():time.sleep(10)
for n in [1,3,4,2]:
 p=O/f'part{n}'
 while not (p/'timing.json').exists():time.sleep(10)
 manifest=json.loads((R/'course_manifest.json').read_text())['parts'][n-1]
 t=json.loads((p/'timing.json').read_text());assert {c['source'] for c in t['cues']}==set(manifest['scripts'])
 archive=p/'superseded-before-learner-panels';archive.mkdir(exist_ok=True)
 for name in [f'Rohail-USACO-V2-Part-{n}.mp4','verification.json']:
  if (p/name).exists() and not (archive/name).exists():shutil.copy2(p/name,archive/name)
 print('FINAL LEARNER RENDER START',n,flush=True)
 with (O/f'part{n}-learner-render.log').open('w') as log:subprocess.run(['python',str(R/'production/render_course.py'),str(n)],stdout=log,stderr=subprocess.STDOUT,check=True)
 with (O/f'part{n}-learner-check.log').open('w') as log:subprocess.run(['python',str(R/'production/verify_delivery.py'),str(n)],stdout=log,stderr=subprocess.STDOUT,check=True)
 print('READY FOR FINAL FRAME REVIEW',n,flush=True)
