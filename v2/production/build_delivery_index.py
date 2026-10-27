"""Build measured student navigation after all four final media checks exist."""
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1];O=Path('/workspace/usaco-film-v2/output/course')
def clock(s):
 s=round(s);return f'{s//3600}:{s//60%60:02d}:{s%60:02d}'
reports=[json.loads((O/f'part{n}/verification.json').read_text()) for n in range(1,5)]
assert all(x.get('manuscript_paragraphs_exact') and x.get('full_decode')=='passed' for x in reports)
delivery=json.loads((O/'delivery.json').read_text());manifest=json.loads((R/'course_manifest.json').read_text())
lines=['ROHAIL’S SCHOOL MUSIC NIGHT — USACO V2','Four guided lessons, with runnable C++17 companions and separate practice solutions.','',f"Measured total video runtime: {clock(sum(x['duration'] for x in reports))}",'','Watch in order. Pause when prompted and attempt the exercise before revealing its answer. The short cue is not intended to supply all the time needed to solve a problem.','']
for n,(report,part) in enumerate(zip(reports,manifest['parts']),1):
 item=delivery['parts'][str(n)]
 assert item['local_sha256']==report['sha256']
 lines.extend([f"PART {n}: {part['title']} — {clock(report['duration'])}",item['url'],f"SHA256 {report['sha256']}"])
 for ch in json.loads((O/f'part{n}/chapters.json').read_text()):lines.append(f"  {clock(ch['start'])}  {ch['title'].title()}")
 lines.append('')
lines.extend(['COMPANIONS','Workbook: https://drive.google.com/file/d/1wuw-O9CgGLuzWQ0rSpkskgmDSEFf5BcJ/view','Code, captions and chapter files: https://drive.google.com/file/d/1TrsFw6DlOWI3AYFVNBjtOCKBmlhdRzUi/view','Source: https://github.com/mohyasser1/CODEX-USACO-Explainer-Video/tree/work/v2','','COVERAGE','C++ and Bronze foundations; selected Silver techniques and Gold foundations. Advanced topics are a prerequisite roadmap, not full implementations or a promise of Platinum mastery. Sustained independent problem solving remains necessary.','','PRESENTATION AND CHECKS','Original synthetic Voice A, delivered at the requested 1.25x tempo. Fictional students; selected user-supplied clean musical hooks, no artist voice or recording.','Diagrams present authored paragraph-level states, not word-synchronized execution. Full decode, manuscript/caption coverage, AV timing, clipping checks and sampled encoded-frame inspection are recorded separately for each part. The agent did not perform full human listening.','V1 is preserved separately.'])
(O/'START-HERE.txt').write_text('\n'.join(lines)+'\n')
(R/'FINAL-DELIVERY.txt').write_text('\n'.join(lines)+'\n')
print(O/'START-HERE.txt')
