"""Wait for original part1/3 writers, then reuse cache to include new lab sections."""
import json,time,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parent;OUT=Path('/workspace/usaco-film-v2/output/course')
for part in [1,3]:
 target=OUT/f'part{part}'/'timing.json'
 while not target.exists():time.sleep(15)
 with (OUT/f'part{part}-extension-refresh.log').open('w') as log:
  subprocess.run(['python',str(ROOT/'narrate_course.py'),str(part)],stdout=log,stderr=subprocess.STDOUT,check=True)
 print('EXTENDED PART COMPLETE',part,flush=True)
