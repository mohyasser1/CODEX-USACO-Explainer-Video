"""Count spoken draft text, excluding metadata before first visual and directions."""
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parent
manifest=json.loads((ROOT/'course_manifest.json').read_text())
rows=[]
for part in manifest['parts']:
    scripts=[]
    for name in part['scripts']:
        raw=(ROOT/name).read_text();raw=raw[raw.index('['):]
        text=re.sub(r'\[[\s\S]*?\]',' ',raw)
        assert not re.search(r'\b(Bessie|Alex)\b',text),name
        scripts.append(dict(file=name,spoken_words=len(text.split())))
    words=sum(s['spoken_words'] for s in scripts)
    rows.append(dict(part=part['number'],spoken_words=words,
                     estimated_minutes=round(words/manifest['provisional_words_per_minute'],2),
                     scripts=scripts,missing_drafts=part['missing_drafts']))
report=dict(status='Provisional estimates; no full-part narration measured',parts=rows,
            total_spoken_words=sum(p['spoken_words'] for p in rows))
(ROOT/'draft-progress.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
