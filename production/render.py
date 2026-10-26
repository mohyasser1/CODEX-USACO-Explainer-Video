"""Resumable 720p motion-graphics renderer; assets remain in cloud scratch."""
import os,sys,json,math,subprocess,textwrap,re,time
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont
from curriculum import lessons
from special_visuals import draw_special
ROOT=Path('/workspace/usaco-film');OUT=ROOT/'output';(OUT/'chapters').mkdir(exist_ok=True)
W,H=1280,720; FPS=15
BG='#0b1020'; PANEL='#151e34'; WHITE='#f2f4ff'; MUTED='#aeb9d4'; MINT='#62f2bc'; PINK='#ff77b7'; YELLOW='#ffdb72'; BLUE='#75adff'
FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf';BOLD='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf';MONO='/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'
fonts={}
def f(size,bold=False,mono=False):
    key=(size,bold,mono)
    if key not in fonts:fonts[key]=ImageFont.truetype(MONO if mono else BOLD if bold else FONT,size)
    return fonts[key]
def text(d,xy,s,size=25,fill=WHITE,bold=False,mono=False):d.text(xy,s,font=f(size,bold,mono),fill=fill)
def wrap(d,s,width,size=25,bold=False,mono=False):
    result=[]
    for paragraph in s.split('\n'):
        line=''
        for word in paragraph.split():
            candidate=(line+' '+word).strip()
            if d.textlength(candidate,font=f(size,bold,mono))>width and line:result.append(line);line=word
            else:line=candidate
        result.append(line)
    return result
def wrapped(d,xy,s,width,size=25,fill=WHITE,bold=False,maxlines=20):
    for j,line in enumerate(wrap(d,s,width,size,bold)[:maxlines]):text(d,(xy[0],xy[1]+j*(size+8)),line,size,fill,bold)
def box(d,rect,fill=PANEL,outline=None,r=18):d.rounded_rectangle(rect,radius=r,fill=fill,outline=outline,width=2)
def arrow(d,a,b,color=MUTED,width=4):
    d.line([a,b],fill=color,width=width);ang=math.atan2(b[1]-a[1],b[0]-a[0]);r=11
    pts=[b,(b[0]-r*math.cos(ang-.5),b[1]-r*math.sin(ang-.5)),(b[0]-r*math.cos(ang+.5),b[1]-r*math.sin(ang+.5))];d.polygon(pts,fill=color)
def cow(d,x,y,t,scale=1):
    bob=math.sin(t*3)*4; y+=bob
    # Original cartoon DJ cow: horns, ears, shades and gold medallion.
    d.ellipse((x-74,y-24,x-22,y+18),fill=WHITE);d.ellipse((x+22,y-24,x+74,y+18),fill=WHITE)
    d.polygon([(x-43,y-42),(x-36,y-82),(x-14,y-44)],fill=YELLOW)
    d.polygon([(x+43,y-42),(x+36,y-82),(x+14,y-44)],fill=YELLOW)
    box(d,(x-54,y-52,x+54,y+61),WHITE,r=35)
    d.ellipse((x+20,y-42,x+49,y-9),fill='#243149')
    box(d,(x-43,y-16,x-4,y+8),BG,r=5);box(d,(x+4,y-16,x+43,y+8),BG,r=5);d.line((x-6,y-8,x+6,y-8),fill=BG,width=5)
    box(d,(x-37,y+14,x+37,y+51),PINK,r=18)
    d.ellipse((x-20,y+25,x-12,y+33),fill=BG);d.ellipse((x+12,y+25,x+20,y+33),fill=BG)
    d.arc((x-36,y+58,x+36,y+115),0,180,fill=YELLOW,width=6)
    d.ellipse((x-13,y+94,x+13,y+120),fill=YELLOW);text(d,(x-7,y+95),'B',18,BG,True)
def cells(d,vals,y=330,x=95,active=(),labels=True,cell=86):
    for j,v in enumerate(vals):
        col=MINT if j in active else '#243149';box(d,(x+j*cell,y,x+j*cell+cell-10,y+65),col,r=12)
        s=str(v);sz=26 if len(s)<5 else 19
        tw=d.textlength(s,font=f(sz,True));text(d,(x+j*cell+(cell-10-tw)/2,y+16),s,sz,BG if j in active else WHITE,True)
        if labels:text(d,(x+j*cell+25,y+72),str(j),17,MUTED)
def graph(d,t,weighted=False,bfs=False,dsu=False):
    pts=[(130,330),(300,255),(300,430),(485,300),(505,465),(700,365)]
    edges=[(0,1,2),(0,2,5),(1,3,3),(2,3,1),(2,4,4),(3,5,2),(4,5,1)]
    sequence=[0,1,2,3,4,5] if bfs else [0,1,3,5,4,2]; count=int(t/1.6)%7
    reached=set(sequence[:count]);
    for u,v,w in edges:
        col=MINT if u in reached and v in reached else '#3b4e70';d.line((pts[u],pts[v]),fill=col,width=5)
        if weighted:
            x=(pts[u][0]+pts[v][0])/2;y=(pts[u][1]+pts[v][1])/2
            d.ellipse((x-16,y-16,x+16,y+16),fill=BG);text(d,(x-7,y-13),str(w),20,YELLOW,True)
    for j,(x,y) in enumerate(pts):
        d.ellipse((x-28,y-28,x+28,y+28),fill=MINT if j in reached else '#283651',outline=WHITE,width=2)
        text(d,(x-9,y-17),str(j),26,BG if j in reached else WHITE,True)
    label='BFS discovery order: 0, 1, 2, 3, 4, 5' if bfs else 'Vertices = states   |   Edges = allowed moves'
    text(d,(95,520),label,23,MUTED)
def tree(d,t,fenwick=False):
    if fenwick:
        vals=[1,2,1,4,1,2,1,8];step=int(t/1.7)%4;inds=[6,4,0]
        for j,length in enumerate(vals):
            yy=245+j*31;x=110+(j+1-length)*72
            box(d,(x,yy,110+(j+1)*72-5,yy+24),MINT if j+1 in inds[:step] else '#344766',r=5)
            text(d,(740,yy-2),f'{j+1}: block {length}',17,MUTED)
        text(d,(100,520),'prefix(6): block 6 + block 4 -> 0',23,YELLOW);return
    pts=[(440,240),(260,335),(620,335),(155,440),(345,440),(535,440),(725,440)]
    labels=['[0,8)','[0,4)','[4,8)','[0,2)','[2,4)','[4,6)','[6,8)'];active=int(t/1.4)%7
    for j in range(1,7):d.line((pts[(j-1)//2],pts[j]),fill=MINT if j==active else '#405475',width=4)
    for j,(x,y) in enumerate(pts):
        box(d,(x-55,y-22,x+55,y+25),MINT if j==active else '#263754',r=12);text(d,(x-42,y-13),labels[j],20,BG if j==active else WHITE,mono=True)
    text(d,(100,520),'Combine children. Keep the summary precise.',23,MUTED)
def visual(d,kind,t,lesson,beat):
    step=int(t/1.7)
    if draw_special(d,t,lesson,(text,box,arrow,cells,wrapped)): return
    if kind in ('graph','bfs','weighted','dsu'):graph(d,t,weighted=kind=='weighted',bfs=kind=='bfs',dsu=kind=='dsu');return
    if kind in ('tree','fenwick'):tree(d,t,kind=='fenwick');return
    if kind=='code' or (lesson['code'] and beat==3):
        code=lesson['code'] or 'read_input();\nmodel_the_problem();\nprove_the_algorithm();\nimplement();\ntest_edge_cases();'
        lines=code.splitlines();size=min(25,int(285/max(1,len(lines)))-4);size=max(17,size)
        for j,line in enumerate(lines):
            if j==step%len(lines):box(d,(85,232+j*(size+7),890,232+(j+1)*(size+7)), '#243651',r=4)
            text(d,(95,232+j*(size+7)),line,size,MINT if j==step%len(lines) else WHITE,mono=True)
        return
    if kind=='prefix':
        n=min(step%7,5);cells(d,[3,1,4,1,5],270,110,(max(0,n-1),));cells(d,[0,3,4,8,9,14],405,110,(n,))
        text(d,(110,230),'a: ticket sales',23,MUTED);text(d,(110,365),'p: totals before each boundary',23,MUTED)
        text(d,(110,520),'sum [1,4) = p[4] - p[1] = 9 - 3 = 6',24,YELLOW);return
    if kind=='pointers':
        pairs=[(0,4),(0,3),(1,3)];l,r=pairs[step%3];cells(d,[1,2,4,7,11],335,160,(l,r))
        text(d,(160+l*86,290),'L',28,MINT,True);text(d,(160+r*86,290),'R',28,PINK,True)
        s=[12,8,9][step%3];text(d,(160,465),f'Sum = {s}    Target = 9    '+['too large','too small','FOUND'][step%3],27,YELLOW,True);return
    if kind=='binary':
        bounds=[(0,7,3),(0,3,1),(2,3,2),(3,3,3)];lo,hi,mid=bounds[step%4]
        cells(d,['F','F','F','T','T','T','T','T'],340,100,(mid,),cell=90)
        text(d,(100,260),'Find the first TRUE. Keep a feasible upper bound.',24,MUTED)
        text(d,(100,465),f'lo = {lo}    hi = {hi}    mid = {mid}',30,MINT,True);return
    if kind=='sort':
        states=[[7,2,9,1,5],[2,7,1,5,9],[2,1,5,7,9],[1,2,5,7,9]];a=states[step%4];cells(d,a,335,170,(step%5,))
        text(d,(110,250),'An ordering exposes useful structure.',28,MINT,True)
        text(d,(110,470),'Illustration: adjacent swaps (not std::sort internals)',22,MUTED);return
    if kind=='dp':
        vals=[0,1,2,1,1,2,2];k=step%7;cells(d,[v if j<=k else '?' for j,v in enumerate(vals)],350,100,(k,),cell=100)
        text(d,(100,250),'Minimum coins: denominations {1, 3, 4}',27,MINT,True)
        text(d,(100,295),'dp[s] = 1 + min(dp[s-c]) over usable coins c',22,MUTED)
        text(d,(100,490),'Base: dp[0] = 0     |     Build smaller totals first',23,YELLOW);return
    if kind=='grid':
        for r in range(5):
            for c in range(8):
                col=MINT if 1<=r<4 and 2<=c<6 else '#263754'
                box(d,(160+c*68,225+r*58,220+c*68,275+r*58),col,r=8)
                text(d,(180+c*68,238+r*58),'1',20,BG if col==MINT else WHITE)
        text(d,(100,535),'Rectangle [1,4) x [2,6): 24 - 6 - 8 + 2 = 12',23,YELLOW);return
    if kind=='interval':
        intervals=[(0,3),(2,5),(3,6),(5,8),(6,9)];sel=step%6
        for j,(a,b) in enumerate(intervals):
            yy=245+j*48;box(d,(130+a*65,yy,130+b*65,yy+30),MINT if j<sel else '#3c5279',r=8)
            text(d,(85,yy),str(j),21,MUTED)
        text(d,(110,525),'[start, finish): touching endpoints are compatible.',23,YELLOW);return
    if kind=='complexity':
        for j,(name,frac,color) in enumerate([('log n',.06,MINT),('n',.22,BLUE),('n log n',.45,YELLOW),('n squared',.95,PINK)]):
            y=245+j*70;text(d,(100,y),name,25,color,True);box(d,(290,y,290+max(5,520*frac*min(t/3,1)),y+35),color,r=7)
        text(d,(100,545),'Qualitative growth comparison, not a timing benchmark',21,MUTED);return
    if kind=='geometry':
        pts=[(170,420),(260,250),(570,240),(730,400),(480,505)];d.polygon(pts,outline=MINT,width=5)
        for x,y in pts:d.ellipse((x-8,y-8,x+8,y+8),fill=YELLOW)
        for x,y in [(330,360),(450,330),(540,410)]:d.ellipse((x-6,y-6,x+6,y+6),fill=MUTED)
        text(d,(100,545),'Orientation + careful degeneracy handling -> convex hull',21,MUTED);return
    if kind=='search':
        mask=step%16
        for j in range(4):box(d,(155+j*160,310,285+j*160,410),MINT if mask>>j&1 else '#2b3a55');text(d,(190+j*160,333),str(j),38,BG if mask>>j&1 else WHITE,True)
        text(d,(155,470),f'Subset mask {mask:04b}   |   2^4 = 16 candidates',28,YELLOW);return
    if kind=='array':
        cells(d,[3,1,4,1,5],330,155,(step%5,));text(d,(110,250),'Visit each element. Track exactly what changes.',27,MINT,True)
        text(d,(110,480),'Indices: 0 through n - 1.  Index n is not a bonus seat.',23,MUTED);return
    # Animated festival stage for story, checkpoints and finale.
    for j in range(12):
        height=40+abs(math.sin(t*3+j*.8))*120;x=110+j*62
        box(d,(x,480-height,x+37,480),[MINT,PINK,BLUE,YELLOW][j%4],r=7)
    text(d,(105,250),'READ  >  MODEL  >  PROVE  >  CODE  >  TEST',27,MINT,True)
    text(d,(110,520),'THE TRAINING ARC     /     You own the keyboard.',23,MUTED)
def frame(i,t,meta):
    lesson=lessons[i];im=Image.new('RGB',(W,H),BG);d=ImageDraw.Draw(im)
    # Subtle original grid and moving beat indicator.
    for x in range(0,W,80):d.line((x,0,x,H),fill='#111a2d')
    for y in range(0,H,80):d.line((0,y,W,y),fill='#111a2d')
    text(d,(45,22),'BESSIE VS. THE ALGORITHM',20,MINT,True)
    text(d,(825,24),f'{lesson["level"]}  /  CHAPTER {i+1:02d} OF {len(lessons)}',18,MUTED)
    title=lesson['title'];size=38
    while d.textlength(title,font=f(size,True))>1170:size-=1
    text(d,(45,69),title,size,WHITE,True)
    beat=next((j for j,b in enumerate(meta['beats']) if b['start']<=t<b['end']),len(meta['beats'])-1);b=meta['beats'][beat]
    text(d,(48,126),b['title'],27,YELLOW,True)
    box(d,(45,180,925,580),PANEL)
    text(d,(70,194),'VISUAL LAB / '+lesson['visual'].upper(),15,MUTED)
    if b['title'] in ('PAUSE & CODE','ANSWER'):
        s=lesson['challenge'] if b['title']=='PAUSE & CODE' else lesson['answer']
        text(d,(90,255),'YOUR TURN' if b['title']=='PAUSE & CODE' else 'CHECK YOUR REASONING',30,MINT,True)
        wrapped(d,(90,318),s,770,29,WHITE,True)
        text(d,(90,525),'Pause as long as you need.' if b['title']=='PAUSE & CODE' else 'Explain WHY before moving on.',24,YELLOW)
    else:visual(d,lesson['visual'],t-b['start'],lesson,beat)
    box(d,(950,180,1235,580),'#1c203b');cow(d,1092,296,t)
    wrapped(d,(973,440),lesson['hook'],238,24,WHITE,True,maxlines=4)
    # Exact sentence audio boundaries, split into short timed caption cards.
    cue=next((c for c in meta['cues'] if c['start']<=t<c['end']),None)
    if cue:
        words=cue['text'].split();chunks=[' '.join(words[j:j+16]) for j in range(0,len(words),16)]
        k=min(len(chunks)-1,int((t-cue['start'])/(cue['end']-cue['start'])*len(chunks)))
        lines=wrap(d,chunks[k],1150,25)
        for j,line in enumerate(lines[:2]):
            tw=d.textlength(line,font=f(25));text(d,((W-tw)/2,606+j*33),line,25,WHITE)
    text(d,(45,688),'ORIGINAL MUSIC + SYNTHETIC NARRATION  |  PAUSE. CODE. REPLAY.',13,MUTED)
    box(d,(45,676,1235,681),'#2d3c58',r=2);d.rectangle((45,676,45+1190*t/meta['duration'],681),fill=MINT)
    return im

def mix_audio(i,meta):
    import soundfile as sf
    voice,sr=sf.read(OUT/'audio'/f'{i:03d}.wav',dtype='float32');n=len(voice);x=np.arange(n)/sr
    # Original 88 BPM instrumental: synthesized kick, snare, hi-hat and bass.
    beat=60/88;phase=x%beat
    kick=np.sin(2*np.pi*(51*phase+2*(1-np.exp(-phase*35))))*np.exp(-phase*24)
    rng=np.random.default_rng(100+i);noise=rng.normal(0,1,n).astype(np.float32)
    snarephase=(x-beat)%(beat*2);snare=noise*np.exp(-snarephase*45)
    hatphase=x%(beat/2);hat=noise*np.exp(-hatphase*140)
    notes=np.array([55,55,65.406,49]);freq=notes[(x//(beat*4)).astype(int)%4]
    bass=np.sin(2*np.pi*freq*x)*np.exp(-phase*7)
    music=.016*kick+.006*snare+.003*hat+.008*bass
    fade=np.minimum(1,x/1.0)*np.minimum(1,(len(x)/sr-x)/1.5)
    mix=np.clip(.90*voice+music*fade,-.98,.98)
    path=OUT/'audio'/f'{i:03d}-mix.wav';sf.write(path,mix,sr);return path

def render(i,sample=False):
    meta=json.loads((OUT/'audio'/f'{i:03d}.json').read_text());path=OUT/'chapters'/f'{i:03d}.mp4'
    if path.exists() and path.stat().st_size>10000 and not sample:return
    duration=min(20,meta['duration']) if sample else meta['duration'];audio=mix_audio(i,meta)
    target=OUT/'sample.mp4' if sample else path.with_suffix('.partial.mp4')
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo','-vcodec','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-i',str(audio),'-t',str(duration),'-c:v','libx264','-preset','veryfast','-crf','24','-threads','2','-pix_fmt','yuv420p','-c:a','aac','-b:a','96k','-movflags','+faststart',str(target)]
    proc=subprocess.Popen(cmd,stdin=subprocess.PIPE)
    for k in range(math.ceil(duration*FPS)):
        proc.stdin.write(frame(i,k/FPS,meta).tobytes())
    proc.stdin.close();rc=proc.wait()
    if rc:raise RuntimeError(f'ffmpeg failed {i}: {rc}')
    if not sample:target.rename(path)
    print(f'Rendered {i+1}/{len(lessons)}: {duration:.1f}s {target.name}',flush=True)
if __name__=='__main__':
    if '--frame' in sys.argv:
        i=int(sys.argv[-1]);meta=json.loads((OUT/'audio'/f'{i:03d}.json').read_text());frame(i,meta['beats'][1]['start']+10,meta).save(OUT/f'preview-{i:03d}.png')
    elif '--sample' in sys.argv:render(0,True)
    else:
        for i in range(len(lessons)):
            while not (OUT/'audio'/f'{i:03d}.json').exists():time.sleep(2)
            render(i)
