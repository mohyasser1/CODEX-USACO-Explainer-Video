"""Structural manuscript checks, not editorial or rendered-media approval."""
import json
from pathlib import Path
from script_text import scenes,narration
root=Path(__file__).resolve().parent
# Regression: nested index brackets inside a multiline visual are not spoken.
assert narration('Metadata\n\n[Show dp[0]=0; a[2] highlighted.\nThen P[3][4]=7.]\nSay these five words only.')=='Say these five words only.'
assert narration('[Input [] with n=0.]\nEmpty input count.\n\n[State a[0] invalid.]\nDo not read it.')=='Empty input count.  Do not read it.'
m=json.loads((root/'course_manifest.json').read_text());pauses=[];count=0
for part in m['parts']:
 for name in part['scripts']:
  seq=scenes((root/name).read_text());count+=1
  for i,(cue,speech) in enumerate(seq):
   if any(w in speech.lower() for w in ['pause and','pause the video','pause for','transfer task:']):
    assert i+1<len(seq),(name,'no reveal scene')
    nxt=seq[i+1][0].lower()
    assert any(w in nxt for w in ['answer','correct sums']),(name,'next scene not labeled answer',nxt)
    pauses.append(dict(script=name,question_scene=i,answer_scene=i+1))
report=dict(passed=True,sections=count,learner_pause_boundaries=pauses,
 limitations='Checks scene boundaries and parser only; cannot detect every semantic spoiler or prove timing/voice quality.')
(root/'verification/script-structure-tests.json').write_text(json.dumps(report,indent=2))
print(f'PASS: {count} sections parsed; {len(pauses)} learner pauses have separate labeled answer scenes; nested-bracket regression passes.')
