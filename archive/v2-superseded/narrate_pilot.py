"""Sentence-resumable V2 synthesis, entirely separate from V1 outputs."""
import os
os.environ['OMP_NUM_THREADS'] = '1'
os.environ['OPENBLAS_NUM_THREADS'] = '1'
import hashlib, json, re, time, importlib
from pathlib import Path
import numpy as np
import soundfile as sf
import onnxruntime as ort
from kokoro_onnx import Kokoro
SCENES=importlib.import_module(os.environ.get('V2_LESSON_MODULE','pilot')).SCENES
PREFIX=os.environ.get('V2_PREFIX','v2-pilot')

OUT = Path('/workspace/usaco-film-v2/output')
CACHE = OUT / 'sentence-cache'
CACHE.mkdir(parents=True, exist_ok=True)
opts = ort.SessionOptions()
opts.intra_op_num_threads = 2
opts.inter_op_num_threads = 1
session = ort.InferenceSession('/workspace/usaco-film/assets/kokoro-v1.0.onnx', sess_options=opts, providers=['CPUExecutionProvider'])
k = Kokoro.from_session(session, '/workspace/usaco-film/assets/voices-v1.0.bin')
pieces, cues, scenes = [], [], []
pos = 0
sr = 24000
for idx, scene in enumerate(SCENES):
    start = pos
    for sentence in re.split(r'(?<=[.!?])\s+', scene['text']):
        key = hashlib.sha256(('am_puck|1.0|int8-v1|' + sentence).encode()).hexdigest()
        path = CACHE / (key + '.wav')
        if path.exists():
            a, sr = sf.read(path, dtype='float32')
        else:
            a, sr = k.create(sentence, voice='am_puck', speed=1.0, lang='en-us')
            sf.write(path, a, sr)
        a = np.asarray(a, dtype=np.float32)
        cues.append(dict(start=pos, end=pos + len(a)/sr, text=sentence, scene=idx))
        pieces.append(a)
        pos += len(a)/sr
        pieces.append(np.zeros(int(sr*.20), np.float32))
        pos += .20
    pieces.append(np.zeros(int(sr*.65), np.float32))
    pos += .65
    scenes.append(dict(start=start, end=pos, **scene))
    print(f'Scene {idx+1}/{len(SCENES)}: cumulative {pos:.1f}s', flush=True)
sf.write(OUT/(PREFIX+'.wav'), np.concatenate(pieces), sr)
(OUT/(PREFIX+'-timing.json')).write_text(json.dumps(dict(duration=pos, cues=cues, scenes=scenes), indent=2))
print(f'COMPLETE {pos:.3f}s', flush=True)
