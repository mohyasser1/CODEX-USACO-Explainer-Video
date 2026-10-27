"""Final-part manuscript/metadata/stream checks plus sampled encoded frames."""
import sys,json,subprocess,hashlib
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from script_text import scenes
R=Path(__file__).resolve().parents[1];OUT=Path('/workspace/usaco-film-v2/output/course')
def verify(n):
 p=OUT/f'part{n}';t=json.loads((p/'timing.json').read_text());v=p/f'Rohail-USACO-V2-Part-{n}.mp4';report=json.loads((p/'verification.json').read_text());manifest=json.loads((R/'course_manifest.json').read_text())['parts'][n-1]
 expected=[(name,i,d,text) for name in manifest['scripts'] for i,(d,text) in enumerate(scenes((R/name).read_text())) if text.strip()]
 actual=[(c['source'],c['scene'],c['direction'],c['text']) for c in t['cues']];assert actual==expected,'Narration manuscript mismatch'
 assert report['words']==sum(len(text.split()) for _,_,_,text in expected)
 assert abs(report['duration']-t['duration']/1.25)<.25
 assert report['embedded_english_subtitles']
 # Decode just the final audio to inspect finite values and sample clipping.
 proc=subprocess.Popen(['ffmpeg','-v','error','-i',str(v),'-map','0:a:0','-f','f32le','-'],stdout=subprocess.PIPE)
 peak=0.0
 while True:
  raw=proc.stdout.read(4*1024*1024)
  if not raw:break
  a=np.frombuffer(raw,dtype=np.float32);assert np.isfinite(a).all();peak=max(peak,float(np.max(np.abs(a))))
 proc.stdout.close();assert proc.wait()==0
 assert peak<1.0,('clipping',peak)
 selected=[]
 for j,c in enumerate(t['cues']):
  if c['scene']==0 or any(x in c['direction'].lower() for x in ['separate answer','answer scene','empty input','proof initialization','amount3','pop2','point addition index4']):selected.append((j,c))
 dest=p/'encoded-frames';dest.mkdir(exist_ok=True)
 for j,c in selected:
  at=c['start']/1.25+.3
  subprocess.run(['ffmpeg','-v','error','-y','-ss',str(at),'-i',str(v),'-frames:v','1',str(dest/f'{j:03}.png')],check=True)
 report.update(manuscript_paragraphs_exact=True,peak_decoded_audio=peak,sampled_frame_indices=[j for j,c in selected],frame_inspection='Extracted; visual inspection pending',sha256=hashlib.sha256(v.read_bytes()).hexdigest(),bytes=v.stat().st_size)
 (p/'verification.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2),flush=True)
if __name__=='__main__':verify(int(sys.argv[1]))
