"""Resumable paragraph synthesis using the approved Voice A configuration."""
import os
os.environ['OMP_NUM_THREADS']='2';os.environ['OPENBLAS_NUM_THREADS']='1'
import sys,json,hashlib,argparse,time
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from script_text import scenes
import numpy as np,soundfile as sf,onnxruntime as ort
from kokoro_onnx import Kokoro
ROOT=Path(__file__).resolve().parents[1];OUT=Path('/workspace/usaco-film-v2/output/course');OUT.mkdir(exist_ok=True,parents=True)
VOICE=dict(voice='af_heart',speed=.74,lang='en-us',continuous=False,sentence_pause=.30,clause_pause=.12)
def run(part_number):
 manifest=json.loads((ROOT/'course_manifest.json').read_text());part=manifest['parts'][part_number-1];dest=OUT/f'part{part_number}';dest.mkdir(exist_ok=True)
 cache=OUT/'audio-cache';cache.mkdir(exist_ok=True)
 opts=ort.SessionOptions();opts.intra_op_num_threads=2;opts.inter_op_num_threads=1
 k=Kokoro.from_session(ort.InferenceSession('/workspace/usaco-film/assets/kokoro-v1.0.onnx',sess_options=opts,providers=['CPUExecutionProvider']),'/workspace/usaco-film/assets/voices-v1.0.bin')
 cues=[];pos=0;sr=24000;started=time.time()
 with sf.SoundFile(dest/'narration.partial.wav',mode='w',samplerate=sr,channels=1,subtype='PCM_16') as wav:
  for chapter_idx,name in enumerate(part['scripts']):
   for scene_idx,(direction,text) in enumerate(scenes((ROOT/name).read_text())):
    if not text.strip():continue
    key=hashlib.sha256((json.dumps(VOICE,sort_keys=True)+text).encode()).hexdigest();p=cache/(key+'.wav')
    if p.exists():a,rate=sf.read(p,dtype='float32')
    else:
     a,rate=k.create(text,**VOICE);tmp=cache/(key+f'.{os.getpid()}.wav');sf.write(tmp,a,rate);tmp.replace(p)
    assert rate==sr and np.isfinite(a).all()
    pause=3.0 if any(q in text.lower() for q in ['pause and','pause the video','pause for','transfer task:']) else .65
    end=pos+len(a)/sr
    cue=dict(chapter=chapter_idx,source=name,scene=scene_idx,direction=direction,text=text,start=pos,speech_end=end,end=end+pause,audio_cache=p.name)
    cues.append(cue);wav.write(a);wav.write(np.zeros(round(sr*pause)));pos=end+pause
    progress=dict(part=part_number,cues_completed=len(cues),last_source=name,last_scene=scene_idx,audio_seconds=pos,elapsed_seconds=time.time()-started,status='synthesizing')
    tmp=dest/'progress.tmp.json';tmp.write_text(json.dumps(progress,indent=2));tmp.replace(dest/'progress.json')
    print(f'PART{part_number} {name} scene{scene_idx}: {pos:.1f}s',flush=True)
 (dest/'narration.partial.wav').replace(dest/'narration.wav')
 words=sum(len(c['text'].split()) for c in cues);report=dict(part=part_number,title=part['title'],voice=VOICE,duration=pos,words=words,overall_wpm=words*60/pos,cues=cues,caption_method='Whole narrated paragraph at exact paragraph audio bounds; no word timestamps')
 (dest/'timing.json').write_text(json.dumps(report,indent=2));progress.update(status='complete',words=words,overall_wpm=words*60/pos);(dest/'progress.json').write_text(json.dumps(progress,indent=2))
 print('COMPLETE',json.dumps(progress),flush=True)
if __name__=='__main__':run(int(sys.argv[1]))
