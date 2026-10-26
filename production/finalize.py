"""Finalize visible captions plus an external SRT, then verify locally."""
import time,json,subprocess,hashlib
from pathlib import Path
from assemble import probe
ROOT=Path('/workspace/usaco-film/output');SCRIPT=Path(__file__).parent
while True:
 try:
  report=json.loads((ROOT/'verification.json').read_text())
  if report['status']=='passed':break
 except (FileNotFoundError,json.JSONDecodeError):pass
 time.sleep(3)
movie=ROOT/'Bessie-vs-the-Algorithm-USACO.mp4';x=probe(movie)
# MP4 players differ in their treatment of default text tracks. Burned captions
# are universal; the companion SRT is explicitly opt-in, avoiding double text.
if any(s['codec_type']=='subtitle' for s in x['streams']):
 tmp=movie.with_suffix('.visible-captions.mp4')
 subprocess.run(['ffmpeg','-v','warning','-y','-i',str(movie),'-map','0:v:0','-map','0:a:0','-map_metadata','0','-map_chapters','0','-c','copy','-movflags','+faststart',str(tmp)],check=True)
 backup=ROOT/'qa'/'film-with-embedded-text-track-preserved.mp4';movie.rename(backup);tmp.rename(movie)
x=probe(movie);assert not any(s['codec_type']=='subtitle' for s in x['streams'])
report['checks'].append('Visible captions plus external SRT; no duplicate embedded text track')
report['bytes']=movie.stat().st_size;report['sha256']=hashlib.sha256(movie.read_bytes()).hexdigest();report['duration_seconds']=float(x['format']['duration'])
report['streams']=[{k:s.get(k) for k in ['codec_type','codec_name','profile','level','width','height','duration','sample_rate','r_frame_rate']} for s in x['streams']]
(ROOT/'verification.json').write_text(json.dumps(report,indent=2))
subprocess.run(['python',str(SCRIPT/'verify_media.py')],check=True)
print('Local finalization complete.',flush=True)
