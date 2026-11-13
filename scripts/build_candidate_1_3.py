from datetime import datetime
from zoneinfo import ZoneInfo
from fontTools.ttLib import TTFont
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.pens.transformPen import TransformPen
from fontTools.feaLib.builder import addOpenTypeFeaturesFromString
from pathlib import Path
import copy
root = Path(__file__).resolve().parents[1]
build = root / 'build'
build.mkdir(exist_ok=True)
src = root / 'fonts/JPCS_Engineering_Font_Improved.ttf'
out = build / 'JPCS_Engineering_Font_1_3_Candidate.ttf'
f=TTFont(src); glyf=f['glyf']; hmtx=f['hmtx'].metrics

def transform(name, sx, sy, dx, dy, advance):
    glyph=glyf[name]; pen=TTGlyphPen(glyf)
    glyph.draw(TransformPen(pen,(sx,0,0,sy,dx,dy)),glyf)
    glyf[name]=pen.glyph(); glyf[name].recalcBounds(glyf)
    hmtx[name]=(advance,glyf[name].xMin)

# Keep the source's uneven outlines while giving the marks a similar optical weight.
transform('period',.72,.72,-88,25,305)
transform('comma',.72,.72,-58,0,355)
transform('quotesingle',.78,.85,-10,225,350)
transform('quotedbl',.78,.85,30,225,660)
# Bring the sidebearings of the existing slanted, single-stroke quotation marks into range.
for name in ('uni2018','uni2019','uni201C','uni201D','endash','emdash'):
    if name in glyf:
        old=glyf[name]; old.recalcBounds(glyf); delta=50-old.xMin; advance=hmtx[name][0]+delta
        transform(name,1,1,delta,0,advance)
transform('hyphen',1,.85,0,84,680)
# Construct punctuation from the source-derived period and comma.
def composite(name, parts, advance):
    pen=TTGlyphPen(glyf)
    for part,dx,dy in parts: pen.addComponent(part,(1,0,0,1,dx,dy))
    glyf[name]=pen.glyph(); glyf[name].recalcBounds(glyf); hmtx[name]=(advance,glyf[name].xMin)
composite('colon',[('period',0,235),('period',220,790)],580)
composite('semicolon',[('comma',0,0),('period',220,790)],580)
# Harmonize the dots of ! and ? without altering their upper strokes.
from fontTools.ttLib.tables.ttProgram import Program
for name, sx, sy, target_bottom in [('exclam',.65,.75,0),('question',.78,.65,0)]:
    g=glyf[name]; coords,ends,flags=g.getCoordinates(glyf)
    start=ends[0]+1; end=ends[1]+1
    xs=[coords[i][0] for i in range(start,end)]; ys=[coords[i][1] for i in range(start,end)]
    center=(min(xs)+max(xs))/2; bottom=min(ys)
    for i in range(start,end):
        x,y=coords[i]; g.coordinates[i]=(round(center+(x-center)*sx),round(target_bottom+(y-bottom)*sy))
    g.program=Program(); g.program.fromBytecode([]); g.recalcBounds(glyf)

# Expand compressed pairs by small, targeted increments, leaving AVATAR's pairs untouched.
pairs=copy.deepcopy(f['kern'].kernTables[0].kernTable)
changes={'SE':70,'EL':90,'EC':120,'CT':70,'TI':60,'IO':35,'ON':60,
         'PR':100,'GR':70,'ES':90,'SS':50,'PE':90,'E2':70,'E0':100,'1L':60,
         }
cmap=f.getBestCmap()
for s,delta in changes.items():
    key=tuple(cmap[ord(ch)] for ch in s); pairs[key]=pairs.get(key,0)+delta
# Numerals have systematic crowding in continuous identifiers; open their pairs evenly.
for a in '0123456789':
    for b in '0123456789':
        key=(cmap[ord(a)],cmap[ord(b)]); pairs[key]=pairs.get(key,0)+65
    for b in '/':
        for key in ((cmap[ord(a)],cmap[ord(b)]),(cmap[ord(b)],cmap[ord(a)])):
            pairs[key]=pairs.get(key,0)+55
# Selective punctuation corrections: reduced sidebearings do most of the work.
# Keep decimal marks close without crowding their neighbours.
period=cmap[ord('.')]
for ch in '0123456789':
    pairs[(cmap[ord(ch)],period)]=-35
    pairs[(period,cmap[ord(ch)])]=100
# Keep the legacy and GPOS kern tables synchronized while retaining mark positioning.
f['kern'].kernTables[0].kernTable=pairs
stage=TTFont(src)
rules='\n'.join('pos %s %s %d;'%(a,b,v) for (a,b),v in pairs.items() if v)
addOpenTypeFeaturesFromString(stage,'feature kern {\n'+rules+'\n} kern;')
assert stage['GPOS'].table.LookupList.Lookup[0].LookupType==2
assert f['GPOS'].table.LookupList.Lookup[0].LookupType==2
f['GPOS'].table.LookupList.Lookup[0]=stage['GPOS'].table.LookupList.Lookup[0]
family='JPCS Engineering Font 1.3 Candidate'
ps='JPCSEngineeringFont13Candidate'
for name in f['name'].names:
    replacement={1:family,3:'JPCS Engineering Font 1.3 Candidate; 2026-11-07',4:family,6:ps,16:family,17:'Regular',5:'Version 1.3 candidate'}.get(name.nameID)
    if replacement is not None:
        try: name.string=replacement.encode(name.getEncoding())
        except UnicodeEncodeError: pass
f['head'].fontRevision=1.3
f.save(out)
print(datetime.now(ZoneInfo('Asia/Manila')).isoformat(), out, 'kerning pairs',len(pairs))
