"""Short no-cost audition; not a claim of approved expressive quality."""
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
OUT.mkdir(parents=True,exist_ok=True)
TEXT="""Meet Rohail. Tenth grade, school music night, and one very suspicious ticket total. His program says eight dollars. The cash box says five. Okay... who bought a ticket with imaginary money? Maya pulls up the transactions: three dollars in, two refunded, five in, one refunded. Rohail spots it. His code ignored the refunds! There's no need for us to rush this through. Let's follow the numbers. Start at zero. Add three: we're at three. Subtract two: one. Add five: six. Subtract one: five. There it is. The cash box was right. Now the interesting question: how do we write a loop that gets this right every time, including an empty list? That's where an invariant earns its backstage pass."""
voices=[('A','af_heart','en-us'),('B','am_eric','en-us')]
opts=ort.SessionOptions();opts.intra_op_num_threads=2;opts.inter_op_num_threads=1
session=ort.InferenceSession('/workspace/usaco-film/assets/kokoro-v1.0.onnx',sess_options=opts,providers=['CPUExecutionProvider'])
k=Kokoro.from_session(session,'/workspace/usaco-film/assets/voices-v1.0.bin')
reports=[]
for label,voice,lang in voices:
    start=time.monotonic()
    audio,sr=k.create(TEXT,voice=voice,speed=1.0,lang=lang,continuous=False,sentence_pause=.30,clause_pause=.12)
    sf.write(OUT/f'voice-{label}.wav',np.asarray(audio,dtype=np.float32),sr)
    r=dict(label=label,stock_voice=voice,duration=len(audio)/sr,build_seconds=time.monotonic()-start,
           synthesis='whole-passage batched generation; no pitch shift/time stretch',listening_review='pending')
    reports.append(r);print(json.dumps(r),flush=True)
(OUT/'audition.json').write_text(json.dumps(dict(text=TEXT,voices=reports,
    hook='Selected user-supplied Too Much heading excerpt; educational reinterpretation; metadata unverified',
    presentation='Rohail, fictional tenth grader; no mascot; no background music for voice evaluation'),indent=2))
