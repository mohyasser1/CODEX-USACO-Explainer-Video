"""Validate an already generated audio-only remux; preserve the prior artifact."""
import json,sys,subprocess,hashlib
from pathlib import Path
n=int(sys.argv[1]);p=Path('/workspace/usaco-film-v2/output/course')/f'part{n}';new=p/'level-corrected.mp4';old=p/f'Rohail-USACO-V2-Part-{n}.mp4'
subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(new),'-f','null','-'],check=True)
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-show_chapters','-of','json',str(new)]));ds=[float(s['duration']) for s in probe['streams'] if s['codec_type'] in ['video','audio']];assert max(ds)-min(ds)<.2
r=json.loads((p/'verification.json').read_text());assert len(probe['chapters'])==r['chapters'];assert any(s['codec_type']=='subtitle' for s in probe['streams']);assert abs(float(probe['format']['duration'])-r['duration'])<.2
archive=p/'superseded-audio-peak';archive.mkdir(exist_ok=True);assert not (archive/old.name).exists();old.rename(archive/old.name);new.rename(old)
r.update(duration=float(probe['format']['duration']),bytes=old.stat().st_size,sha256=hashlib.sha256(old.read_bytes()).hexdigest(),av_end_difference=max(ds)-min(ds),audio_level_correction_db=-2,audio_rebuild_source='Cached lossless narration.wav; same atempo=1.25 and loudnorm settings, then volume=-2dB; video stream copied unchanged',full_decode='passed');(p/'verification.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
