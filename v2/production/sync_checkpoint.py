"""Synchronize provisional prose counts from the parsed manuscript report."""
import json,re
from pathlib import Path
r=Path(__file__).resolve().parents[1];d=json.loads((r/'draft-progress.json').read_text());m=json.loads((r/'course_manifest.json').read_text())
for name in ['PLAN.txt','REVIEW-CHECKPOINT.txt']:
 p=r/name;t=p.read_text()
 for x in d['parts']:
  n=x['part'];w=x['spoken_words'];minutes=x['estimated_minutes']
  t=re.sub(r'(PART '+str(n)+r' —[^\n]*\n)[\d,]+ words; estimated [\d.]+ minutes\.',lambda z:z[1]+f'{w:,} words; estimated {minutes:.2f} minutes.',t)
  t=re.sub(r'Part '+str(n)+r': [\d,]+ (?:narration |spoken )?words; estimated [\d.]+ minutes[^\n]*',f'Part {n}: {w:,} words; estimated {minutes:.2f} minutes at the provisional pace.',t)
 t=re.sub(r'Total:? [\d,]+ (?:narration )?words[^\n]*',f"Total: {d['total_spoken_words']:,} words; estimated {d['total_spoken_words']/m['provisional_words_per_minute']:.2f} minutes. Not measured full-part audio.",t)
 t=re.sub(r'Workbook:\d+ pages,32 exercises', 'Workbook: see verification/workbook-layout.json for current page count;32 exercises',t)
 p.write_text(t)
