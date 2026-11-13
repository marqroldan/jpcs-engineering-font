from datetime import datetime
from zoneinfo import ZoneInfo
from fontTools.ttLib import TTFont
from fontTools.feaLib.builder import addOpenTypeFeaturesFromString
from pathlib import Path
import copy
root = Path(__file__).resolve().parents[1]
build = root / 'build'
build.mkdir(exist_ok=True)
src = root / 'fonts/JPCS_Engineering_Font_1_3_Candidate.ttf'
out = build / 'JPCS_Engineering_Font_1_4_Candidate.ttf'
f=TTFont(src); cmap=f.getBestCmap(); pairs=copy.deepcopy(f['kern'].kernTables[0].kernTable)
for s,v in [('C4',-200),('E4',-240),('C6',-60),('C8',-60),('E6',-135),('E8',-135)]:pairs[tuple(cmap[ord(ch)] for ch in s)]=v
f['kern'].kernTables[0].kernTable=pairs
stage=TTFont(src); rules='\n'.join('pos %s %s %d;'%(a,b,v) for (a,b),v in pairs.items() if v)
addOpenTypeFeaturesFromString(stage,'feature kern {\n'+rules+'\n} kern;')
assert stage['GPOS'].table.LookupList.Lookup[0].LookupType==2
f['GPOS'].table.LookupList.Lookup[0]=stage['GPOS'].table.LookupList.Lookup[0]
family='JPCS Engineering Font 1.4 Candidate'; ps='JPCSEngineeringFont14Candidate'
for name in f['name'].names:
 replacement={1:family,3:'JPCS Engineering Font 1.4 Candidate; 2026-11-07',4:family,6:ps,16:family,17:'Regular',5:'Version 1.4 candidate'}.get(name.nameID)
 if replacement is not None:
  try:name.string=replacement.encode(name.getEncoding())
  except UnicodeEncodeError:pass
f['head'].fontRevision=1.4;f.save(out); print(datetime.now(ZoneInfo('Asia/Manila')).isoformat(), out)
