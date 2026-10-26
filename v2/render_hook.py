"""Representative supplied-excerpt integration, with explicit Boolean state."""
import json,math,os,subprocess
from pathlib import Path
if os.environ.get('ALLOW_SUPERSEDED_REVIEW_RENDER') != '1':
    raise SystemExit('Superseded presentation: use v2/recast; no current-style full renders.')
from functools import lru_cache
from PIL import Image,ImageDraw,ImageFont
import numpy as np
import soundfile as sf
OUT=Path('/workspace/usaco-film-v2/output')
data=json.loads((OUT/'v2-hook-timing.json').read_text())
speech,sr=sf.read(OUT/'v2-hook.wav',dtype='float32');music=np.zeros_like(speech)
for beat in np.arange(0,len(speech)/sr,60/88):
    start=int(beat*sr);length=min(int(sr*.15),len(speech)-start);t=np.arange(length)/sr
    music[start:start+length]+=.012*np.sin(2*np.pi*(65*t-70*t*t))*np.exp(-30*t)
sf.write(OUT/'v2-hook-mix.wav',np.clip(speech+music,-1,1),sr)
@lru_cache(maxsize=20)
def font(size,mono=False):
    return ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans'+('Mono' if mono else '')+'.ttf',size)
def onset(scene,prefix,end=False):
    return next(c['end' if end else 'start'] for c in data['cues'] if c['scene']==scene and c['text'].startswith(prefix))
cards=[]
for c in data['cues']:
    words=c['text'].split();n=max(1,math.ceil(len(words)/14))
    for j in range(n):
        a=len(words)*j//n;b=len(words)*(j+1)//n
        cards.append(dict(start=c['start']+(c['end']-c['start'])*a/len(words),end=c['start']+(c['end']-c['start'])*b/len(words),text=' '.join(words[a:b])))
def state(t):
    idx=next((i for i,s in enumerate(data['scenes']) if s['start']<=t<s['end']),3)
    lamp=False;step=0;highlight=0
    if idx==1:
        step=int(t>=onset(1,'Store true',True))+int(t>=onset(1,'Store false',True))
        lamp=step==1;highlight=1 if t<onset(1,'Now execute') else 2
    elif idx==2:
        step=int(t>=onset(2,'Execute it once',True))+int(t>=onset(2,'Execute it twice',True))
        lamp=step>0;highlight=1 if t<onset(2,'Execute it twice') else 2
    elif idx==3:
        step=3 if t>=onset(3,'The states after',True) else 0
        lamp=step==3;highlight=-1
    return idx,lamp,step,highlight
def frame(t):
    idx,lamp,step,h=state(t);s=data['scenes'][idx]
    im=Image.new('RGB',(1280,720),'#0b1020');d=ImageDraw.Draw(im)
    d.text((35,22),'V2 HOOK -> EXPLANATION -> TRACE',font=font(23),fill='#62f2bc')
    d.text((35,63),s['title'],font=font(34),fill='white')
    d.text((35,112),'Supplied excerpt labeled “Nonstop” · classroom reinterpretation',font=font(18),fill='#aebed6')
    d.rounded_rectangle((35,158,720,440),18,fill='#182239')
    code=['bool lamp = false;','lamp = !lamp;','lamp = !lamp;']
    if idx==2:code=['bool lamp = false;','lamp = true;','lamp = true;']
    if idx==3:code=['bool lamp = false;','// toggle three times','lamp = !lamp;  // each time']
    for j,line in enumerate(code):
        if j==h:d.rounded_rectangle((48,179+j*66,705,229+j*66),8,fill='#294c48')
        d.text((62,186+j*66),line,font=font(30,True),fill='#62f2bc' if j==h else 'white')
    d.text((60,389),'!false = true       !true = false',font=font(24,True),fill='#ffdb72')
    cx,cy=980,270
    if lamp:
        for r in range(115,80,-5):d.ellipse((cx-r,cy-r,cx+r,cy+r),outline='#59512b',width=3)
    d.ellipse((cx-78,cy-78,cx+78,cy+78),fill='#ffdb72' if lamp else '#344157',outline='white',width=3)
    d.rounded_rectangle((cx-35,cy+65,cx+35,cy+118),8,fill='#8fa2bc')
    d.text((860,420),'lamp = '+('true' if lamp else 'false'),font=font(30,True),fill='#62f2bc')
    if idx==3 and step==0:lesson='Use player pause: predict three toggles from false.'
    elif idx==3:lesson='Trace: false -> true -> false -> true'
    elif idx==2:lesson=f'Assignment #{step}: stores true; does not invert the old value.'
    else:lesson=f'Toggles completed: {step}. Read old value -> NOT -> store result.'
    d.text((35,492),lesson,font=font(25),fill='#ff77b7')
    d.text((35,540),'Original synthetic narrator and original percussion · no artist imitation',font=font(18),fill='#aebed6')
    d.rectangle((0,590,1280,686),fill='#050914')
    cue=next((c for c in cards if c['start']<=t<c['end']),None)
    if cue:
        lines=[];line=''
        for word in cue['text'].split():
            trial=(line+' '+word).strip()
            if font(26).getlength(trial)>1190 and line:lines.append(line);line=word
            else:line=trial
        if line:lines.append(line)
        assert len(lines)<=2
        for j,line in enumerate(lines):d.text((40,602+j*34),line,font=font(26),fill='white')
    d.rectangle((0,702,int(1280*t/data['duration']),710),fill='#62f2bc')
    return im
for i,s in enumerate(data['scenes']):frame((s['start']+s['end'])/2).save(OUT/f'hook-frame-{i}.png')
checks=[]
for i,prefix,expected in [(1,'Store true',True),(1,'Store false',False),(2,'Execute it twice',True),(3,'The states after',True)]:
    t=onset(i,prefix,True)+.05;assert state(t)[1]==expected
    checks.append(dict(time=t,lamp=expected));frame(t).save(OUT/f'hook-evidence-{len(checks)}.png')
(OUT/'hook-state-tests.json').write_text(json.dumps(dict(passed=True,probes=checks),indent=2))
target=OUT/'V2-hook-Boolean-switch.mp4';temp=OUT/f'hook-{os.getpid()}.partial.mp4'
p=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s','1280x720','-r','15','-i','-','-i',str(OUT/'v2-hook-mix.wav'),'-c:v','libx264','-preset','veryfast','-crf','24','-threads','2','-pix_fmt','yuv420p','-c:a','aac','-b:a','96k','-af','loudnorm=I=-16:TP=-1.5:LRA=11','-shortest','-movflags','+faststart',str(temp)],stdin=subprocess.PIPE)
try:
    for n in range(math.ceil(data['duration']*15)):p.stdin.write(frame(n/15).tobytes())
finally:p.stdin.close()
assert p.wait()==0;temp.replace(target);print(target)
