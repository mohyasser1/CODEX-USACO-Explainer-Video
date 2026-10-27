"""Four unchanged narration excerpts demonstrating corrected learner panels."""
import sys,json,math,subprocess,hashlib
from pathlib import Path
import soundfile as sf,numpy as np
from PIL import ImageDraw
from render_course import base,motion,FPS,TEMPO,stamp
from art import model
O=Path('/workspace/usaco-film-v2/output/course');D=O/'renderer-repair';D.mkdir(exist_ok=True)
t=json.loads((O/'part1/timing.json').read_text());wanted={('part1_loop_trace_script.txt',9),('part1_functions_cost_script.txt',6),('part1_string_lab_script.txt',9),('part1_backtracking_script.txt',8)}
cues=[];pos=0;sr=24000
with sf.SoundFile(O/'part1/narration.wav') as src,sf.SoundFile(D/'audio.wav','w',samplerate=sr,channels=1,subtype='PCM_16') as dst:
 for old in t['cues']:
  if (old['source'],old['scene']) not in wanted:continue
  a=round(old['start']*sr);b=round(old['end']*sr);src.seek(a);audio=src.read(b-a,dtype='float32');dst.write(audio)
  c=dict(old);c.update(start=pos,speech_end=pos+old['speech_end']-old['start'],end=pos+len(audio)/sr);cues.append(c);pos=c['end']
(D/'timing.json').write_text(json.dumps({'source':'Four excerpts from unchanged approved Part1 audio','tempo':TEMPO,'duration':pos/TEMPO,'cues':cues},indent=2))
(D/'captions.srt').write_text('\n\n'.join(f"{i+1}\n{stamp(c['start']/TEMPO)} --> {stamp(c['speech_end']/TEMPO)}\n{c['text']}" for i,c in enumerate(cues)))
video=D/'V2-Renderer-Repair-Teaching-Excerpts.mp4';proc=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s','1280x720','-r',str(FPS),'-i','-','-i',str(D/'audio.wav'),'-af',f'atempo={TEMPO},loudnorm=I=-16:TP=-1.5:LRA=11','-c:v','libx264','-preset','veryfast','-crf','26','-threads','2','-pix_fmt','yuv420p','-c:a','aac','-b:a','96k','-shortest','-movflags','+faststart',str(video)],stdin=subprocess.PIPE)
images=[base(c,1,'') for c in cues];blank=[base(c,1,'',False) for c in cues];idx=0
for frame in range(math.ceil(pos/TEMPO*FPS)):
 at=frame/FPS*TEMPO
 while idx+1<len(cues) and at>=cues[idx]['end']:idx+=1
 c=cues[idx];im=(images[idx] if at<c['speech_end'] else blank[idx]).copy();motion(ImageDraw.Draw(im),model(c),c['scene'],(at-c['start'])/TEMPO);proc.stdin.write(im.tobytes())
proc.stdin.close();assert proc.wait()==0
subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(video),'-f','null','-'],check=True)
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(video)]));ds=[float(s['duration']) for s in probe['streams']];assert max(ds)-min(ds)<.2
for i,c in enumerate(cues):subprocess.run(['ffmpeg','-v','error','-y','-ss',str(c['start']/TEMPO+2),'-i',str(video),'-frames:v','1',str(D/f'encoded-{i}.png')],check=True)
r={'duration':float(probe['format']['duration']),'full_decode':'passed','av_end_difference':max(ds)-min(ds),'sha256':hashlib.sha256(video.read_bytes()).hexdigest(),'bytes':video.stat().st_size,'scope':'Four complete unchanged narration paragraphs; repaired learner-facing visuals; not a new voice audition'};(D/'verification.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
