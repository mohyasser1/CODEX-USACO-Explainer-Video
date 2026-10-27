import sys,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from script_text import scenes
from render_course import base
from PIL import Image
r=Path(__file__).resolve().parents[1];m=json.loads((r/'course_manifest.json').read_text());out=Path('/workspace/usaco-film-v2/output/course/layout');out.mkdir(exist_ok=True);count=0
picked=[('part3_bfs_script.txt',6),('part3_dynamic_programming_script.txt',9),('part4_fenwick_script.txt',6),('part4_knapsack_script.txt',4),('part2_prefix_script.txt',5),('part3_grid_lab_script.txt',6),('part4_lis_lab_script.txt',7),('part2_dashboard_lab_script.txt',4)];sheet=Image.new('RGB',(1280,1440),'white')
for p in m['parts']:
 for f in p['scripts']:
  for i,(direction,text) in enumerate(scenes((r/f).read_text())):
   c=dict(source=f,scene=i,direction=direction,text=text)
   try:im=base(c,p['number'],p['title'])
   except Exception as e:raise RuntimeError((f,i,str(e))) from e
   count+=1
   if (f,i) in picked:
    j=picked.index((f,i));im.save(out/f'{j}.png');sheet.paste(im.resize((640,360)),((j%2)*640,(j//2)*360))
sheet.save(out/'representative-contact.png');report=dict(passed=True,scenes=count,representative_frames=picked,limits='Layout bounds only; independent state and visual inspection separate');(r/'verification/course-layout.json').write_text(json.dumps(report,indent=2));print('PASS layout',count,'scenes')
