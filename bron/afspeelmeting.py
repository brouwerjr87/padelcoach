"""Meet de afgespeelde beweging (zoals de app hem afspeelt): polshoeken en draaiing van het racket per tijdstap.
python3 afspeelmeting.py diag tid level [stap_ms]"""
import sys, json, os, threading, http.server, functools
from playwright.sync_api import sync_playwright
D, tid, lv = sys.argv[1], sys.argv[2], sys.argv[3]; stap = int(sys.argv[4]) if len(sys.argv) > 4 else 20
srv=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(http.server.SimpleHTTPRequestHandler,directory=D)); srv.RequestHandlerClass.log_message=lambda *a:None
threading.Thread(target=srv.serve_forever,daemon=True).start()
U=f"http://127.0.0.1:{srv.server_port}/index.html"
JS=r"""(stap)=>{const R=window.__rig,e=window.__mot,K=v=>{const l=Math.hypot(...v)||1;return v.map(x=>x/l)},S=(a,b)=>a.map((x,i)=>x-b[i]),D=(a,b)=>a.reduce((s,x,i)=>s+x*b[i],0),X=(a,b)=>[a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]];
const uit=[];let vorig=null;
for(let t=0;t<=e.totaal;t+=stap){const s=R.Vt(e,t),p=s.pose||s,j=R.vt(p);
 const fa=K(S(j.handR,j.elleboogR)),ua=K(S(j.elleboogR,j.schouderR)),as=j.racketAs,pl=j.palm,ie=R.Ie(fa,as,pl);
 const elb=180-Math.acos(Math.max(-1,Math.min(1,D(ua,fa))))*180/Math.PI;
 // draaisnelheid racketframe
 let draai=0;if(vorig){const a=Math.acos(Math.max(-1,Math.min(1,D(vorig.as,as))))*180/Math.PI,b=Math.acos(Math.max(-1,Math.min(1,D(vorig.pl,pl))))*180/Math.PI;draai=Math.max(a,b)}
 // onderarmrol: hoek van palm om de onderarmas t.o.v. vlak door bovenarm
 const rol=R.Ue(j.schouderR,j.elleboogR,j.handR,pl,1);
 uit.push({t,th:Math.round(ie.th),ph:Math.round(ie.ph),elb:Math.round(elb),rol:Math.round(rol),draai:Math.round(draai),pols:(p.arm&&p.arm.pols||[]).map(x=>Math.round(x*180/Math.PI)),fase:null});
 vorig={as,pl}}
return {uit,sleutels:e.sleutels.map(k=>k.t)}}"""
with sync_playwright() as p:
    b=p.chromium.launch(args=['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader'])
    pg=b.new_page(viewport={'width':420,'height':900}); pg.goto(U)
    pg.evaluate("localStorage.setItem('padel-app-v1', JSON.stringify({versie:1,hand:'"+os.environ.get('HAND','rechts')+"',posities:{},voortgang:{},training:[],uitlegGezien:true}))")
    pg.goto(U+f"#t={tid}&l={lv}"); pg.reload(); pg.wait_for_timeout(800); pg.evaluate("window.__mot=null"); pg.wait_for_function('window.__mot'); pg.wait_for_timeout(500)
    r=pg.evaluate(JS,stap); b.close()
json.dump(r,open(f'/tmp/claude-0/afspeel-{tid}{lv}.json','w'))
print('sleutels', r['sleutels'])
for x in r['uit']:
    vlag=('  <<< draai' if x['draai']>25 else '')
    print(f"{x['t']:5d} th {x['th']:4d} ph {x['ph']:4d} elleboog {x['elb']:4d} rol {x['rol']!s:>5} draai/stap {x['draai']:3d} pols {x['pols']}{vlag}")
