"""Resumable local narration with exclusive chapter locks and sentence caches."""
import os,json,re,time,sys,hashlib,fcntl
from pathlib import Path
os.environ['OMP_NUM_THREADS']='1'
os.environ['OPENBLAS_NUM_THREADS']='1'
ROOT=Path('/workspace/usaco-film'); OUT=ROOT/'output'

def worker(worker_id=0):
 import numpy as np
 import soundfile as sf
 import onnxruntime as ort
 from kokoro_onnx import Kokoro
 from curriculum import lessons
 (OUT/'audio').mkdir(exist_ok=True);(OUT/'sentence-cache').mkdir(exist_ok=True)
 opts=ort.SessionOptions();opts.intra_op_num_threads=1;opts.inter_op_num_threads=1
 opts.add_session_config_entry('session.intra_op.allow_spinning','0')
 session=ort.InferenceSession(str(ROOT/'assets/kokoro-v1.0.onnx'),sess_options=opts,providers=['CPUExecutionProvider'])
 k=Kokoro.from_session(session,str(ROOT/'assets/voices-v1.0.bin'))
 for i,lesson in enumerate(lessons):
  path=OUT/'audio'/f'{i:03d}.json';digest=hashlib.sha256(json.dumps(lesson,sort_keys=True).encode()).hexdigest()
  if path.exists() and json.loads(path.read_text()).get('digest')==digest:continue
  with open(OUT/'audio'/f'{i:03d}.lock','w') as lock:
   try:fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
   except BlockingIOError:continue
   if path.exists() and json.loads(path.read_text()).get('digest')==digest:continue
   start=time.monotonic();pieces=[];cues=[];beats=[];pos=0.;sr=24000
   segments=[('title',lesson['title']+'. '+lesson['hook'])]+[(h,t) for h,t in lesson['beats']]
   if lesson['challenge']:segments += [('PAUSE & CODE','Pause the video and try this challenge. '+lesson['challenge']),('ANSWER',lesson['answer'])]
   for j,(heading,paragraph) in enumerate(segments):
    begin=pos
    for sentence in re.split(r'(?<=[.!?])\s+',paragraph):
     if not sentence.strip():continue
     key=hashlib.sha256(('af_heart|0.98|int8-v1.0|'+sentence).encode()).hexdigest();cache=OUT/'sentence-cache'/(key+'.wav')
     if cache.exists():a,sr=sf.read(cache,dtype='float32')
     else:
      a,sr=k.create(sentence,voice='af_heart',speed=.98,lang='en-us');a=np.asarray(a,dtype=np.float32)
      tmp=cache.with_name(cache.stem+f'.{worker_id}.tmp.wav');sf.write(tmp,a,sr);tmp.replace(cache)
     cues.append(dict(start=pos,end=pos+len(a)/sr,text=sentence,beat=j));pieces.append(a);pos+=len(a)/sr
     gap=np.zeros(int(sr*.22),np.float32);pieces.append(gap);pos+=len(gap)/sr
    gap=np.zeros(int(sr*(7 if heading=='PAUSE & CODE' else .65)),np.float32);pieces.append(gap);pos+=len(gap)/sr
    beats.append(dict(title=heading,start=begin,end=pos))
   sf.write(OUT/'audio'/f'{i:03d}.wav',np.concatenate(pieces),sr)
   tmp=path.with_suffix('.tmp.json');tmp.write_text(json.dumps(dict(duration=pos,cues=cues,beats=beats,digest=digest),indent=2));tmp.replace(path)
   done=len(list((OUT/'audio').glob('[0-9][0-9][0-9].json')))
   print(f'Worker {worker_id}: chapter {i+1:02d}, {pos:.1f}s audio, {time.monotonic()-start:.1f}s build; {done}/{len(lessons)} complete',flush=True)
   if '--sample' in sys.argv:break
if __name__=='__main__':
 if '--workers' in sys.argv:
  from concurrent.futures import ProcessPoolExecutor
  count=int(sys.argv[sys.argv.index('--workers')+1])
  with ProcessPoolExecutor(max_workers=count) as pool:list(pool.map(worker,range(count)))
 else:worker()
