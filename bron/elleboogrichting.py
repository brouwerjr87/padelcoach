"""Per houding: waar wijst de elleboog (t.o.v. de lijn schouder-hand), in romp-assen voor/op/rechts, en de elleboogshoek."""
import json, sys, threading, http.server, functools
from playwright.sync_api import sync_playwright
D=sys.argv[1]; H=json.load(open(sys.argv[2])); namen=sys.argv[3:] or list(H)
srv=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(http.server.SimpleHTTPRequestHandler,directory=D)); srv.RequestHandlerClass.log_message=lambda *a:None
threading.Thread(target=srv.serve_forever,daemon=True).start()
JS=r"""([H,namen])=>{const R=window.__rig,S=(a,b)=>a.map((x,i)=>x-b[i]),D=(a,b)=>a.reduce((s,x,i)=>s+x*b[i],0),N=a=>Math.hypot(...a),K=a=>a.map(x=>x/N(a)),X=(a,b)=>[a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]];
const out={};for(const k of namen){const p=H[k];if(!p||!p.handR||typeof p.handR==='string')continue;let j;try{j=R.vt(p)}catch(e){continue}
const sh=j.schouderR,el=j.elleboogR,h=j.handR,ax=K(S(h,sh)),m=S(el,sh),perp=S(m,ax.map(x=>x*D(m,ax)));const pn=N(perp)<1e-6?[0,0,0]:K(perp);
const op=K(X(j.rompRechts,j.rompVoor)),hoek=Math.acos(Math.max(-1,Math.min(1,D(K(S(sh,el)),K(S(h,el))))))*180/Math.PI;
out[k]={voor:+D(pn,j.rompVoor).toFixed(2),op:+D(pn,op).toFixed(2),rechts:+D(pn,j.rompRechts).toFixed(2),hoek:Math.round(hoek),hint:p.elleboogR}}return out}"""
with sync_playwright() as pw:
    b=pw.chromium.launch(args=['--use-gl=angle','--use-angle=swiftshader']);pg=b.new_page()
    pg.goto(f"http://127.0.0.1:{srv.server_port}/index.html");pg.wait_for_function('window.__rig',timeout=10000)
    r=pg.evaluate(JS,[H,namen]);b.close()
for k,v in r.items(): print(f"{k:24s} voor {v['voor']:+.2f} op {v['op']:+.2f} rechts {v['rechts']:+.2f} hoek {v['hoek']:4d} hint {v['hint']}")
