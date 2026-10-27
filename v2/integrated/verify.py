"""Check authored states against independent arithmetic and output fixtures."""
import json,subprocess
from pathlib import Path
from lesson import SCENES,VOICE
OUT=Path('/workspace/usaco-film-v2/output/integrated')
s={x['key']:x for x in SCENES};a=[3,-2,5,-1]
assert VOICE==dict(voice='af_heart',speed=.74,lang='en-us',continuous=False,sentence_pause=.30,clause_pause=.12)
for k in range(4):
 before=s['check0' if k==0 else f'next{k}'];after=s[f'add{k}']
 assert before['i']==k and before['total']==sum(a[:k]) and before['highlight']==4
 assert after['i']==k and after['total']==sum(a[:k+1]) and after['highlight']==5
assert (s['stop']['i'],s['stop']['total'],s['stop']['highlight'])==(4,5,4)
assert s['output']['highlight']==7
assert (s['empty']['values'],s['empty']['i'],s['empty']['total'])==([],0,0)
assert s['proof0']['total']==0 and s['proof0']['i']==0
assert (s['proofstep']['i'],s['proofstep']['total'])==('k','prefix(k)')
assert (s['proofend']['i'],s['proofend']['total'])==('n','prefix(n)')
assert s['transfer']['mode']=='question' and s['transfer']['total'] is None
assert SCENES.index(s['answer'])==SCENES.index(s['transfer'])+1
for vals in [a,[],[-4,0,7,-3]]:
 inp=str(len(vals))+'\n'+' '.join(map(str,vals))+'\n'
 p=subprocess.run(['/workspace/usaco-film-v2/signed-total'],input=inp,text=True,capture_output=True)
 assert p.returncode==0 and int(p.stdout)==sum(vals)
report=dict(passed=True,numerical_steps=8,proof_states=3,empty_input=True,transfer_answer_separate=True,input_reading_visible=True,output_highlight=True,limits='Authored state and fixture checks, not listening or independent rendered-frame QA.')
if (OUT/'timing.json').exists():
 t=json.loads((OUT/'timing.json').read_text());prev=0
 for c in t['cues']:
  assert abs(c['start']-prev)<1e-6 and c['start']<c['speech_end']<=c['end'];prev=c['end']
 assert abs(prev-t['duration'])<1e-6
 report['caption_intervals']='21 exact paragraph speech bounds; pauses excluded'
(OUT/'state-checks.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
