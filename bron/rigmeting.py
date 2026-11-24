"""Meet per houding: polshoek (th: racket t.o.v. onderarm naar duimkant, ph: buiging), of de racketstand geklemd wordt, en of de slagarm door de romp gaat."""
import json, sys, threading, http.server, functools
from playwright.sync_api import sync_playwright
D=sys.argv[1]; H=json.load(open(sys.argv[2])); namen=sys.argv[3:] or list(H)
srv=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(http.server.SimpleHTTPRequestHandler,directory=D)); srv.RequestHandlerClass.log_message=lambda *a:None
threading.Thread(target=srv.serve_forever,daemon=True).start()
JS="""([H,namen])=>{const R=window.__rig,K=e=>{const l=Math.hypot(...e)||1;return e.map(x=>x/l)},S=(a,b)=>a.map((x,i)=>x-b[i]),D=(a,b)=>a.reduce((s,x,i)=>s+x*b[i],0);
const uit={};for(const k of namen){const p=H[k];if(!p||!Array.isArray(p.handR)||!p.racket)continue;const j=R.vt(p);
const fa=K(S(j.handR,j.elleboogR));const w=K(p.racket.richting);const v=p.racket.vlak;const pl=K(S(v,w.map(x=>x*D(v,w))));
const a=R.Ie(fa,w,pl);
const romp={bekken:j.bekken,borst:j.borst,op:j.rugRichting,voor:j.rompVoor,rechts:j.rompRechts};
const door=R.Ye(j.schouderR,j.elleboogR,j.handR,romp);
const klem=Math.acos(Math.min(1,D(j.racketAs,w)))*180/Math.PI;
const pro=R.Ue(j.schouderR,j.elleboogR,j.handR,pl,1),elb=180-Math.acos(Math.max(-1,Math.min(1,D(K(S(j.elleboogR,j.schouderR)),fa))))*180/Math.PI;uit[k]={pro:Math.round(pro),elb:Math.round(elb),th:Math.round(a.th),ph:Math.round(a.ph),klem:Math.round(klem),door:+door.toFixed(3),hand:j.handR.map(x=>+x.toFixed(2)),ell:j.elleboogR.map(x=>+x.toFixed(2))}}return uit}"""
with sync_playwright() as p:
    b=p.chromium.launch(args=['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader'])
    pg=b.new_page(); pg.goto(f"http://127.0.0.1:{srv.server_port}/index.html"); pg.wait_for_function('window.__rig')
    res=pg.evaluate(JS,[H,namen]); b.close()
json.dump(res,open('/tmp/claude-0/rig.json','w'))
for k,v in res.items():
    vlag=[]
    if v['th'] is None or v['th']!=v['th']: v['th']=-999
    if v['th']>75 or v['th']<20: vlag.append('pols-th')
    if abs(v['ph'])>40: vlag.append('pols-ph')
    if v['klem']>8: vlag.append('geklemd')
    if v['door']>0.05: vlag.append('door-romp')
    print(f"{k:24s} pro {v['pro']!s:>5} elb {v['elb']!s:>4} th {v['th']!s:>5} ph {v['ph']!s:>5} klem {v['klem']!s:>4} door {v['door']:.2f}  {' '.join(vlag)}")
