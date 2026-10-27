"""Paragraph-timed captions; authored semantic states, no cycling highlights."""
import json,math,subprocess,hashlib
from pathlib import Path
from functools import lru_cache
from PIL import Image,ImageDraw,ImageFont
from lesson import CODE
OUT=Path('/workspace/usaco-film-v2/output/integrated');W,H,FPS=1280,720,12
@lru_cache(None)
def font(n,bold=False,mono=False):
 return ImageFont.truetype('/usr/share/fonts/truetype/dejavu/'+('DejaVuSansMono' if mono else 'DejaVuSans')+('-Bold' if bold else '')+'.ttf',n)
def wrap(t,f,width):
 result=[]
 for para in t.split('\n'):
  line=''
  for word in para.split():
   candidate=(line+' '+word).strip()
   if f.getlength(candidate)>width and line:result.append(line);line=word
   else:line=candidate
  if line:result.append(line)
 return result
BG='#fbf5e9';INK='#17354b';GREEN='#426954';ORANGE='#b64c2a'
def base(s,caption=True):
 im=Image.new('RGB',(W,H),BG);d=ImageDraw.Draw(im)
 d.rectangle((0,0,W,8),fill=ORANGE)
 d.text((30,23),'ROHAIL / SCHOOL MUSIC NIGHT',font=font(18,True),fill=GREEN)
 d.text((30,60),s['title'],font=font(29,True),fill=INK)
 for x,name,color in [(1030,'Rohail','#bd8867'),(1150,'Maya','#a96c51')]:
  d.ellipse((x,23,x+30,53),fill=color);d.rounded_rectangle((x-8,55,x+38,77),6,fill=GREEN)
  d.text((x-11,81),name,font=font(16),fill=INK)
 d.rounded_rectangle((25,116,715,445),14,fill='white',outline='#d8d4c5',width=2)
 for j,line in enumerate(CODE):
  y=131+j*37;active=j==s['highlight'] or s['mode']=='input' and j in [0,1,2]
  if active:d.rounded_rectangle((35,y-3,705,y+31),6,fill='#d8ebda')
  d.text((44,y),line,font=font(22,mono=True),fill=GREEN if active else INK)
 d.rounded_rectangle((735,116,1255,445),14,fill='#e7eee4')
 mode=s['mode'];vals=s['values']
 d.text((755,135),'NEW INPUT' if mode in ['question','answer'] or not vals else 'TRANSACTION LEDGER',font=font(18,True),fill=GREEN)
 if vals:
  for j,v in enumerate(vals):
   x=755+j*120;active=s['i']==j
   d.rounded_rectangle((x,174,x+104,245),8,fill='#f5d6c5' if v<0 else 'white',outline=ORANGE if active else '#bdcabb',width=4 if active else 1)
   d.text((x+24,188),str(v),font=font(30,True),fill=INK)
   d.text((x+31,252),f'[{j}]',font=font(17,mono=True),fill=INK)
 else:d.text((760,192),'a = [ ]   n = 0',font=font(28,mono=True),fill=INK)
 if mode=='question':
  d.text((760,299),'i = ?     total = ?',font=font(25,mono=True),fill=INK)
 elif mode=='answer':
  for j,l in enumerate(['i:      0   1   2   3   4','total:  0  -4  -4   3   0']):d.text((755,305+j*39),l,font=font(20,mono=True),fill=INK)
 elif s['i'] is not None:
  d.text((760,300),'i = '+str(s['i']),font=font(28,mono=True),fill=INK)
  d.text((760,350),'total = '+str(s['total']),font=font(25,mono=True),fill=GREEN)
 else:
  msg='Wrong report $8 / actual $5' if s['key']=='story' else 'Payments AND refunds count'
  for j,l in enumerate(wrap(msg,font(26,True),460)):d.text((760,305+j*35),l,font=font(26,True),fill=INK)
 lines=wrap(s['note'],font(23,True),1200)
 assert len(lines)<=2,(s['key'],'note overflow')
 for j,l in enumerate(lines):d.text((30,459+j*29),l,font=font(23,True),fill=GREEN)
 d.rectangle((0,529,W,683),fill='white')
 if caption:
  lines=wrap(s['text'],font(22),1210);assert len(lines)<=5,(s['key'],'caption overflow',len(lines))
  for j,l in enumerate(lines):d.text((34,540+j*27),l,font=font(22),fill=INK)
 else:d.text((34,565),'Pause the video to work; resume for the answer.' if mode=='question' else 'Follow the highlighted statement and its state.',font=font(24),fill=GREEN)
 footer='Supplied “Too Much” hook · educational reinterpretation · original synthetic narrator' if s['key']=='input' else 'Integrated teaching review · fictional students · code excerpt uses valid input'
 d.text((30,692),footer,font=font(14),fill=INK)
 return im

def stamp(sec):
 ms=round(sec*1000);h,ms=divmod(ms,3600000);m,ms=divmod(ms,60000);s,ms=divmod(ms,1000)
 return f'{h:02}:{m:02}:{s:02},{ms:03}'
def main():
 data=json.loads((OUT/'timing.json').read_text());cues=data['cues'];frames=[]
 for s in cues:
  frames.append((base(s),base(s,False)));base(s).save(OUT/(s['key']+'.png'))
 (OUT/'lesson.srt').write_text('\n\n'.join(f"{i+1}\n{stamp(s['start'])} --> {stamp(s['speech_end'])}\n{s['text']}" for i,s in enumerate(cues)))
 mp4=OUT/'Rohail-Integrated-Teaching-Review.mp4';temp=mp4.with_suffix('.partial.mp4')
 p=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s','1280x720','-r',str(FPS),'-i','-','-i',str(OUT/'lesson.wav'),'-c:v','libx264','-preset','veryfast','-crf','23','-threads','2','-pix_fmt','yuv420p','-c:a','aac','-b:a','128k','-af','loudnorm=I=-16:TP=-1.5:LRA=11','-shortest','-movflags','+faststart',str(temp)],stdin=subprocess.PIPE)
 idx=0
 try:
  for n in range(math.ceil(data['duration']*FPS)):
   t=n/FPS
   while idx+1<len(cues) and t>=cues[idx]['end']:idx+=1
   s=cues[idx];im=frames[idx][int(t>=s['speech_end'])].copy();d=ImageDraw.Draw(im)
   # Moving receipt pointer exists only at the selected current array index.
   if isinstance(s['i'],int) and 0<=s['i']<len(s['values']):
    x=807+s['i']*120;y=166+int(3*math.sin((t-s['start'])*3))
    d.polygon([(x-7,y-8),(x+7,y-8),(x,y)],fill=ORANGE)
   if s['key'].startswith('add'):
    # Animate the selected receipt into the executed addition's balance box.
    u=min(1,max(0,(t-s['start'])/1.8))
    if u<1:
     x=int((807+s['i']*120)*(1-u)+1080*u)
     y=int(210*(1-u)+365*u-55*math.sin(math.pi*u))
     d.rounded_rectangle((x-28,y-19,x+28,y+19),7,fill=ORANGE)
     d.text((x-17,y-15),str(s['values'][s['i']]),font=font(22,True),fill='white')
   d.rectangle((0,716,int(W*t/data['duration']),720),fill=ORANGE)
   p.stdin.write(im.tobytes())
 finally:p.stdin.close()
 assert p.wait()==0;temp.replace(mp4)
 subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(mp4),'-f','null','-'],check=True)
 probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(mp4)]))
 ds=[float(x['duration']) for x in probe['streams'] if x['codec_type'] in ['audio','video']];assert max(ds)-min(ds)<.15
 report=dict(bytes=mp4.stat().st_size,sha256=hashlib.sha256(mp4.read_bytes()).hexdigest(),duration=float(probe['format']['duration']),overall_wpm=data['overall_wpm'],words=data['words'],full_decode='passed',av_end_difference=max(ds)-min(ds),captions='Exact paragraph audio bounds, quantized to 12fps for burned-in display; no word-level alignment claim',state_mapping='One authored semantic state per narration paragraph; checked independently by verify.py',human_listening='Not performed by agent; user approved prior slower voice sample; integrated independent QA pending')
 (OUT/'verification.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
if __name__=='__main__':main()
