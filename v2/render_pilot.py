"""V2 instructional pilot: state changes follow the relevant spoken sentence."""
import json, math, subprocess, textwrap, os
from functools import lru_cache
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import soundfile as sf
from pilot import CODE, VALUES
OUT=Path('/workspace/usaco-film-v2/output')
data=json.loads((OUT/'v2-pilot-timing.json').read_text())
# Original procedural percussion. No sampled recordings or artist reference.
speech,sr=sf.read(OUT/'v2-pilot.wav',dtype='float32')
music=np.zeros_like(speech);rng=np.random.default_rng(441)
for beat in np.arange(0,len(speech)/sr,60/88):
    start=int(beat*sr); length=min(int(.16*sr),len(speech)-start)
    x=np.arange(length)/sr
    kick=np.sin(2*np.pi*(65*x-70*x*x))*np.exp(-30*x)*.014
    music[start:start+length]+=kick
    hatstart=start+int(30/88*sr);hatlen=min(int(.045*sr),len(speech)-hatstart)
    if hatlen>0:music[hatstart:hatstart+hatlen]+=rng.normal(0,.003,hatlen)*np.exp(-np.arange(hatlen)/sr*95)
sf.write(OUT/'v2-pilot-mix.wav',np.clip(speech+music,-1,1),sr)
W,H,FPS=1280,720,15
BG='#0b1020'; FG='#edf3ff'; MINT='#62f2bc'; PINK='#ff77b7'; YELLOW='#ffdb72'
@lru_cache(maxsize=24)
def font(size,mono=False,bold=False):
    name='DejaVuSansMono' if mono else 'DejaVuSans'
    return ImageFont.truetype('/usr/share/fonts/truetype/dejavu/'+name+('-Bold' if bold else '')+'.ttf',size)
def wrap(txt, f, width):
    lines=[]; line=''
    for word in txt.split():
        test=(line+' '+word).strip()
        if f.getlength(test)>width and line:lines.append(line);line=word
        else:line=test
    if line:lines.append(line)
    return lines
def scene_at(t):
    return next((s for s in data['scenes'] if s['start']<=t<s['end']),data['scenes'][-1])
cards=[]
for cue in data['cues']:
    words=cue['text'].split(); count=max(1,math.ceil(len(words)/15))
    for j in range(count):
        a=len(words)*j//count;b=len(words)*(j+1)//count
        cards.append(dict(start=cue['start']+(cue['end']-cue['start'])*a/len(words),
                          end=cue['start']+(cue['end']-cue['start'])*b/len(words),text=' '.join(words[a:b])))
def change_time(s):
    # Keep old state until the explicit result sentence has been spoken.
    candidates=[c for c in data['cues'] if c['start']>=s['start'] and c['end']<=s['end']]
    markers={3:'Old total',4:'Three plus',5:'At index',6:'Six plus'}
    idx=data['scenes'].index(s)
    return next((c['end'] for c in candidates if c['text'].startswith(markers.get(idx,'!!!'))),s['end'])
def increment_time(s):
    idx=data['scenes'].index(s)
    markers={3:'Then the increment',4:'Store one',5:'Then advance',6:'Increment i'}
    return next((c['end'] for c in data['cues'] if s['start']<=c['start']<s['end'] and c['text'].startswith(markers.get(idx,'!!!'))),s['end'])
def frame(t):
    s=scene_at(t); im=Image.new('RGB',(W,H),BG);d=ImageDraw.Draw(im)
    d.text((35,22),'BESSIE’S ALGORITHM TOUR  /  V2 TEACHING PILOT',font=font(20, bold=True),fill=MINT)
    d.text((35,60),s['title'],font=font(35,bold=True),fill=FG)
    # Small original cow host, deliberately outside code and caption areas.
    bob=int(3*math.sin(t*2*math.pi*88/60));cx=1187;cy=63+bob
    d.ellipse((cx-38,cy-30,cx+38,cy+30),fill='#edf3ff')
    d.polygon([(cx-32,cy-19),(cx-46,cy-42),(cx-15,cy-27)],fill=YELLOW)
    d.polygon([(cx+32,cy-19),(cx+46,cy-42),(cx+15,cy-27)],fill=YELLOW)
    d.ellipse((cx-25,cy-5,cx-15,cy+5),fill=BG);d.ellipse((cx+15,cy-5,cx+25,cy+5),fill=BG)
    d.ellipse((cx-25,cy+8,cx+25,cy+29),fill=PINK)
    d.rounded_rectangle((30,120,735,420),18,fill='#182239')
    changed='next_total' in s and t>=change_time(s)
    incremented='next_total' in s and t>=increment_time(s)
    active=s['i']+int(incremented)
    highlight=2 if incremented else s['line']
    transfer=False; transfer_answer=False
    if s is data['scenes'][-1]:
        transfer_start=next(c['start'] for c in data['cues'] if c['text'].startswith('Your transfer task'))
        answer_start=next(c['end'] for c in data['cues'] if c['text'].startswith('The totals are'))
        transfer=t>=transfer_start;transfer_answer=t>=answer_start
        if transfer:highlight=-1
    for j,line in enumerate(CODE):
        if j==highlight:d.rounded_rectangle((42,136+j*42,725,176+j*42),8,fill='#294c48')
        d.text((50,143+j*42),line,font=font(23,mono=True),fill=MINT if j==highlight else FG)
    d.text((770,126),'TRANSFER INPUT' if transfer else 'TRANSACTIONS a',font=font(23,bold=True),fill=FG)
    value=s.get('next_total') if changed else s['total']
    if transfer:active=4 if transfer_answer else -1;value=0 if transfer_answer else '?'
    for j,v in enumerate([-4,0,7,-3] if transfer else VALUES):
        x=775+j*110
        d.rounded_rectangle((x,176,x+94,251),10,fill='#294c48' if j==active else '#182239',outline=MINT if j==active else '#51617d',width=3)
        d.text((x+25,193),str(v),font=font(30,mono=True),fill=FG)
        d.text((x+31,261),str(j),font=font(20),fill='#9dacbf')
    d.text((775,311),f'i = {active if active>=0 else "?"}',font=font(29,mono=True),fill=YELLOW)
    d.text((775,359),f'total = {value}',font=font(29,mono=True),fill=MINT)
    phase='BODY UPDATED; increment next' if changed and not incremented else 'At condition check'
    if transfer:phase='Final condition check' if transfer_answer else 'Pause and trace this input'
    d.text((775,402),phase,font=font(19),fill=PINK)
    d.text((45,449),'CONTRACT: add ALL signed values, including refunds.',font=font(24,bold=True),fill=FG)
    d.text((45,495),'INVARIANT at each condition check:',font=font(23,bold=True),fill=YELLOW)
    d.text((45,532),'total = sum of the first i elements',font=font(27,mono=True),fill=MINT)
    cue=next((c for c in cards if c['start']<=t<c['end']),None)
    d.rectangle((0,590,W,682),fill='#050914')
    if cue:
        for j,line in enumerate(wrap(cue['text'],font(26),1190)):
            d.text((45,600+j*33),line,font=font(26),fill=FG)
    d.rectangle((0,699,int(W*t/data['duration']),709),fill=MINT)
    return im
def stamp(t):
    ms=round(t*1000);h,ms=divmod(ms,3600000);m,ms=divmod(ms,60000);s,ms=divmod(ms,1000)
    return f'{h:02}:{m:02}:{s:02},{ms:03}'
(OUT/'v2-pilot.srt').write_text('\n\n'.join(f"{i+1}\n{stamp(c['start'])} --> {stamp(c['end'])}\n{c['text']}" for i,c in enumerate(cards)))
for j,s in enumerate(data['scenes']):frame((s['start']+s['end'])/2).save(OUT/f'pilot-frame-{j:02}.png')
target=OUT/'V2-pilot-execution-and-proof.mp4'
temp=OUT/f'V2-pilot-{os.getpid()}.partial.mp4'
cmd=['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-i',str(OUT/'v2-pilot-mix.wav'),'-c:v','libx264','-preset','veryfast','-crf','24','-threads','2','-pix_fmt','yuv420p','-c:a','aac','-b:a','96k','-af','loudnorm=I=-16:TP=-1.5:LRA=11','-shortest','-movflags','+faststart',str(temp)]
p=subprocess.Popen(cmd,stdin=subprocess.PIPE)
try:
    for n in range(math.ceil(data['duration']*FPS)):
        p.stdin.write(frame(n/FPS).tobytes())
        if n%(FPS*30)==0:print(f'{n/FPS:.0f}/{data["duration"]:.0f}s rendered',flush=True)
finally:p.stdin.close()
if p.wait()!=0:raise RuntimeError('FFmpeg failed; temporary preserved')
temp.replace(target)
print(str(target),flush=True)
