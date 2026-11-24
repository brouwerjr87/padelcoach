"""Voegt tussenhoudingen toe waar de app de onderarm de lange weg rond laat draaien (of buiten het anatomische bereik).

python3 tussenfix.py tid:level [tid:level ...]
Werkt technieken.json en houdingen3d.json bij; bouwt diag/index.html opnieuw na elke toevoeging.
"""
import json, sys, math, subprocess, threading, http.server, functools
from playwright.sync_api import sync_playwright
from sleutels import sleutels
D = 'diag'
srv = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(http.server.SimpleHTTPRequestHandler, directory=D)); srv.RequestHandlerClass.log_message = lambda *a: None
threading.Thread(target=srv.serve_forever, daemon=True).start()
U = f"http://127.0.0.1:{srv.server_port}/index.html"

def bouw():
    subprocess.run(['node', 'bouw.js', D + '/index.html', D + '/index.html', 'technieken.json', 'houdingen3d.json'], check=True, capture_output=True)

SCAN = r"""()=>{const R=window.__rig,e=window.__mot,K=v=>{const l=Math.hypot(...v)||1;return v.map(x=>x/l)},S=(a,b)=>a.map((x,i)=>x-b[i]);
const out=[];for(let t=0;t<=e.totaal;t+=15){const s=R.Vt(e,t),p=s.pose||s,j=R.vt(p);out.push([t,R.Ue(j.schouderR,j.elleboogR,j.handR,j.palm,1)])}return out}"""

MAAK = r"""([A,B,f,pA,pB,thD,phD])=>{const R=window.__rig,K=e=>{const l=Math.hypot(...e)||1;return e.map(x=>x/l)},
 S=(a,b)=>a.map((x,i)=>x-b[i]),Ad=(a,b)=>a.map((x,i)=>x+b[i]),M=(a,s)=>a.map(x=>x*s),D=(a,b)=>a.reduce((s,x,i)=>s+x*b[i],0),
 X=(a,b)=>[a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]],rad=x=>x*Math.PI/180;
 const p=JSON.parse(JSON.stringify(R.yt(A,B,f)));delete p.arm;p.bal=null;p.handL=(A.handL==='hals'&&B.handL==='hals')?'hals':p.handL;
 const doel=pA+(pB-pA)*f;let best=null;
 for(let it=0;it<8;it++){const j=R.vt(p),a=K(S(j.handR,j.elleboogR));const q1=Math.abs(a[1])<.9?K(X(a,[0,1,0])):K(X(a,[1,0,0])),q2=X(a,q1);
  const th=rad(thD),ph=rad(phD),af=[Math.cos(ph)*Math.cos(th),Math.cos(ph)*Math.sin(th),Math.sin(ph)],bf=Math.abs(af[2])<.9?K(X(af,[0,0,1])):K(X(af,[1,0,0])),cf=X(af,bf);
  best=null;for(let r=0;r<360;r+=2){const b=Ad(M(q1,Math.cos(rad(r))),M(q2,Math.sin(rad(r)))),c=X(a,b),col=i=>Ad(Ad(M(a,af[i]),M(b,bf[i])),M(c,cf[i]));
   const t=col(0),n=col(2),pro=R.Ue(j.schouderR,j.elleboogR,j.handR,n,1);if(isNaN(pro))continue;const sc=Math.abs(pro-doel);if(!best||sc<best.sc)best={sc,t,n,pro}}
  if(!best)break;p.racket={richting:best.t.map(x=>+x.toFixed(3)),vlak:best.n.map(x=>+x.toFixed(3))}}
 const j=R.vt(p);return{pose:p,pro:R.Ue(j.schouderR,j.elleboogR,j.handR,j.palm,1),doel}}"""

PRO = r"""(P)=>{const R=window.__rig,j=R.vt(P);return R.Ue(j.schouderR,j.elleboogR,j.handR,j.palm,1)}"""

def slecht(samples):
    vorig = None
    for t, pro in samples:
        if pro is None or (isinstance(pro, float) and math.isnan(pro)): vorig = None; continue
        if pro < -100 or pro > 115: return t
        if vorig is not None and abs(pro - vorig[1]) > 60: return t
        vorig = (t, pro)
    return None

with sync_playwright() as pw:
    b = pw.chromium.launch(args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'])
    pg = b.new_page(viewport={'width': 420, 'height': 900}); pg.goto(U)
    pg.evaluate("localStorage.setItem('padel-app-v1', JSON.stringify({versie:1,hand:'rechts',posities:{},voortgang:{},training:[],uitlegGezien:true}))")
    for doel in sys.argv[1:]:
        tid, lv = doel.split(':')
        for ronde in range(6):
            bouw()
            pg.evaluate('window.__mot=null'); pg.goto(U + f"#t={tid}&l={lv}"); pg.reload(); pg.wait_for_function('window.__mot'); pg.wait_for_timeout(200)
            tb = slecht(pg.evaluate(SCAN))
            if tb is None: print(doel, 'schoon'); break
            sl = sleutels(tid, lv)
            k = max(i for i, s in enumerate(sl) if s[0] <= tb)
            if k >= len(sl) - 1: print(doel, 'fout na laatste sleutel', tb); break
            A, B = sl[k], sl[k + 1]
            if A[1] == B[1]: print(doel, 'zelfde houding', A, B); break
            T = json.load(open('technieken.json')); H = json.load(open('houdingen3d.json'))
            pA, pB = pg.evaluate(PRO, H[A[1]]), pg.evaluate(PRO, H[B[1]])
            r = pg.evaluate(MAAK, [H[A[1]], H[B[1]], 0.5, pA, pB, 45, 18])
            naam = f"{A[1]}-naar-{B[1]}"
            H[naam] = r['pose']
            arr = T if isinstance(T, list) else list(T.values())
            L = [t for t in arr if t['id'] == tid][0]['levels'][int(lv) - 1]
            ms_mid = (A[0] + B[0]) / 2
            if B[3] == 'eind':
                i = L['eind'].index(next(x for x in L['eind'] if x['houding'] == B[1]))
                L['eind'][i]['ms'] = int(B[0] - ms_mid); L['eind'].insert(i, {'houding': naam, 'ms': int(ms_mid - A[0])})
            else:
                fi = B[2]; t0 = max(s[0] for s in sl if s[2] == fi - 1 and s[3] == 'fase') if fi > 0 else 0
                f = L['fases'][fi]; f.setdefault('tussen', []).append({'houding': naam, 'ms': int(ms_mid - t0)}); f['tussen'].sort(key=lambda x: x['ms'])
            json.dump(T, open('technieken.json', 'w'), ensure_ascii=False); json.dump(H, open('houdingen3d.json', 'w'), ensure_ascii=False)
            print(f"{doel}: fout bij {tb} ms tussen {A[1]} ({round(pA)}) en {B[1]} ({round(pB)}) -> {naam} pro {round(r['pro'])} (doel {round(r['doel'])})")
    b.close()
