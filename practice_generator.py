#!/usr/bin/env python3
"""
WRENTHAM 10/9U — Practice Plan PDF Generator
=============================================
52 drills across 6 categories. Auto-detects layout:
  - 1-4 drills  -> 2x2 single page
  - 5-6 drills  -> 2x3 single page
  - 7+ drills   -> 2x2 multi-page
Empty card slots automatically become lined notes blocks.
No footer. No date. Clean print-ready output.

USAGE:
  python wrentham_generator.py "Theme Name" "id:mins,id:mins,..."
  e.g. python wrentham_generator.py "Stealing & Situational" "33:12,34:12,36:8,37:10"

  Or import and call directly:
  from wrentham_generator import generate_practice_plan
  generate_practice_plan("Theme", [(33,12),(34,12)], "output.pdf")

OUTPUT: /mnt/user-data/outputs/wrentham_practice_plan.pdf (or custom path)

RESTORE AFTER CONTAINER RESET:
  pip install reportlab --break-system-packages -q
  # then run this file or fetch from GitHub
"""
import sys, math
from datetime import date
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, white
from reportlab.lib.units import inch
from reportlab.pdfbase.pdfmetrics import stringWidth

CAT_COLORS = {
    "infield":"#132448","outfield":"#1A6B3C","throwing":"#854F0B",
    "situational":"#534AB7","baserunning":"#993556","hitting":"#B31B1B",
}

DRILLS = {
    1:{"name":"Short Hops","cat":"infield","game":False,"desc1":"Bounce short hops 8-10 ft, work glove angles and soft hands","desc2":"Focus on glove position and late squeeze timing","cues":["Get low early — don't wait for the hop","Glove out front, not tucked","Soft hands — squeeze late"]},
    2:{"name":"Rapid-Fire Grounders","cat":"infield","game":False,"desc1":"Coach fires rapid-fire grounders to 3 infield positions simultaneously","desc2":"Forces quick feet and transitions under pressure","cues":["Charge the ball — don't wait","Field at your left foot","Come up throwing — no pause"]},
    3:{"name":"4-Corner Relay","cat":"throwing","game":False,"desc1":"Ball moves around all four bases as fast as possible. Race the clock","desc2":"Emphasizes catch-and-turn efficiency at each base","cues":["Catch and turn in one motion","Step toward target","Strong crow hop before throwing"]},
    4:{"name":"Knockout","cat":"throwing","game":True,"desc1":"Players queue at the mound. One throw each to hit the target. Miss = eliminated","desc2":"Competitive pressure throwing — last player standing wins","cues":["Pick a spot on the target","Full effort every rep","Compete — no lazy throws"]},
    5:{"name":"Drop Step & Go","cat":"outfield","game":False,"desc1":"OFs read a ball going over their head. Drop-step and run to the spot","desc2":"Builds hip turn and angle-run mechanics for deep balls","cues":["Drop step first — never backpedal","Turn hips — run on angle","Get to the spot before the ball"]},
    6:{"name":"Do-or-Die","cat":"outfield","game":True,"desc1":"Ball rolled in front of OF. Runner on 3rd, 1 out. Charge, field on the run, throw home","desc2":"Game-speed decision making on the do-or-die play","cues":["Charge hard — never slow down","Field on throwing-side foot","Throw a line drive, not a rainbow"]},
    7:{"name":"Cutoff Relay","cat":"situational","game":False,"desc1":"Full relay: OF to cutoff to home. Communication and relay footwork emphasized","desc2":"Everyone must know their position in the relay chain","cues":["Cutoff: hands up, give OF a target","Square up fast — one motion","Call it — silence loses runs"]},
    8:{"name":"Double Play Footwork","cat":"situational","game":False,"desc1":"Teach the 2B pivot. Slow reps first, full speed second. SS and 2B alternate","desc2":"Bag contact, pivot efficiency, and getting off the bag","cues":["Get to the bag early","Touch the corner — not the top","Get off the bag as fast as you got on"]},
    9:{"name":"Crow Hop Station","cat":"throwing","game":False,"desc1":"Isolated throwing mechanics. Gather-hop-throw pattern. Pairs, 40-50 ft","desc2":"Build proper weight transfer and hip lead before the throw","cues":["Gather weight on back foot","Short hop into the throw","Lead with hip — finish over front foot"]},
    10:{"name":"First Step / Reaction","cat":"outfield","game":False,"desc1":"Coach hits without cue. OFs react with correct first step in 1-2 beats","desc2":"Pre-pitch stance and instant first-step read development","cues":["Weight on balls of feet","Crossover wide, drop step deep","React with feet, not eyes"]},
    11:{"name":"Rundown (Pickle)","cat":"situational","game":True,"desc1":"Fielders aim to get out in 1 throw. Runner tries to extend the rundown","desc2":"Teaches run-hard, throw-ahead discipline in rundown situations","cues":["Run hard at runner — make them commit","Throw ahead of runner","Never throw behind"]},
    12:{"name":"Tag-Up Race","cat":"baserunning","game":True,"desc1":"Fly ball to OF, runner on 3rd tags up and races to score against live throw","desc2":"Foot contact, timing, and aggressive read off the catch","cues":["Foot on base — don't leave early","Sprint the moment they catch it","Always slide if it's close"]},
    13:{"name":"Leads & Reads","cat":"baserunning","game":False,"desc1":"Primary and secondary leads, reading the pitcher, post-pitch reactions","desc2":"Builds the habit of taking correct lead lengths by situation","cues":["2 steps primary lead","Shuffle 2 steps on pitch","Dirt ball: go — don't hesitate"]},
    14:{"name":"Infield Triangle","cat":"infield","game":False,"desc1":"SS, 2B, 1B work base coverage and communication on steals and bunts","desc2":"Pre-pitch communication so everyone knows their assignment","cues":["Talk before the pitch — not during","SS: signal who has 2nd","Everyone has a job — no standing still"]},
    15:{"name":"Bucket Challenge","cat":"throwing","game":True,"desc1":"Throw to hit a bucket from increasing distances. Win = advance to next distance","desc2":"Accuracy focus with competitive distance progression","cues":["Pick the bucket — aim small","Four-seam grip every throw","Accuracy over velocity"]},
    16:{"name":"Fly Ball Communication","cat":"outfield","game":False,"desc1":"Two OFs chase the same ball. Call rules, back-off rules, priority system","desc2":"Builds voice habits and outfield priority understanding","cues":["Call it LOUD and early","CF beats corner OFs — always","Peel off when you hear the call"]},
    17:{"name":"Soft Toss","cat":"hitting","game":False,"desc1":"Partner feeds from 45 degree angle. Load, hip turn, contact point. High-rep","desc2":"Reinforce load timing and hip rotation through the zone","cues":["Load before toss arrives","Short to ball, long through it","Stay back — don't lunge"]},
    18:{"name":"Bunt Coverage","cat":"situational","game":False,"desc1":"Everyone has a role. P charges, 3B reads, 1B covers 1st, 2B covers 2nd","desc2":"Full defensive assignment execution on bunt situations","cues":["P: off mound fast","Call the base before you throw","3B: read then decide"]},
    19:{"name":"Tennis Ball Reaction","cat":"outfield","game":True,"desc1":"Coach throws tennis balls from 15-20 ft without warning. React and catch","desc2":"Hand-eye and reaction speed in a low-stakes competitive format","cues":["Stay on your toes","Expect every ball","Hands out front"]},
    20:{"name":"Game Situation Gauntlet","cat":"situational","game":False,"desc1":"Coach announces scenario, hits ball, full defense reacts as a real game","desc2":"Debrief each play — understanding the why matters as much as execution","cues":["Know the situation before every pitch","Say the play out loud","Back up every throw"]},
    21:{"name":"Goalie","cat":"infield","game":True,"desc1":"Two gloves as goalposts 6 ft apart. Coach at 15 yds. Field clean or eliminated","desc2":"Stop-the-ball-first mentality in a competitive elimination format","cues":["Get low and stay wide","Stop the ball first — don't reach","Glove down, body behind it"]},
    22:{"name":"Relay Race Throw","cat":"throwing","game":True,"desc1":"Two teams, lines 10 yds per player. Ball relays front to back. First done wins","desc2":"Speed and accuracy under team competition pressure","cues":["Pivot and turn in one motion","Strong accurate throw — not just fast","Catch and go — no pause"]},
    23:{"name":"Wide Receiver","cat":"outfield","game":True,"desc1":"OFs run downfield routes. Coach throws — track the ball over the shoulder","desc2":"Builds over-the-shoulder catch and route-running tracking skills","cues":["Run the route first — don't watch early","Turn your head at the spot","Eyes on ball all the way in"]},
    24:{"name":"Belly Ups","cat":"infield","game":True,"desc1":"Players lie flat in infield. Coach hits grounder — get to feet and throw to 1st","desc2":"Explosive recovery and composure when compromised","cues":["Get to feet fast — don't crawl","Settle your feet before the throw","Strong throw — you're already compromised"]},
    25:{"name":"King of the Hill","cat":"infield","game":True,"desc1":"Coach hits grounders to ranked line. Error = move down. Clean play = hold or advance","desc2":"Field clean AND throw strong to hold the top spot","cues":["Attack the ball","Field it clean AND throw it strong","No easy reps at the front"]},
    26:{"name":"Scramble","cat":"infield","game":True,"desc1":"Field and throw 5 consecutive grounders to 1B as fast and accurately as possible","desc2":"Low-reset quick-feet reps under speed pressure","cues":["Stay low between reps","Quick feet — don't fully reset","Grip fast — don't fuss"]},
    27:{"name":"3-2-1 Run","cat":"baserunning","game":True,"desc1":"Runner races home to 2nd before 3B delivers 3 throws to 2nd","desc2":"First base corner mechanics and turn-and-go aggression","cues":["Hit 1B on the inside corner","Explode out of the turn","Head down all the way"]},
    28:{"name":"Doubles","cat":"baserunning","game":True,"desc1":"Batter tries to leg out a double while OF throws them out at 2nd","desc2":"Aggressive first-base turn and read into 2nd base","cues":["Round 1st aggressively","Head up approaching 2nd — read the throw","Slide hard"]},
    29:{"name":"Arizona","cat":"situational","game":True,"desc1":"3 teams: 1 bats, 2 play defense. Batter racks up total bases. Defense races to track","desc2":"Count total bases not just outs — keeps offense aggressive","cues":["Offense: run hard — pressure defense","Defense: communicate on contact","Count total bases not just outs"]},
    30:{"name":"Bunt-Off","cat":"situational","game":True,"desc1":"Team competition — best bunts by location. 3B line vs 1B line zones","desc2":"Directional bunt execution with zone scoring","cues":["Top half of the ball — no pop-ups","Angle the bat early","1B and 3B lines are different targets"]},
    31:{"name":"Ultimate Baseball","cat":"throwing","game":True,"desc1":"Football-style: advance ball into endzone by throwing and catching only","desc2":"Move fast after catch — pivot only, drops turn it over","cues":["Find the open teammate","Catch with two hands — drops turn it over","Move fast after catch — pivot only"]},
    32:{"name":"Pinball","cat":"infield","game":True,"desc1":"Coach hits grounders to ranked line. Errors move you down. Hold the top","desc2":"Pressure reps — embrace the competition or fall in the rankings","cues":["Attack the ball — don't wait","Glove work AND throw both count","Pressure makes you better — embrace it"]},
    33:{"name":"Steal Coverage","cat":"situational","game":False,"desc1":"Full-team live rep. Catcher throws, SS and 2B communicate coverage via signals","desc2":"Pitcher holds runner, 1B communicates, baserunners actually run. Rotate everyone through","cues":["Signal before the pitch — not after","One person calls it, other confirms","Catcher: hit your cutoff, not a lob"]},
    34:{"name":"First & Third Defense","cat":"situational","game":True,"desc1":"Offense on 1st and 3rd. Defense executes one of three reads: throw through, cut and fire home, or fake","desc2":"SS covers bag, 2B reads runner at 3rd. Score it — hardest play in youth baseball","cues":["SS: get to the bag early, no drift","2B: eyes on 3rd runner — communicate the read","Catcher: call the play before the pitch"]},
    35:{"name":"First to Third","cat":"baserunning","game":True,"desc1":"Live OF reads. Coach hits ball to OF while runner on 1st reads the defender","desc2":"Rule taught: if OF moves more than one step laterally, runner goes to 3rd. Score by team","cues":["Read the outfielder, not the ball","One lateral step = you go","Round 2nd wide — don't cheat the turn"]},
    36:{"name":"Wild Pitch Advance","cat":"baserunning","game":True,"desc1":"Runner on 2nd or 3rd takes secondary lead as coach rolls a ball past the catcher","desc2":"Team scores for advances, catcher scores for runners held or thrown out","cues":["Secondary lead timing is everything","React before the ball stops rolling","Slide — never assume you're safe"]},
    37:{"name":"Cover Two Live","cat":"situational","game":True,"desc1":"Runner on 1st, coach hits grounder to SS or 2B side. They communicate who fields and who covers","desc2":"Runner tries to advance. Out = defense point, safe = offense point","cues":["Call it before the pitch — not during","SS fields right side, 2B fields left side default","No ball, get to the bag fast"]},
    38:{"name":"Cutoff Decision","cat":"situational","game":False,"desc1":"Full relay scenario with runner in motion. Cutoff reads: cut and fire home, let it go, or redirect","desc2":"Coach calls different base situations before each rep — decision reps are the whole point","cues":["Cutoff: hands up early, make yourself a target","Read the runner before you decide","Call your decision loud — no silent cuts"]},
    39:{"name":"Bunt Scramble","cat":"situational","game":True,"desc1":"Two teams. Offense bunts every pitch. Defense executes full coverage rotation","desc2":"Fair bunt safe = offense point, out = defense point, pop-up = defense gets two","cues":["Defense: assignments before pitch — always","P: off mound at first movement","Call the base before you field it"]},
    40:{"name":"Oppo Tee Challenge","cat":"hitting","game":True,"desc1":"Outside tee placement, ball set deep in the zone. Hit 3 consecutive balls to the opposite field","desc2":"One point per clean oppo hit — pull it foul and you're out of rotation","cues":["Let the ball get deep — don't reach","Stay through the ball to the opposite gap","Hands inside, barrel outside"]},
    41:{"name":"Two-Tee Location Game","cat":"hitting","game":True,"desc1":"Two tees set inside and outside. Coach calls the location, hitter adjusts and hits correct tee","desc2":"Wrong tee = out of rotation. Builds plate coverage and pitch recognition in the box","cues":["React to the call — not the guess","Inside: pull angle, Outside: oppo angle","Adjust your feet, not just your hands"]},
    42:{"name":"Situation Sprint","cat":"situational","game":True,"desc1":"Coach calls scenario out loud: 'Runner on 2nd, single to right... GO.' No pre-setup","desc2":"Full team. Offense runs, defense rotates and executes the correct play. Score it live","cues":["Know your assignment before the ball lands","Talk — silence is the same as wrong","This is a test of every rep you've done all season"]},
    43:{"name":"Four-Outfield Alignment","cat":"outfield","game":True,"desc1":"Full 4-OF setup. Coach calls the situation and OFs set positioning as a unit before the ball is hit","desc2":"Emphasis on gap coverage, priority calls between LCF and RCF, and how alignment shifts by hitter type","cues":["LCF and RCF must negotiate the middle — CF no longer owns it","Call your zone before the pitch, not after contact","Scored: ball drops uncalled = offense point"]},
    44:{"name":"Shade & Depth","cat":"outfield","game":False,"desc1":"Coach calls a batter type and count. OFs adjust positioning before the pitch — no ball hit","desc2":"Pure pre-pitch IQ rep. Builds the habit of reading situations and moving before the ball is in play","cues":["Pull hitter: shade 10 steps toward the pull side","2-strike count: creep in two steps","Talk to each other — everyone adjusts together"]},
    45:{"name":"Long Toss Ladder","cat":"throwing","game":True,"desc1":"Pairs start at 30ft and step back every 3 clean exchanges. Max distance at the end wins","desc2":"Builds arm strength and crow hop consistency under distance pressure over a full session","cues":["Crow hop every throw — no flat feet","Arc it slightly at distance — don't muscle it flat","3 clean in a row to step back, one bounce and you hold"]},
    46:{"name":"Accuracy Ladder","cat":"throwing","game":True,"desc1":"Two targets at 30, 45, and 60ft. Hit the target to advance. Miss and hold. Race your partner","desc2":"Competitive accuracy format — forces grip focus and follow-through at each distance","cues":["Pick a specific spot on the target — aim small","Four-seam grip every rep","Follow through to the target — don't pull off early"]},
    47:{"name":"Score From Second","cat":"situational","game":True,"desc1":"Runner on 2nd, single to the OF. Runner reads the hit and makes the turn-or-hold decision at 3rd","desc2":"Scored by team. Teaches the read at 3rd base coach and the decision to go or stop","cues":["Read the ball off the bat — don't wait for the hop","Round 3rd wide if you're going","If you stop at 3rd, stop hard — don't drift past the bag"]},
    48:{"name":"Backup Positioning","cat":"situational","game":False,"desc1":"Coach hits to various spots. Every player not fielding sprints to their correct backup position","desc2":"Coach freezes the play and checks positioning. Pure team IQ — teaches who backs up what","cues":["If you don't have the ball, you have a backup assignment","P backs up every throw to a base — always","Never watch the play standing still"]},
    49:{"name":"OF Cutoff Alignment","cat":"situational","game":False,"desc1":"Ball hit to left, center, or right. Cutoff man aligns himself between OF and the target base","desc2":"OF holds the ball until cutoff is properly set. Teaches the alignment piece most teams never practice","cues":["Cutoff: get in line between OF arm and the base","Hands up — give the OF a target to throw to","Read the throw early — cut or let it go, commit loud"]},
    50:{"name":"Dirt Ball Read","cat":"baserunning","game":True,"desc1":"Runner on 3rd, 3-2 count, full go. Coach bounces pitch in the dirt. Runner reads and goes or holds","desc2":"Catcher scored for blocks and throws, runner scored for clean advances","cues":["Go on contact with the dirt — don't wait to see the block","If catcher blocks it clean and close, slam the brakes","Never get thrown out at home on a dirt ball — make them earn it"]},
    51:{"name":"Gap Shot","cat":"baserunning","game":True,"desc1":"Ball hit to the gap with runner on 1st. Runner reads the hit, rounds 2nd aggressively, decides at 3rd","desc2":"Full OF plays out live. Scored: runner scores = offense point, thrown out = defense point","cues":["Read gap off the bat — go immediately, don't hesitate","Round 2nd at full speed, look up at 3rd coach coming into the bag","Aggressive default: when in doubt, keep running"]},
    52:{"name":"Front Toss Battle","cat":"hitting","game":True,"desc1":"Two hitters compete head to head, coach front-tossing 5 pitches each. Scored by zone","desc2":"Oppo = 2pts, up the middle = 1pt, pull = 0. Forces intentional hitting under real competition pressure","cues":["Pick your zone before the toss — commit to it","Stay back and let the ball travel to your spot","Oppo isn't weak — it's disciplined"]},
}

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
    else:
        r=dmd(); bases(r)
    c.restoreState()


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
        c.setFillColor(HexColor("#132448")); c.setFont("Helvetica-Bold",8); c.drawCentredString(cx_card+cw-br-6,cy_card+ch-HDR/2-3,str(did))
        c.setFillColor(white); c.setFont("Helvetica-Bold",9)
        c.drawString(cx_card+8,cy_card+ch-14,wt(drill["name"].upper(),"Helvetica-Bold",9,cw-br*2-20)[0])
        ty=cy_card+ch-HDR-13; c.setFillColor(color); c.setFont("Helvetica-Bold",7); c.drawString(cx_card+TP,ty,cat.upper())
        if drill["game"]:
            gw=48; c.setFillColor(white); c.setStrokeColor(white); c.roundRect(cx_card+cw-gw-6,ty-2,gw,12,3,fill=1,stroke=0)
            c.setFillColor(HexColor("#132448")); c.setFont("Helvetica-Bold",6.5); c.drawCentredString(cx_card+cw-gw/2-6,ty+2,"GAME-BASED")
        dh=ch*0.30; dy=cy_card+ch-HDR-15-dh
        draw_diagram(c,cx_card+4,dy,cw-8,dh,did)
        desc_y=dy-12; c.setFillColor(HexColor("#444444")); c.setFont("Helvetica",7)
        for text in [drill["desc1"],drill["desc2"]]:
            for line in wt(text,"Helvetica",7,TW): c.drawString(cx_card+TP,desc_y,line); desc_y-=9
        cy2=desc_y-8; c.setFillColor(HexColor("#132448")); c.setFont("Helvetica-Bold",7)
        c.drawString(cx_card+TP,cy2,"COACHING CUES"); c.setFont("Helvetica",7); c.setFillColor(HexColor("#333333")); cy2-=9
        for cue in drill["cues"][:3]:
            for line in wt(f"\u2022  {cue}","Helvetica",7,TW): c.drawString(cx_card+TP,cy2,line); cy2-=9

    content_top=PAGE_H-HEADER_H-8
    warmup_y=content_top-WARMUP_H
    col_w=(PAGE_W-2*MARGIN-CARD_MARGIN)/2

    if 5<=n<=6:
        ROWS=3; avail_h=warmup_y-BOTTOM_PAD-CARD_MARGIN; card_h=(avail_h-2*CARD_MARGIN)/ROWS
        draw_header(1); draw_warmup(MARGIN,warmup_y,PAGE_W-2*MARGIN,WARMUP_H)
        all_pos=[]
        for row in range(ROWS):
            for col in range(2):
                all_pos.append((MARGIN+col*(col_w+CARD_MARGIN), warmup_y-CARD_MARGIN-(row+1)*(card_h+CARD_MARGIN)+CARD_MARGIN))
        for i,(did,mins) in enumerate(drill_ids_times): draw_card(did,mins,*all_pos[i],col_w,card_h)
        for i in range(n,ROWS*2): draw_notes(*all_pos[i],col_w,card_h)
    else:
        avail_h=warmup_y-BOTTOM_PAD-CARD_MARGIN; card_h=(avail_h-CARD_MARGIN)/2
        full_h=(content_top-BOTTOM_PAD-CARD_MARGIN-CARD_MARGIN)/2
        pn=1; draw_header(pn); draw_warmup(MARGIN,warmup_y,PAGE_W-2*MARGIN,WARMUP_H)
        p1=[(MARGIN+col*(col_w+CARD_MARGIN), warmup_y-CARD_MARGIN-(row+1)*(card_h+CARD_MARGIN)+CARD_MARGIN) for row in range(2) for col in range(2)]
        ex=[(MARGIN+col*(col_w+CARD_MARGIN), content_top-CARD_MARGIN-(row+1)*(full_h+CARD_MARGIN)+CARD_MARGIN) for row in range(2) for col in range(2)]
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
            if lf!=0:
                for s in range(lf,4): draw_notes(*ex[s],col_w,full_h)
    c.save()

if __name__=="__main__":
    if len(sys.argv)>=3:
        pairs=sys.argv[2].split(",")
        drill_list=[(int(p.split(":")[0]),int(p.split(":")[1])) for p in pairs]
        generate_practice_plan(sys.argv[1],drill_list,"/mnt/user-data/outputs/wrentham_practice_plan.pdf")
    else:
        generate_practice_plan("Test",[(26,10),(20,12),(33,12),(47,10),(36,10),(4,10)],"/mnt/user-data/outputs/wrentham_practice_plan.pdf")
