"""Semantic teaching state, separate from rendering; deterministic QA probes."""
from pilot import CODE, VALUES
INPUT_CODE=['int n;', 'cin >> n;', 'vector<int> a(n);', 'for (int &x : a) {', '    cin >> x;', '}', '// Bounds checked in companion program']
def state_at(data,t):
    s=next((s for s in data['scenes'] if s['start']<=t<s['end']),data['scenes'][-1])
    idx=data['scenes'].index(s)
    cues=[c for c in data['cues'] if c['scene']==idx]
    cue=next((c for c in reversed(cues) if c['start']<=t),cues[0])
    text=cue['text']
    def at(prefix,end=False):
        return next(c['end' if end else 'start'] for c in cues if c['text'].startswith(prefix))
    r=dict(scene=s,code=CODE,highlight=-1,values=VALUES,i=s['i'],total=s['total'],
           label='TRANSACTIONS a',phase='At condition check',mode='array',n=4,
           invariant='total = sum of the first i elements')
    if idx==0:r.update(mode='contract',phase='Input contract, before execution')
    if idx==1:
        h=0 if text.startswith('Our integer') else 2 if text.startswith(('The vector','Think of','Its first','With four','Index four','Reading outside')) else 4 if text.startswith('The line that reads') else -1
        r.update(code=INPUT_CODE,highlight=h,label='INPUT: n = 4',phase='Values after successful input')
    if idx==2:
        h=2 if text.startswith(('Focus','The index')) else 1 if text.startswith('The variable') else 3 if text.startswith(('Assignment','The expression')) else -1
        r.update(highlight=h,mode='types' if t>=at('We assume') else 'array',phase='Initialize before the loop')
    if idx in (3,4,5,6):
        change={3:'Old total',4:'Three plus',5:'At index',6:'Six plus'}[idx]
        inc={3:'Then the increment',4:'Store one',5:'Then advance',6:'Increment i'}[idx]
        changed=t>=at(change,True);incremented=t>=at(inc,True)
        r.update(total=s['next_total'] if changed else s['total'],i=s['i']+int(incremented),highlight=2 if incremented else 3,
                 phase='BODY UPDATED; increment next' if changed and not incremented else 'At condition check')
        if text.startswith(('The condition','Now one','Then the increment','Increment i')):r['highlight']=2
        if text.startswith(('The answer','The code prints','Contest judges')):r.update(highlight=5,phase='Output after loop')
        if text.startswith('Notice that'):r['highlight']=2
        if idx==3 and text.startswith(('A for loop','It does not','Freeze','The next','If your','Our manager','The judge')):r['highlight']=-1
        if idx==4 and t>=at('This is why'):r['highlight']=-1
    if idx==7:
        r.update(i='i',total='prefix(i)',highlight=-1,label='PROOF: arbitrary i',phase='Invariant at a condition check')
        if text.startswith('Our loop'):r['highlight']=2
        if text.startswith('Initially'):r.update(i=0,total=0,highlight=1,label='PROOF: initialization')
        if text.startswith('If the invariant'):r.update(i='i',total='prefix(i)',highlight=3,label='PROOF: preservation',phase='Next add a[i]',invariant='prefix(i) + a[i] = prefix(i+1)')
        if text.startswith('Incrementing'):r.update(i='i+1',total='prefix(i+1)',highlight=2,label='PROOF: preservation',phase='Invariant restored')
        if t>=at('When the loop'):r.update(i=4,total=5,highlight=2,label='PROOF: termination',phase='i == n; all elements processed')
    if idx==8:
        r['highlight']=-1
        if t>=at('Your transfer task'):
            answered=t>=at('The totals are',True)
            r.update(values=[-4,0,7,-3],i=4 if answered else '?',total=0 if answered else '?',
                     label='TRANSFER INPUT',phase='Final condition check' if answered else 'Use player pause to work')
        if t>=at('With no elements'):
            r.update(values=[],n=0,i=0,total=0,label='EMPTY INPUT: n = 0',highlight=2,
                     phase='0 < 0 is false; body skipped')
            if t>=at('With no elements',True):r.update(highlight=5,phase='Print initialized total: 0')
    return r
