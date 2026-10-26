"""Selected Voice A identity; new connected story and deliberate delivery."""
import os
os.environ['OMP_NUM_THREADS']='1'
os.environ['OPENBLAS_NUM_THREADS']='1'
import json,time
from pathlib import Path
import numpy as np
import soundfile as sf
import onnxruntime as ort
from kokoro_onnx import Kokoro
OUT=Path('/workspace/usaco-film-v2/output/recast')
PASSAGES=[
("On Friday afternoon, Rohail is helping Maya prepare for their school music night. He has written a little program to check the ticket money, and for a moment, everything seems to be working.", .8, 'Establish the scene before introducing the problem.'),
("The program reports eight dollars, but Maya finds only five in the cash box. Before anyone blames a missing sandwich or an imaginary ticket, she asks Rohail to look at the refunds with her.", 1.2, 'Let the mismatch register; neither student is blamed.'),
("There's no need for us to rush this through. They read the transactions in order: three dollars came in, two went back, another five came in, and one more was refunded. What should remain?", 2.0, 'A short prediction opportunity after the complete input.'),
("Rohail follows the balance carefully, moving from three dollars to one, then to six, and finally to five. Now he understands the mistake: his program counted incoming payments, but ignored money that went back out.", 1.2, 'Reflect on why the plausible first approach failed.'),
("Together, they change the plan so that every payment and every refund affects the running total. Next, we will turn that idea into a loop, and explain why it works for any valid list.", .6, 'Transition from story to the forthcoming general proof.'),
]
opts=ort.SessionOptions();opts.intra_op_num_threads=2;opts.inter_op_num_threads=1
session=ort.InferenceSession('/workspace/usaco-film/assets/kokoro-v1.0.onnx',sess_options=opts,providers=['CPUExecutionProvider'])
k=Kokoro.from_session(session,'/workspace/usaco-film/assets/voices-v1.0.bin')
pieces=[];cues=[];position=0;sr=24000;start=time.monotonic()
for text,pause,purpose in PASSAGES:
    a,sr=k.create(text,voice='af_heart',speed=.74,lang='en-us',continuous=False,sentence_pause=.30,clause_pause=.12)
    a=np.asarray(a,dtype=np.float32);pieces.append(a)
    cues.append(dict(start=position,end=position+len(a)/sr,text=text,pause_after=pause,pause_purpose=purpose))
    position+=len(a)/sr;pieces.append(np.zeros(round(sr*pause),np.float32));position+=pause
sf.write(OUT/'voice-A-storytelling.wav',np.concatenate(pieces),sr)
words=sum(len(t.split()) for t,_,_ in PASSAGES)
report=dict(voice='af_heart',model='/workspace/usaco-film/assets/kokoro-v1.0.onnx',
    previous_voice_A_settings=dict(speed=1.0,continuous=False,sentence_pause=.30,clause_pause=.12),
    current_settings=dict(speed=.74,continuous=False,sentence_pause=.30,clause_pause=.12,lang='en-us'),
    delivery_changes='Connected medium-length sentences in contextual paragraphs; native synthesis pacing; purposeful reflection pauses; no audio time stretch or pitch shift.',
    duration_seconds=position,spoken_words=words,overall_words_per_minute=words*60/position,
    explicit_pause_seconds=sum(p for _,p,_ in PASSAGES),cues=cues,
    build_seconds=time.monotonic()-start,listening_approval='pending')
(OUT/'voice-A-storytelling.json').write_text(json.dumps(report,indent=2));print(json.dumps({k:v for k,v in report.items() if k!='cues'},indent=2))
