from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.boundsPen import BoundsPen
from PIL import Image, ImageDraw, ImageFont, ImageChops
from pathlib import Path
import hashlib,json,subprocess
root=Path(__file__).resolve().parents[1] / 'fonts'; out=root.parent/'build'/'proof-1.3'; out.mkdir(parents=True,exist_ok=True)
a=root/'JPCS_Engineering_Font_Improved.ttf'; b=root/'JPCS_Engineering_Font_1_3_Candidate.ttf'
f=TTFont(a); g=TTFont(b)
def outline(font,ch):
 name=font.getBestCmap()[ord(ch)]; pen=RecordingPen(); font.getGlyphSet()[name].draw(pen); return pen.value
chars='1Il/0O'; preserved={c:outline(f,c)==outline(g,c) and f['hmtx'][f.getBestCmap()[ord(c)]]==g['hmtx'][g.getBestCmap()[ord(c)]] for c in chars}
invalid=[]
for cp,name in g.getBestCmap().items():
 if cp in (32,160):continue
 pen=BoundsPen(g.getGlyphSet());g.getGlyphSet()[name].draw(pen)
 if pen.bounds is None:invalid.append((cp,name))
def sample(path):
 im=Image.new('L',(600,100),'white'); d=ImageDraw.Draw(im);font=ImageFont.truetype(str(path),56,layout_engine=ImageFont.Layout.RAQM);d.text((20,5),'AVATAR',font=font,fill='black',features=['kern']);return im
same_avatar=ImageChops.difference(sample(a),sample(b)).getbbox() is None
hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [(root.parent/'source/jpcs_engring_font.ttf'),a,b]}
result={'sha256':hashes,'cmap_same':f.getBestCmap()==g.getBestCmap(),'mapped_codepoints':len(g.getBestCmap()),'empty_mapped_nonspaces':invalid,'preserved_outlines_and_metrics':preserved,'AVATAR_raster_identical_56px':same_avatar,'font_name':g['name'].getDebugName(1),'font_revision':g['head'].fontRevision,'legacy_kerning_pairs':len(g['kern'].kernTables[0].kernTable),'GPOS_lookups':[x.LookupType for x in g['GPOS'].table.LookupList.Lookup],'GSUB_features':[x.FeatureTag for x in g['GSUB'].table.FeatureList.FeatureRecord]}
assert result['cmap_same'] and not invalid and all(preserved.values()) and same_avatar
(out/'metrics-check.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
