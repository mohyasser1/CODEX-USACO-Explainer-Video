"""Final-part manuscript/metadata/stream checks plus sampled encoded frames."""
import sys,json,subprocess,hashlib
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from script_text import scenes
R=Path(__file__).resolve().parents[1];OUT=Path('/workspace/usaco-film-v2/output/course')
def verify(n):
 p=OUT/f'part{n}';t=json.loads((p/'timing.json').read_text());v=p/f'Rohail-USACO-V2-Part-{n}.mp4';report=json.loads((p/'verification.json').read_text());manifest=json.loads((R/'course_manifest.json').read_text())['parts'][n-1]
 expected=[(name,i,d,text) for name in manifest['scripts'] for i,(d,text) in enumerate(scenes((R/name).read_text())) if text.strip()]
 actual=[(c['source'],c['scene'],c['direction'],c['text']) for c in t['cues']];assert actual==expected,'Narration manuscript mismatch'
 assert report['words']==sum(len(text.split()) for _,_,_,text in expected)
 assert abs(report['duration']-t['duration']/1.25)<.25
 assert report['embedded_english_subtitles']
 # Decode just the final audio to inspect finite values and sample clipping.
 proc=subprocess.Popen(['ffmpeg','-v','error','-i',str(v),'-map','0:a:0','-f','f32le','-'],stdout=subprocess.PIPE)
 peak=0.0
 while True:
  raw=proc.stdout.read(4*1024*1024)
  if not raw:break
  a=np.frombuffer(raw,dtype=np.float32);assert np.isfinite(a).all();peak=max(peak,float(np.max(np.abs(a))))
 proc.stdout.close();assert proc.wait()==0
 assert peak<1.0,('clipping',peak)
 important={
 'part1_foundations_script.txt':{2,3,15},'part1_loop_trace_script.txt':{3,4,6,9,14,15},'part1_functions_cost_script.txt':{6},'part1_string_lab_script.txt':{9,11,12},'part1_backtracking_script.txt':{4,6,8,10,11},
 'part2_prefix_script.txt':{4,5,9,13},'part2_ranges_script.txt':{6,7,8,11},'part2_dashboard_lab_script.txt':{4,9,13},'part2_two_pointers_script.txt':{1,2,8,9,11,13},'part2_binary_search_script.txt':{7,8,9,13},'part2_greedy_script.txt':{2,4,8},'part2_transfer_script.txt':{1},
 'part3_graph_models_script.txt':{5},'part3_bfs_script.txt':{3,6,10,15,16},'part3_grid_lab_script.txt':{6,13,14},'part3_parity_script.txt':{4,6,7},'part3_functional_graph_script.txt':{7},'part3_dynamic_programming_script.txt':{9,13,17},'part3_topological_script.txt':{4,6},
 'part4_knapsack_script.txt':{4,8,9,10,13},'part4_lis_lab_script.txt':{3,7,9,11,14},'part4_dijkstra_script.txt':{2,3,4,6,12},'part4_dsu_mst_script.txt':{2},'part4_fenwick_script.txt':{3,6,8,9,13},'part4_segment_sparse_script.txt':{2,4,8},'part4_debug_clinic_script.txt':{1,3,4},'part4_practice_script.txt':{1}}
 selected=[]
 for j,c in enumerate(t['cues']):
  if c['scene']==0 or c['scene'] in important.get(c['source'],set()) or any(x in c['direction'].lower() for x in ['separate answer','answer scene','empty input','proof initialization','amount3','pop2','point addition index4']):selected.append((j,c))
 dest=p/'encoded-frames';dest.mkdir(exist_ok=True)
 for j,c in selected:
  at=c['start']/1.25+.3
  subprocess.run(['ffmpeg','-v','error','-y','-ss',str(at),'-i',str(v),'-frames:v','1',str(dest/f'{j:03}.png')],check=True)
 report.update(manuscript_paragraphs_exact=True,peak_decoded_audio=peak,sampled_frame_indices=[j for j,c in selected],frame_inspection='Extracted; visual inspection pending',sha256=hashlib.sha256(v.read_bytes()).hexdigest(),bytes=v.stat().st_size)
 (p/'verification.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2),flush=True)
if __name__=='__main__':verify(int(sys.argv[1]))
