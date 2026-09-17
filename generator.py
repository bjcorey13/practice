#!/usr/bin/env python3
"""
generator.py — PDF layout engine. Imports from drills, diagrams, tags.
This file never needs to change when you add drills.

USAGE:
  python generator.py "Theme" "id:mins,id:mins,..."
  e.g. python generator.py "Situational Day" "33:12,34:12,36:8"

  Or import:
  from generator import generate_practice_plan
  generate_practice_plan("Theme", [(33,12),(34,12)], "output.pdf")

LAYOUT AUTO-DETECTION:
  1-4 drills  -> 2x2, empty slots = notes blocks
  5-6 drills  -> 2x3 single page, empty slot = notes block
  7+ drills   -> 2x2 multi-page, empty slots on last page = notes blocks

OUTPUT: /mnt/user-data/outputs/wrentham_practice_plan.pdf (or custom path)

RESTORE AFTER CONTAINER RESET:
  pip install reportlab --break-system-packages -q
  curl -sO https://raw.githubusercontent.com/bjcorey13/practice/main/drills.py
  curl -sO https://raw.githubusercontent.com/bjcorey13/practice/main/diagrams.py
  curl -sO https://raw.githubusercontent.com/bjcorey13/practice/main/tags.py
  curl -sO https://raw.githubusercontent.com/bjcorey13/practice/main/generator.py
"""

import sys, math
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, white
from reportlab.lib.units import inch
from reportlab.pdfbase.pdfmetrics import stringWidth

from drills import DRILLS, CAT_COLORS
from diagrams import draw_diagram
from tags import DRILL_TAGS, SLOT_COLORS, TYPE_COLORS

CAT_LABELS = {
    "infield":"INFIELD","outfield":"OUTFIELD","throwing":"THROWING",
    "situational":"SITUATIONAL","baserunning":"BASERUNNING","hitting":"HITTING",
    "catching":"CATCHING","pitching":"PITCHING",
}

def generate_practice_plan(theme, drill_ids_times, output_path):
    PAGE_W, PAGE_H = letter
    MARGIN = 0.45 * inch
    HEADER_H = 60
    WARMUP_H = 28
    CARD_MARGIN = 8
    BOTTOM_PAD = 8
    total_mins = sum(t for _,t in drill_ids_times) + 10
    n = len(drill_ids_times)
    c = canvas.Canvas(output_path, pagesize=letter)

    def wt(text, fn, fs, mw):
        words=text.split(); lines=[]; cur=""
        for word in words:
            t=(cur+" "+word).strip()
            if stringWidth(t,fn,fs)<=mw: cur=t
            else:
                if cur: lines.append(cur)
                cur=word
        if cur: lines.append(cur)
        return lines

    def draw_header(pn):
        c.setFillColor(HexColor("#132448")); c.rect(0,PAGE_H-HEADER_H,PAGE_W,HEADER_H,fill=1,stroke=0)
        c.setFillColor(white); c.setFont("Helvetica-Bold",16); c.drawString(MARGIN,PAGE_H-28,"WRENTHAM 10/9U")
        c.setFillColor(HexColor("#A8B8CC")); c.setFont("Helvetica",10); c.drawString(MARGIN,PAGE_H-46,theme)
        c.setFont("Helvetica",9); c.drawRightString(PAGE_W-MARGIN,PAGE_H-28,f"{total_mins} MIN  |  {n} DRILLS  |  PAGE {pn}")

    def draw_warmup(wx,wy,ww,wh):
        c.setFillColor(HexColor("#EAF3DE")); c.roundRect(wx,wy,ww,wh,5,fill=1,stroke=0)
        c.setFillColor(HexColor("#27500A")); c.setFont("Helvetica-Bold",9); c.drawString(wx+10,wy+wh-14,"WARMUP (10 MIN)")
        c.setFont("Helvetica",8); c.drawString(wx+10,wy+wh-26,"Dynamic stretch  |  Arm circles  |  Light toss pairs")

    def draw_notes(nx,ny,nw,nh):
        c.setFillColor(HexColor("#FAFBFC")); c.setStrokeColor(HexColor("#DDE2EA")); c.setLineWidth(0.5)
        c.roundRect(nx,ny,nw,nh,6,fill=1,stroke=1)
        HDR=22; c.setFillColor(HexColor("#4A5568"))
        p=c.beginPath(); p.moveTo(nx+6,ny+nh); p.lineTo(nx+nw-6,ny+nh)
        p.arcTo(nx+nw-12,ny+nh-12,nx+nw,ny+nh,0,90); p.lineTo(nx+nw,ny+nh-HDR); p.lineTo(nx,ny+nh-HDR)
        p.arcTo(nx,ny+nh-12,nx+12,ny+nh,90,90); p.close(); c.drawPath(p,fill=1,stroke=0)
        c.setFillColor(white); c.setFont("Helvetica-Bold",9); c.drawString(nx+10,ny+nh-14,"NOTES")
        ly=ny+nh-HDR-18; c.setStrokeColor(HexColor("#DDE2EA")); c.setLineWidth(0.5)
        while ly>ny+8: c.line(nx+10,ly,nx+nw-10,ly); ly-=18

    def draw_card(did,mins,cx_card,cy_card,cw,ch):
        drill=DRILLS[did]; cat=drill["cat"]; color=HexColor(CAT_COLORS[cat])
        radius=6; TP=10; TW=cw-TP*2
        c.setFillColor(white); c.setStrokeColor(HexColor("#DDE2EA")); c.setLineWidth(0.5)
        c.roundRect(cx_card,cy_card,cw,ch,radius,fill=1,stroke=1)
        HDR=22; c.setFillColor(color)
        p=c.beginPath(); p.moveTo(cx_card+radius,cy_card+ch); p.lineTo(cx_card+cw-radius,cy_card+ch)
        p.arcTo(cx_card+cw-2*radius,cy_card+ch-2*radius,cx_card+cw,cy_card+ch,0,90)
        p.lineTo(cx_card+cw,cy_card+ch-HDR); p.lineTo(cx_card,cy_card+ch-HDR)
        p.arcTo(cx_card,cy_card+ch-2*radius,cx_card+2*radius,cy_card+ch,90,90); p.close(); c.drawPath(p,fill=1,stroke=0)
        br=8; c.setFillColor(white); c.setLineWidth(0); c.circle(cx_card+cw-br-6,cy_card+ch-HDR/2,br,fill=1,stroke=0)
        c.setFillColor(HexColor("#132448")); c.setFont("Helvetica-Bold",8)
        c.drawCentredString(cx_card+cw-br-6,cy_card+ch-HDR/2-3,str(did))
        c.setFillColor(white); c.setFont("Helvetica-Bold",9)
        c.drawString(cx_card+8,cy_card+ch-14,wt(drill["name"].upper(),"Helvetica-Bold",9,cw-br*2-20)[0])
        ty=cy_card+ch-HDR-13; c.setFillColor(color); c.setFont("Helvetica-Bold",7)
        c.drawString(cx_card+TP,ty,CAT_LABELS.get(cat,cat.upper()))
        if drill["game"]:
            gw=48; c.setFillColor(white); c.setStrokeColor(white)
            c.roundRect(cx_card+cw-gw-6,ty-2,gw,12,3,fill=1,stroke=0)
            c.setFillColor(HexColor("#132448")); c.setFont("Helvetica-Bold",6.5)
            c.drawCentredString(cx_card+cw-gw/2-6,ty+2,"GAME-BASED")

        def draw_pill(lbl,px,py,cp,bold=False):
            bg,fg=cp; fn="Helvetica-Bold" if bold else "Helvetica"; SZ=8
            tw=stringWidth(lbl,fn,SZ); pw=tw+12; ph=13
            c.setFillColor(HexColor(bg)); c.roundRect(px,py,pw,ph,3,fill=1,stroke=0)
            c.setFillColor(HexColor(fg)); c.setFont(fn,SZ); c.drawString(px+6,py+3.5,lbl)
            return pw

        tags=DRILL_TAGS.get(did,("Skill Block",None,"Individual Skill",None))
        ps,as_,pt,at=tags
        r1y=ty-18; xc=cx_card+TP; pw=draw_pill(ps,xc,r1y,SLOT_COLORS[ps],bold=True)
        if as_: xc+=pw+4; draw_pill(as_,xc,r1y,SLOT_COLORS[as_])
        xc=cx_card+TP; r2y=r1y-17; pw=draw_pill(pt,xc,r2y,TYPE_COLORS[pt],bold=True)
        if at: xc+=pw+4; draw_pill(at,xc,r2y,TYPE_COLORS[at])

        dh=ch*0.30; dy=cy_card+ch-HDR-15-28-dh
        draw_diagram(c,cx_card+4,dy,cw-8,dh,did)

        desc_y=dy-12; c.setFillColor(HexColor("#444444")); c.setFont("Helvetica",7)
        for text in [drill["desc1"],drill["desc2"]]:
            for line in wt(text,"Helvetica",7,TW): c.drawString(cx_card+TP,desc_y,line); desc_y-=9
        cy2=desc_y-8; c.setFillColor(HexColor("#132448")); c.setFont("Helvetica-Bold",7)
        c.drawString(cx_card+TP,cy2,"COACHING CUES"); c.setFont("Helvetica",7)
        c.setFillColor(HexColor("#333333")); cy2-=9
        for cue in drill["cues"][:3]:
            for line in wt(f"\u2022  {cue}","Helvetica",7,TW): c.drawString(cx_card+TP,cy2,line); cy2-=9

    content_top=PAGE_H-HEADER_H-8
    warmup_y=content_top-WARMUP_H
    col_w=(PAGE_W-2*MARGIN-CARD_MARGIN)/2

    if 5<=n<=6:
        ROWS=3; avail_h=warmup_y-BOTTOM_PAD-CARD_MARGIN; card_h=(avail_h-2*CARD_MARGIN)/ROWS
        draw_header(1); draw_warmup(MARGIN,warmup_y,PAGE_W-2*MARGIN,WARMUP_H)
        all_pos=[(MARGIN+col*(col_w+CARD_MARGIN), warmup_y-CARD_MARGIN-(row+1)*(card_h+CARD_MARGIN)+CARD_MARGIN)
                 for row in range(ROWS) for col in range(2)]
        for i,(did,mins) in enumerate(drill_ids_times): draw_card(did,mins,*all_pos[i],col_w,card_h)
        for i in range(n,ROWS*2): draw_notes(*all_pos[i],col_w,card_h)
    else:
        avail_h=warmup_y-BOTTOM_PAD-CARD_MARGIN; card_h=(avail_h-CARD_MARGIN)/2
        full_h=(content_top-BOTTOM_PAD-CARD_MARGIN*2)/2
        pn=1; draw_header(pn); draw_warmup(MARGIN,warmup_y,PAGE_W-2*MARGIN,WARMUP_H)
        p1=[(MARGIN+col*(col_w+CARD_MARGIN), warmup_y-CARD_MARGIN-(row+1)*(card_h+CARD_MARGIN)+CARD_MARGIN)
            for row in range(2) for col in range(2)]
        ex=[(MARGIN+col*(col_w+CARD_MARGIN), content_top-CARD_MARGIN-(row+1)*(full_h+CARD_MARGIN)+CARD_MARGIN)
            for row in range(2) for col in range(2)]
        for i,(did,mins) in enumerate(drill_ids_times):
            if i<4: draw_card(did,mins,*p1[i],col_w,card_h)
            else:
                pp=i-4
                if pp%4==0: c.showPage(); pn+=1; draw_header(pn)
                draw_card(did,mins,*ex[pp%4],col_w,full_h)
        if n<=4:
            for s in range(n,4): draw_notes(*p1[s],col_w,card_h)
        else:
            lf=(n-4)%4
            if lf: 
                for s in range(lf,4): draw_notes(*ex[s],col_w,full_h)
    c.save()

if __name__=="__main__":
    if len(sys.argv)>=3:
        pairs=sys.argv[2].split(",")
        drill_list=[(int(p.split(":")[0]),int(p.split(":")[1])) for p in pairs]
        generate_practice_plan(sys.argv[1],drill_list,"/mnt/user-data/outputs/wrentham_practice_plan.pdf")
    else:
        generate_practice_plan("Smoke Test",[(26,10),(20,12),(33,12),(47,10),(36,10),(4,10)],"/mnt/user-data/outputs/wrentham_practice_plan.pdf")
