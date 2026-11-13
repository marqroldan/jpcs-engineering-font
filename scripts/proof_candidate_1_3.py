from PIL import Image, ImageDraw, ImageFont, ImageChops
from pathlib import Path
root=Path(__file__).resolve().parents[1] / 'fonts'
out=root.parent/'build'/'proof-1.3'; out.mkdir(parents=True,exist_ok=True)
fonts=[root/'JPCS_Engineering_Font_Improved.ttf',root/'JPCS_Engineering_Font_1_3_Candidate.ttf']
rows=[(18,"Lorem ipsum. V = I × R."),(18,'Lorem ipsum dolor sit amet, consectetur adipiscing elit.'),(18,'E001.   PART-01 / C4   No. 1   2026/01/15'),(18,'0.2   3.14   .5   1.0   12.50   42,000.75'),(18,"A: B; C! D? 'quote'  “curly quote”  A–B  A—B"),(28,'TOPIC SELECTION   IN PROGRESS'),(28,'AVATAR   PART-01   0123456789')]
canvas=[]
for fontpath in fonts:
    im=Image.new('RGB',(1880,840),'white'); d=ImageDraw.Draw(im)
    label=ImageFont.load_default(); d.text((25,10),'18 pt and 28 pt at 144 dpi',font=label,fill='gray')
    y=48
    for pt,s in rows:
        font=ImageFont.truetype(str(fontpath),pt*2,layout_engine=ImageFont.Layout.RAQM)
        d.text((40,y),s,font=font,fill=(20,20,20),features=['kern'])
        y+=94 if pt==18 else 125
    canvas.append(im)
canvas[0].save(out/'proof-before.png');canvas[1].save(out/'proof-candidate.png')
Image.blend(canvas[0],canvas[1],.5).save(out/'proof-overlay.png')
ImageChops.difference(canvas[0],canvas[1]).save(out/'proof-difference.png')
combined=Image.new('RGB',(1880,1720),'white');d=ImageDraw.Draw(combined);d.text((30,5),'BEFORE — improved font',fill='black');combined.paste(canvas[0],(0,25));d.text((30,865),'CANDIDATE — 1.3',fill='black');combined.paste(canvas[1],(0,890));combined.save(out/'proof-before-after.png')
