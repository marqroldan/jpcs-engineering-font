from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.ttGlyphPen import TTGlyphPen
from math import atan2, cos, sin, pi
from datetime import datetime
from zoneinfo import ZoneInfo

root = Path(__file__).resolve().parents[1]
build = root / 'build'
build.mkdir(exist_ok=True)
src = root / 'source/jpcs_engring_font.ttf'
out = build / 'JPCS_Engineering_Extended_Draft.ttf'
f=TTFont(src); g=f['glyf']; cmap=f.getBestCmap(); order=f.getGlyphOrder(); h=f['hmtx'].metrics
# Remove empty character mappings so applications can substitute another font.
for t in f['cmap'].tables:
 if t.isUnicode():
  for cp,name in list(t.cmap.items()):
   if cp not in (0x20,0xa0) and g[name].numberOfContours==0: del t.cmap[cp]

def mapglyph(cp,name):
 for t in f['cmap'].tables:
  if t.isUnicode() and (t.format != 4 or cp<=0xffff): t.cmap[cp]=name

def add(cp,paths,width=1150,weight=86):
 name=cmap.get(cp,'uni%04X'%cp)
 p=TTGlyphPen(None)
 def point(x,y): return (round(x+y*.17+90),round(y))
 def capsule(a,b,w):
  ax,ay=point(*a); bx,by=point(*b); angle=atan2(by-ay,bx-ax); r=w/2
  pts=[]
  for i in range(9):
   t=angle+pi/2+pi*i/8; pts.append((round(ax+r*cos(t)),round(ay+r*sin(t))))
  for i in range(9):
   t=angle-pi/2+pi*i/8; pts.append((round(bx+r*cos(t)),round(by+r*sin(t))))
  p.moveTo(pts[0]); [p.lineTo(pt) for pt in pts[1:]]; p.closePath()
 for path in paths:
  for a,b in zip(path,path[1:]): capsule(a,b,weight)
 glyph=p.glyph(); g[name]=glyph
 if name not in order: order.append(name)
 h[name]=(width,80); mapglyph(cp,name)

def alias(cp,source):
 name=cmap[ord(source)] if isinstance(source,str) else source
 mapglyph(cp,name)

def ring(cx,cy,rx,ry,n=20):
 return [(round(cx+rx*cos(2*pi*i/n)),round(cy+ry*sin(2*pi*i/n))) for i in range(n+1)]
def S(ch,paths,w=1150): add(ord(ch),paths,w)
# Engineering punctuation and mathematical operators, drawn as rounded monoline strokes.
S('<',[[(800,1150),(150,700),(800,250)]],1060)
S('>',[[(150,1150),(800,700),(150,250)]],1060)
S('|',[[(250,-100),(250,1500)]],550)
S('^',[[(100,1050),(400,1450),(700,1050)]],850)
S('`',[[(200,1450),(440,1220)]],650)
S('~',[[(100,620),(230,720),(380,720),(560,620),(710,620),(840,720)]],1020)
S('°',[ring(280,1220,180,180)],650)
S('±',[[(100,800),(800,800)],[(450,450),(450,1150)],[(100,220),(800,220)]],1020)
S('×',[[(130,300),(800,1000)],[(130,1000),(800,300)]],1060)
S('÷',[[(100,650),(850,650)],[(475,1010),(475,1030)],[(475,270),(475,290)]],1060)
S('−',[[(100,650),(850,650)]],1060)
S('≤',[[(800,1100),(150,700),(800,300)],[(150,100),(800,100)]],1060)
S('≥',[[(150,1100),(800,700),(150,300)],[(150,100),(800,100)]],1060)
S('≠',[[(100,450),(850,450)],[(100,850),(850,850)],[(260,100),(700,1200)]],1060)
S('≈',[[(100,790),(260,880),(440,880),(610,790),(790,790),(880,850)],[(100,430),(260,520),(440,520),(610,430),(790,430),(880,490)]],1100)
S('∞',[[(100,650),(170,830),(320,900),(480,830),(730,480),(890,410),(1040,480),(1110,650),(1040,830),(890,900),(730,830),(480,480),(320,410),(170,480),(100,650)]],1330)
S('√',[[(60,500),(240,350),(400,50),(720,1450),(1050,1450)]],1250)
S('∆',[[(110,70),(570,1450),(1030,70),(110,70)]],1250)
S('∑',[[(1000,1400),(180,1400),(620,740),(180,70),(1000,70)]],1220)
S('∏',[[(140,70),(140,1400),(980,1400),(980,70)]],1200)
S('∫',[[(800,1500),(650,1510),(550,1430),(350,-170),(260,-250),(110,-230)]],1000)
S('∠',[[(120,100),(320,1000)],[(120,100),(900,100)]],1100)
S('∅',[ring(490,740,390,620),[(100,40),(880,1440)]],1130)
S('⌀',[ring(490,740,390,620),[(100,40),(880,1440)]],1130)
S('∥',[[(200,100),(200,1300)],[(600,100),(600,1300)]],850)
S('⊥',[[(100,120),(900,120)],[(500,120),(500,1300)]],1120)
S('∩',[[(100,120),(100,700),(150,980),(300,1150),(500,1200),(700,1150),(850,980),(900,700),(900,120)]],1100)
S('∪',[[(100,1200),(100,620),(150,340),(300,170),(500,120),(700,170),(850,340),(900,620),(900,1200)]],1100)
S('∴',[[(500,1000),(500,1020)],[(180,300),(180,320)],[(820,300),(820,320)]],1100)
S('∵',[[(180,1000),(180,1020)],[(820,1000),(820,1020)],[(500,300),(500,320)]],1100)
S('→',[[(90,650),(990,650)],[(650,970),(990,650),(650,330)]],1200)
S('←',[[(100,650),(1000,650)],[(440,970),(100,650),(440,330)]],1200)
S('↔',[[(100,650),(1000,650)],[(440,970),(100,650),(440,330)],[(660,970),(1000,650),(660,330)]],1200)
S('↑',[[(500,50),(500,1350)],[(180,1010),(500,1350),(820,1010)]],1100)
S('↓',[[(500,50),(500,1350)],[(180,390),(500,50),(820,390)]],1100)
S('′',[[(250,1400),(130,1050)]],500)
S('″',[[(200,1400),(80,1050)],[(500,1400),(380,1050)]],800)
S('₱',[[(150,50),(150,1400),(550,1400),(750,1300),(800,1100),(750,900),(550,800),(150,800)],[(80,1150),(930,1150)],[(80,950),(930,950)]],1150)
# Greek forms used in engineering; Latin-equivalent capitals reuse the source outlines.
for greek,latin in zip('ΑΒΕΖΗΙΚΜΝΟΡΤΧ','ABEZHIKMNOPTX'): alias(ord(greek),latin)
S('Δ',[[(80,40),(510,1450),(940,40),(80,40)]])
S('Γ',[[(100,40),(100,1450),(850,1450)]])
S('Λ',[[(100,40),(500,1450),(900,40)]])
S('Π',[[(100,40),(100,1450),(900,1450),(900,40)]])
S('Σ',[[(900,1450),(120,1450),(530,740),(120,40),(900,40)]])
S('Φ',[ring(500,740,400,480),[(500,50),(500,1450)]],1200)
S('Θ',[ring(500,740,400,680),[(220,740),(780,740)]],1200)
S('Ω',[[(300,100),(100,100),(100,360),(170,480),(80,730),(100,1080),(250,1350),(500,1450),(750,1350),(900,1080),(920,730),(830,480),(900,360),(900,100),(700,100)]],1200)
S('α',[ring(410,550,320,440),[(800,970),(650,100),(800,70)]],1060)
S('β',[[(150,-300),(150,1080),(220,1330),(370,1450),(570,1450),(720,1310),(750,1120),(650,950),(500,880),(650,850),(790,700),(800,450),(700,220),(500,100),(300,150)]],1000)
S('γ',[[(80,1000),(250,1000),(460,100),(380,-300)],[(800,1000),(460,100)]],1000)
S('δ',[ring(430,470,330,430),[(300,880),(180,1100),(200,1300),(370,1450),(650,1380)]],1030)
S('ε',[[(760,920),(580,1000),(310,980),(150,850),(150,700),(300,550),(580,550)],[(300,550),(140,430),(140,260),(300,100),(580,80),(780,170)]],1000)
S('θ',[ring(430,740,320,690),[(170,740),(690,740)]],1030)
S('λ',[[(100,1450),(310,1400),(710,50)],[(420,800),(100,50)]],900)
S('μ',[[(150,-300),(150,1000)],[(150,480),(200,180),(340,80),(510,90),(680,260)],[(680,1000),(680,250),(750,90),(850,80)]],1060)
alias(ord('µ'),cmap.get(ord('mu'),'mu')) if False else None
mapglyph(ord('µ'),cmap.get(ord('μ'),'mu'))
S('π',[[(80,930),(900,930)],[(300,930),(300,100)],[(700,930),(700,250),(760,100),(900,100)]],1100)
S('ρ',[[(150,-300),(150,550),(200,800),(350,960),(550,980),(740,880),(820,680),(800,400),(680,180),(480,100),(300,140),(150,280)]],1040)
S('σ',[ring(420,520,320,420),[(420,940),(850,940)]],1050)
S('τ',[[(100,930),(900,930)],[(500,930),(500,250),(560,100),(730,100)]],1050)
S('φ',[ring(500,520,390,390),[(500,-280),(500,1050)]],1200)
S('ω',[[(100,900),(100,300),(180,120),(330,100),(490,300),(500,650)],[(500,650),(510,300),(670,100),(820,120),(900,300),(900,900)]],1200)
# Remaining standard Greek alphabet and common notation.
alias(ord('Υ'),'Y')
alias(ord('ο'),'o')
S('Ξ',[[(100,1400),(900,1400)],[(200,740),(800,740)],[(100,80),(900,80)]])
S('Ψ',[[(100,1350),(100,950),(220,740),(500,670),(780,740),(900,950),(900,1350)],[(500,1450),(500,50)]],1200)
S('ζ',[[(100,1320),(800,1320),(140,370),(130,230),(220,120),(650,-70),(700,-200),(610,-300)]],1000)
S('η',[[(130,-300),(130,1000)],[(130,700),(260,930),(420,1000),(610,950),(700,750),(700,-300)]],950)
S('ι',[[(220,1000),(220,250),(280,100),(430,100)]],650)
S('κ',[[(150,100),(150,1000)],[(750,1000),(150,500),(780,100)]],950)
S('ν',[[(80,1000),(330,80),(730,1000)]],920)
S('ξ',[[(750,1350),(550,1450),(300,1400),(180,1270),(200,1100),(370,1000),(650,1000)],[(370,1000),(180,900),(130,720),(210,570),(600,400),(700,250),(650,100),(500,30),(700,-100),(650,-280)]],950)
S('υ',[[(100,1000),(100,420),(170,190),(320,100),(510,120),(680,280),(750,500),(750,1000)]],950)
S('χ',[[(100,1000),(750,-300)],[(760,1000),(100,-300)]],950)
S('ψ',[[(100,1000),(100,500),(180,270),(340,170),(660,170),(820,270),(900,500),(900,1000)],[(500,1050),(500,-300)]],1200)
S('∂',[ring(410,480,320,390),[(690,680),(700,1030),(570,1320),(300,1450),(170,1410)]],1000)
S('∝',[ring(330,650,230,260),[(530,790),(820,450)],[(530,510),(820,850)]],1000)
S('∈',[[(850,1100),(400,1100),(190,980),(100,750),(100,550),(190,320),(400,200),(850,200)],[(130,650),(750,650)]],1050)
S('∉',[[(850,1100),(400,1100),(190,980),(100,750),(100,550),(190,320),(400,200),(850,200)],[(130,650),(750,650)],[(180,100),(850,1250)]],1050)
S('≡',[[(100,1000),(850,1000)],[(100,650),(850,650)],[(100,300),(850,300)]],1050)
S('⊙',[ring(500,720,420,620),[(500,710),(500,730)]],1200)
S('⊕',[ring(500,720,420,620),[(500,300),(500,1140)],[(200,720),(800,720)]],1200)
S('∓',[[(100,1050),(800,1050)],[(100,450),(800,450)],[(450,100),(450,800)]],1020)
S('∼',[[(100,620),(230,720),(380,720),(560,620),(710,620),(840,720)]],1020)
S('∇',[[(110,1400),(1030,1400),(570,50),(110,1400)]],1250)
# Superscript and subscript figures use scaled source numerals, retaining their shapes.
def derived(cp,base,scale,dy):
 name=cmap.get(cp,'uni%04X'%cp); base_name=cmap[ord(base)]; p=TTGlyphPen(g)
 p.addComponent(base_name,(scale,0,0,scale,20,dy)); g[name]=p.glyph()
 if name not in order: order.append(name)
 h[name]=(round(h[base_name][0]*scale+80),20); mapglyph(cp,name)
for i,ch in enumerate('⁰¹²³⁴⁵⁶⁷⁸⁹'): derived(ord(ch),str(i),.52,720)
for i,ch in enumerate('₀₁₂₃₄₅₆₇₈₉'): derived(ord(ch),str(i),.52,-210)
for ch,base in [('₊','+'),('₋','-'),('₌','='),('₍','('),('₎',')')]: derived(ord(ch),base,.52,-210)
# Compose common accented Latin letters with the original drawing and monoline accents.
import unicodedata
accents={0x300:[[(180,220),(360,50)]],0x301:[[(160,50),(350,220)]],0x302:[[(80,50),(250,220),(420,50)]],0x303:[[(70,100),(160,170),(260,170),(350,100),(450,100)]],0x308:[[(130,130),(130,145)],[(370,130),(370,145)]],0x30a:[ring(250,120,95,95)],0x327:[[(250,0),(180,-150),(320,-180)]]}
for mark,paths in accents.items(): add(mark,paths,0,weight=80)
for cp in range(0x00c0,0x0180):
 decomp=unicodedata.normalize('NFD',chr(cp))
 if len(decomp)!=2 or ord(decomp[1]) not in accents or ord(decomp[0]) not in cmap: continue
 base=cmap[ord(decomp[0])]
 if g[base].numberOfContours==0: continue
 mark=ord(decomp[1]); accent='uni%04X'%mark
 name=cmap.get(cp,'uni%04X'%cp); p=TTGlyphPen(g); p.addComponent(base,(1,0,0,1,0,0))
 bounds=g[base]; xmid=(bounds.xMin+bounds.xMax)/2
 # accent shapes already have a small left margin; below marks attach at baseline.
 dx=round(xmid-360); dy=-20 if mark==0x327 else round(bounds.yMax+90)
 p.addComponent(accent,(1,0,0,1,dx,dy)); g[name]=p.glyph()
 if name not in order: order.append(name)
 h[name]=h[base]; mapglyph(cp,name)
f.setGlyphOrder(order)
# Distinct family avoids overwriting the original installed font; retain original copyright.
for n in f['name'].names:
 if n.nameID in (1,4,6,16):
  value={1:'JPCS Engineering Extended Draft',4:'JPCS Engineering Extended Draft',6:'JPCSEngineeringExtendedDraft',16:'JPCS Engineering Extended Draft'}[n.nameID]
  try: n.string=value.encode(n.getEncoding())
  except Exception: pass
 if n.nameID==5:
  try: n.string='Version 1.1 draft'.encode(n.getEncoding())
  except Exception: pass
f['head'].fontRevision=1.1
# Optical pair spacing from actual rasterized outlines at a fixed em size.
# These are starting adjustments; final typography still needs human proofing.
f.save(out)
from PIL import Image, ImageDraw, ImageFont
from fontTools.ttLib import newTable
from fontTools.ttLib.tables._k_e_r_n import KernTable_format_0
font=ImageFont.truetype(out,256)
charset='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789ΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩαβγδεζηθικλμνξοπρστυφχψω'
active_cmap=f.getBestCmap()
profiles={}
for ch in charset:
 im=Image.new('L',(700,450),0); draw=ImageDraw.Draw(im); draw.text((150,290),ch,font=font,fill=255,anchor='ls')
 pix=im.load(); rows={}
 for y in range(450):
  positions=[x for x in range(700) if pix[x,y]>=100]
  if positions: rows[y]=(min(positions)-150,max(positions)-150)
 profiles[ch]=(rows,font.getlength(ch,features=['-kern']))
kern=KernTable_format_0(); kern.version=0; kern.coverage=1; kern.kernTable={}
for a in charset:
 for b in charset:
  pa,advance=profiles[a]; pb,_=profiles[b]
  gaps=sorted(advance+pb[y][0]-pa[y][1]-1 for y in pa.keys() & pb.keys())
  if not gaps: continue
  near=gaps[int((len(gaps)-1)*.15)]
  # target 40/256 em with a safeguard against touching at the closest row
  adjust=max(40-near,20-gaps[0]); adjust=max(-8,min(55,adjust))
  value=round(adjust*8)
  if abs(value)>=16: kern.kernTable[(active_cmap[ord(a)],active_cmap[ord(b)])]=value
kt=newTable('kern'); kt.version=0; kt.kernTables=[kern]; f['kern']=kt
# OpenType GPOS for layout engines that prefer it over legacy kern.
from fontTools.feaLib.builder import addOpenTypeFeaturesFromString
rules='\n'.join('pos %s %s %d;' % (a,b,v) for (a,b),v in kern.kernTable.items())
addOpenTypeFeaturesFromString(f,'feature kern {\n'+rules+'\n} kern;')
f.save(out)
print(datetime.now(ZoneInfo('Asia/Manila')).isoformat(), 'optical kerning pairs',len(kern.kernTable))
print(datetime.now(ZoneInfo('Asia/Manila')).isoformat(), 'saved',out)
