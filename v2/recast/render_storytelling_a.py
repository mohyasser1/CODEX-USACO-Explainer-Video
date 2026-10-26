"""Short story audition with semantic scene cards, not full-course approval."""
import json,math,subprocess,hashlib
from pathlib import Path
from functools import lru_cache
from PIL import Image,ImageDraw,ImageFont
OUT=Path('/workspace/usaco-film-v2/output/recast')
data=json.loads((OUT/'voice-A-storytelling.json').read_text())
@lru_cache(maxsize=20)
def font(size,bold=False):return ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans'+('-Bold' if bold else '')+'.ttf',size)
def wrap(text,f,width):
    lines=[];line=''
    for word in text.split():
        s=(line+' '+word).strip()
        if f.getlength(s)>width and line:lines.append(line);line=word
        else:line=s
    if line:lines.append(line)
    return lines
cards=[]
for c in data['cues']:
    words=c['text'].split();n=math.ceil(len(words)/14)
    for j in range(n):
        a=len(words)*j//n;b=len(words)*(j+1)//n
        cards.append(dict(start=c['start']+(c['end']-c['start'])*a/len(words),end=c['start']+(c['end']-c['start'])*b/len(words),text=' '.join(words[a:b])))
titles=['FRIDAY AFTERNOON','SOMETHING DOESN’T ADD UP','LET’S READ THE WHOLE LEDGER','THE REFUNDS EXPLAIN IT','A BETTER PLAN']
def frame(t):
    idx=max(i for i,c in enumerate(data['cues']) if c['start']<=t)
    c=data['cues'][idx];im=Image.new('RGB',(1280,720),'#fbf5e9');d=ImageDraw.Draw(im)
    d.rectangle((0,0,1280,10),fill='#ef794b')
    d.text((40,30),'ROHAIL / SCHOOL MUSIC NIGHT',font=font(22,True),fill='#567365')
    d.text((40,75),titles[idx],font=font(35,True),fill='#17354b')
    d.text((40,125),'Voice A · new storytelling audition · fictional student',font=font(19),fill='#526572')
    d.rounded_rectangle((40,180,360,550),18,fill='#e6eee5')
    d.text((65,212),'THE TICKET DESK',font=font(21,True),fill='#17354b')
    for j,name in enumerate(['Rohail','Maya']):
        y=280+j*95
        d.ellipse((70,y,125,y+55),fill='#dca783' if j==0 else '#b9896f')
        d.text((87,y+10),name[0],font=font(25,True),fill='white')
        d.text((145,y+12),name,font=font(25),fill='#17354b')
    d.text((65,490),'One program. One puzzle.',font=font(19),fill='#526572')
    shift=int(20*max(0,1-(t-c['start'])/.35))
    x=405+shift;d.rounded_rectangle((x,180,1235,550),18,fill='white',outline='#e5d8c4',width=2)
    if idx==0:
        for j,line in enumerate(['A school music night is coming.', 'Rohail wants to help check the ticket money.', 'A small program seems like a good start.']):
            d.text((x+35,240+j*80),line,font=font(27),fill='#17354b')
    elif idx==1:
        d.text((x+45,230),'PROGRAM',font=font(24),fill='#526572');d.text((x+470,230),'CASH BOX',font=font(24),fill='#526572')
        d.text((x+85,290),'$8',font=font(75,True),fill='#bf6948');d.text((x+505,290),'$5',font=font(75,True),fill='#567365')
        d.text((x+65,450),'Why are the two totals different?',font=font(31),fill='#17354b')
    else:
        for j,(number,label) in enumerate([('+3','payment'),('-2','refund'),('+5','payment'),('-1','refund')]):
            xx=x+35+j*190
            d.rounded_rectangle((xx,235,xx+160,355),10,fill='#e6eee5' if number[0]=='+' else '#f5e0d5')
            d.text((xx+44,250),number,font=font(42,True),fill='#17354b');d.text((xx+25,315),label,font=font(22),fill='#526572')
        message='What should remain?' if idx==2 else 'Balance: 0 → 3 → 1 → 6 → 5' if idx==3 else 'Include every payment AND every refund.'
        d.text((x+40,405),message,font=font(30,True),fill='#17354b')
        if idx==4:d.text((x+40,470),'Next: build the loop and justify every step.',font=font(24),fill='#567365')
    subtitle=next((z['text'] for z in cards if z['start']<=t<z['end']),None)
    if subtitle:
        for j,line in enumerate(wrap(subtitle,font(26),1170)):
            d.text((45,590+j*34),line,font=font(26),fill='#17354b')
    elif idx==2:d.text((45,600),'Take a moment to predict the balance.',font=font(26),fill='#567365')
    d.text((45,675),'Selected supplied “Too Much” excerpt · original narration · no artist recording',font=font(17),fill='#526572')
    return im
for i,c in enumerate(data['cues']):frame((c['start']+c['end'])/2).save(OUT/f'storytelling-frame-{i}.png')
mp4=OUT/'Rohail-Voice-A-Storytelling-Audition.mp4';temp=mp4.with_suffix('.partial.mp4')
p=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s','1280x720','-r','15','-i','-','-i',str(OUT/'voice-A-storytelling.wav'),'-c:v','libx264','-preset','veryfast','-crf','24','-threads','2','-pix_fmt','yuv420p','-c:a','aac','-b:a','128k','-af','loudnorm=I=-16:TP=-1.5:LRA=11','-shortest','-movflags','+faststart',str(temp)],stdin=subprocess.PIPE)
try:
    for n in range(math.ceil(data['duration_seconds']*15)):p.stdin.write(frame(n/15).tobytes())
finally:p.stdin.close()
assert p.wait()==0;temp.replace(mp4)
subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(mp4),'-f','null','-'],check=True)
info=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(mp4)]))
durations=[float(s['duration']) for s in info['streams'] if s['codec_type'] in ('audio','video')]
assert max(durations)-min(durations)<.15
data.update(file=mp4.name,bytes=mp4.stat().st_size,sha256=hashlib.sha256(mp4.read_bytes()).hexdigest(),
    complete_decode='passed',av_end_difference_seconds=max(durations)-min(durations),
    subtitle_timing='word-fraction approximation within each synthesized paragraph',human_listening='pending')
(OUT/'storytelling-verification.json').write_text(json.dumps(data,indent=2));print(json.dumps({k:v for k,v in data.items() if k!='cues'},indent=2))
