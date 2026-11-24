"""Opdrachten voor polsfix.py (stevige pols, geen arm door de romp, slice met open blad)."""
import json, itertools, math
H=json.load(open('houdingen3d.json'))
def n(v): l=math.sqrt(sum(x*x for x in v)); return [round(x/l,3) for x in v]
TH=[30,40,50,60]; PHc=[0,10,20,30,35]; PHp=[20,30,40,50]
def handvar(xs,ys,zs,romps,extra=None):
    out=[]
    for x,y,z,r in itertools.product(xs,ys,zs,romps):
        v={"handR":[x,y,z],"rompDraai":r,"heupDraai":round(r*0.5)}
        if extra: v.update(extra)
        out.append(v)
    return out
def balvar(xs,ys,zs,els):
    return [{"_bal":[x,y,z],"elleboogR":e} for x,y,z,e in itertools.product(xs,ys,zs,els)]
EL=[[-0.6,0.2,0.5],[-0.2,0.3,1],[0.2,0.1,1],[-0.5,-0.3,0.8]]
op=[]
# --- Bandeja: dienblad, raken voor-naast het hoofd, door met open blad, uitzwaai links op borsthoogte
op.append({"naam":"bandeja-laden","ths":TH,"phs":PHp,"N":[0.1,0.95,0.25],"T":[-0.95,0.25,0.1],"wT":0.6,"phMax":50})
op.append({"naam":"bandeja-raak","ths":TH,"phs":PHc,"N":[0.848,0.423,-0.318],"T":[-0.2,0.85,0.45],"wT":0.2,"iter":4,
  "varianten":balvar((0.5,0.65),(1.75,1.85),(0.5,0.65),EL)})
op.append({"naam":"bandeja-door","ths":TH,"phs":PHc,"N":n([0.55,0.75,-0.35]),"T":n([0.35,0.6,-0.7]),"wT":0.3,
  "varianten":handvar((0.65,0.8),(1.4,1.5),(0.1,0.25),(25,10))})
op.append({"naam":"bandeja-uit","ths":TH,"phs":[0,10,20,30],"N":n([0.3,0.85,-0.4]),"wN":0.5,"T":n([0.45,-0.1,-0.88]),"wT":0.6,
  "varianten":handvar((0.75,0.85,0.95),(1.15,1.25),(-0.2,-0.05,0.1),(-10,-25,-40),{"elleboogR":None})+handvar((0.8,0.9),(1.2,),(-0.1,0.05),(-15,-30),{"elleboogR":[0.2,-0.6,0.8]})})
# --- Víbora: verder geladen, raken naast het hoofd op hoofdhoogte, samoeraislag naar de linkerheup
op.append({"naam":"vibora-laden","ths":TH,"phs":PHp,"N":n([0.3,0.7,0.65]),"T":n([-0.7,0.65,0.3]),"wT":0.5,"phMax":50,
  "varianten":[{"handR":[x,y,z],"elleboogR":e} for x,y,z,e in itertools.product((-0.45,-0.3),(1.6,1.72),(0.12,0.3),([-0.6,0.2,0.5],[-0.2,0.6,0.8],[0,0.3,1]))]})
op.append({"naam":"vibora-raak","ths":TH,"phs":PHc,"N":[0.727,0.5,-0.472],"T":n([-0.1,0.7,0.7]),"wT":0.3,"iter":4,"zet":{"heupDraai":15,"rompDraai":20},
  "varianten":balvar((0.25,0.4),(1.58,1.66),(0.66,0.78),EL)})
op.append({"naam":"vibora-door","van":"vibora-raak","ths":TH,"phs":PHc,"N":n([0.5,0.8,-0.35]),"T":n([0.25,0.45,0.85]),"wT":0.3,
  "zet":{"heupDraai":5,"rompDraai":0,"bal":None,"elleboogR":None},"varianten":handvar((0.7,0.85),(1.3,1.4),(0.15,0.3),(0,-10))})
op.append({"naam":"vibora-uit","ths":TH,"phs":[-10,0,10,20],"N":[0.3,0.9,0.2],"wN":0.2,"T":[-0.2,-0.6,-0.75],"wT":1,
  "varianten":handvar((0.8,0.9),(0.95,1.05),(-0.35,-0.2),(-20,-35))})
# --- Bajada forehand en backhand
b=H['bajada-raak']['bal']
op.append({"naam":"bajada-raak","ths":TH,"phs":PHc,"N":[0.871,0.423,-0.25],"T":n([-0.2,0.85,0.45]),"wT":0.2,"iter":4,
  "varianten":balvar((b[0]-0.05,b[0]+0.1),(b[1]-0.1,b[1],b[1]+0.08),(b[2]-0.1,b[2],b[2]+0.1),EL)})
op.append({"naam":"bajada-uit","ths":TH,"phs":[0,10,20,30],"N":n([0.3,0.85,-0.4]),"wN":0.3,"T":n([0.6,-0.4,-0.7]),"wT":0.8,
  "varianten":handvar((0.85,0.95),(0.95,1.1),(-0.2,0.0),(-10,-25))})
b=H['bh-bajada-raak']['bal']
op.append({"naam":"bh-bajada-raak","backhand":True,"ths":TH,"phs":[-35,-30,-20,-10,0,10,20,30],"N":[0.871,0.423,-0.25],"T":n([-0.3,0.7,-0.65]),"wT":0.2,"iter":4,
  "varianten":[{"_bal":[x,y,z],"elleboogR":e} for x,y,z,e in itertools.product((b[0]-0.05,b[0]+0.08),(b[1]-0.08,b[1]+0.05),(b[2],b[2]+0.1),(None,[0.3,-0.5,-0.8],[-0.3,0.2,-1],[0.2,0.5,-0.8]))]})
# --- Smash: uitzwaai langs het lichaam zonder door de romp
op.append({"naam":"smash-uit","ths":TH,"phs":[-10,0,10,20,30],"N":[0,-1,0],"wN":0.1,"T":n([0.3,-0.8,-0.5]),"wT":1,
  "varianten":handvar((0.75,0.9),(0.85,1.0),(-0.35,-0.2),(-20,-40))})
# --- Backhandvolley: korte stoot, stevige pols, blad licht open
VV={"bh-volley-voor":[{"handR":[x,y,z],"elleboogR":e} for x,y,z,e in itertools.product((0.2,0.32),(1.15,1.25),(-0.5,-0.62),(None,[0.3,-0.5,-0.8],[-0.2,0,-1]))]}
for k,N,T in [("bh-volley-voor",n([0.8,0.45,-0.35]),n([-0.3,0.75,-0.6])),("bh-volley-raak",n([0.85,0.35,-0.4]),n([0.0,0.65,-0.75])),("bh-volley-uit",n([0.8,0.45,-0.4]),n([0.35,0.5,-0.8]))]:
    op.append({"naam":k,"backhand":True,"ths":[40,50,60,70],"phs":[-30,-20,-10,0,10,20],"N":N,"T":T,"wT":0.4,
               **({"bal":H[k]['bal']} if H[k].get('bal') else {}), **({"varianten":VV[k]} if k in VV else {})})
json.dump(op,open('polsopdrachten.json','w'))
print(len(op),'opdrachten')
