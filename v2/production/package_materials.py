"""Create compact student materials; media stays outside Git and this ZIP."""
import json,zipfile,hashlib,subprocess
from pathlib import Path
R=Path(__file__).resolve().parents[1];O=Path('/workspace/usaco-film-v2/output/course')
commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip()
path=O/'Rohail-V2-Course-Materials.zip'
with zipfile.ZipFile(path,'w',zipfile.ZIP_DEFLATED) as z:
 for p in sorted(R.rglob('*')):
  if p.is_file() and '__pycache__' not in p.parts and p.suffix in ['.txt','.py','.cpp','.json','.md']:
   z.write(p,'source/v2/'+str(p.relative_to(R)))
 z.write(O/'Rohail-USACO-V2-Workbook.pdf','Rohail-USACO-V2-Workbook.pdf')
 for n in range(1,5):
  for name in ['captions.srt','chapters.txt','chapters.json','verification.json']:
   p=O/f'part{n}'/name
   if p.exists():z.write(p,f'part{n}/'+name)
 z.writestr('SOURCE-CHECKPOINT.txt',commit+'\nStudent programs use C++17. Videos are separate Drive files.\n')
report={'file':str(path),'bytes':path.stat().st_size,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'source_commit':commit}
(O/'materials-verification.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
