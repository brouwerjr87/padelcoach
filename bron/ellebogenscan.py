"""Scant ellebogen/armen in de afspeelbeweging: elleboog boven schouder, arm door hoofd, elleboog over de middenlijn of ver achter de rug.
python3 ellebogenscan.py site-dir [tid:level ...]   (HAND=links mogelijk)"""
import sys, json, os, threading, http.server, functools
from playwright.sync_api import sync_playwright
D=sys.argv[1]; T=json.load(open('/home/claude/herstel/technieken.json'))
doelen=[a.split(':') for a in sys.argv[2:]] or [(t['id'],str(l['level'])) for t in T for l in t['levels'] if any(f.get('houding') for f in l['fases'])]
srv=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(http.server.SimpleHTTPRequestHandler,directory=D)); srv.RequestHandlerClass.log_message=lambda *a:None
threading.Thread(target=srv.serve_forever,daemon=True).start()
U=f"http://127.0.0.1:{srv.server_port}/index.html"
JS=r"""()=>{const R=window.__rig,e=window.__mot,S=(a,b)=>a.map((x,i)=>x-b[i]),D=(a,b)=>a.reduce((s,x,i)=>s+x*b[i],0),N=a=>Math.hypot(...a);
const seg=(p,a,b)=>{const ab=S(b,a),t=Math.max(0,Math.min(1,D(S(p,a),ab)/D(ab,ab)));return N(S(p,a.map((x,i)=>x+ab[i]*t)))};
const out=[];for(let t=0;t<=e.totaal;t+=20){const s=R.Vt(e,t),p=s.pose||s,j=R.vt(p);const r={t};
 for(const z of ['R','L']){const sh=j['schouder'+z],el=j['elleboog'+z],h=j['hand'+z],sg=z=='R'?1:-1;
  r['boven'+z]=+(el[1]-sh[1]).toFixed(2);
  r['hoofd'+z]=+Math.min(seg(j.hoofd,el,h),seg(j.hoofd,sh,el)).toFixed(2);
  r['mid'+z]=+(sg*D(S(el,j.borst),j.rompRechts)).toFixed(2);
  r['achter'+z]=+D(S(el,sh),j.rompVoor).toFixed(2);
  r['romp'+z]=+Math.min(seg(j.borst,el,h),seg(j.lende,el,h)).toFixed(2);}
 out.push(r)}return out}"""
res={}
with sync_playwright() as p:
    b=p.chromium.launch(args=['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader'])
    pg=b.new_page(viewport={'width':420,'height':900}); pg.goto(U)
    pg.evaluate("localStorage.setItem('padel-app-v1', JSON.stringify({versie:1,hand:'"+os.environ.get('HAND','rechts')+"',posities:{},voortgang:{},training:[],uitlegGezien:true}))")
    for tid,lv in doelen:
        pg.evaluate('window.__mot=null'); pg.goto(U+f"#t={tid}&l={lv}"); pg.reload()
        try: pg.wait_for_function('window.__mot',timeout=6000)
        except Exception: continue
        pg.wait_for_timeout(200); res[f'{tid}:{lv}']=pg.evaluate(JS)
    b.close()
json.dump(res,open('/tmp/claude-0/elscan.json','w'))
def fase(tid,lv,t):
    L=[l for x in T if x['id']==tid for l in x['levels'] if str(l['level'])==lv][0]; c=0
    for i,f in enumerate(L['fases']):
        c+=f.get('duurMs',1000)
        if t<=c: return f"f{i+1}:{f.get('houding')}"
    return 'eind'
for k,rows in res.items():
    tid,lv=k.split(':'); v=[]
    for z in 'RL':
        for naam,key,cond in [('boven','boven'+z,lambda x:x>float(os.environ.get('BOVEN','0.12'))),('hoofd','hoofd'+z,lambda x:x<0.13),('midden','mid'+z,lambda x:x<-0.12),('rug','achter'+z,lambda x:x<-0.3),('romp','romp'+z,lambda x:x<0.08)]:
            hits=[r for r in rows if cond(r[key])]
            if hits:
                w=max(hits,key=lambda r:abs(r[key])) if naam!='hoofd' and naam!='romp' else min(hits,key=lambda r:r[key])
                v.append(f"{naam}{z} {w[key]} @{w['t']} {fase(tid,lv,w['t'])} ({len(hits)}x)")
    print(f"{k:16s} "+(' | '.join(v) if v else 'ok'))
