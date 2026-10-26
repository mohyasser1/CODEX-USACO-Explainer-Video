"""Simple story cards for listening evaluation; not a final animation template."""
import json,subprocess,hashlib
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
OUT=Path('/workspace/usaco-film-v2/output/recast')
data=json.loads((OUT/'audition.json').read_text())
def font(size,bold=False):
    return ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans'+('-Bold' if bold else '')+'.ttf',size)
def wrap(text,width,f):
    lines=[];line=''
    for word in text.split():
        candidate=(line+' '+word).strip()
        if f.getlength(candidate)>width and line:lines.append(line);line=word
        else:line=candidate
    if line:lines.append(line)
    return lines
for voice in data['voices']:
    label=voice['label'];im=Image.new('RGB',(1280,720),'#fbf5e9');d=ImageDraw.Draw(im)
    d.rectangle((0,0,1280,12),fill='#ef794b')
    d.text((50,38),f'VOICE {label}  /  SCHOOL MUSIC NIGHT',font=font(33,True),fill='#17354b')
    d.text((50,91),'Rohail is a fictional tenth grader. This is a voice-and-story audition.',font=font(23),fill='#425a69')
    d.rounded_rectangle((35,140,1245,510),18,fill='white',outline='#e5d8c4',width=2)
    lines=wrap(data['text'],1140,font(25));assert len(lines)<=10,len(lines)
    for j,line in enumerate(lines):d.text((65,164+j*32),line,font=font(25),fill='#17354b')
    for j,(value,kind) in enumerate([('+3','payment'),('-2','refund'),('+5','payment'),('-1','refund')]):
        x=50+j*245;d.rounded_rectangle((x,540,x+215,640),12,fill='#e8eee7' if value[0]=='+' else '#f5e0d5')
        d.text((x+22,551),value,font=font(35,True),fill='#17354b');d.text((x+22,599),kind,font=font(19),fill='#425a69')
    d.text((1060,557),'NET',font=font(19),fill='#425a69');d.text((1080,587),'5',font=font(36,True),fill='#17354b')
    d.text((50,672),'Music-free listening sample · includes supplied excerpt labeled “Too Much”',font=font(18),fill='#425a69')
    png=OUT/f'voice-{label}-card.png';im.save(png)
    mp4=OUT/f'Voice-{label}-Rohail-story-audition.mp4'
    subprocess.run(['ffmpeg','-v','error','-y','-loop','1','-framerate','10','-i',str(png),'-i',str(OUT/f'voice-{label}.wav'),'-t',str(voice['duration']),'-c:v','libx264','-preset','veryfast','-crf','23','-pix_fmt','yuv420p','-c:a','aac','-b:a','128k','-af','loudnorm=I=-16:TP=-1.5:LRA=11','-movflags','+faststart',str(mp4)],check=True)
    subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(mp4),'-f','null','-'],check=True)
    voice.update(file=mp4.name,bytes=mp4.stat().st_size,sha256=hashlib.sha256(mp4.read_bytes()).hexdigest(),complete_decode='passed')
(OUT/'audition-verification.json').write_text(json.dumps(data,indent=2))
print(json.dumps(data['voices'],indent=2))
