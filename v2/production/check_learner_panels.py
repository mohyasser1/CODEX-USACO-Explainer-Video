"""Reject production-note leakage and test the displayed main excerpt independently."""
import sys,json,re,subprocess
from pathlib import Path
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R))
from script_text import scenes
from art import model
count=0
for part in json.loads((R/'course_manifest.json').read_text())['parts']:
 for name in part['scripts']:
  for i,(direction,text) in enumerate(scenes((R/name).read_text())):
   m=model(dict(source=name,scene=i,direction=direction,text=text))
   display=' '.join(str(m.get(k,'')) for k in ['label','notes','rows','steps','small'])
   assert m['kind']!='concept',(name,i)
   assert not re.search(r'\b(?:animate|highlight|draw|show|stage directions|answer scene|user.supplied excerpt)\b|on screen|do not display',display,re.I),(name,i,display)
   count+=1
name='part1_string_lab_script.txt';d,t=scenes((R/name).read_text())[9];code=model(dict(source=name,scene=9,direction=d,text=t))['code']
p=Path('/workspace/usaco-film-v2/output/course/displayed_string.cpp')
p.write_text('#include <bits/stdc++.h>\nusing namespace std;\nint main(){\n'+'\n'.join(code)+'\n}\n')
subprocess.run(['g++','-std=c++17','-fsanitize=undefined','-o',str(p.with_suffix('')),str(p)],check=True)
for word in ['', 'A','AAAA','SWISS','BANANA','ZYX']:
 expected=next((i for i,c in enumerate(word) if word.count(c)==1),-1)
 result=subprocess.run([str(p.with_suffix(''))],input=word+'\n',capture_output=True,text=True,check=True)
 assert result.stdout==str(expected)+'\n' and not result.stderr,(word,result.stdout,result.stderr)
report={'scenes':count,'no_production_directions':True,'no_concept_fallback':True,'displayed_string_main_oracle_cases':6,'passed':True,'scope':'All authored panel text plus compiled displayed string excerpt; rendered frames and audio require separate review'}
(R/'verification/learner-panels.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
