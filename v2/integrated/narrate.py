import os
os.environ['OMP_NUM_THREADS']='1';os.environ['OPENBLAS_NUM_THREADS']='1'
import json,hashlib,time
from pathlib import Path
import numpy as np
import soundfile as sf
import onnxruntime as ort
from kokoro_onnx import Kokoro
from lesson import SCENES,VOICE
OUT=Path('/workspace/usaco-film-v2/output/integrated');CACHE=OUT/'cache';CACHE.mkdir(parents=True,exist_ok=True)
o=ort.SessionOptions();o.intra_op_num_threads=2;o.inter_op_num_threads=1
k=Kokoro.from_session(ort.InferenceSession('/workspace/usaco-film/assets/kokoro-v1.0.onnx',sess_options=o,providers=['CPUExecutionProvider']),'/workspace/usaco-film/assets/voices-v1.0.bin')
parts=[];cues=[];pos=0;sr=24000
for s in SCENES:
 key=hashlib.sha256((json.dumps(VOICE,sort_keys=True)+s['text']).encode()).hexdigest();p=CACHE/(key+'.wav')
 if p.exists():a,sr=sf.read(p,dtype='float32')
 else:a,sr=k.create(s['text'],**VOICE);sf.write(p,a,sr)
 a=np.asarray(a,dtype=np.float32);end=pos+len(a)/sr
 cues.append(dict(**s,start=pos,speech_end=end,end=end+s['pause']));parts.extend([a,np.zeros(round(sr*s['pause']),np.float32)]);pos=end+s['pause']
 print(s['key'],round(pos,2),flush=True)
sf.write(OUT/'lesson.wav',np.concatenate(parts),sr)
words=sum(len(s['text'].split()) for s in SCENES)
report=dict(voice=VOICE,cues=cues,duration=pos,words=words,overall_wpm=words*60/pos,caption_method='Full paragraph shown for exact synthesized paragraph interval; no inferred word timestamps.',voice_user_approval='2026-10-27 slower Voice A approved; integrated technical QA pending')
(OUT/'timing.json').write_text(json.dumps(report,indent=2));print('COMPLETE',words,pos,words*60/pos,flush=True)
