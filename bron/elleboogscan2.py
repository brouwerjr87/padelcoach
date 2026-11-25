import sys, json, os, threading, http.server, functools
from playwright.sync_api import sync_playwright
D=sys.argv[1]; doelen=[a.split(':') for a in sys.argv[2:]]
srv=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(http.server.SimpleHTTPRequestHandler,directory=D)); srv.RequestHandlerClass.log_message=lambda *a:None
threading.Thread(target=srv.serve_forever,daemon=True).start()
U=f"http://127.0.0.1:{srv.server_port}/index.html"
JS=r"""()=>{const R=window.__rig,e=window.__mot,S=(a,b)=>a.map((x,i)=>x-b[i]),D=(a,b)=>a.reduce((s,x,i)=>s+x*b[i],0),N=a=>Math.hypot(...a),K=a=>a.map(x=>x/N(a)),X=(a,b)=>[a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]];
const o=[];for(let t=0;t<=e.totaal;t+=20){const s=R.Vt(e,t),p=s.pose||s,j=R.vt(p),sh=j.schouderR,el=j.elleboogR,h=j.handR,ax=K(S(h,sh)),m=S(el,sh),pn=K(S(m,ax.map(x=>x*D(m,ax)))),op=K(X(j.rompRechts,j.rompVoor)),hoek=Math.acos(Math.max(-1,Math.min(1,D(K(S(sh,el)),K(S(h,el))))))*180/Math.PI;
o.push([t,+D(pn,j.rompVoor).toFixed(2),+D(pn,op).toFixed(2),+D(pn,j.rompRechts).toFixed(2),Math.round(hoek),+D(S(h,sh),j.rompVoor).toFixed(2)])}return o}"""
with sync_playwright() as p:
    b=p.chromium.launch(args=['--use-gl=angle','--use-angle=swiftshader']);pg=b.new_page(viewport={'width':420,'height':900});pg.goto(U)
    pg.evaluate("localStorage.setItem('padel-app-v1', JSON.stringify({versie:1,hand:'rechts',posities:{},voortgang:{},training:[],uitlegGezien:true}))")
    for tid,lv in doelen:
        pg.evaluate('window.__mot=null');pg.goto(U+f"#t={tid}&l={lv}");pg.reload();pg.wait_for_function('window.__mot',timeout=8000);pg.wait_for_timeout(200)
        r=pg.evaluate(JS)
        slecht=[x for x in r if x[3]<-0.45 and x[4]>110 and x[5]<0.1]
        print(tid,lv,'slecht',len(slecht),slecht[:3], 'rechts-min',min(x[3] for x in r))
    b.close()
