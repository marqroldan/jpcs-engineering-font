from pathlib import Path
from fontTools.ttLib import TTFont
import hashlib,json,subprocess
root=Path(__file__).resolve().parents[1] / 'fonts'; old=root/'JPCS_Engineering_Font_1_3_Candidate.ttf'; new=root/'JPCS_Engineering_Font_1_4_Candidate.ttf'; prior=root/'JPCS_Engineering_Font_Improved.ttf'
output=root.parent/'build'; output.mkdir(exist_ok=True)
a,b=TTFont(old),TTFont(new); ak=a['kern'].kernTables[0].kernTable;bk=b['kern'].kernTables[0].kernTable
changed={str(k):[ak.get(k,0),bk.get(k,0)] for k in set(ak)|set(bk) if ak.get(k,0)!=bk.get(k,0)}
data={'sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (prior,old,new)},'unchanged_raw_tables':{tag:a.getTableData(tag)==b.getTableData(tag) for tag in ['glyf','loca','hmtx','cmap','GSUB']},'changed_pairs_units_per_2048_em':changed,'C4_added_spacing_units':406,'C4_added_spacing_pixels_144dpi':{'18pt':406*36/2048,'28pt':406*56/2048},'shaping':{}}
for text in ['C4','E4','C6','C8','E6','E8','AVATAR','Lorem ipsum.','3.14','j\u0301']:
 data['shaping'][text]=[subprocess.check_output(['hb-shape',str(p),text],text=True).strip() for p in (old,new)]
assert all(data['unchanged_raw_tables'].values()) and len(changed)==6
assert data['sha256'][old.name]=='4ffdcfbdf28a3385e0e2e1111114aa50ce774bc4dc268ebba2a342146524c52d'
assert data['sha256'][prior.name]=='072fada41dc03586713eac1ddff247dffa997cae19103f2d66fed45eab05f752'
for s in ['AVATAR',"Lorem ipsum.",'3.14','j\u0301']:assert data['shaping'][s][0]==data['shaping'][s][1]
(output/'metrics-check-1.4.json').write_text(json.dumps(data,indent=2)+'\n'); print(json.dumps(data,indent=2))
