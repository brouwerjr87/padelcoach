"""python3 frames.py site uit.png tid:level:fase:view ...  (fase = index vanaf 0)"""
import sys, io, threading, http.server, functools
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw, ImageFont
D, uit, specs = sys.argv[1], sys.argv[2], [s.split(':') for s in sys.argv[3:]]
srv=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(http.server.SimpleHTTPRequestHandler,directory=D)); srv.RequestHandlerClass.log_message=lambda *a:None
threading.Thread(target=srv.serve_forever,daemon=True).start()
U=f"http://127.0.0.1:{srv.server_port}/index.html"
zet="(el, v) => { const s = Object.getOwnPropertyDescriptor(HTMLInputElement.prototype,'value').set; s.call(el, v); el.dispatchEvent(new Event('input', {bubbles:true})) }"
f=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',22)
ims=[]
with sync_playwright() as p:
    b=p.chromium.launch(args=['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader'])
    pg=b.new_page(viewport={'width':420,'height':900}, device_scale_factor=1.5)
    pg.goto(U); pg.evaluate("localStorage.setItem('padel-app-v1', JSON.stringify({versie:1,hand:'rechts',posities:{},voortgang:{},training:[],uitlegGezien:true}))")
    huidig=None
    for tid,lv,fase,view in specs:
        if huidig!=(tid,lv): pg.goto(U+f"#t={tid}&l={lv}"); pg.reload(); pg.wait_for_timeout(1300); huidig=(tid,lv)
        pg.locator('.aanzichten .chip', has_text=view).click(); pg.wait_for_timeout(500)
        pg.locator('.tijdlijn').evaluate(zet,'0'); pg.wait_for_timeout(150)
        for _ in range(int(fase)): pg.get_by_label('Volgende fase').click(); pg.wait_for_timeout(120)
        pg.wait_for_timeout(200)
        im=Image.open(io.BytesIO(pg.locator('.beeld3d').screenshot())).convert('RGB')
        naam=pg.locator('.fase-naam').first.inner_text()
        ImageDraw.Draw(im).text((8,6),f'{tid} {lv} {view}: {naam}',fill='black',font=f); ims.append(im)
    b.close()
k=min(4,len(ims)); W,H=ims[0].size; o=Image.new('RGB',(W*k,H*((len(ims)+k-1)//k)),'white')
for i,im in enumerate(ims): o.paste(im,((i%k)*W,(i//k)*H))
o.thumbnail((2400,2400)); o.save(uit); print(uit,o.size)
