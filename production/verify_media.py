"""Post-export integrity and bounded synchronization checks."""
import json,subprocess,re
from pathlib import Path
from assemble import probe
from curriculum import lessons
ROOT=Path('/workspace/usaco-film/output');movie=ROOT/'Bessie-vs-the-Algorithm-USACO.mp4'
x=probe(movie);v=next(s for s in x['streams'] if s['codec_type']=='video');a=next(s for s in x['streams'] if s['codec_type']=='audio')
start_gap=abs(float(v.get('start_time',0))-float(a.get('start_time',0)))
end_gap=abs(float(v.get('start_time',0))+float(v['duration'])-float(a.get('start_time',0))-float(a['duration']))
assert start_gap<.09 and end_gap<.25,(start_gap,end_gap)
packets={}
for kind in ['v','a']:
 raw=subprocess.check_output(['ffprobe','-v','error','-select_streams',kind,'-show_packets','-show_entries','packet=dts_time','-of','json',str(movie)])
 ts=[float(p['dts_time']) for p in json.loads(raw)['packets'] if 'dts_time' in p]
 assert all(t<u for t,u in zip(ts,ts[1:])),kind
 packets[kind]=len(ts)
expected=sum(int(next(s for s in probe(ROOT/'chapters'/f'{i:03d}.mp4')['streams'] if s['codec_type']=='video')['nb_frames']) for i in range(len(lessons)))
assert int(v['nb_frames'])==expected
assert len(x['chapters'])==len(lessons)
report={'status':'passed','video_frames_preserved':expected,'audio_video_start_gap_seconds':start_gap,'audio_video_end_gap_seconds':end_gap,'strictly_monotonic_DTS_packet_counts':packets,'code_tests':(ROOT/'code-test-results.txt').read_text().strip(),'notes':['Audio/video boundary tolerance covers one video frame plus encoder padding.','Per-sentence speech timings are measured; within-sentence caption cards use proportional timing.','No claim that every word has been manually listened to or every frame manually inspected.']}
(ROOT/'final-QA.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
