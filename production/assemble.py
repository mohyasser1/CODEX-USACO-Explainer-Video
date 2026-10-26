"""Join completed chapters, preserve chapter navigation, export captions, validate."""
import json,subprocess,time,sys,hashlib,zipfile
from pathlib import Path
from curriculum import lessons
ROOT=Path('/workspace/usaco-film/output');REPO=Path(__file__).resolve().parents[1]
def probe(path):return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_format','-show_streams','-show_chapters','-of','json',str(path)]))
def stamp(s):
 ms=round(s*1000);h,ms=divmod(ms,3600000);m,ms=divmod(ms,60000);sec,ms=divmod(ms,1000);return f'{h:02}:{m:02}:{sec:02},{ms:03}'
def run():
 paths=[ROOT/'chapters'/f'{i:03d}.mp4' for i in range(len(lessons))]
 while not all(p.exists() for p in paths):
  if '--wait' not in sys.argv:raise RuntimeError('Chapters are still rendering')
  time.sleep(3)
 srt=[];chapters=[];ffmeta=[';FFMETADATA1','title=Bessie vs. the Algorithm','artist=Original educational production','comment=Synthetic narration; original procedural music; C++ through Platinum extensions.'];offset=0.;counter=1
 for i,path in enumerate(paths):
  media=probe(path);duration=float(media['format']['duration']);meta=json.loads((ROOT/'audio'/f'{i:03d}.json').read_text())
  video=next(s for s in media['streams'] if s['codec_type']=='video');audio=next(s for s in media['streams'] if s['codec_type']=='audio')
  assert video['width']==1280 and video['height']==720 and video['codec_name']=='h264'
  assert abs(float(video.get('duration',duration))-meta['duration'])<.25,(i,'video timing')
  assert abs(float(audio.get('duration',duration))-meta['duration'])<.25,(i,'audio timing')
  chapters.append(dict(number=i+1,title=lessons[i]['title'],level=lessons[i]['level'],start=offset,duration=duration))
  ffmeta += ['[CHAPTER]','TIMEBASE=1/1000',f'START={round(offset*1000)}',f'END={round((offset+duration)*1000)}','title='+lessons[i]['title'].replace('=','\\=').replace(';','\\;').replace('#','\\#')]
  for cue in meta['cues']:
   words=cue['text'].split();chunks=[' '.join(words[j:j+16]) for j in range(0,len(words),16)]
   for j,chunk in enumerate(chunks):
    begin=offset+cue['start']+(cue['end']-cue['start'])*j/len(chunks);end=offset+cue['start']+(cue['end']-cue['start'])*(j+1)/len(chunks)
    import textwrap
    srt.append(f'{counter}\n{stamp(begin)} --> {stamp(end)}\n'+ '\n'.join(textwrap.wrap(chunk,48))+'\n');counter+=1
  offset+=duration
 (ROOT/'Bessie-USACO-captions.srt').write_text('\n'.join(srt));(ROOT/'chapters.json').write_text(json.dumps(chapters,indent=2));(ROOT/'chapters.ffmeta').write_text('\n'.join(ffmeta)+'\n')
 (ROOT/'chapter-index.txt').write_text('\n'.join(f'{stamp(c["start"]).split(",")[0]}  {c["number"]:02d}. {c["title"]} [{c["level"]}]' for c in chapters)+'\n')
 (ROOT/'concat.txt').write_text('\n'.join("file '"+str(p)+"'" for p in paths)+'\n')
 # Build one PCM track, padding each chapter to its actual container duration.
 # This avoids AAC priming/timestamp discontinuities across independent encodes.
 import soundfile as sf
 import numpy as np
 joined_audio=ROOT/'continuous-narration-and-music.wav'
 with sf.SoundFile(joined_audio,'w',samplerate=24000,channels=1,subtype='PCM_16') as sink:
  for i,ch in enumerate(chapters):
   data,sr=sf.read(ROOT/'audio'/f'{i:03d}-mix.wav',dtype='float32');assert sr==24000
   # Round cumulative boundaries, avoiding per-chapter rounding accumulation.
   target=round((ch['start']+ch['duration'])*sr)-round(ch['start']*sr)
   assert abs(target-len(data))<sr*.25
   if len(data)<target:data=np.pad(data,(0,target-len(data)))
   else:data=data[:target]
   sink.write(data)
 final=ROOT/'Bessie-vs-the-Algorithm-USACO.mp4';partial=final.with_suffix('.partial.mp4')
 subprocess.run(['ffmpeg','-hide_banner','-loglevel','warning','-y','-f','concat','-safe','0','-i',str(ROOT/'concat.txt'),'-i',str(joined_audio),'-i',str(ROOT/'chapters.ffmeta'),'-i',str(ROOT/'Bessie-USACO-captions.srt'),'-map','0:v:0','-map','1:a:0','-map','3:0','-map_metadata','2','-map_chapters','2','-c:v','copy','-c:a','aac','-b:a','128k','-af','loudnorm=I=-16:TP=-1.5:LRA=11','-ar','48000','-c:s','mov_text','-metadata:s:s:0','language=eng','-metadata:s:s:0','title=English','-movflags','+faststart',str(partial)],check=True)
 partial.rename(final)
 result=probe(final);actual=float(result['format']['duration']);assert abs(actual-offset)<2,(actual,offset)
 assert len(result['chapters'])==len(lessons)
 # Decode every audio/video packet; corrupt frames or truncated streams fail the build.
 subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(final),'-map','0:v:0','-map','0:a:0','-f','null','-'],check=True)
 sha=hashlib.sha256(final.read_bytes()).hexdigest()
 report=dict(status='passed',chapters=len(lessons),caption_cards=counter-1,duration_seconds=actual,bytes=final.stat().st_size,sha256=sha,streams=[{k:s.get(k) for k in ['codec_type','codec_name','width','height','duration','sample_rate']} for s in result['streams']],checks=['All chapter audio/video duration differences <0.25s','All video chapters 1280x720 H.264','46 embedded navigation chapters','Final duration within 2s of chapter sum','Complete audio/video decode with -xerror'],limits=['Visual layouts spot-checked; not every frame manually reviewed','Sentence boundaries measured from synthesis; within-sentence caption cards proportionally timed','Synthetic voice; no claim of human listening review of the entire film','Advanced chapters include surveys requiring additional study'])
 (ROOT/'verification.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2),flush=True)
if __name__=='__main__':run()
