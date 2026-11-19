#!/usr/bin/env python3
"""Authoring-time illustration renderer. Pillow is not a runtime dependency."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import math
import json
import hashlib

ROOT = Path(__file__).resolve().parents[1]
S = 2
PAPER = '#f5f0e5'
INK = '#152d3c'
MUTED = '#54626a'
RED = '#ad4637'
TEAL = '#1f716f'
GOLD = '#c28a39'
RULE = '#c4beb1'
FONT_DIR = Path('/usr/share/fonts/truetype/liberation')
FONTS = {'body': 'LiberationSans-Regular.ttf', 'bold': 'LiberationSans-Bold.ttf', 'serif': 'LiberationSerif-Bold.ttf'}
image = Image.new('RGB', (1024*S, 1024*S), PAPER)
d = ImageDraw.Draw(image)
boxes = []

def font(size, face='body'):
    return ImageFont.truetype(str(FONT_DIR / FONTS[face]), round(size*S))

def rect(box, fill, outline=None, width=1):
    d.rectangle(tuple(round(v*S) for v in box), fill=fill, outline=outline, width=round(width*S))

def line(points, fill=INK, width=1):
    d.line([(round(x*S), round(y*S)) for x,y in points], fill=fill, width=round(width*S), joint='curve')

def ellipse(box, fill=None, outline=None, width=1):
    d.ellipse(tuple(round(v*S) for v in box), fill=fill, outline=outline, width=round(width*S))

def polygon(points, fill, outline=None):
    d.polygon([(round(x*S), round(y*S)) for x,y in points], fill=fill, outline=outline, width=S)

def text(x,y,value,size=14,face='body',color=INK):
    f=font(size,face)
    d.text((round(x*S),round(y*S)),value,font=f,fill=color,stroke_width=0)
    return d.textlength(value,font=f)/S

def wrapped(value,x,y,w,size,lines=3,face='body',color=INK,leading=1.12):
    for fs in range(size, 11, -1):
        f=font(fs,face);result=[];current=''
        for word in value.split():
            trial=(current+' '+word).strip()
            if d.textlength(trial,font=f) <= w*S:
                current=trial
            else:
                if current:result.append(current)
                current=word
        if current:result.append(current)
        if len(result)<=lines:break
    if len(result)>lines:raise ValueError('Text will not fit: '+value)
    bottom=y+len(result)*fs*leading
    boxes.append({'text':value,'x':x,'y':y,'right':x+w,'bottom':bottom,'font_size':fs})
    for i,v in enumerate(result):text(x,y+i*fs*leading,v,fs,face,color)
    return bottom

def label(x,y,value,color=TEAL):
    text(x,y,value,11,'bold',color)

def star(x,y,r=5,color=GOLD):
    polygon([(x+math.cos(-math.pi/2+i*math.pi/5)*(r if i%2==0 else r*.43),y+math.sin(-math.pi/2+i*math.pi/5)*(r if i%2==0 else r*.43)) for i in range(10)],color)

def skyline(x,y,w,h,color,kind='city'):
    for i in range(10):
        ww=w/11;hh=h*(.3+((i*7)%9)/12)
        rect((x+i*ww,y-hh,x+i*ww+ww*.72,y),color)
        if kind=='city':
            for j in range(2):rect((x+i*ww+3,y-hh+5+j*8,x+i*ww+5,y-hh+7+j*8),PAPER)

def flag(x,y,kind,w=48,h=28):
    if kind=='us':
        rect((x,y,x+w,y+h),'#eee7d8')
        for j in range(0,7,2):rect((x,y+j*h/7,x+w,y+(j+1)*h/7),'#a3473d')
        rect((x,y,x+w*.45,y+h*.56),'#244758')
    elif kind=='china':rect((x,y,x+w,y+h),'#a9493c');star(x+10,y+9,5,'#efcc77')
    elif kind=='russia':
        for j,c in enumerate(['#e8dfd0','#456575','#a44e44']):rect((x,y+j*h/3,x+w,y+(j+1)*h/3),c)
    elif kind=='philippines':
        rect((x,y,x+w,y+h/2),'#35617d');rect((x,y+h/2,x+w,y+h),'#ab4b40');polygon([(x,y),(x+w*.42,y+h/2),(x,y+h)],PAPER);star(x+7,y+h/2,3)
    elif kind=='iran':
        for j,c in enumerate(['#548575',PAPER,'#ad5144']):rect((x,y+j*h/3,x+w,y+(j+1)*h/3),c)

def person(x,y,scale=1,color=INK):
    ellipse((x-5*scale,y-16*scale,x+5*scale,y-6*scale),color)
    polygon([(x-8*scale,y-4*scale),(x+8*scale,y-4*scale),(x+12*scale,y+23*scale),(x-12*scale,y+23*scale)],color)

# A restrained newsroom masthead.
rect((0,0,1024,9),TEAL)
label(28,23,'AN ILLUSTRATED WORLD BRIEF',TEAL)
text(746,23,'12 STORIES / 8 ILLUSTRATIONS',11,'bold',MUTED)
text(25,40,'THE WORLD, TODAY',48,'serif')
text(28,99,'WEDNESDAY 18 NOVEMBER 2026',22,'bold')
text(646,105,'DIPLOMACY / CONFLICT / WORK / DISCOVERY',11,'bold',MUTED)
line([(28,132),(996,132)],INK,3)

# Lead one: a journey, not a claim that tomorrow's summit already happened.
label(28,146,'01 / ASIA-PACIFIC / DIPLOMACY')
wrapped('Trump in Manila, then China',28,164,596,39,2,'serif')
wrapped('Trump meets Marcos, then arrives in China. A first Trump–Xi–Putin trilateral is expected on 19 November.',28,214,590,17,3)
rect((28,285,628,407),'#dce5df')
line([(53,368),(602,368)],'#96aea9',2)
# Manila waterfront and China conference architecture.
skyline(48,364,142,64,'#93aaa3')
polygon([(63,345),(91,318),(119,345)],'#355a62');rect((72,345,110,368),'#355a62')
for xx in [78,89,100]:rect((xx,348,xx+3,367),PAPER)
rect((437,326,593,368),'#355a62');polygon([(423,326),(515,304),(607,326)],'#355a62')
for xx in range(449,588,20):rect((xx,335,xx+5,368),'#dce5df')
# Flight route.
line([(185,335),(242,310),(315,307),(388,327)],TEAL,2)
polygon([(311,298),(340,307),(310,313),(315,307)],INK)
flag(160,370,'philippines',37,22);flag(208,370,'us',37,22)
flag(442,370,'china',37,22);flag(490,370,'russia',37,22)
text(57,382,'MANILA',12,'bold');text(540,382,'SHENZHEN',12,'bold')
text(28,414,'NYT / REUTERS, via Just Security · 18 NOV',10,'bold',MUTED)

# Lead two: source-attributed military claim.
line([(647,147),(647,429)],RULE)
label(668,146,'02 / MIDDLE EAST / IRAN WAR',RED)
wrapped('Gulf bases under fire',668,165,328,32,2,'serif')
# Align the two lead decks; shorten dead bands above the card illustrations.
wrapped('Iran strikes Kuwait and Bahrain; says it targeted a US base after US strikes on Qeshm Island.',668,214,321,17,4)
rect((668,299,996,407),'#e7d9cb')
flag(681,343,'iran',38,23)
line([(737,352),(797,368)],RED,2)
polygon([(794,362),(806,372),(790,371)],RED)
rect((842,366,972,386),'#567078');rect((860,347,876,366),'#567078')
line([(868,348),(868,339)],INK,2);ellipse((853,340,879,345),None,INK,1)
text(683,382,'QESHM → KUWAIT / BAHRAIN',12,'bold',RED)
text(668,414,'REUTERS / WSJ, via Just Security · 18 NOV',10,'bold',MUTED)
line([(28,437),(996,437)],INK,2)

# Six concise illustrated cards, with pictures each meaning something specific.
CARDS=[
 ('03 / EUROPE / UKRAINE','Crimea bridge hit again','Traffic halted after a third attack this week, Russian-installed governor says.','The Guardian · 18 NOV 23:27 GMT','bridge'),
 ('04 / AFRICA / SECURITY','Border war fears rise','Ethiopia and Eritrea amass forces along their shared border, sources say.','Reuters via Just Security · 18 NOV','africa'),
 ('05 / SOUTH ASIA / LABOUR','Workers demand more','Bangladesh garment workers block a highway; at least 30 factories close.','The Daily Star · 18 NOV','labor'),
 ('06 / SPACE / SCIENCE','One light-day away','Voyager 1 reaches a 24-hour radio-signal distance from Earth, CNN reports.','CNN · 18 NOV','space'),
 ('07 / CARIBBEAN / HAITI','Gang stronghold hit','Salvadoran forces destroy a Haitian gang leader’s house in Canaan.','AP via Current Events · 18 NOV','haiti'),
 ('08 / OCEANIA / CULTURE','Artists push back on AI','At Australia’s ARIAs, Elton John backs artists seeking consent and payment.','The Guardian · 18 NOV','arts')
]

def scene(kind,x,y,w=304,h=63):
    rect((x,y,x+w,y+h),'#e5e3d7')
    if kind=='bridge':
        rect((x,y+41,x+w,y+h),'#a7bdbe')
        for xx in [20,75,175,230,285]:rect((x+xx,y+22,x+xx+7,y+58),'#55727b')
        line([(x+8,y+29),(x+112,y+29)],INK,6);line([(x+144,y+29),(x+w-8,y+29)],INK,6)
        line([(x+112,y+29),(x+125,y+44)],RED,4)
        for xx in [43,204]:line([(x+xx,y+24),(x+xx+28,y+10),(x+xx+58,y+24)],INK,2)
        text(x+146,y+46,'KERCH STRAIT',10,'bold',INK)
    elif kind=='africa':
        polygon([(x+107,y+6),(x+151,y+5),(x+174,y+18),(x+209,y+17),(x+183,y+35),(x+159,y+54),(x+134,y+54),(x+118,y+33)],'#8fa59a')
        line([(x+111,y+26),(x+155,y+30),(x+177,y+22)],RED,3)
        text(x+8,y+10,'ERITREA',11,'bold');text(x+195,y+42,'ETHIOPIA',11,'bold')
        for xx,yy in [(97,17),(187,38)]:
            rect((x+xx,y+yy,x+xx+20,y+yy+6),INK);ellipse((x+xx,y+yy+5,x+xx+20,y+yy+12),INK)
            line([(x+xx+8,y+yy),(x+xx+24,y+yy-3)],INK,2)
    elif kind=='labor':
        skyline(x+4,y+49,120,36,'#9ba69a','factory')
        for xx in [154,185,215,246]:person(x+xx,y+39,.6)
        line([(x+162,y+46),(x+162,y+7)],INK,2);rect((x+138,y+4,x+187,y+23),TEAL)
        text(x+141,y+7,'FAIR PAY',10,'bold',PAPER)
    elif kind=='space':
        rect((x,y,x+w,y+h),INK)
        for xx,yy in [(12,10),(77,18),(123,9),(162,49),(261,11),(285,46)]:ellipse((x+xx,y+yy,x+xx+1,y+yy+1),PAPER)
        ellipse((x+17,y+26,x+46,y+55),'#7da7aa')
        line([(x+53,y+40),(x+225,y+40)],'#cbbd97',1)
        text(x+86,y+18,'24 h / one way',14,'bold',PAPER)
        ellipse((x+239,y+15,x+263,y+44),'#d8c89f',PAPER)
        line([(x+252,y+29),(x+279,y+51)],PAPER,2)
        line([(x+253,y+30),(x+281,y+12)],PAPER,1)
    elif kind=='haiti':
        skyline(x+8,y+55,90,43,'#a3aea0')
        polygon([(x+136,y+28),(x+179,y+8),(x+218,y+28)],'#657a75')
        rect((x+144,y+28,x+209,y+55),'#84968c')
        polygon([(x+172,y+23),(x+166,y+35),(x+180,y+38),(x+170,y+55)],PAPER)
        line([(x+216,y+54),(x+230,y+47),(x+240,y+55),(x+252,y+50)],INK,2)
        text(x+9,y+8,'CANAAN',11,'bold')
    elif kind=='arts':
        for xx in [30,65,100]:
            ellipse((x+xx,y+13,x+xx+10,y+29),TEAL)
            line([(x+xx+9,y+17),(x+xx+9,y+4),(x+xx+20,y+2)],TEAL,2)
        rect((x+151,y+10,x+200,y+52),INK)
        text(x+158,y+16,'AI',25,'bold',PAPER)
        ellipse((x+230,y+8,x+281,y+57),None,RED,3)
        text(x+243,y+13,'©',28,'bold',RED)
for i,(k,head,body,source,kind) in enumerate(CARDS):
    rr,cc=divmod(i,3);x=28+cc*330;y=452+rr*211
    label(x,y,k,TEAL if i%3 else RED)
    bottom=wrapped(head,x,y+18,306,26,2,'serif')
    # The fixed scene box starts nearer the single-line headline.
    scene(kind,x,y+63,h=80)
    wrapped(body,x,y+149,305,16,3)
    text(x,y+198,source,9,'bold',MUTED)
    if cc<2:line([(x+318,y),(x+318,y+203)],RULE)
line([(28,879),(996,879)],INK,2)
label(28,890,'ALSO REPORTED ON 18 NOVEMBER',TEAL)
BRIEFS=[
 ('SOUTH ASIA / HEALTH','Winter smog grips cities; Al Jazeera details the health risks.'),
 ('US / DIPLOMACY','Carney announces Trump meeting at APEC over trade. [NYT / JS]'),
 ('GAZA / CONFLICT','Israel launches a central-Gaza operation as families flee. [BBC]'),
 ('US / MARKETS','Anthropic prices IPO shares at $83; trading due Thursday. [NYT]')
]
for i,(tag,body) in enumerate(BRIEFS):
    rr,cc=divmod(i,2);x=28+cc*494;y=908+rr*39
    text(x,y,tag,10,'bold',TEAL)
    wrapped(body,x,y+12,468,13,2)
line([(28,991),(996,991)],RULE)
text(28,998,'Sources dated 18 Nov unless noted · JS = Just Security daily brief · Original schematic illustrations',10,'body',MUTED)
assert len(CARDS)+len(BRIEFS)+2 == 12
image=image.resize((1024,1024),Image.Resampling.LANCZOS)
image.save(ROOT/'entry.png',optimize=True)
preview=image.resize((300,300),Image.Resampling.LANCZOS)
preview.save(ROOT/'preview-300.png',optimize=True)
(ROOT/'layout-audit.json').write_text(json.dumps(boxes,indent=2)+'\n')
b=(ROOT/'entry.png').read_bytes()
assert len(b)<=1048576
print(json.dumps({'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'dimensions':[1024,1024],'stories':12,'illustrations':8}))
