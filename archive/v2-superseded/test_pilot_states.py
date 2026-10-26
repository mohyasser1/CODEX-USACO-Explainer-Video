"""Regression checks for independently reviewed narration/visual mismatches."""
import json
from pathlib import Path
from pilot_states import state_at
root=Path('/workspace/usaco-film-v2/output')
data=json.loads((root/'v2-pilot-timing.json').read_text())
checks=[]
for t,highlight in [(94,4),(106,2),(160,2),(196,2),(274,5),(305,1),(312,3),(318,2),(379,2),(383,5)]:
    s=state_at(data,t);assert s['highlight']==highlight,(t,s)
    checks.append(dict(time=t,highlight=highlight,line=s['code'][highlight],i=s['i'],total=s['total'],values=s['values']))
assert 'cin >> x' in state_at(data,94)['code'][4]
for t in (378,379,380,381,382,383,390):
    s=state_at(data,t);assert s['values']==[] and s['i']==0 and s['total']==0 and s['n']==0
assert state_at(data,305)['i']==0 and state_at(data,305)['total']==0
assert state_at(data,312)['i']=='i' and state_at(data,318)['i']=='i+1'
count=0
for tick in range(int(data['duration']*5)):
    s=state_at(data,tick/5)
    if 'condition check' in s['phase'] and isinstance(s['i'],int) and isinstance(s['total'],int):
        assert s['total']==sum(s['values'][:s['i']]),(tick/5,s)
        count+=1
report=dict(passed=True,review_regression_probes=checks,invariant_samples=count,
            note='Semantic checks supplement sampled-frame and full-video review; not a listening review.')
(root/'pilot-state-tests.json').write_text(json.dumps(report,indent=2));print('PASS',count,'concrete invariant samples and 10 highlight regressions')
