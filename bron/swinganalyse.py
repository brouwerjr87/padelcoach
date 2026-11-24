import json, math, sys
H=json.load(open('houdingen3d.json'))
def n(v): l=math.sqrt(sum(x*x for x in v)); return [x/l for x in v]
def dot(a,b): return sum(x*y for x,y in zip(a,b))
def cross(a,b): return [a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]]
def frame(p):
    r=n(p['racket']['richting']); v=p['racket']['vlak']; v=n([v[i]-dot(v,r)*r[i] for i in range(3)]); w=cross(r,v)
    return r,v,w
def kop(p): r=n(p['racket']['richting']); return [p['handR'][i]+0.3*r[i] for i in range(3)]
def rotas(a,b):
    A=frame(a); B=frame(b)
    # R = B * A^T ; kolommen
    R=[[sum(B[k][i]*A[k][j] for k in range(3)) for j in range(3)] for i in range(3)]
    tr=R[0][0]+R[1][1]+R[2][2]; ang=math.degrees(math.acos(max(-1,min(1,(tr-1)/2))))
    ax=[R[2][1]-R[1][2],R[0][2]-R[2][0],R[1][0]-R[0][1]]
    return ang, n(ax) if sum(x*x for x in ax)>1e-9 else [0,0,0]
def f(v): return '['+', '.join(f'{x:+.2f}' for x in v)+']'
SLAGEN=[('bandeja','bandeja-laden','bandeja-raak','bandeja-uit'),('vibora','vibora-laden','vibora-raak','vibora-uit'),
 ('bajada fh','bandeja-laden','bajada-raak','bajada-uit'),('bajada bh','bh-bajada-laden','bh-bajada-raak','bh-bajada-uit'),
 ('dejada','dejada-voor','dejada-raak','dejada-uit'),('fh volley','fh-volley-voor','fh-volley-raak','fh-volley-uit'),
 ('bh volley','bh-volley-voor','bh-volley-raak','bh-volley-uit'),('fh volley laag','fh-volley-laag-voor','fh-volley-laag-raak','fh-volley-laag-uit'),
 ('bh slice','bh-slice-voorbereiden','bh-slice-raak','bh-slice-uitzwaai'),('fh cortado','fh-laag-voorbereiden','fh-laag-raak','fh-laag-uitzwaai'),
 ('srv slice','srv-stuiten','srv-slice-raak','srv-uit'),('smash (vlak)','smash-laden','smash-raak','smash-uit')]
print('slag            | koppad laden->raak (x vooruit, y omhoog, z opzij) | raak->uit | blad bij raken (netkant) | draai laden->uit: hoek, as')
for naam,a,b,c in SLAGEN:
    A,B,C=H[a],H[b],H[c]
    v1=[kop(B)[i]-kop(A)[i] for i in range(3)]; v2=[kop(C)[i]-kop(B)[i] for i in range(3)]
    r,v,w=frame(B); s=1 if v[0]>=0 else -1; nb=[s*x for x in v]
    ang,ax=rotas(A,C)
    print(f'{naam:15s} | {f(v1)} | {f(v2)} | {f(nb)} | {ang:5.0f}°, as {f(ax)}')
