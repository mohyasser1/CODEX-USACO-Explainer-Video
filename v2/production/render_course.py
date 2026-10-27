"""Warm course panels with authored models and paragraph-bounded captions."""
import sys,json,math,subprocess,hashlib,re
from pathlib import Path
from functools import lru_cache
from PIL import Image,ImageDraw,ImageFont
from art import model,topic
ROOT=Path(__file__).resolve().parents[1];OUT=Path('/workspace/usaco-film-v2/output/course');W,H,FPS=1280,720,12;TEMPO=1.25
BG='#fbf5e9';INK='#17354b';GREEN='#426954';ORANGE='#b64c2a';PALE='#e7eee4'
@lru_cache(None)
def font(n,bold=False,mono=False):return ImageFont.truetype('/usr/share/fonts/truetype/dejavu/'+('DejaVuSansMono' if mono else 'DejaVuSans')+('-Bold' if bold else '')+'.ttf',n)
def wrap(t,f,width):
 rows=[]
 for para in str(t).split('\n'):
  line=''
  for word in para.split():
   q=(line+' '+word).strip()
   if f.getlength(q)>width and line:rows.append(line);line=word
   else:line=q
  if line:rows.append(line)
 return rows
def fitted(d,text,box,maxsize=25,minsize=16,bold=False,mono=False):
 x,y,w,h=box
 for size in range(maxsize,minsize-1,-1):
  f=font(size,bold,mono);lines=str(text).splitlines() if mono else wrap(text,f,w)
  if len(lines)*(size+5)<=h and all(f.getlength(l)<=w for l in lines):break
 else:raise ValueError(('text overflow',str(text)[:80],box))
 for j,line in enumerate(lines):d.text((x,y+j*(size+5)),line,font=f,fill=INK)
 return size

def diagram(d,m,box):
 x,y,w,h=box;k=m['kind']
 if k=='array':
  a=m['values'];gap=min(88,w/max(1,len(a)));start=x+10
  for j,v in enumerate(a):
   xx=start+j*gap;active=j in m.get('active',[])
   d.rounded_rectangle((xx,y+35,xx+gap-8,y+100),8,fill='white',outline=ORANGE if active else '#becdbd',width=3 if active else 1)
   fitted(d,str(v),(xx+8,y+52,gap-24,40),26,16,True)
   d.text((xx+gap/2-10,y+109),str(j+m.get('index_start',0)),font=font(18),fill=GREEN)
  if m.get('small'):fitted(d,m['small'],(x+10,y+160,w-20,60),23)
 elif k in ['rows','tree']:
  rows=m['rows'];rh=min(49,h/max(1,len(rows)))
  for j,row in enumerate(rows):
   yy=y+j*rh;d.rounded_rectangle((x,yy,x+w,yy+rh-5),6,fill='white')
   fitted(d,str(row[0]),(x+12,yy+7,min(230,w*.35)-15,rh-10),20,15,True)
   fitted(d,str(row[1]),(x+min(230,w*.35),yy+7,w-min(230,w*.35)-14,rh-10),23,15)
 elif k=='table':
  rows=[m['headers']]+m['rows'];rh=min(32,h/max(1,len(rows)));cw=w/len(m['headers'])
  for j,row in enumerate(rows):
   for col,v in enumerate(row):
    xx=x+col*cw;yy=y+j*rh;d.rectangle((xx,yy,xx+cw-2,yy+rh-2),fill='#d8ebda' if j==0 else 'white')
    fitted(d,str(v),(xx+5,yy+4,cw-10,rh-5),20,12,j==0)
 elif k=='graph':
  n=m['n'];coords={j:(x+70+(j%3)*190,y+40+(j//3)*70) for j in range(n)}
  if n==4:coords={0:(x+75,y+110),1:(x+300,y+35),2:(x+300,y+185),3:(x+530,y+110)}
  path=set(zip(m.get('path',[]),m.get('path',[])[1:]))
  for edge in m['edges']:
   u,v=edge[:2];a,b=coords[u],coords[v];color=ORANGE if (u,v) in path or (v,u) in path else '#879b88'
   if u==v:d.arc((a[0]-35,a[1]-45,a[0]+35,a[1]+10),180,500,fill=color,width=3);continue
   d.line([a,b],fill=color,width=3)
   if m.get('directed'):
    ang=math.atan2(b[1]-a[1],b[0]-a[0]);tx=b[0]-24*math.cos(ang);ty=b[1]-24*math.sin(ang)
    d.polygon([(tx,ty),(tx-12*math.cos(ang-.5),ty-12*math.sin(ang-.5)),(tx-12*math.cos(ang+.5),ty-12*math.sin(ang+.5))],fill=color)
   if len(edge)>2:
    tx=(a[0]+b[0])/2;ty=(a[1]+b[1])/2;d.rectangle((tx-16,ty-12,tx+24,ty+16),fill=PALE);d.text((tx-10,ty-10),str(edge[2]),font=font(19,True),fill=INK)
  for j,(xx,yy) in coords.items():
   d.ellipse((xx-22,yy-22,xx+22,yy+22),fill='white',outline=GREEN,width=2);d.text((xx-7,yy-13),str(j+m.get('node_offset',0)),font=font(22,True),fill=INK)
   value=m.get('dist',[None]*n)[j]
   if value is not None:d.text((xx+27,yy-11),str(value),font=font(18),fill=ORANGE)
  if m.get('queue'):d.text((x+8,y+h-25),'Queue: '+str(m['queue']),font=font(21,True),fill=INK)
 elif k=='grid':
  grid=m['grid'];height=len(grid);width=len(grid[0]);cell=min(62,(h-15)/height);sx=x+40
  for r,row in enumerate(grid):
   for c,v in enumerate(row):
    xx=sx+c*cell;yy=y+r*cell;d.rectangle((xx,yy,xx+cell-3,yy+cell-3),fill='#263c49' if v=='#' else 'white')
    if v!='#':
     d.text((xx+8,yy+5),v,font=font(23,True),fill=INK)
     if r*width+c in m.get('dist',{}):d.text((xx+cell-24,yy+cell-25),str(m['dist'][r*width+c]),font=font(17),fill=ORANGE)
  if m.get('dist'):d.text((sx+width*cell+15,y+15),'Orange = distance',font=font(19),fill=ORANGE)
 elif k=='grid_compare':
  for j,grid in enumerate(m['grids']):
   bx=x+j*w/2;fitted(d,m['case_labels'][j],(bx+8,y,w/2-15,32),19,15,True)
   cell=58
   for r,row in enumerate(grid):
    for c,v in enumerate(row):
     xx=bx+20+c*cell;yy=y+45+r*cell
     d.rectangle((xx,yy,xx+cell-3,yy+cell-3),fill='#263c49' if v=='#' else 'white')
     if v!='#':d.text((xx+16,yy+12),v,font=font(23,True),fill=INK)
 elif k=='fenwick':
  cell=w/8
  for i,v in enumerate(m['values']):
   d.text((x+i*cell+10,y),str(v),font=font(20,True),fill=INK)
   d.text((x+i*cell+7,y+23),'idx'+str(i),font=font(12),fill=GREEN)
  # Each row is a stored block, with its own internal index and sum.
  for i in range(1,9):
   yy=y+45+(i-1)*21;l=i-(i&-i);color='#f0c9b5' if i in m.get('active',[]) else 'white'
   d.rounded_rectangle((x+l*cell,yy,x+i*cell-3,yy+20),4,fill=color,outline='#b8c6b5')
   d.text((x+l*cell+4,yy),f'b{i}={m["bit"][i]}',font=font(16),fill=INK)
 elif k=='question':
  if m.get('question_model'):
   diagram(d,m['question_model'],box)
  else:fitted(d,'ROHAIL’S NEXT CHALLENGE\n\nPredict → trace → explain\n\nPause here. Resume for the answer.',(x+25,y+20,w-50,h-20),27,20,True)
 else:
  fitted(d,m['notes'],(x+15,y+10,w-30,h-20),27,16)

def base(c,part,title,caption=True):
 m=model(c);im=Image.new('RGB',(W,H),BG);d=ImageDraw.Draw(im)
 d.rectangle((0,0,W,7),fill=ORANGE)
 d.text((25,17),f'ROHAIL / SCHOOL MUSIC NIGHT     PART {part}',font=font(18,True),fill=GREEN)
 head=topic(c['source']).replace('_',' ').upper();d.text((25,48),head,font=font(29,True),fill=INK)
 d.text((1050,24),'Rohail  +  Maya',font=font(20),fill=GREEN)
 d.rounded_rectangle((20,95,760,374),12,fill=PALE)
 fitted(d,m['label'],(35,105,710,30),20,17,True)
 diagram(d,m,(35,143,710,219))
 d.rounded_rectangle((778,95,1260,374),12,fill='white',outline='#ded8cb')
 code=m.get('code',[])
 if code and not m['question']:
  d.text((792,108),'CORE STEPS · COMPANION HAS FULL CODE',font=font(16,True),fill=GREEN)
  fitted(d,'\n'.join(code),(792,146,450,212),19,14,False,True)
 else:
  d.text((792,108),'WHAT TO NOTICE',font=font(18,True),fill=GREEN)
  fitted(d,m['notes'],(792,143,450,214),23,15)
 d.rectangle((0,392,W,689),fill='white')
 if caption:fitted(d,c['text'],(28,401,1224,276),23,17)
 else:fitted(d,'Pause the video to work; resume for the answer.' if m['question'] else 'Follow the model and the meaning of its state.',(28,445,1220,130),27,20)
 d.text((25,695),'Original synthetic narrator · supplied clean educational hooks · diagrams are paragraph-level trace panels',font=font(13),fill=GREEN)
 return im

def motion(d,m,scene,elapsed):
 # Short illustrative transitions follow authored affected objects, never code cycling.
 if m['topic']=='bfs' and scene in [4,5,6,7] and elapsed<1.8:
  u,v={4:(0,1),5:(1,3),6:(2,4),7:(3,5)}[scene]
  coords=lambda j:(105+(j%3)*190,183+(j//3)*70)
  a,b=coords(u),coords(v);f=max(0,min(1,elapsed/1.8));x=a[0]+(b[0]-a[0])*f;y=a[1]+(b[1]-a[1])*f
  d.ellipse((x-7,y-7,x+7,y+7),fill=ORANGE)
 elif m['topic']=='dynamic_programming' and scene in [8,9,10,11] and elapsed<1.8:
  amount={8:2,9:3,10:5,11:6}[scene];x=45+amount*88;alpha=max(1,int(5*(1-elapsed/1.8)))
  d.rounded_rectangle((x,178,x+80,243),8,outline=ORANGE,width=alpha)
 elif m['kind']=='fenwick' and scene==6 and elapsed<3:
  i=[5,6,8][min(2,int(elapsed))];cell=710/8;l=i-(i&-i);y=188+(i-1)*21
  d.rounded_rectangle((35+l*cell,y,35+i*cell-3,y+20),4,outline=ORANGE,width=3)

def stamp(sec):
 ms=round(sec*1000);h,ms=divmod(ms,3600000);m,ms=divmod(ms,60000);s,ms=divmod(ms,1000)
 return f'{h:02}:{m:02}:{s:02},{ms:03}'
def render(part):
 dest=OUT/f'part{part}';timing=json.loads((dest/'timing.json').read_text());cues=timing['cues'];duration=timing['duration']/TEMPO
 manifest=json.loads((ROOT/'course_manifest.json').read_text());expected=manifest['parts'][part-1]['scripts'];assert set(expected)==set(c['source'] for c in cues),'Missing extended chapters'
 # Save reusable chapter and subtitle references, scaled with audio/video together.
 (dest/'captions.srt').write_text('\n\n'.join(f"{i+1}\n{stamp(c['start']/TEMPO)} --> {stamp(c['speech_end']/TEMPO)}\n{c['text']}" for i,c in enumerate(cues)))
 chapters=[]
 for c in cues:
  if not chapters or chapters[-1]['source']!=c['source']:chapters.append(dict(source=c['source'],start=c['start']/TEMPO,title=topic(c['source']).replace('_',' ')))
 (dest/'chapters.json').write_text(json.dumps(chapters,indent=2));(dest/'chapters.txt').write_text('\n'.join(f"{stamp(x['start']).split(',')[0]} {x['title']}" for x in chapters))
 # Generate each paragraph panel once; animate the transition/progress independently.
 panels=[];blank=[];models=[model(c) for c in cues]
 for c in cues:panels.append(base(c,part,timing['title']));blank.append(base(c,part,timing['title'],False))
 mp4=dest/f'Rohail-USACO-V2-Part-{part}.mp4';temp=mp4.with_suffix('.partial.mp4')
 p=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s','1280x720','-r',str(FPS),'-i','-','-i',str(dest/'narration.wav'),'-af',f'atempo={TEMPO},loudnorm=I=-16:TP=-1.5:LRA=11','-c:v','libx264','-preset','veryfast','-crf','26','-threads','2','-pix_fmt','yuv420p','-c:a','aac','-b:a','96k','-shortest','-movflags','+faststart',str(temp)],stdin=subprocess.PIPE)
 idx=0
 try:
  for n in range(math.ceil(duration*FPS)):
   delivered=n/FPS;source=delivered*TEMPO
   while idx+1<len(cues) and source>=cues[idx]['end']:idx+=1
   c=cues[idx];im=(panels[idx] if source<c['speech_end'] else blank[idx]).copy();d=ImageDraw.Draw(im)
   # Pulse marks the newly introduced paragraph/model; no fabricated execution clock.
   phase=min(1,(source-c['start'])/.8)
   if phase<1:d.rounded_rectangle((20,95,760,374),12,outline=ORANGE,width=1+int(3*(1-phase)))
   motion(d,models[idx],c['scene'],(source-c['start'])/TEMPO)
   d.rectangle((0,716,int(W*delivered/duration),720),fill=ORANGE)
   p.stdin.write(im.tobytes())
   if n%(FPS*60)==0:(dest/'render-progress.json').write_text(json.dumps(dict(rendered_seconds=delivered,target_seconds=duration,chapter=c['source'])))
 finally:p.stdin.close()
 assert p.wait()==0;temp.replace(mp4)
 # Embed navigation chapters and an optional selectable English subtitle track.
 metadata=[';FFMETADATA1','title=Rohail USACO V2 Part '+str(part)]
 for j,ch in enumerate(chapters):
  end=chapters[j+1]['start'] if j+1<len(chapters) else duration
  metadata.extend(['[CHAPTER]','TIMEBASE=1/1000','START='+str(round(ch['start']*1000)),'END='+str(round(end*1000)),'title='+ch['title']])
 meta=dest/'chapters.ffmetadata';meta.write_text('\n'.join(metadata)+'\n');muxed=mp4.with_suffix('.chapters.mp4')
 subprocess.run(['ffmpeg','-v','error','-y','-i',str(mp4),'-i',str(meta),'-i',str(dest/'captions.srt'),'-map','0:v','-map','0:a','-map','2:0','-map_metadata','1','-map_chapters','1','-c','copy','-c:s','mov_text','-metadata:s:s:0','language=eng','-disposition:s:0','0','-movflags','+faststart',str(muxed)],check=True)
 muxed.replace(mp4)
 subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(mp4),'-f','null','-'],check=True)
 probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-show_chapters','-of','json',str(mp4)]));ds=[float(s['duration']) for s in probe['streams'] if s['codec_type'] in ['video','audio']];assert max(ds)-min(ds)<.2
 report=dict(part=part,duration=float(probe['format']['duration']),source_audio_duration=timing['duration'],tempo=TEMPO,words=timing['words'],delivered_wpm=timing['words']*60/float(probe['format']['duration']),bytes=mp4.stat().st_size,sha256=hashlib.sha256(mp4.read_bytes()).hexdigest(),full_decode='passed',av_end_difference=max(ds)-min(ds),chapters=len(chapters),caption_paragraphs=len(cues),human_listening='Not performed by agent',state_timing='Authored paragraph-level trace panels, not word-synchronized execution')
 assert len(probe.get('chapters',[]))==len(chapters)
 report['embedded_english_subtitles']=any(s['codec_type']=='subtitle' for s in probe['streams'])
 (dest/'verification.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2),flush=True)
if __name__=='__main__':render(int(sys.argv[1]))
