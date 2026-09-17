#!/usr/bin/env python3
"""
diagrams.py — draw_diagram function for all 110 drills.
Imports nothing from drills.py or tags.py.
Called by generator.py with: draw_diagram(c, x, y, w, h, drill_id)
To add a new drill diagram: add one elif block before the final else clause.
"""
import math
from reportlab.lib.colors import HexColor, white

def draw_diagram(c, x, y, w, h, drill_id):
    cx=x+w/2; cy=y+h/2
    NAVY=HexColor("#132448"); GREEN=HexColor("#1A6B3C"); AMBER=HexColor("#C47D0E")
    RED=HexColor("#B31B1B"); PURPLE=HexColor("#534AB7"); PINK=HexColor("#993556")
    GRAY=HexColor("#999999"); LGRAY=HexColor("#CCCCCC"); DIRT=HexColor("#E8D5B0")
    GRASS=HexColor("#D4EDDA"); DKGRASS=HexColor("#A8D5B5")
    BASE_CLR=HexColor("#F5F0E0"); HOME_CLR=HexColor("#EEEEEE"); CHALK=HexColor("#FFFFFF")
    c.saveState()
    c.setFillColor(HexColor("#F7F9FC")); c.rect(x,y,w,h,fill=1,stroke=0)

    def dmd(scale=1.0):
        r=min(w,h)*0.36*scale
        c.setFillColor(GRASS)
        pts=[(cx,cy+r),(cx+r,cy),(cx,cy-r),(cx-r,cy)]
        p=c.beginPath(); p.moveTo(*pts[0])
        for pt in pts[1:]: p.lineTo(*pt)
        p.close(); c.drawPath(p,fill=1,stroke=0)
        c.setFillColor(DIRT); c.circle(cx,cy-r*0.1,r*0.72,fill=1,stroke=0)
        c.setFillColor(GRASS)
        p=c.beginPath(); p.moveTo(*pts[0])
        for pt in pts[1:]: p.lineTo(*pt)
        p.close(); c.drawPath(p,fill=1,stroke=0)
        c.setStrokeColor(CHALK); c.setLineWidth(0.7)
        c.line(cx,cy-r,cx-r*1.5,cy-r*2.5); c.line(cx,cy-r,cx+r*1.5,cy-r*2.5)
        c.setStrokeColor(HexColor("#C0AA80")); c.setLineWidth(0.5)
        p2=[(cx,cy+r),(cx+r,cy),(cx,cy-r),(cx-r,cy),(cx,cy+r)]
        for i in range(4): c.line(p2[i][0],p2[i][1],p2[i+1][0],p2[i+1][1])
        return r

    def bp(r): return {"2B":(cx,cy+r),"1B":(cx+r,cy),"HM":(cx,cy-r),"3B":(cx-r,cy),"P":(cx,cy-r*0.35)}

    def base(bx,by,sz=7,is_home=False):
        if is_home:
            s=sz*0.8; p=c.beginPath(); p.moveTo(bx-s,by+s*0.4); p.lineTo(bx+s,by+s*0.4)
            p.lineTo(bx+s,by-s*0.3); p.lineTo(bx,by-s*0.9); p.lineTo(bx-s,by-s*0.3); p.close()
            c.setFillColor(HOME_CLR); c.setStrokeColor(LGRAY); c.setLineWidth(0.8); c.drawPath(p,fill=1,stroke=1)
        else:
            c.setFillColor(BASE_CLR); c.setStrokeColor(NAVY); c.setLineWidth(0.8); c.rect(bx-sz/2,by-sz/2,sz,sz,fill=1,stroke=1)

    def bases(r):
        b=bp(r)
        for n,(bx,by) in b.items(): base(bx,by,is_home=(n=="HM"))
        return b

    def dot(px,py,col=NAVY,r=5,lbl="",above=False):
        c.setFillColor(col); c.setStrokeColor(CHALK); c.setLineWidth(0.5); c.circle(px,py,r,fill=1,stroke=1)
        if lbl:
            c.setFillColor(col); c.setFont("Helvetica-Bold",6)
            c.drawCentredString(px,py+(r+4 if above else -(r+6)),lbl)

    def ball(bx,by,r=3.5):
        c.setFillColor(CHALK); c.setStrokeColor(HexColor("#CC4444")); c.setLineWidth(0.8); c.circle(bx,by,r,fill=1,stroke=1)

    def ah(x1,y1,x2,y2,col,wd):
        ang=math.atan2(y2-y1,x2-x1); al=max(5,wd*3.5); sp=0.42
        c.setFillColor(col); p=c.beginPath(); p.moveTo(x2,y2)
        p.lineTo(x2-al*math.cos(ang-sp),y2-al*math.sin(ang-sp))
        p.lineTo(x2-al*math.cos(ang+sp),y2-al*math.sin(ang+sp))
        p.close(); c.drawPath(p,fill=1,stroke=0)

    def arr(x1,y1,x2,y2,col=AMBER,wd=1.5,dash=False):
        c.setStrokeColor(col); c.setLineWidth(wd)
        if dash: c.setDash(4,3)
        c.line(x1,y1,x2,y2); c.setDash()
        dx=x2-x1; dy=y2-y1; dist=math.sqrt(dx*dx+dy*dy) or 1
        ah(x2-dx/dist*3,y2-dy/dist*3,x2,y2,col,wd)

    def bounce(x1,y1,x2,y2,n=2,col=AMBER,wd=1.5):
        dx=x2-x1; dy=y2-y1; dist=math.sqrt(dx*dx+dy*dy) or 1
        s=n+1; sdx=dx/s; sdy=dy/s; hh=min(dist*0.18,h*0.18)
        c.setStrokeColor(col); c.setLineWidth(wd)
        for i in range(s):
            sx=x1+i*sdx; sy=y1+i*sdy; ex=sx+sdx; ey=sy+sdy
            mx=(sx+ex)/2; my=(sy+ey)/2
            px2=-sdy/s; py2=sdx/s; mag=math.sqrt(px2**2+py2**2) or 1
            ax=mx+(px2/mag)*hh*(1-i*0.3); ay=my+(py2/mag)*hh*(1-i*0.3)
            p=c.beginPath(); p.moveTo(sx,sy)
            p.curveTo(sx+(ax-sx)*0.5,sy+(ay-sy)*0.5,ax,ay,ex,ey); c.drawPath(p,fill=0,stroke=1)
        ah(x2-dx/dist*3,y2-dy/dist*3,x2,y2,col,wd)

    def arc(x1,y1,x2,y2,col=AMBER,wd=1.5,hf=0.35):
        mx=(x1+x2)/2; my=(y1+y2)/2; ah2=math.sqrt((x2-x1)**2+(y2-y1)**2)*hf
        p=c.beginPath(); c.setStrokeColor(col); c.setLineWidth(wd)
        p.moveTo(x1,y1); p.curveTo(x1+(mx-x1)*0.5,y1+(my+ah2-y1)*0.5,mx,my+ah2,x2,y2)
        c.drawPath(p,fill=0,stroke=1)
        dx=x2-x1; dy=y2-y1; dist=math.sqrt(dx*dx+dy*dy) or 1
        ah(x2-dx/dist*3,y2-dy/dist*3,x2,y2,col,wd)

    def dash(x1,y1,x2,y2,col=GRAY,wd=1.0,dk=(3,3)):
        c.setStrokeColor(col); c.setLineWidth(wd); c.setDash(*dk); c.line(x1,y1,x2,y2); c.setDash()

    def route(pts,col=GREEN,wd=1.8):
        c.setStrokeColor(col); c.setLineWidth(wd)
        p=c.beginPath(); p.moveTo(*pts[0])
        for pt in pts[1:]: p.lineTo(*pt)
        c.drawPath(p,fill=0,stroke=1)
        x1,y1=pts[-2]; x2,y2=pts[-1]; dx=x2-x1; dy=y2-y1; dist=math.sqrt(dx*dx+dy*dy) or 1
        ah(x2-dx/dist*3,y2-dy/dist*3,x2,y2,col,wd)

    def lbl(txt,lx,ly,sz=6,col=NAVY,bold=False):
        c.setFillColor(col); c.setFont("Helvetica-Bold" if bold else "Helvetica",sz); c.drawCentredString(lx,ly,txt)

    def box(txt,lx,ly,sz=6,bg=NAVY,fg=CHALK):
        from reportlab.pdfbase.pdfmetrics import stringWidth
        tw=stringWidth(txt,"Helvetica-Bold",sz); pad=3
        c.setFillColor(bg); c.roundRect(lx-tw/2-pad,ly-1,tw+pad*2,sz+3,2,fill=1,stroke=0)
        c.setFillColor(fg); c.setFont("Helvetica-Bold",sz); c.drawCentredString(lx,ly+1,txt)

    def ofbg():
        c.setFillColor(DKGRASS)
        p=c.beginPath(); p.moveTo(x,y+h*0.35); p.arcTo(x-w*0.1,y+h*0.05,x+w*1.1,y+h*1.15,160,-140); p.close(); c.drawPath(p,fill=1,stroke=0)
        c.setFillColor(GRASS)
        p=c.beginPath(); p.moveTo(x,y+h*0.35); p.arcTo(x+w*0.05,y+h*0.15,x+w*0.95,y+h*0.95,155,-130); p.close(); c.drawPath(p,fill=1,stroke=0)

    def hitbg():
        c.setFillColor(DIRT); c.circle(cx,cy,min(w,h)*0.45,fill=1,stroke=0)
        c.setFillColor(GRASS); bw,bh=w*0.18,h*0.32
        c.rect(cx-bw*1.8,cy-bh/2,bw,bh,fill=1,stroke=0); c.rect(cx+bw*0.8,cy-bh/2,bw,bh,fill=1,stroke=0)

    if drill_id==1:
        r=dmd(); b=bases(r); coach_x,coach_y=cx-r*0.35,cy+r*0.2; dot(coach_x,coach_y,RED,lbl="C",above=True)
        fx,fy=cx+r*0.1,cy+r*0.45; dot(fx,fy,NAVY,lbl="F",above=True); bounce(coach_x,coach_y-5,fx,fy+5,2,AMBER); box("SHORT HOP",cx,cy-r*0.6,6,NAVY)
    elif drill_id==2:
        r=dmd(); b=bases(r); dot(cx,cy-r*0.1,RED,lbl="COACH",above=True)
        for (fx,fy),lb in [((cx-r*0.45,cy+r*0.2),"SS"),((cx+r*0.35,cy+r*0.2),"2B"),((cx-r*0.7,cy-r*0.1),"3B")]:
            dot(fx,fy,NAVY,lbl=lb,above=True); bounce(cx,cy-r*0.06,fx,fy,1,AMBER,1.2)
    elif drill_id==3:
        r=dmd(); b=bases(r); order=["HM","1B","2B","3B","HM"]; cols=[AMBER,GREEN,PURPLE,RED]
        for i in range(4):
            x1,y1=b[order[i]]; x2,y2=b[order[i+1]]; dx=x2-x1; dy=y2-y1; dist=math.sqrt(dx*dx+dy*dy) or 1
            arr(x1+dx/dist*9,y1+dy/dist*9,x2-dx/dist*9,y2-dy/dist*9,cols[i],1.8)
        box("RACE THE CLOCK",cx,cy-r*1.1,6,NAVY)
    elif drill_id==4:
        r=dmd(); b=bases(r); hx,hy=b["HM"]; c.setFillColor(RED); c.roundRect(hx-10,hy+8,20,16,3,fill=1,stroke=0)
        lbl("TARGET",hx,hy+14,5.5,CHALK,True); px2,py2=b["P"]; dot(px2,py2,NAVY,lbl="P1",above=True)
        for i,off in enumerate([(0,-14),(0,-24),(0,-34)]): dot(px2+off[0],py2+off[1],NAVY if i==0 else LGRAY,r=4)
        arr(px2,py2-5,hx,hy+10,AMBER,2); box("LINE UP — THROW — ELIMINATE",cx,y+6,5.5,RED)
    elif drill_id==5:
        ofbg(); dot(cx,cy+h*0.05,NAVY,lbl="OF"); route([(cx,cy+h*0.05),(cx-8,cy+h*0.05-8),(cx-22,cy+h*0.05+28)],GREEN,2)
        arc(cx-w*0.25,cy-h*0.3,cx-w*0.22,cy+h*0.38,AMBER,1.5,0.3); ball(cx-w*0.22,cy+h*0.38); box("DROP STEP — RUN TO SPOT",cx,y+5,5.5,GREEN)
    elif drill_id==6:
        r=dmd(); b=bases(r); dot(b["3B"][0]+8,b["3B"][1],PINK,lbl="R",above=True)
        ball_x,ball_y=cx+r*0.3,cy+r*0.55; ball(ball_x,ball_y)
        of_x,of_y=cx+r*0.85,cy+r*0.85; dot(of_x,of_y,GREEN,lbl="OF",above=True)
        arr(of_x,of_y,ball_x+4,ball_y+4,GREEN,2); hx,hy=b["HM"]; arr(ball_x,ball_y,hx+4,hy+6,AMBER,2)
        arr(b["3B"][0],b["3B"][1],hx-6,hy+4,PINK,1.5,True); box("CHARGE — FIELD — THROW HOME",cx,y+5,5.5,RED)
    elif drill_id==7:
        r=dmd(); b=bases(r); of_x,of_y=cx-r*0.5,cy+r*1.45; dot(of_x,of_y,GREEN,lbl="OF",above=True)
        cut_x,cut_y=cx-r*0.25,cy+r*0.55; dot(cut_x,cut_y,NAVY,lbl="SS",above=True)
        hx,hy=b["HM"]; arr(of_x,of_y-6,cut_x,cut_y+6,AMBER,2); arr(cut_x,cut_y-6,hx,hy+8,RED,2)
        lbl("HANDS UP",cut_x+14,cut_y+10,5.5,NAVY,True); box("OF > CUT > HOME — TWO THROWS",cx,y+5,5.5,NAVY)
    elif drill_id==8:
        r=dmd(); b=bases(r); ss_x,ss_y=cx-r*0.5,cy+r*0.25; dot(ss_x,ss_y,NAVY,lbl="SS",above=True)
        b2x,b2y=b["2B"]; dot(b2x+10,b2y-6,PURPLE,lbl="2B",above=True); b1x,b1y=b["1B"]; dot(b1x+6,b1y+6,GREEN,lbl="1B",above=True)
        arr(ss_x+5,ss_y+3,b2x+7,b2y-4,AMBER,2); arr(b2x+12,b2y-6,b1x+3,b1y+5,RED,2)
        c.setStrokeColor(PURPLE); c.setLineWidth(1); c.arc(b2x+2,b2y-14,b2x+20,b2y+4,30,150)
        lbl("PIVOT",b2x+20,b2y-10,5.5,PURPLE,True); box("FEED > PIVOT > THROW 1B",cx,y+5,5.5,NAVY)
    elif drill_id==9:
        c.setFillColor(GRASS); c.rect(x,y,w,h,fill=1,stroke=0)
        p1x,p1y=cx-w*0.32,cy; p2x,p2y=cx+w*0.32,cy
        dot(p1x,p1y,NAVY,lbl="P1",above=True); dot(p2x,p2y,GREEN,lbl="P2",above=True)
        hop_x=p1x+w*0.1; c.setFillColor(AMBER); c.circle(p1x+w*0.06,p1y,3,fill=1,stroke=0)
        c.setStrokeColor(AMBER); c.setLineWidth(1.5)
        p=c.beginPath(); p.moveTo(p1x+5,p1y); p.curveTo(p1x+12,p1y+12,hop_x+4,p1y+12,hop_x+8,p1y); c.drawPath(p,fill=0,stroke=1)
        arr(hop_x+10,p1y,p2x-6,p2y,AMBER,2); dash(cx,cy-h*0.35,cx,cy+h*0.35,GRAY,0.8,(4,4))
        lbl("40-50 FT",cx,cy-h*0.38,6,GRAY); box("GATHER — HOP — THROW",cx,y+5,5.5,HexColor("#854F0B"))
    elif drill_id==10:
        ofbg(); dot(cx,cy+h*0.05,NAVY,lbl="OF")
        arr(cx,cy+h*0.05,cx-w*0.28,cy+h*0.05+h*0.32,GREEN,1.5)
        arr(cx,cy+h*0.05,cx+w*0.28,cy+h*0.05+h*0.32,GREEN,1.5)
        arr(cx,cy+h*0.05,cx,cy+h*0.05-h*0.28,AMBER,1.5)
        dot(cx,cy-h*0.38,RED,lbl="COACH"); box("READ — REACT — FIRST STEP",cx,y+5,5.5,GREEN)
    elif drill_id==11:
        r=dmd(); b=bases(r); r1x,r1y=b["1B"]; r2x,r2y=b["2B"]
        dot(r1x+12,r1y,NAVY,lbl="F1",above=True); dot(r2x-8,r2y+8,NAVY,lbl="F2",above=True)
        run_x=(r1x+r2x)/2+5; run_y=(r1y+r2y)/2; dot(run_x,run_y,PINK,5,lbl="R",above=True)
        arr(r1x+12,r1y,run_x-4,run_y,AMBER,2); dash(run_x,run_y,r2x-10,r2y+6,NAVY,1,(3,3)); box("RUN HARD — THROW AHEAD",cx,y+5,5.5,NAVY)
    elif drill_id==12:
        r=dmd(); b=bases(r); dot(b["3B"][0]-8,b["3B"][1],PINK,lbl="R",above=True)
        of_x,of_y=cx+r*0.5,cy+r*1.3; dot(of_x,of_y,GREEN,lbl="OF",above=True); ball(of_x-5,of_y+8)
        hx,hy=b["HM"]; arr(b["3B"][0]-6,b["3B"][1],hx-6,hy+8,PINK,2); arr(of_x-5,of_y,hx+4,hy+6,AMBER,1.8); box("TAG UP — SPRINT HOME",cx,y+5,5.5,PINK)
    elif drill_id==13:
        r=dmd(); b=bases(r); b1x,b1y=b["1B"]; dot(b1x+8,b1y,RED,lbl="R",above=True)
        lead1_x=b1x+24; dot(lead1_x,b1y,PINK,4); dash(b1x+12,b1y,lead1_x-4,b1y,NAVY,1,(3,3)); lbl("PRIMARY",lead1_x+8,b1y+4,5,NAVY)
        lead2_x=lead1_x+12; dot(lead2_x,b1y-4,PURPLE,4); dash(lead1_x+4,b1y,lead2_x-3,b1y-4,PURPLE,1,(3,3))
        dot(b["P"][0],b["P"][1],NAVY,lbl="P",above=True); box("READ PITCHER — REACT",cx,y+5,5.5,NAVY)
    elif drill_id==14:
        r=dmd(); b=bases(r); dot(cx-r*0.45,cy+r*0.2,NAVY,lbl="SS",above=True); dot(cx+r*0.35,cy+r*0.2,NAVY,lbl="2B",above=True)
        dot(b["1B"][0]+8,b["1B"][1],NAVY,lbl="1B",above=True); dot(b["1B"][0]+8,b["1B"][1]+14,PINK,4,lbl="R",above=True)
        dash(cx-r*0.4,cy+r*0.25,cx+r*0.3,cy+r*0.25,PURPLE,1.2,(2,3)); box("WHO COVERS 2ND?",cx,y+5,5.5,NAVY)
    elif drill_id==15:
        c.setFillColor(GRASS); c.rect(x,y,w,h,fill=1,stroke=0)
        bkt_x,bkt_y=cx+w*0.3,cy; c.setFillColor(RED); c.roundRect(bkt_x-8,bkt_y,16,20,2,fill=1,stroke=0)
        lbl("TARGET",bkt_x,bkt_y+10,5.5,CHALK,True)
        for i,(px2,dl) in enumerate([(cx-w*0.3,"30ft"),(cx-w*0.1,"45ft"),(cx+w*0.08,"60ft")]):
            dot(px2,cy+(i-1)*10,NAVY if i==0 else LGRAY,4+i); lbl(dl,px2,cy+(i-1)*10-14,5.5,GRAY)
            arr(px2+4,cy+(i-1)*10,bkt_x-8,bkt_y+10,AMBER if i==0 else LGRAY,1.2+i*0.3)
        box("HIT TARGET — ADVANCE",cx,y+5,5.5,HexColor("#854F0B"))
    elif drill_id==16:
        ofbg(); ball_x,ball_y=cx,cy+h*0.32; arc(cx-w*0.1,cy-h*0.3,ball_x,ball_y,AMBER,1.5); ball(ball_x,ball_y)
        dot(cx-w*0.28,cy+h*0.1,NAVY,lbl="LF"); dot(cx+w*0.28,cy+h*0.1,GREEN,lbl="CF")
        arr(cx-w*0.28+5,cy+h*0.1+5,ball_x-6,ball_y-6,NAVY,1.5); arr(cx+w*0.28-5,cy+h*0.1+5,ball_x+6,ball_y-6,GREEN,1.5)
        lbl("MINE!",cx+w*0.28+14,cy+h*0.1+10,6.5,GREEN,True); lbl("BACK OFF",cx-w*0.28-16,cy+h*0.1+10,5.5,RED,True)
        box("CALL IT — CF HAS PRIORITY",cx,y+5,5.5,GREEN)
    elif drill_id==17:
        hitbg(); hx,hy=cx+w*0.05,cy
        s=7*0.8; p=c.beginPath(); p.moveTo(hx-s,hy+s*0.4); p.lineTo(hx+s,hy+s*0.4); p.lineTo(hx+s,hy-s*0.3); p.lineTo(hx,hy-s*0.9); p.lineTo(hx-s,hy-s*0.3); p.close()
        c.setFillColor(HOME_CLR); c.setStrokeColor(LGRAY); c.setLineWidth(0.8); c.drawPath(p,fill=1,stroke=1)
        dot(hx,hy+8,NAVY,lbl="H",above=True); fx,fy=cx-w*0.3,cy-h*0.15; dot(fx,fy,RED,lbl="F")
        arc(fx+5,fy+4,hx-8,hy+6,AMBER,1.8,0.25); lbl("45°",fx+14,fy+18,6,AMBER,True); box("LOAD — HIP TURN — CONTACT",cx,y+5,5.5,RED)
    elif drill_id==18:
        r=dmd(); b=bases(r); hx,hy=b["HM"]; dot(hx,hy+10,RED,lbl="B",above=True); ball(hx-12,hy+22)
        px2,py2=b["P"]; dot(px2,py2,NAVY,lbl="P",above=True); arr(px2,py2-5,hx-10,hy+20,GREEN,1.8)
        dot(b["3B"][0]+8,b["3B"][1],PURPLE,lbl="3B",above=True); arr(b["3B"][0]+10,b["3B"][1],hx-14,hy+20,PURPLE,1.5)
        dot(b["1B"][0]+8,b["1B"][1],GREEN,lbl="1B",above=True); dot(b["2B"][0]-8,b["2B"][1]-8,HexColor("#534AB7"),lbl="2B",above=True)
        box("EVERYONE HAS A ROLE",cx,y+5,5.5,PURPLE)
    elif drill_id==19:
        ofbg(); dot(cx,cy+h*0.05,NAVY,lbl="OF"); dot(cx,cy-h*0.3,RED,lbl="COACH")
        for tx,ty in [(cx-w*0.25,cy+h*0.3),(cx+w*0.2,cy+h*0.25),(cx-w*0.1,cy+h*0.35)]:
            arc(cx,cy-h*0.25,tx,ty,AMBER,1.2,0.2); ball(tx,ty,r=4)
        box("NO WARNING — REACT",cx,y+5,5.5,GREEN)
    elif drill_id==20:
        r=dmd(); b=bases(r)
        for pos,(px2,py2) in [("SS",(cx-r*0.45,cy+r*0.2)),("2B",(cx+r*0.35,cy+r*0.2)),("3B",(b["3B"][0]+8,b["3B"][1])),("1B",(b["1B"][0]+8,b["1B"][1])),("P",b["P"])]:
            dot(px2,py2,NAVY,lbl=pos,above=True)
        dot(cx,cy-r*1.2,RED,lbl="COACH"); box("COACH CALLS — DEFENSE REACTS",cx,y+5,5.5,PURPLE)
    elif drill_id==21:
        c.setFillColor(GRASS); c.rect(x,y,w,h,fill=1,stroke=0)
        goal_w=w*0.4; gx1,gx2=cx-goal_w/2,cx+goal_w/2; goal_y=cy+h*0.2
        c.setStrokeColor(NAVY); c.setLineWidth(2.5)
        c.line(gx1,goal_y-14,gx1,goal_y+4); c.line(gx2,goal_y-14,gx2,goal_y+4); c.setLineWidth(1.5); c.line(gx1,goal_y+4,gx2,goal_y+4)
        lbl("GLOVE",gx1-12,goal_y-6,5.5,NAVY); lbl("GLOVE",gx2+12,goal_y-6,5.5,NAVY)
        dot(cx,goal_y-4,NAVY,lbl="F"); dot(cx,cy-h*0.32,RED,lbl="COACH")
        bounce(cx,cy-h*0.27,cx,goal_y-8,2,AMBER,2); box("STOP THE BALL — ANY MEANS",cx,y+5,5.5,NAVY)
    elif drill_id==22:
        c.setFillColor(GRASS); c.rect(x,y,w,h,fill=1,stroke=0)
        for ty,col,lb in [(cy+h*0.18,NAVY,"TEAM 1"),(cy-h*0.12,GREEN,"TEAM 2")]:
            box(lb,x+w*0.08,ty+4,5.5,col)
            pxs=[x+w*0.22+i*w*0.14 for i in range(5)]
            for px2 in pxs: dot(px2,ty,col,4)
            for i in range(len(pxs)-1): arr(pxs[i]+4,ty,pxs[i+1]-4,ty,AMBER if col==NAVY else HexColor("#CC8800"),1.3)
        box("FIRST TEAM DONE WINS",cx,y+5,5.5,HexColor("#854F0B"))
    elif drill_id==23:
        ofbg(); dot(cx,cy-h*0.35,RED,lbl="COACH")
        route([(cx-w*0.2,cy+h*0.05),(cx-w*0.2,cy+h*0.38)],GREEN,2); dot(cx-w*0.2,cy+h*0.05,NAVY,lbl="OF1"); ball(cx-w*0.2,cy+h*0.36,r=3.5)
        arc(cx,cy-h*0.3,cx-w*0.2,cy+h*0.3,AMBER,1.8,0.28)
        route([(cx+w*0.18,cy+h*0.05),(cx+w*0.28,cy+h*0.18),(cx+w*0.18,cy+h*0.4)],GREEN,2); dot(cx+w*0.18,cy+h*0.05,GREEN,lbl="OF2")
        lbl("RUN ROUTE",cx-w*0.05,cy+h*0.28,5.5,NAVY,True); lbl("THEN LOOK",cx-w*0.05,cy+h*0.2,5.5,NAVY,True)
        box("TRACK BALL OVER SHOULDER",cx,y+5,5.5,GREEN)
    elif drill_id==24:
        r=dmd(); b=bases(r)
        for fx,fy in [(cx-r*0.5,cy+r*0.15),(cx+r*0.1,cy+r*0.3),(cx-r*0.1,cy-r*0.1)]:
            c.setFillColor(NAVY); c.setStrokeColor(NAVY); c.setLineWidth(3); c.line(fx-10,fy,fx+10,fy)
        dot(cx,cy+r*0.55,NAVY,lbl="UP!",above=True); arr(cx,cy+r*0.5,b["1B"][0]-5,b["1B"][1]+5,AMBER,2)
        dot(cx,cy-r*0.1,RED,lbl="COACH"); bounce(cx,cy-r*0.06,cx-r*0.1,cy+r*0.5,1,AMBER,1.5); box("LIE FLAT — HEAR HIT — GO",cx,y+5,5.5,NAVY)
    elif drill_id==25:
        r=dmd(); b=bases(r); qx,qy=cx-r*0.45,cy+r*0.2
        for i,col in enumerate([RED,NAVY,LGRAY,LGRAY]): dot(qx,qy-i*14,col,4+(1 if i==0 else 0))
        lbl("#1",qx+12,qy+6,6,RED,True); dot(cx,cy-r*0.1,RED,lbl="COACH")
        bounce(cx,cy-r*0.06,qx+4,qy+4,1,AMBER); arr(qx,qy-5,b["1B"][0]-5,b["1B"][1]+5,AMBER,1.8); box("CLEAN PLAY = HOLD TOP SPOT",cx,y+5,5.5,NAVY)
    elif drill_id==26:
        r=dmd(); b=bases(r); fx,fy=cx-r*0.3,cy+r*0.4; dot(fx,fy,NAVY,lbl="F",above=True)
        dot(b["1B"][0]+8,b["1B"][1],GREEN,lbl="1B",above=True); dot(cx,cy-r*0.1,RED,lbl="COACH")
        for i in range(5): bounce(cx,cy-r*0.06,fx+(i-2)*4,fy+i*2,1,AMBER,0.8)
        arr(fx,fy-5,b["1B"][0]-5,b["1B"][1]+5,RED,2); box("5 GROUNDERS — STAY LOW",cx,y+5,5.5,NAVY)
    elif drill_id==27:
        r=dmd(); b=bases(r); route([(b["HM"][0],b["HM"][1]-6),(b["1B"][0],b["1B"][1]-4),(b["2B"][0]+4,b["2B"][1])],PINK,2)
        dot(b["HM"][0],b["HM"][1]-10,PINK,lbl="R"); dot(b["3B"][0]-8,b["3B"][1],NAVY,lbl="3B")
        for i in range(3): arr(b["3B"][0]-4,b["3B"][1]+i*5,b["2B"][0]-6,b["2B"][1]+i*5,AMBER if i==0 else LGRAY,1.2)
        lbl("x3",b["2B"][0]-18,b["2B"][1]+14,7,AMBER,True); box("RACE 3B's 3 THROWS",cx,y+5,5.5,PINK)
    elif drill_id==28:
        r=dmd(); b=bases(r); dot(b["HM"][0],b["HM"][1]-10,PINK,lbl="B")
        route([(b["HM"][0],b["HM"][1]-6),(b["1B"][0],b["1B"][1]),(b["2B"][0],b["2B"][1]+5)],PINK,2)
        of_x,of_y=cx+r*0.7,cy+r*0.9; dot(of_x,of_y,GREEN,lbl="OF",above=True); ball(of_x-5,of_y+6)
        arr(of_x-5,of_y,b["2B"][0]+4,b["2B"][1],AMBER,2); box("LEG OUT THE DOUBLE",cx,y+5,5.5,PINK)
    elif drill_id==29:
        r=dmd(); b=bases(r); dot(b["HM"][0],b["HM"][1]-10,RED,lbl="B"); dot(b["1B"][0]+8,b["1B"][1]+8,PINK,4,lbl="R",above=True)
        dot(cx-r*0.45,cy+r*0.2,NAVY,lbl="SS",above=True); dot(cx+r*0.6,cy+r*0.9,GREEN,lbl="OF",above=True)
        arc(b["HM"][0],b["HM"][1]+6,cx+r*0.55,cy+r*0.85,AMBER,1.8); box("COUNT TOTAL BASES",cx,y+5,5.5,PURPLE)
    elif drill_id==30:
        r=dmd(); b=bases(r); hx,hy=b["HM"]; dot(hx,hy-10,RED,lbl="B")
        c.setFillColor(HexColor("#CCEECC")); c.setStrokeColor(GREEN); c.setLineWidth(1); c.roundRect(hx-30,hy+8,22,16,3,fill=1,stroke=1); lbl("3B ZONE",hx-19,hy+14,5,GREEN,True)
        c.setFillColor(HexColor("#FFEEDD")); c.setStrokeColor(AMBER); c.roundRect(hx+8,hy+8,22,16,3,fill=1,stroke=1); lbl("1B ZONE",hx+19,hy+14,5,AMBER,True)
        bounce(hx,hy+4,hx-20,hy+12,1,NAVY,1.5); box("BUNT TO TARGET ZONE",cx,y+5,5.5,PURPLE)
    elif drill_id==31:
        c.setFillColor(GRASS); c.rect(x,y,w,h,fill=1,stroke=0)
        c.setFillColor(HexColor("#DDEEFF")); c.rect(x,y+h*0.82,w,h*0.1,fill=1,stroke=0); c.rect(x,y+h*0.08,w,h*0.1,fill=1,stroke=0)
        lbl("END ZONE",cx,y+h*0.9,6,NAVY,True); lbl("END ZONE",cx,y+h*0.1,6,NAVY,True)
        p1=(cx-w*0.25,cy+h*0.2); p2=(cx+w*0.2,cy+h*0.35); p3=(cx-w*0.1,cy+h*0.55)
        dot(*p1,NAVY,lbl="P1"); dot(*p2,GREEN,lbl="P2"); dot(*p3,PURPLE,lbl="P3")
        arr(p1[0]+5,p1[1]+3,p2[0]-5,p2[1]-3,AMBER,1.8); arr(p2[0]-3,p2[1]+4,p3[0]+3,p3[1]-4,AMBER,1.8)
        box("THROW ONLY — NO RUNNING",cx,y+5,5.5,HexColor("#854F0B"))
    elif drill_id==32:
        r=dmd(); b=bases(r); qx=cx-r*0.45
        for i,col in enumerate([RED,NAVY,LGRAY,LGRAY]): dot(qx,cy+r*0.2-i*14,col,4+(1 if i==0 else 0))
        lbl("#1",qx+12,cy+r*0.24,6,RED,True); bounce(cx,cy-r*0.06,qx+4,cy+r*0.22,1,AMBER)
        arr(qx,cy+r*0.15,b["1B"][0]-5,b["1B"][1]+5,AMBER,2); dot(cx,cy-r*0.1,RED,lbl="COACH"); box("ERROR = MOVE DOWN",cx,y+5,5.5,NAVY)
    elif drill_id==33:
        r=dmd(); b=bases(r); dot(b["1B"][0]+8,b["1B"][1]+10,PINK,4,lbl="R",above=True)
        ss_x,ss_y=cx-r*0.45,cy+r*0.2; b2x,b2y=cx+r*0.35,cy+r*0.2
        dot(ss_x,ss_y,NAVY,lbl="SS",above=True); dot(b2x,b2y,PURPLE,lbl="2B",above=True)
        dash(ss_x+5,ss_y,b2x-5,b2y,PURPLE,1.5,(2,3)); lbl("SIGNAL",cx,ss_y+10,6,PURPLE,True)
        dot(b["HM"][0],b["HM"][1]-10,GREEN,lbl="C"); arr(b["HM"][0],b["HM"][1]+4,b["2B"][0]-4,b["2B"][1]-8,AMBER,2)
        box("SIGNAL — WHO COVERS 2ND?",cx,y+5,5.5,PURPLE)
    elif drill_id==34:
        r=dmd(); b=bases(r); dot(b["1B"][0]+8,b["1B"][1]+10,PINK,4,lbl="R1",above=True); dot(b["3B"][0]-8,b["3B"][1]+8,RED,4,lbl="R3",above=True)
        dot(b["HM"][0],b["HM"][1]-10,NAVY,lbl="C"); dot(b["2B"][0]-8,b["2B"][1]-8,NAVY,lbl="SS",above=True)
        arr(b["HM"][0],b["HM"][1]+4,b["2B"][0]-6,b["2B"][1]-6,AMBER,1.8)
        mid_x,mid_y=(b["HM"][0]+b["2B"][0])/2,(b["HM"][1]+b["2B"][1])/2
        dot(mid_x,mid_y,PURPLE,3,lbl="CUT?",above=True); dash(mid_x,mid_y,b["HM"][0]+4,b["HM"][1]+8,RED,1.5,(3,3))
        box("3 READS: THRU / CUT / FAKE",cx,y+5,5.5,RED)
    elif drill_id==35:
        r=dmd(); b=bases(r); dot(b["1B"][0]+8,b["1B"][1]+8,PINK,4,lbl="R",above=True)
        of_x,of_y=cx+r*0.7,cy+r*0.85; dot(of_x,of_y,GREEN,lbl="OF",above=True)
        arc(b["HM"][0],b["HM"][1]+8,of_x-5,of_y+5,AMBER,1.5); route([(b["1B"][0]+8,b["1B"][1]+8),(b["2B"][0],b["2B"][1]),(b["3B"][0]+4,b["3B"][1])],PINK,2)
        arr(of_x,of_y,of_x-18,of_y,HexColor("#CC4444"),1.5); lbl("1 STEP = GO",of_x-30,of_y+12,5.5,RED,True); box("READ OF LATERAL MOVE",cx,y+5,5.5,PINK)
    elif drill_id==36:
        r=dmd(); b=bases(r); b2x,b2y=b["2B"]; dot(b2x-10,b2y-12,PINK,4,lbl="R")
        dash(b2x-4,b2y-6,b2x-10,b2y-12,PINK,1,(3,3)); lbl("2nd LEAD",b2x-24,b2y-6,5.5,PINK)
        dot(b["HM"][0],b["HM"][1]-10,NAVY,lbl="C"); bounce(b["P"][0],b["P"][1]+5,b["HM"][0]+14,b["HM"][1],2,AMBER,2)
        ball(b["HM"][0]+20,b["HM"][1]-5); arr(b2x-10,b2y-14,b["3B"][0]+4,b["3B"][1]+4,PINK,2); box("SECONDARY LEAD — READ — GO",cx,y+5,5.5,PINK)
    elif drill_id==37:
        r=dmd(); b=bases(r); dot(b["1B"][0]+8,b["1B"][1]+10,PINK,4,lbl="R",above=True)
        ss_x,ss_y=cx-r*0.45,cy+r*0.2; b2x,b2y=cx+r*0.35,cy+r*0.2
        dot(ss_x,ss_y,NAVY,lbl="SS",above=True); dot(b2x,b2y,PURPLE,lbl="2B",above=True); dot(cx,cy-r*0.1,RED,lbl="COACH")
        bounce(cx,cy-r*0.06,ss_x+4,ss_y+4,1,AMBER); arr(ss_x,ss_y-5,b["2B"][0]-5,b["2B"][1]-6,AMBER,2)
        arr(b2x-4,b2y,b["2B"][0]+4,b["2B"][1]-5,PURPLE,1.5,True); lbl("COVERS!",cx+r*0.12,cy+r*0.35,6,PURPLE,True); box("WHO FIELDS — WHO COVERS",cx,y+5,5.5,PURPLE)
    elif drill_id==38:
        r=dmd(); b=bases(r); of_x,of_y=cx-r*0.5,cy+r*1.4; dot(of_x,of_y,GREEN,lbl="OF",above=True)
        cut_x,cut_y=cx-r*0.25,cy+r*0.55; dot(cut_x,cut_y,NAVY,lbl="CUT",above=True)
        arr(of_x,of_y-6,cut_x,cut_y+7,AMBER,2); arr(cut_x,cut_y-6,b["3B"][0]+6,b["3B"][1]+4,GREEN,1.5)
        lbl("LET GO",b["3B"][0]+18,b["3B"][1]+12,5.5,GREEN); dash(cut_x,cut_y-6,b["HM"][0]+4,b["HM"][1]+8,RED,1.5,(4,3))
        lbl("CUT!",b["HM"][0]+16,b["HM"][1]+20,5.5,RED,True); box("READ RUNNER — DECIDE LOUD",cx,y+5,5.5,PURPLE)
    elif drill_id==39:
        r=dmd(); b=bases(r); hx,hy=b["HM"]; dot(hx,hy-10,RED,lbl="B"); ball(hx-15,hy+20)
        px2,py2=b["P"]; dot(px2,py2,NAVY,lbl="P",above=True); arr(px2,py2-5,hx-12,hy+18,GREEN,1.8)
        dot(b["3B"][0]+8,b["3B"][1],PURPLE,lbl="3B",above=True); arr(b["3B"][0]+10,b["3B"][1],hx-14,hy+18,PURPLE,1.5)
        dot(b["1B"][0]+8,b["1B"][1],GREEN,lbl="1B",above=True); dot(b["2B"][0]-8,b["2B"][1]-8,HexColor("#534AB7"),lbl="2B",above=True)
        box("BUNT EVERY PITCH — FULL COVERAGE",cx,y+5,5,PURPLE)
    elif drill_id==40:
        hitbg(); hx,hy=cx+w*0.05,cy
        s=7*0.8; p=c.beginPath(); p.moveTo(hx-s,hy+s*0.4); p.lineTo(hx+s,hy+s*0.4); p.lineTo(hx+s,hy-s*0.3); p.lineTo(hx,hy-s*0.9); p.lineTo(hx-s,hy-s*0.3); p.close()
        c.setFillColor(HOME_CLR); c.setStrokeColor(LGRAY); c.setLineWidth(0.8); c.drawPath(p,fill=1,stroke=1)
        dot(hx,hy+8,NAVY,lbl="H",above=True); tee_x,tee_y=hx+w*0.14,hy-4
        c.setFillColor(AMBER); c.rect(tee_x-2,tee_y,4,14,fill=1,stroke=0); ball(tee_x,tee_y+17,r=4)
        arr(tee_x,tee_y+17,hx-w*0.28,hy+h*0.22,GREEN,2.5); lbl("OPPO",hx-w*0.3,hy+h*0.28,6.5,GREEN,True); box("LET IT TRAVEL — HIT OPPO",cx,y+5,5.5,RED)
    elif drill_id==41:
        hitbg(); hx,hy=cx+w*0.05,cy
        s=7*0.8; p=c.beginPath(); p.moveTo(hx-s,hy+s*0.4); p.lineTo(hx+s,hy+s*0.4); p.lineTo(hx+s,hy-s*0.3); p.lineTo(hx,hy-s*0.9); p.lineTo(hx-s,hy-s*0.3); p.close()
        c.setFillColor(HOME_CLR); c.setStrokeColor(LGRAY); c.setLineWidth(0.8); c.drawPath(p,fill=1,stroke=1)
        dot(hx,hy+8,NAVY,lbl="H",above=True)
        c.setFillColor(RED); c.rect(hx-w*0.1-2,hy-2,4,12,fill=1,stroke=0); ball(hx-w*0.1,hy+13,r=4); lbl("IN",hx-w*0.1,hy+22,6,RED,True)
        c.setFillColor(AMBER); c.rect(hx+w*0.12-2,hy-4,4,12,fill=1,stroke=0); ball(hx+w*0.12,hy+11,r=4); lbl("OUT",hx+w*0.12,hy+20,6,AMBER,True)
        dot(cx-w*0.3,cy-h*0.3,RED,lbl="COACH"); box("COACH CALLS — HITTER ADJUSTS",cx,y+5,5.5,RED)
    elif drill_id==42:
        r=dmd(); b=bases(r)
        for pos,coords in [("SS",(cx-r*0.45,cy+r*0.2)),("2B",(cx+r*0.35,cy+r*0.2)),("3B",(b["3B"][0]+8,b["3B"][1])),("1B",(b["1B"][0]+8,b["1B"][1])),("OF",(cx+r*0.55,cy+r*0.95))]:
            dot(*coords,NAVY,lbl=pos,above=True)
        dot(b["1B"][0]+8,b["1B"][1]+14,PINK,4,lbl="R",above=True); dot(cx,cy-r*1.1,RED,lbl="COACH CALLS")
        box("NO SETUP — FULL SPEED REACT",cx,y+5,5.5,PURPLE)
    elif drill_id==43:
        ofbg(); r=min(w,h)*0.2
        c.setStrokeColor(HexColor("#AAAAAA")); c.setLineWidth(0.5)
        pts=[(cx,cy+r*0.8),(cx+r*0.8,cy),(cx,cy-r*0.8),(cx-r*0.8,cy)]
        p=c.beginPath(); p.moveTo(*pts[0])
        for pt in pts[1:]: p.lineTo(*pt)
        p.close(); c.drawPath(p,fill=0,stroke=1)
        for ox,oy,lb in [(cx-w*0.38,cy+h*0.28,"LF"),(cx-w*0.12,cy+h*0.38,"LCF"),(cx+w*0.12,cy+h*0.38,"RCF"),(cx+w*0.38,cy+h*0.28,"RF")]:
            dot(ox,oy,GREEN,lbl=lb,above=True)
        for bx2 in [cx-w*0.12,cx+w*0.12]: dash(bx2,cy+h*0.08,bx2,cy+h*0.42,GRAY,1,(3,3))
        lbl("NEGOTIATE GAP",cx,cy+h*0.16,5.5,NAVY,True); box("4-OF ALIGNMENT — CALL YOUR ZONE",cx,y+5,5.5,GREEN)
    elif drill_id==44:
        ofbg()
        norms=[(cx-w*0.3,cy+h*0.2),(cx,cy+h*0.3),(cx+w*0.3,cy+h*0.2)]
        adjusted=[(cx-w*0.15,cy+h*0.18,"LF"),(cx+w*0.14,cy+h*0.28,"CF"),(cx+w*0.38,cy+h*0.18,"RF")]
        for nx2,ny2 in norms: dot(nx2,ny2,LGRAY,4)
        for (ox,oy,lb),(nx2,ny2) in zip(adjusted,norms):
            dot(ox,oy,GREEN,lbl=lb,above=True); arr(nx2,ny2,ox,oy,AMBER,1.5)
        box("HITTER TYPE = ADJUST SHADE",cx,y+5,5.5,GREEN)
    elif drill_id==45:
        c.setFillColor(GRASS); c.rect(x,y,w,h,fill=1,stroke=0)
        p1x,p1y=x+w*0.12,cy; p2x,p2y=x+w*0.88,cy
        dot(p1x,p1y,NAVY,lbl="P1",above=True); dot(p2x,p2y,GREEN,lbl="P2",above=True)
        arr(p1x+5,p1y+2,p2x-5,p2y+2,AMBER,2); arr(p2x-5,p2y-2,p1x+5,p1y-2,GREEN,1.5)
        for frac,dl in [(0.25,"30ft"),(0.5,"45ft"),(0.75,"60ft+")]:
            mx=x+w*frac; c.setStrokeColor(LGRAY); c.setLineWidth(0.8); c.setDash(2,4); c.line(mx,cy-18,mx,cy+18); c.setDash(); lbl(dl,mx,cy-26,5.5,GRAY)
        lbl("3 CLEAN = STEP BACK",cx,cy+22,6,NAVY,True); box("STEP BACK EVERY 3 CLEAN",cx,y+5,5.5,HexColor("#854F0B"))
    elif drill_id==46:
        c.setFillColor(GRASS); c.rect(x,y,w,h,fill=1,stroke=0); dot(x+w*0.12,cy,NAVY,lbl="P",above=True)
        for tx,dl,col in [(x+w*0.42,"30ft",RED),(x+w*0.62,"45ft",AMBER),(x+w*0.82,"60ft",GREEN)]:
            c.setFillColor(col); c.roundRect(tx-8,cy-12,16,24,3,fill=1,stroke=0); lbl("X",tx,cy-2,8,CHALK,True); lbl(dl,tx,cy-20,5.5,col)
        arr(x+w*0.17,cy,x+w*0.34,cy,AMBER,2); box("HIT TARGET — ADVANCE",cx,y+5,5.5,HexColor("#854F0B"))
    elif drill_id==47:
        r=dmd(); b=bases(r); dot(b["2B"][0]-8,b["2B"][1]-6,PINK,4,lbl="R")
        of_x,of_y=cx+r*0.6,cy+r*0.85; dot(of_x,of_y,GREEN,lbl="OF",above=True)
        arc(b["HM"][0],b["HM"][1]+8,of_x-4,of_y+4,AMBER,1.5)
        route([(b["2B"][0]-8,b["2B"][1]-6),(b["3B"][0]+4,b["3B"][1]),(b["HM"][0]-4,b["HM"][1]+8)],PINK,2)
        b3x,b3y=b["3B"]; c.setFillColor(RED); c.circle(b3x+4,b3y+10,5,fill=1,stroke=0); lbl("?",b3x+4,b3y+7,7,CHALK,True)
        box("READ 3B COACH — GO OR STOP",cx,y+5,5.5,PURPLE)
    elif drill_id==48:
        r=dmd(); b=bases(r); arr(b["HM"][0]+4,b["HM"][1]+8,b["1B"][0]-5,b["1B"][1]+5,AMBER,2)
        dot(b["1B"][0]+8,b["1B"][1],NAVY,lbl="1B",above=True)
        p_back_x,p_back_y=b["1B"][0]+20,b["1B"][1]-12; dot(p_back_x,p_back_y,GREEN,lbl="P")
        arr(b["P"][0],b["P"][1],p_back_x-4,p_back_y+4,GREEN,1.5,True); lbl("BACKUP",p_back_x+14,p_back_y+4,5.5,GREEN,True)
        box("NO BALL = BACKUP SOMEWHERE",cx,y+5,5.5,PURPLE)
    elif drill_id==49:
        r=dmd(); b=bases(r); of_x,of_y=cx-r*0.4,cy+r*1.5; dot(of_x,of_y,GREEN,lbl="LF",above=True)
        cut_x,cut_y=cx-r*0.2,cy+r*0.6; dot(cut_x,cut_y,NAVY,lbl="SS",above=True)
        dash(of_x,of_y,b["3B"][0],b["3B"][1],LGRAY,1,(3,3)); arr(of_x+4,of_y-5,cut_x-3,cut_y+7,AMBER,2); arr(cut_x-3,cut_y-6,b["3B"][0]+6,b["3B"][1]+4,RED,2)
        lbl("ALIGN ON LINE",cut_x+18,cut_y+8,5.5,RED,True); box("GET IN LINE — OF TO BASE",cx,y+5,5.5,PURPLE)
    elif drill_id==50:
        r=dmd(); b=bases(r); dot(b["3B"][0]-8,b["3B"][1]+4,PINK,4,lbl="R",above=True); dot(b["HM"][0],b["HM"][1]-10,NAVY,lbl="C"); dot(b["P"][0],b["P"][1],RED,lbl="P",above=True)
        bounce(b["P"][0],b["P"][1]+5,b["HM"][0]+18,b["HM"][1]-6,2,AMBER,2); ball(b["HM"][0]+22,b["HM"][1]-8)
        arr(b["3B"][0]-8,b["3B"][1],b["HM"][0]-6,b["HM"][1]+8,PINK,2); lbl("READ!",b["HM"][0]+28,b["HM"][1]+2,6,RED,True); box("DIRT = READ — GO OR HOLD",cx,y+5,5.5,PINK)
    elif drill_id==51:
        r=dmd(); b=bases(r); dot(b["1B"][0]+8,b["1B"][1]+10,PINK,4,lbl="R",above=True)
        of_x,of_y=cx+r*0.75,cy+r*0.95; dot(of_x,of_y,GREEN,lbl="OF",above=True)
        arc(b["HM"][0],b["HM"][1]+8,of_x-5,of_y+5,AMBER,1.5)
        route([(b["1B"][0]+8,b["1B"][1]+10),(b["2B"][0],b["2B"][1]),(b["3B"][0]+4,b["3B"][1]+4)],PINK,2)
        b3x,b3y=b["3B"]; c.setFillColor(RED); c.circle(b3x+4,b3y+12,5,fill=1,stroke=0); lbl("?",b3x+4,b3y+9,7,CHALK,True)
        arr(of_x,of_y-5,b3x+8,b3y+8,AMBER,1.8); box("GAP HIT — ROUND 2ND — DECIDE",cx,y+5,5.5,PINK)
    elif drill_id==52:
        hitbg(); h1x,h1y=cx-w*0.2,cy+h*0.1; h2x,h2y=cx+w*0.2,cy+h*0.1
        for hx2,hy2,lb,col in [(h1x,h1y,"H1",NAVY),(h2x,h2y,"H2",GREEN)]:
            s=5*0.8; p=c.beginPath(); p.moveTo(hx2-s,hy2-12+s*0.4); p.lineTo(hx2+s,hy2-12+s*0.4); p.lineTo(hx2+s,hy2-12-s*0.3); p.lineTo(hx2,hy2-12-s*0.9); p.lineTo(hx2-s,hy2-12-s*0.3); p.close()
            c.setFillColor(HOME_CLR); c.setStrokeColor(LGRAY); c.setLineWidth(0.8); c.drawPath(p,fill=1,stroke=1)
            dot(hx2,hy2+5,col,lbl=lb,above=True)
        coach_x,coach_y=cx,cy-h*0.32; dot(coach_x,coach_y,RED,lbl="COACH")
        arc(coach_x,coach_y+5,h1x-4,h1y,AMBER,1.5,0.2); arc(coach_x,coach_y+5,h2x+4,h2y,AMBER,1.5,0.2)
        box("2pts OPPO",h1x-w*0.18,cy+h*0.3,5.5,GREEN); box("1pt CENTER",cx,cy+h*0.34,5.5,AMBER); box("0pts PULL",h2x+w*0.18,cy+h*0.3,5.5,RED)
        box("HEAD TO HEAD — INTENTIONAL HITTING",cx,y+5,5,RED)
    elif drill_id==53:
        r=dmd(); b=bases(r)
        # 4 infielders
        for pos,(px2,py2) in [("SS",(cx-r*0.45,cy+r*0.2)),("2B",(cx+r*0.35,cy+r*0.2)),("3B",(b["3B"][0]+8,b["3B"][1])),("1B",(b["1B"][0]+8,b["1B"][1]))]:
            dot(px2,py2,NAVY,lbl=pos,above=True)
        # Hitter at plate
        dot(b["HM"][0],b["HM"][1]-10,RED,lbl="H",above=False)
        # Coach soft tossing
        dot(b["HM"][0]-18,b["HM"][1]+6,PURPLE,lbl="C",above=False)
        arc(b["HM"][0]-14,b["HM"][1]+8,b["HM"][0]-4,b["HM"][1]+8,AMBER,1.5,0.3)
        # Runner on 1B
        dot(b["1B"][0]+8,b["1B"][1]+12,PINK,4,lbl="R",above=True)
        box("LIVE SITUATIONS — CALL THE PLAY",cx,y+5,5.5,PURPLE)
    elif drill_id==54:
        c.setFillColor(GRASS); c.rect(x,y,w,h,fill=1,stroke=0)
        # Two team lanes
        for ty,col,lb in [(cy+h*0.22,NAVY,"TEAM 1"),(cy-h*0.08,GREEN,"TEAM 2")]:
            box(lb,x+w*0.08,ty+4,5.5,col)
            # Balls lined up
            ball_xs=[x+w*0.28+i*w*0.12 for i in range(4)]
            for bx2 in ball_xs: ball(bx2,ty,r=3.5)
            # Sprinting player
            dot(x+w*0.2,ty,col,5)
            arr(x+w*0.2,ty,ball_xs[0]-4,ty,col,1.5)
            # Catcher teammate at end
            dot(x+w*0.85,ty,col,5,lbl="CATCH",above=True)
            arr(ball_xs[0]+4,ty,x+w*0.82,ty,AMBER,1.8)
        box("SPRINT — FIELD — THROW — REPEAT",cx,y+5,5.5,HexColor("#854F0B"))
    elif drill_id==55:
        ofbg(); of_x,of_y=cx,cy+h*0.1
        for i,(dx,dl) in enumerate([(-14,"1"),(0,"2"),(14,"3")]):
            dot(of_x+dx,of_y-i*2,NAVY if i==0 else LGRAY,4,lbl=dl,above=True)
        ball(of_x-20,of_y+18); arr(of_x-18,of_y+15,of_x-2,of_y+2,AMBER,1.8)
        arr(of_x+2,of_y,cx,cy-h*0.32,GREEN,1.8); box("CATCH — GRIP — THROW",cx,y+5,5.5,GREEN)
    elif drill_id==56:
        ofbg(); dot(cx,cy-h*0.15,NAVY,lbl="OF")
        ball(cx-w*0.32,cy+h*0.4); route([(cx,cy-h*0.1),(cx-w*0.18,cy+h*0.18),(cx-w*0.3,cy+h*0.35)],GREEN,2)
        box("CLOSE THE GAP — DON'T LET IT PASS",cx,y+5,5.5,GREEN)
    elif drill_id==57:
        ofbg(); dot(cx-w*0.1,cy+h*0.05,NAVY,lbl="OF")
        route([(cx-w*0.1,cy+h*0.05),(cx+w*0.05,cy+h*0.2)],GREEN,2)
        ball(cx-w*0.2,cy+h*0.32); arc(cx+w*0.05,cy+h*0.2,cx-w*0.2,cy+h*0.3,AMBER,1.5,0.3)
        lbl("TURN!",cx+w*0.1,cy+h*0.3,6,RED,True); box("REACT — TURN — RECOVER",cx,y+5,5.5,GREEN)
    elif drill_id==58:
        ofbg(); dot(cx,cy,NAVY,lbl="OF"); lbl("BACK TO FENCE",cx,cy-14,5.5,GRAY)
        ball(cx+w*0.05,cy+h*0.4); dash(cx,cy+8,cx+w*0.05,cy+h*0.36,GRAY,1,(3,3))
        box("HEAD TURNED — EYES ON BALL",cx,y+5,5.5,GREEN)
    elif drill_id==59:
        ofbg(); c.setStrokeColor(NAVY); c.setLineWidth(3); c.line(cx-12,cy,cx+12,cy)
        lbl("DOWN",cx,cy-12,5.5,NAVY,True); dot(cx-w*0.28,cy-h*0.25,RED,lbl="COACH")
        ball(cx+w*0.15,cy+h*0.3); arr(cx,cy+4,cx+w*0.12,cy+h*0.28,AMBER,1.8)
        box("HEAR IT — LOOK UP — SCRAMBLE",cx,y+5,5.5,GREEN)
    elif drill_id==60:
        ofbg(); dot(cx,cy,NAVY,lbl="OF")
        dash(cx,cy+8,cx,cy+h*0.3,GRAY,1,(3,3)); ball(cx,cy+h*0.32)
        lbl("BEHIND BACK",cx,cy-14,5.5,NAVY,True); box("OVERHEAD — GLOVE BEHIND BACK",cx,y+5,5.5,GREEN)
    elif drill_id==61:
        ofbg(); dot(cx,cy,NAVY,lbl="OF")
        dash(cx,cy+8,cx,cy+h*0.3,GRAY,1,(3,3)); ball(cx,cy+h*0.32)
        lbl("UNDER LEG",cx,cy-14,5.5,NAVY,True); box("GLOVE THREADED BETWEEN LEGS",cx,y+5,5.5,GREEN)
    elif drill_id==62:
        ofbg(); route([(cx-w*0.22,cy-h*0.1),(cx,cy+h*0.12)],NAVY,2)
        c.setStrokeColor(NAVY); c.setLineWidth(2); c.setDash(2,2); c.line(cx-6,cy+h*0.1,cx+10,cy+h*0.16); c.setDash()
        ball(cx+w*0.1,cy+h*0.2); lbl("SLIDE",cx,cy+h*0.02,5.5,NAVY,True)
        box("CHARGE — SLIDE — CATCH",cx,y+5,5.5,GREEN)
    elif drill_id==63:
        c.setFillColor(GRASS); c.rect(x,y,w,h,fill=1,stroke=0)
        dot(cx,cy,RED,lbl="COACH"); dot(cx,cy-h*0.28,NAVY,lbl="OF")
        for ang in [30,150,210,330]:
            dx2=math.cos(math.radians(ang))*w*0.28; dy2=math.sin(math.radians(ang))*h*0.22
            arr(cx,cy-h*0.28,cx+dx2,cy-h*0.28+dy2,AMBER,1.3)
        box("REACT TO THE SIGNAL — NO FALSE STEP",cx,y+5,5.5,GREEN)

    elif drill_id==64:
        r=dmd(); b=bases(r); ball_x,ball_y=cx-r*0.15,cy+r*0.05; ball(ball_x,ball_y)
        fx,fy=cx-r*0.4,cy-r*0.15; dot(fx,fy,NAVY,lbl="IF",above=True)
        arc(fx,fy,ball_x,ball_y,AMBER,1.5,0.25); arr(ball_x,ball_y,b["1B"][0]-6,b["1B"][1]+5,RED,2)
        box("CIRCLE — FIELD MOVING — THROW",cx,y+5,5.5,NAVY)
    elif drill_id==65:
        r=dmd(); b=bases(r); px2,py2=b["P"]; dot(px2,py2,RED,lbl="P",above=True)
        fx,fy=cx-r*0.45,cy+r*0.15; dot(fx,fy,NAVY,lbl="IF",above=True)
        c.setStrokeColor(AMBER); c.setLineWidth(1.5); c.setDash(2,2); c.line(fx-4,fy-8,fx+4,fy-2); c.setDash()
        lbl("2 STEPS",fx,fy-16,5.5,AMBER,True); box("TIME THE STEPS TO THE PITCH",cx,y+5,5.5,NAVY)
    elif drill_id==66:
        c.setFillColor(GRASS); c.rect(x,y,w,h,fill=1,stroke=0)
        p1x,p1y=x+w*0.15,cy; p2x,p2y=x+w*0.85,cy
        dot(p1x,p1y,GREEN,lbl="P1",above=True); dot(p2x,p2y,NAVY,lbl="P2",above=True)
        bounce(p1x+6,p1y,p2x-6,p2y,2,AMBER,1.5); box("ROLL — FIELD — ROLL BACK",cx,y+5,5.5,NAVY)
    elif drill_id==67:
        c.setFillColor(GRASS); c.rect(x,y,w,h,fill=1,stroke=0)
        p1x,p1y=x+w*0.15,cy; p2x,p2y=x+w*0.85,cy
        dot(p1x,p1y,GREEN,lbl="P1",above=True); dot(p2x,p2y,NAVY,lbl="P2",above=True)
        arc(p1x+6,p1y+3,p2x-6,p2y+3,AMBER,1.5,0.25); lbl("NO GLOVE",cx,cy+16,5.5,AMBER,True)
        box("CUSHION — DON'T SQUEEZE",cx,y+5,5.5,NAVY)
    elif drill_id==68:
        c.setFillColor(GRASS); c.rect(x,y,w,h,fill=1,stroke=0)
        p1x,p1y=x+w*0.15,cy; p2x,p2y=x+w*0.85,cy
        dot(p1x,p1y,GREEN,lbl="P1",above=True); dot(p2x,p2y,NAVY,lbl="P2",above=True)
        arc(p1x+6,p1y+3,p2x-6,p2y+3,AMBER,1.5,0.25); lbl("TRAP IT",p2x-18,p2y+14,5.5,AMBER,True)
        box("BACK OF GLOVE + BARE HAND",cx,y+5,5.5,NAVY)
    elif drill_id==69:
        c.setFillColor(GRASS); c.rect(x,y,w,h,fill=1,stroke=0)
        p1x,p1y=x+w*0.15,cy; p2x,p2y=x+w*0.85,cy
        dot(p1x,p1y,GREEN,lbl="P1",above=True); dot(p2x,p2y,NAVY,lbl="P2",above=True)
        arc(p1x+6,p1y+3,p2x-6,p2y+3,AMBER,1.5,0.25); lbl("POCKET OPEN",p2x-22,p2y+14,5.5,AMBER,True)
        box("CATCH OPEN — QUICK PULL",cx,y+5,5.5,NAVY)

    elif drill_id==70:
        c.setFillColor(GRASS); c.rect(x,y,w,h,fill=1,stroke=0)
        p1x,p1y=x+w*0.15,cy; p2x,p2y=x+w*0.85,cy
        dot(p1x,p1y,NAVY,lbl="P1",above=True); dot(p2x,p2y,GREEN,lbl="P2",above=True)
        arr(p1x+6,p1y,p2x-6,p2y,AMBER,2); box("4-SEAM GRIP",cx,y+5,5.5,HexColor("#854F0B"))
    elif drill_id==71:
        c.setFillColor(GRASS); c.rect(x,y,w,h,fill=1,stroke=0)
        p1x,p1y=x+w*0.15,cy; p2x,p2y=x+w*0.85,cy
        dot(p1x,p1y,NAVY,lbl="P1",above=True); dot(p2x,p2y,GREEN,lbl="P2",above=True)
        arr(p1x+6,p1y,p2x-6,p2y,AMBER,2); lbl("FEET PLANTED",cx,cy+16,5.5,GRAY)
        box("NO STRIDE — HIPS AND TORSO",cx,y+5,5.5,HexColor("#854F0B"))
    elif drill_id==72:
        c.setFillColor(GRASS); c.rect(x,y,w,h,fill=1,stroke=0)
        p1x,p1y=x+w*0.15,cy; p2x,p2y=x+w*0.85,cy
        dot(p1x,p1y,NAVY,lbl="P1",above=True); dot(p2x,p2y,GREEN,lbl="P2",above=True)
        bounce(p1x+6,p1y,p2x-6,p2y,1,AMBER,2); box("ONE-HOP AT 1/3 DISTANCE",cx,y+5,5.5,HexColor("#854F0B"))
    elif drill_id==73:
        c.setFillColor(GRASS); c.rect(x,y,w,h,fill=1,stroke=0)
        p1x,p1y=x+w*0.15,cy; p2x,p2y=x+w*0.85,cy
        dot(p1x,p1y,NAVY,lbl="P1",above=True); dot(p2x,p2y,GREEN,lbl="P2",above=True)
        c.setFillColor(RED); c.roundRect(p2x-8,p2y+10,16,10,2,fill=1,stroke=0); lbl("TGT",p2x,p2y+13,5,CHALK,True)
        arr(p1x+6,p1y+2,p2x-8,p2y+14,AMBER,1.8); box("CALL THE TARGET — THEN THROW",cx,y+5,5.5,HexColor("#854F0B"))

    elif drill_id==74:
        r=dmd(); b=bases(r)
        route([(b["HM"][0],b["HM"][1]-8),(b["2B"][0]-6,b["2B"][1]),(b["1B"][0]+6,b["1B"][1]),(b["HM"][0]+6,b["HM"][1]-6)],AMBER,1.8)
        route([(b["HM"][0],b["HM"][1]-8),(b["3B"][0]+6,b["3B"][1]),(b["2B"][0],b["2B"][1]+6),(b["1B"][0]+6,b["1B"][1]),(b["HM"][0]+6,b["HM"][1]-6)],PURPLE,1.4)
        box("CONTINUOUS ROTATION — RACE THE CLOCK",cx,y+5,5.5,NAVY)
    elif drill_id==75:
        r=dmd(); b=bases(r); px2,py2=b["P"]; dot(px2,py2,NAVY,lbl="P",above=True)
        b1x,b1y=b["1B"]; dot(b1x+8,b1y,GREEN,lbl="1B",above=True)
        ball_x,ball_y=(px2+b1x)/2,(py2+b1y)/2+6; ball(ball_x,ball_y)
        c.setFillColor(RED); c.circle(ball_x,ball_y+14,6,fill=1,stroke=0); lbl("?",ball_x,ball_y+11,7,CHALK,True)
        box("BALL FIRST — BAG SECOND",cx,y+5,5.5,NAVY)
    elif drill_id==76:
        r=dmd(); b=bases(r); b1x,b1y=b["1B"]; b2x,b2y=cx+r*0.35,cy+r*0.2
        dot(b1x+8,b1y,GREEN,lbl="1B",above=True); dot(b2x,b2y,PURPLE,lbl="2B",above=True)
        ball_x,ball_y=(b1x+b2x)/2,(b1y+b2y)/2+4; ball(ball_x,ball_y)
        arc(b1x+6,b1y+3,ball_x,ball_y,GREEN,1.3,0.2); arc(b2x-6,b2y+3,ball_x,ball_y,PURPLE,1.3,0.2)
        dot(b["P"][0],b["P"][1],RED,lbl="P",above=True); arr(b["P"][0],b["P"][1],b1x-4,b1y+5,RED,1.5,True)
        box("BOTH GO — PITCHER COVERS 1ST",cx,y+5,5.5,NAVY)
    elif drill_id==77:
        r=dmd(); b=bases(r); b1x,b1y=b["1B"]; dot(b1x+8,b1y,GREEN,lbl="1B",above=True)
        ss_x,ss_y=b["2B"][0]-8,b["2B"][1]-4; dot(ss_x,ss_y,NAVY,lbl="SS",above=True)
        dot(b["P"][0],b["P"][1],RED,lbl="P",above=True)
        arr(b1x+4,b1y+3,ss_x-4,ss_y+3,AMBER,1.8); arr(ss_x+4,ss_y-4,b["P"][0]-3,b["P"][1]-3,AMBER,1.8)
        box("1B > SS COVERING 2ND > P",cx,y+5,5.5,NAVY)
    elif drill_id==78:
        r=dmd(); b=bases(r); dot(b["2B"][0],b["2B"][1]+10,PINK,4,lbl="PICKOFF",above=True)
        of_x,of_y=cx-r*0.3,cy+r*1.5; dot(of_x,of_y,GREEN,lbl="OF",above=True)
        arc(b["2B"][0],b["2B"][1]+8,of_x,of_y-4,AMBER,1.5,0.25)
        dot(cx-r*0.3,cy+r*0.55,NAVY,lbl="CUT",above=True); arr(of_x,of_y-6,cx-r*0.3+4,cy+r*0.6,GREEN,1.8)
        arr(cx-r*0.3+4,cy+r*0.5,b["3B"][0]+6,b["3B"][1]+4,RED,1.8)
        dot(b["P"][0],b["P"][1],RED,lbl="P"); dash(b["P"][0],b["P"][1],b["3B"][0],b["3B"][1],GRAY,1,(3,3))
        box("PITCHER SPRINTS TO BACK UP 3RD",cx,y+5,5.5,NAVY)

    elif drill_id==79:
        c.setFillColor(GRASS); c.rect(x,y,w,h,fill=1,stroke=0)
        for i,lb in enumerate(["HIGH KNEES","BUTTKICKS","GRAPEVINE","BOUND","BACKWARD"]):
            px2=x+w*(0.12+i*0.19); dot(px2,cy,NAVY if i%2==0 else GREEN,4)
            box(lb,px2,y+h*0.78,4.8,NAVY if i%2==0 else GREEN)
        box("ROTATE THROUGH ALL FIVE",cx,y+5,5.5,PINK)
    elif drill_id==80:
        r=dmd(); b=bases(r); b1x,b1y=b["1B"]
        dot(b1x-14,b1y+10,PINK,4,lbl="R",above=True)
        c.setStrokeColor(PINK); c.setLineWidth(1); c.setDash(2,2); c.line(b1x-14,b1y+10,b1x-6,b1y+14); c.setDash()
        arr(b1x-6,b1y+14,cx+r*0.15,cy+r*0.4,PINK,1.8); box("SHUFFLE — CROSSOVER — SPRINT",cx,y+5,5.5,PINK)
    elif drill_id==81:
        c.setFillColor(GRASS); c.rect(x,y,w,h,fill=1,stroke=0)
        dot(cx,cy,NAVY); c.setStrokeColor(AMBER); c.setLineWidth(2)
        p=c.beginPath(); p.moveTo(cx-4,cy+10); p.curveTo(cx+16,cy+18,cx+16,cy-6,cx+4,cy-10); c.drawPath(p,fill=0,stroke=1)
        ah(cx+8,cy-9,cx+4,cy-10,AMBER,2); lbl("SHOULDER TURN",cx,cy-22,5.5,AMBER,True)
        box("ARM ACROSS BODY — HIPS FOLLOW",cx,y+5,5.5,PINK)
    elif drill_id==82:
        r=dmd(); b=bases(r)
        route([(b["HM"][0],b["HM"][1]-6),(b["1B"][0],b["1B"][1]),(b["2B"][0],b["2B"][1]),(b["3B"][0],b["3B"][1]),(b["HM"][0]-4,b["HM"][1]-4)],GREEN,2)
        box("SQUARE TURNS — SHARP ANGLES",cx,y+5,5.5,PINK)
    elif drill_id==83:
        r=dmd(); b=bases(r); b1x,b1y=b["1B"]
        route([(b["HM"][0],b["HM"][1]-6),(b1x,b1y)],GREEN,2)
        cone_x,cone_y=(b1x+b["2B"][0])/2,(b1y+b["2B"][1])/2; c.setFillColor(AMBER); c.roundRect(cone_x-4,cone_y-4,8,10,2,fill=1,stroke=0)
        route([(b1x,b1y),(cone_x,cone_y)],AMBER,1.8); lbl("BREAK DOWN",cone_x+18,cone_y,5.5,AMBER,True)
        box("RUN THROUGH 1ST — READ THE THROW",cx,y+5,5.5,PINK)
    elif drill_id==84:
        r=dmd(); b=bases(r); b2x,b2y=b["2B"]
        route([(b["1B"][0],b["1B"][1]),(b2x-10,b2y-10)],GREEN,2)
        c.setStrokeColor(NAVY); c.setLineWidth(2); c.setDash(2,2); c.line(b2x-10,b2y-10,b2x,b2y); c.setDash()
        lbl("SLIDE",b2x-4,b2y-18,5.5,NAVY,True); box("BENT LEG — REAR END DOWN",cx,y+5,5.5,PINK)

    elif drill_id==85:
        hitbg(); hx,hy=cx+w*0.05,cy
        dot(hx,hy+8,NAVY,lbl="H",above=True); lbl("NO BALL — WALK THE PHASES",hx,hy-16,5.5,GRAY)
        box("RELAX — READY — STRIDE — SWING",cx,y+5,5.5,RED)
    elif drill_id==86:
        hitbg(); hx,hy=cx+w*0.05,cy
        dot(hx,hy+8,NAVY,lbl="H",above=True)
        c.setStrokeColor(AMBER); c.setLineWidth(1.5); c.setDash(2,2)
        c.line(hx-4,hy+2,hx-w*0.25,hy+h*0.2); c.setDash()
        lbl("WHOOSH",hx-w*0.2,hy+h*0.26,5.5,AMBER,True); box("LISTEN FOR THE SOUND'S DIRECTION",cx,y+5,5.5,RED)
    elif drill_id==87:
        hitbg(); hx,hy=cx+w*0.05,cy
        dot(hx,hy+8,NAVY,lbl="H",above=True); c.setFillColor(HexColor("#333333")); c.roundRect(hx-6,hy-2,12,26,4,fill=1,stroke=0)
        lbl("BAG",hx,hy-10,5,CHALK,True); box("SWING INTO THE BAG",cx,y+5,5.5,RED)
    elif drill_id==88:
        hitbg(); hx,hy=cx+w*0.05,cy; dot(hx,hy+8,NAVY,lbl="H",above=True)
        for tx,dl in [(hx-w*0.1,"OUT"),(hx,"MID"),(hx+w*0.1,"IN")]:
            c.setFillColor(AMBER); c.rect(tx-2,hy-4,4,14,fill=1,stroke=0); lbl(dl,tx,hy-14,5,AMBER,True)
        box("MOVE THE TEE BY PITCH LOCATION",cx,y+5,5.5,RED)
    elif drill_id==89:
        hitbg(); hx,hy=cx+w*0.05,cy; dot(hx,hy+8,NAVY,lbl="H",above=True)
        cx2,cy2=cx-w*0.3,cy-h*0.15; dot(cx2,cy2,RED,lbl="COACH")
        ball(cx2+10,cy2+6); arc(cx2+10,cy2+6,hx-8,hy+4,AMBER,1.5,0.25)
        box("STRIDE CUE — THEN THE TOSS",cx,y+5,5.5,RED)
    elif drill_id==90:
        c.setFillColor(GRASS); c.rect(x,y,w,h,fill=1,stroke=0)
        dot(cx-w*0.3,cy,NAVY,lbl="H",above=True)
        for i,fx in enumerate([cx,cx+w*0.15,cx+w*0.3]):
            dot(fx,cy+(i-1)*10,GREEN,4,lbl=f"F{i+1}")
        arr(cx-w*0.24,cy,cx-w*0.05,cy,AMBER,1.8); box("TAP IT — FIELD IT — REPEAT",cx,y+5,5.5,RED)
    elif drill_id==91:
        r=dmd(); b=bases(r); hx,hy=b["HM"]
        for gx,gl,col in [(hx-r*0.4,"OPPO",GREEN),(hx,"CTR",AMBER),(hx+r*0.4,"PULL",RED)]:
            dash(hx,hy+4,gx,cy+r*0.9,col,1,(3,3)); lbl(gl,gx,cy+r*0.95,5.5,col,True)
        box("HIT THROUGH THE RIGHT GAP",cx,y+5,5.5,RED)

    elif drill_id==92:
        hx,hy=cx,cy
        s=7; p=c.beginPath(); p.moveTo(hx-s,hy+s*0.4); p.lineTo(hx+s,hy+s*0.4); p.lineTo(hx+s,hy-s*0.3); p.lineTo(hx,hy-s*0.9); p.lineTo(hx-s,hy-s*0.3); p.close()
        c.setFillColor(HOME_CLR); c.setStrokeColor(LGRAY); c.setLineWidth(0.8); c.drawPath(p,fill=1,stroke=1)
        dot(hx,hy-h*0.32,AMBER,lbl="C",above=True)
        box("FEET — KNEES — LOWER GRADUALLY",cx,y+5,5.5,HexColor("#B8860B"))
    elif drill_id==93:
        dot(cx,cy,AMBER,lbl="C",above=True)
        c.setStrokeColor(AMBER); c.setLineWidth(1); c.setDash(2,2); c.line(cx-16,cy,cx-6,cy); c.line(cx+6,cy,cx+16,cy); c.setDash()
        lbl("STEP",cx-16,cy+10,5,AMBER); lbl("STEP",cx+16,cy+10,5,AMBER)
        box("STAY DOWN — SHORT CONTROLLED STEP",cx,y+5,5.5,HexColor("#B8860B"))
    elif drill_id==94:
        dot(cx,cy,AMBER,lbl="C",above=True); arr(cx,cy+6,cx,cy+h*0.28,AMBER,2)
        dash(cx,cy+h*0.3,cx+w*0.3,cy+h*0.45,GRAY,1,(3,3)); lbl("THROW",cx+w*0.3,cy+h*0.5,5.5,GRAY,True)
        box("CATCH — RISE — GRIP — THROW",cx,y+5,5.5,HexColor("#B8860B"))
    elif drill_id==95:
        dot(cx,cy,AMBER,lbl="C",above=True); dot(cx-w*0.25,cy+h*0.15,RED,lbl="COACH")
        bounce(cx-w*0.22,cy+h*0.12,cx-6,cy+6,1,AMBER,1.5); box("BLOCK IN FRONT — KEEP IT CLOSE",cx,y+5,5.5,HexColor("#B8860B"))
    elif drill_id==96:
        dot(cx,cy,AMBER,lbl="C",above=True); dot(cx-w*0.32,cy+h*0.05,RED,lbl="P",above=True)
        bounce(cx-w*0.28,cy+h*0.05,cx-6,cy+6,2,AMBER,1.5); lbl("LIVE BULLPEN",cx-w*0.15,cy+h*0.25,5.5,GRAY)
        box("BLOCK EVERY ONE IN THE DIRT",cx,y+5,5.5,HexColor("#B8860B"))
    elif drill_id==97:
        dot(cx,cy,AMBER,lbl="C",above=True); ball(cx+w*0.18,cy+h*0.15)
        arr(cx+2,cy+4,cx+w*0.15,cy+h*0.13,AMBER,1.8); arr(cx+w*0.15,cy+h*0.13,cx+w*0.35,cy-h*0.05,RED,1.8)
        lbl("1B",cx+w*0.37,cy-h*0.08,5.5,RED,True); box("SPRING — FIELD — THROW",cx,y+5,5.5,HexColor("#B8860B"))
    elif drill_id==98:
        dot(cx,cy,AMBER,lbl="C",above=True); ball(cx+w*0.22,cy-h*0.05)
        for lb,(lx,ly) in [("FRONT",(cx,cy-h*0.25)),("BACK",(cx,cy+h*0.3)),("1B",(cx+w*0.35,cy)),("3B",(cx-w*0.35,cy))]:
            lbl(lb,lx,ly,5.5,RED,True)
        box("CALL IT — SCOOP — FIND THE GRIP",cx,y+5,5.5,HexColor("#B8860B"))

    elif drill_id==99:
        c.setFillColor(GRASS); c.rect(x,y,w,h,fill=1,stroke=0); c.setFillColor(DIRT); c.circle(cx,cy,min(w,h)*0.22,fill=1,stroke=0)
        dot(cx,cy,PURPLE,lbl="P",above=True); lbl("HOLD 5 CT",cx,cy-h*0.22,5.5,GRAY)
        box("PIVOT FOOT — STRIDE LEG UP",cx,y+5,5.5,HexColor("#0E7C7B"))
    elif drill_id==100:
        c.setFillColor(GRASS); c.rect(x,y,w,h,fill=1,stroke=0); c.setFillColor(DIRT); c.circle(cx,cy,min(w,h)*0.22,fill=1,stroke=0)
        dot(cx,cy,PURPLE,lbl="P",above=True); lbl("T-POSITION",cx,cy-h*0.22,5.5,GRAY)
        box("BALANCE ON STRIDE FOOT ALONE",cx,y+5,5.5,HexColor("#0E7C7B"))
    elif drill_id==101:
        c.setFillColor(GRASS); c.rect(x,y,w,h,fill=1,stroke=0); c.setFillColor(DIRT); c.circle(cx,cy,min(w,h)*0.22,fill=1,stroke=0)
        dot(cx,cy,PURPLE,lbl="P",above=True); lbl("HOP x3",cx,cy-h*0.22,5.5,GRAY)
        box("HOP ON THE PIVOT FOOT",cx,y+5,5.5,HexColor("#0E7C7B"))
    elif drill_id==102:
        c.setFillColor(GRASS); c.rect(x,y,w,h,fill=1,stroke=0); c.setFillColor(DIRT); c.circle(cx,cy,min(w,h)*0.22,fill=1,stroke=0)
        dot(cx,cy,PURPLE,lbl="P",above=True); lbl("HOP x3",cx,cy-h*0.22,5.5,GRAY)
        box("HOP ON THE STRIDE FOOT",cx,y+5,5.5,HexColor("#0E7C7B"))
    elif drill_id==103:
        c.setFillColor(GRASS); c.rect(x,y,w,h,fill=1,stroke=0); c.setFillColor(DIRT); c.circle(cx,cy,min(w,h)*0.22,fill=1,stroke=0)
        dot(cx,cy,PURPLE,lbl="P",above=True); lbl("EYES CLOSED",cx,cy-h*0.22,5.5,GRAY)
        box("ALL 4 BALANCE DRILLS — NO SIGHT",cx,y+5,5.5,HexColor("#0E7C7B"))
    elif drill_id==104:
        c.setFillColor(GRASS); c.rect(x,y,w,h,fill=1,stroke=0); c.setFillColor(DIRT); c.circle(cx,cy,min(w,h)*0.22,fill=1,stroke=0)
        dot(cx,cy,PURPLE,lbl="P",above=True)
        for i,lb in enumerate(["STANCE","PIVOT","STRIDE","RELEASE"]):
            box(lb,x+w*(0.15+i*0.24),y+h*0.82,4.6,PURPLE if i%2==0 else NAVY)
        box("ONE PHASE AT A TIME",cx,y+5,5.5,HexColor("#0E7C7B"))
    elif drill_id==105:
        c.setFillColor(GRASS); c.rect(x,y,w,h,fill=1,stroke=0); dot(cx,cy,PURPLE,lbl="P",above=True)
        c.setStrokeColor(HexColor("#8B5A2B")); c.setLineWidth(2); c.line(cx+8,cy+4,cx+22,cy-8)
        lbl("STICK",cx+26,cy-8,5,HexColor("#8B5A2B")); box("LISTEN FOR THE WHIP SOUND",cx,y+5,5.5,HexColor("#0E7C7B"))
    elif drill_id==106:
        c.setFillColor(GRASS); c.rect(x,y,w,h,fill=1,stroke=0); dot(cx-w*0.3,cy,PURPLE,lbl="P",above=True)
        dot(cx+w*0.28,cy,RED,lbl="TGT",above=True); c.setStrokeColor(HexColor("#DDDDDD")); c.setLineWidth(2)
        c.line(cx-w*0.24,cy+4,cx+w*0.2,cy+2); arr(cx-w*0.1,cy+3,cx+w*0.2,cy+2,AMBER,1.5)
        box("SNAP THE TOWEL ONTO THE TARGET",cx,y+5,5.5,HexColor("#0E7C7B"))
    elif drill_id==107:
        c.setFillColor(GRASS); c.rect(x,y,w,h,fill=1,stroke=0); c.setFillColor(DIRT); c.circle(cx,cy,min(w,h)*0.22,fill=1,stroke=0)
        dot(cx,cy,PURPLE,lbl="P",above=True); lbl("HEEL UP + OUT",cx,cy-h*0.22,5.5,GRAY)
        box("PIVOT FOOT ROTATES ON FOLLOW-THROUGH",cx,y+5,5.5,HexColor("#0E7C7B"))
    elif drill_id==108:
        c.setFillColor(GRASS); c.rect(x,y,w,h,fill=1,stroke=0); c.setFillColor(DIRT); c.circle(cx,cy,min(w,h)*0.22,fill=1,stroke=0)
        dot(cx,cy,PURPLE,lbl="P",above=True); c.setFillColor(HexColor("#EEEEEE")); c.circle(cx-14,cy-10,4,fill=1,stroke=0)
        lbl("CUP",cx-14,cy-20,5,GRAY); box("CIRCLE THE FOOT OVER THE CUP",cx,y+5,5.5,HexColor("#0E7C7B"))
    elif drill_id==109:
        c.setFillColor(GRASS); c.rect(x,y,w,h,fill=1,stroke=0); dot(cx,cy,PURPLE,lbl="P",above=True)
        lbl("THUMBS DOWN",cx,cy-h*0.22,5.5,GRAY); box("HANDS SEPARATE — ARM UP EARLY",cx,y+5,5.5,HexColor("#0E7C7B"))
    elif drill_id==110:
        c.setFillColor(GRASS); c.rect(x,y,w,h,fill=1,stroke=0); dot(cx-w*0.3,cy,PURPLE,lbl="P",above=True)
        cone_x,cone_y=cx+w*0.1,cy; c.setFillColor(AMBER); c.roundRect(cone_x-4,cone_y-4,8,10,2,fill=1,stroke=0)
        bounce(cx-w*0.24,cy,cone_x,cone_y,1,AMBER,1.8); box("ONE-HOP JUST SHORT OF THE CONE",cx,y+5,5.5,HexColor("#0E7C7B"))
    else:
        r=dmd(); bases(r)
    c.restoreState()
