"""Zoek per houding de elleboog-hint waarbij de elleboog in de gewenste richting wijst (romp-assen voor/op/rechts)."""
import json, sys, threading, http.server, functools
from playwright.sync_api import sync_playwright
D=sys.argv[1]; H=json.load(open(sys.argv[2])); doel=json.loads(sys.argv[3])  # {naam:[voor,op,rechts]}
srv=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(http.server.SimpleHTTPRequestHandler,directory=D)); srv.RequestHandlerClass.log_message=lambda *a:None
threading.Thread(target=srv.serve_forever,daemon=True).start()
JS=r"""([H,doel])=>{const R=window.__rig,S=(a,b)=>a.map((x,i)=>x-b[i]),D=(a,b)=>a.reduce((s,x,i)=>s+x*b[i],0),N=a=>Math.hypot(...a),K=a=>a.map(x=>x/N(a)),X=(a,b)=>[a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]];
const meet=p=>{const j=R.vt(p),sh=j.schouderR,el=j.elleboogR,h=j.handR,ax=K(S(h,sh)),m=S(el,sh),perp=S(m,ax.map(x=>x*D(m,ax))),pn=K(perp),op=K(X(j.rompRechts,j.rompVoor));return [D(pn,j.rompVoor),D(pn,op),D(pn,j.rompRechts)]};
const uit={};for(const k in doel){const p=JSON.parse(JSON.stringify(H[k])),t=K(doel[k]);let best=null;
for(let a=0;a<360;a+=10)for(let b=-80;b<=80;b+=10){const ca=Math.cos(a*Math.PI/180),sa=Math.sin(a*Math.PI/180),cb=Math.cos(b*Math.PI/180),sb=Math.sin(b*Math.PI/180);const hnt=[+(cb*ca).toFixed(2),+sb.toFixed(2),+(cb*sa).toFixed(2)];p.elleboogR=hnt;let r;try{r=meet(p)}catch(e){continue}if(r.some(isNaN))continue;const sc=N(S(r,t));if(!best||sc<best.sc)best={sc,hnt,r:r.map(x=>+x.toFixed(2))}}
uit[k]=best}return uit}"""
with sync_playwright() as pw:
    b=pw.chromium.launch(args=['--use-gl=angle','--use-angle=swiftshader']);pg=b.new_page()
    pg.goto(f"http://127.0.0.1:{srv.server_port}/index.html");pg.wait_for_function('window.__rig',timeout=10000)
    r=pg.evaluate(JS,[H,doel]);b.close()
print(json.dumps(r))
