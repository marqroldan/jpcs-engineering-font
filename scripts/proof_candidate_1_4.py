from PIL import Image,ImageDraw,ImageFont,ImageChops
from pathlib import Path
root=Path(__file__).resolve().parents[1] / 'fonts';out=root.parent/'build'/'proof-1.4'; out.mkdir(parents=True,exist_ok=True)
fonts=[root/'JPCS_Engineering_Font_1_3_Candidate.ttf',root/'JPCS_Engineering_Font_1_4_Candidate.ttf']
rows=[(18,'/ C4'),(18,'PART-01 / C4'),(28,'/ C4'),(28,'PART-01 / C4'),(18,'C0  C1  C2  C3  C4  C5  C6  C7  C8  C9'),(18,'E0  E1  E2  E3  E4  E5  E6  E7  E8  E9')]
canvases=[]
for file in fonts:
 im=Image.new('RGB',(1350,710),'white');d=ImageDraw.Draw(im); y=35
 for pt,s in rows:
  d.text((30,y),s,font=ImageFont.truetype(str(file),pt*2,layout_engine=ImageFont.Layout.RAQM),fill='#111',features=['kern']);y+=100 if pt==18 else 135
 canvases.append(im)
canvases[0].save(out/'before.png');canvases[1].save(out/'after.png')
Image.blend(*canvases,.5).save(out/'overlay.png');ImageChops.difference(*canvases).save(out/'difference.png')
combined=Image.new('RGB',(1350,1470),'white');d=ImageDraw.Draw(combined);font=ImageFont.load_default()
d.text((25,5),'BEFORE — v1.3    18 pt / 28 pt at 144 dpi',font=font,fill='black');combined.paste(canvases[0],(0,25))
d.text((25,735),'AFTER — v1.4    18 pt / 28 pt at 144 dpi',font=font,fill='black');combined.paste(canvases[1],(0,755));combined.save(out/'C4-before-after.png')
