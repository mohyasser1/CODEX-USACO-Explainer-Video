"""Two cloud CPU workers; each synthesizes two parts sequentially."""
import subprocess,concurrent.futures
from pathlib import Path
ROOT=Path(__file__).resolve().parent;OUT=Path('/workspace/usaco-film-v2/output/course')
def worker(parts):
 for p in parts:
  with (OUT/f'part{p}-narration.log').open('w') as log:
   subprocess.run(['python',str(ROOT/'narrate_course.py'),str(p)],stdout=log,stderr=subprocess.STDOUT,check=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
 fs=[pool.submit(worker,[1,2]),pool.submit(worker,[3,4])]
 for f in fs:f.result()
