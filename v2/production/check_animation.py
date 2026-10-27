"""Short silent engineering clip: verify graph/DP/range transitions before batches."""
import sys,json,subprocess,hashlib
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from script_text import scenes
from render_course import base,motion,FPS,ORANGE,font
from art import model
from PIL import ImageDraw
r=Path(__file__).resolve().parents[1];out=Path('/workspace/usaco-film-v2/output/course/layout')
items=[('part3_bfs_script.txt',i) for i in [4,5,6,7]]+[('part3_dynamic_programming_script.txt',i) for i in [8,9,10,11]]+[('part4_fenwick_script.txt',i) for i in [3,5,6,7]]
video=out/'Graph-DP-Range-Animation-Engineering-Check.mp4'
p=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s','1280x720','-r',str(FPS),'-i','-','-an','-c:v','libx264','-preset','veryfast','-crf','24','-threads','1','-pix_fmt','yuv420p','-movflags','+faststart',str(video)],stdin=subprocess.PIPE)
for name,i in items:
 cue,text=scenes((r/name).read_text())[i];c=dict(source=name,scene=i,direction=cue,text=text);m=model(c);im=base(c,int(name[4]),'engineering check')
 for j in range(FPS*3):
  f=im.copy();d=ImageDraw.Draw(f);motion(d,m,i,j/FPS);d.rectangle((0,685,1280,720),fill='white');d.text((25,693),'SILENT ENGINEERING CHECK · not teaching pace · '+name+' / scene '+str(i),font=font(15),fill=ORANGE);p.stdin.write(f.tobytes())
p.stdin.close();assert p.wait()==0
subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(video),'-f','null','-'],check=True)
# Extract a frame inside the moving Fenwick update path (eleventh 3s panel).
subprocess.run(['ffmpeg','-v','error','-y','-ss','31.5','-i',str(video),'-frames:v','1',str(out/'encoded-fenwick-motion.png')],check=True)
report=dict(passed=True,panels=len(items),duration_seconds=36,full_decode='passed',sha256=hashlib.sha256(video.read_bytes()).hexdigest(),scope='Silent graph,coin-DP and Fenwick transition engineering check; numerical oracles in course-models.json; not an audio pacing sample')
(r/'verification/course-animation.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
