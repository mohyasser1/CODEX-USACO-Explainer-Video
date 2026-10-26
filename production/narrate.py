import os
os.environ['OMP_NUM_THREADS']='2'
import json,re,time,sys,hashlib
from pathlib import Path
import numpy as np
import soundfile as sf
import onnxruntime as ort
from kokoro_onnx import Kokoro
from curriculum import lessons
ROOT=Path('/workspace/usaco-film'); OUT=ROOT/'output'; (OUT/'audio').mkdir(exist_ok=True)
k=Kokoro(str(ROOT/'assets/kokoro-v1.0.onnx'),str(ROOT/'assets/voices-v1.0.bin'))
# Bound CPU concurrency for predictable cloud rendering alongside synthesis.
opts=ort.SessionOptions(); opts.intra_op_num_threads=2; opts.inter_op_num_threads=1
k.sess=ort.InferenceSession(str(ROOT/'assets/kokoro-v1.0.onnx'),sess_options=opts,providers=['CPUExecutionProvider']) if hasattr(k,'sess') else None
for i,lesson in enumerate(lessons):
    if i < int(os.environ.get("START_CHAPTER", "0")): continue
    path=OUT/'audio'/f'{i:03d}.json'
    digest=hashlib.sha256(json.dumps(lesson,sort_keys=True).encode()).hexdigest()
    if path.exists() and json.loads(path.read_text()).get('digest')==digest: continue
    pieces=[]; cues=[]; beats=[]; pos=0.; sr=24000
    segments=[('title',lesson['title']+'. '+lesson['hook'])]+[(h,t) for h,t in lesson['beats']]
    if lesson['challenge']:
        segments += [('PAUSE & CODE', 'Pause the video and try this challenge. '+lesson['challenge']),('ANSWER',lesson['answer'])]
    for j,(heading,paragraph) in enumerate(segments):
        begin=pos
        for sentence in re.split(r'(?<=[.!?])\s+',paragraph):
            if not sentence.strip():continue
            a,sr=k.create(sentence,voice='af_heart',speed=0.98,lang='en-us')
            a=np.asarray(a,dtype=np.float32)
            cues.append(dict(start=pos,end=pos+len(a)/sr,text=sentence,beat=j))
            pieces.append(a);pos+=len(a)/sr
            gap=np.zeros(int(sr*.22),np.float32);pieces.append(gap);pos+=len(gap)/sr
        gaplen=7 if heading=='PAUSE & CODE' else .65
        gap=np.zeros(int(sr*gaplen),np.float32);pieces.append(gap);pos+=len(gap)/sr
        beats.append(dict(title=heading,start=begin,end=pos))
    audio=np.concatenate(pieces)
    sf.write(OUT/'audio'/f'{i:03d}.wav',audio,sr)
    path.write_text(json.dumps(dict(duration=pos,cues=cues,beats=beats,digest=digest),indent=2))
    print(f'{i+1}/{len(lessons)} {lesson["title"]}: {pos:.1f}s',flush=True)
    if '--sample' in sys.argv:break
