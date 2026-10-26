"""Structural checks, complete decode and local hashes; no listening claim."""
import hashlib,json,subprocess
from pathlib import Path
OUT=Path('/workspace/usaco-film-v2/output')
movie=OUT/'V2-pilot-execution-and-proof.mp4'
timing=json.loads((OUT/'v2-pilot-timing.json').read_text())
info=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(movie)]))
video=next(s for s in info['streams'] if s['codec_type']=='video')
audio=next(s for s in info['streams'] if s['codec_type']=='audio')
assert (video['width'],video['height'])==(1280,720)
assert video['avg_frame_rate']=='15/1'
assert abs(float(video['duration'])-float(audio['duration']))<.15
assert abs(float(info['format']['duration'])-timing['duration'])<.15
assert all(0<=c['start']<c['end']<=timing['duration'] for c in timing['cues'])
assert all(a['end']<=b['start']+.0001 for a,b in zip(timing['cues'],timing['cues'][1:]))
subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(movie),'-f','null','-'],check=True)
report=dict(file=movie.name,bytes=movie.stat().st_size,sha256=hashlib.sha256(movie.read_bytes()).hexdigest(),
 duration_seconds=float(info['format']['duration']),narration_seconds=timing['duration'],
 resolution='1280x720',fps=15,complete_decode='passed',caption_intervals='ordered and in bounds',
 av_end_difference_seconds=abs(float(video['duration'])-float(audio['duration'])),
 limitations=['No full human listening review','Captions are timed within synthesized sentences by word fraction',
              'This is an early visual/teaching pilot, not a finished one-hour part'])
(OUT/'pilot-verification.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
