"""Scant alle technieken zoals de app ze afspeelt: polsbereik, onderarmrotatie, draaisnelheid, elleboog, knie.
python3 afspeelscan.py site-dir [tid:level ...]"""
import sys, json, os, threading, http.server, functools
from playwright.sync_api import sync_playwright
D=sys.argv[1]; T=json.load(open('/home/claude/herstel/technieken.json')); arr=T if isinstance(T,list) else list(T.values())
doelen=[a.split(':') for a in sys.argv[2:]] or [(t['id'],str(l['level'])) for t in arr for l in t['levels'] if any(f.get('houding') for f in l['fases'])]
srv=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(http.server.SimpleHTTPRequestHandler,directory=D)); srv.RequestHandlerClass.log_message=lambda *a:None
threading.Thread(target=srv.serve_forever,daemon=True).start()
U=f"http://127.0.0.1:{srv.server_port}/index.html"
JS=r"""()=>{const R=window.__rig,e=window.__mot,K=v=>{const l=Math.hypot(...v)||1;return v.map(x=>x/l)},S=(a,b)=>a.map((x,i)=>x-b[i]),D=(a,b)=>a.reduce((s,x,i)=>s+x*b[i],0),ang=(a,b)=>Math.acos(Math.max(-1,Math.min(1,D(K(a),K(b)))))*180/Math.PI;
let r={thMin:999,thMax:-999,phMin:999,phMax:-999,proMin:999,proMax:-999,proSprong:0,draaiMax:0,draaiT:0,elbMin:999,elbMax:0,knieMin:999,polsRol:0},v=null,vp=null,p0=null;
for(let t=0;t<=e.totaal;t+=20){const s=R.Vt(e,t),p=s.pose||s,j=R.vt(p),fa=K(S(j.handR,j.elleboogR)),ie=R.Ie(fa,j.racketAs,j.palm),pro=R.Ue(j.schouderR,j.elleboogR,j.handR,j.palm,1),elb=180-ang(S(j.elleboogR,j.schouderR),fa),kn=180-ang(S(j.heupR,j.knieR),S(j.knieR,j.enkelR));
 r.thMin=Math.min(r.thMin,ie.th);r.thMax=Math.max(r.thMax,ie.th);r.phMin=Math.min(r.phMin,ie.ph);r.phMax=Math.max(r.phMax,ie.ph);
 if(!isNaN(pro)){r.proMin=Math.min(r.proMin,pro);r.proMax=Math.max(r.proMax,pro);if(vp!=null)r.proSprong=Math.max(r.proSprong,Math.abs(pro-vp));vp=pro}
 r.elbMin=Math.min(r.elbMin,elb);r.elbMax=Math.max(r.elbMax,elb);r.knieMin=Math.min(r.knieMin,kn);
 if(v){const d=Math.max(ang(v.as,j.racketAs),ang(v.pl,j.palm));if(d>r.draaiMax){r.draaiMax=d;r.draaiT=t}}v={as:j.racketAs,pl:j.palm};
 const pr=p.arm&&p.arm.pols;if(pr){if(p0==null)p0=pr[2];r.polsRol=Math.max(r.polsRol,Math.abs(pr[2]-p0)*180/Math.PI)}}
for(const k in r)r[k]=Math.round(r[k]);return r}"""
res={}
with sync_playwright() as p:
    b=p.chromium.launch(args=['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader'])
    pg=b.new_page(viewport={'width':420,'height':900}); pg.goto(U)
    pg.evaluate("localStorage.setItem('padel-app-v1', JSON.stringify({versie:1,hand:'rechts',posities:{},voortgang:{},training:[],uitlegGezien:true}))")
    for tid,lv in doelen:
        pg.evaluate('window.__mot=null'); pg.goto(U+f"#t={tid}&l={lv}"); pg.reload()
        try: pg.wait_for_function('window.__mot',timeout=6000)
        except Exception: continue
        pg.wait_for_timeout(200); res[f'{tid}:{lv}']=pg.evaluate(JS)
    b.close()
json.dump(res,open('/tmp/claude-0/scan.json','w'))
for k,r in res.items():
    vl=[]
    if r['draaiMax']>25: vl.append(f"draai {r['draaiMax']}°/20ms @{r['draaiT']}")
    if r['proMax']-r['proMin']>150 or r['proSprong']>40: vl.append(f"onderarm {r['proMin']}..{r['proMax']} sprong {r['proSprong']}")
    if r['polsRol']>200: vl.append(f"rol {r['polsRol']}")
    if r['phMax']-r['phMin']>40: vl.append(f"pols-ph {r['phMin']}..{r['phMax']}")
    if r['thMax']-r['thMin']>40: vl.append(f"pols-th {r['thMin']}..{r['thMax']}")
    print(f"{k:16s} elb {r['elbMin']}-{r['elbMax']} knie≥{r['knieMin']}  "+(' | '.join(vl) if vl else 'ok'))
