"""python3 tijden.py site uit.png tid:level:fase:view:offsets(ms, komma) ...  render rond de start van een fase"""
import os, sys, io, threading, http.server, functools
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw, ImageFont
D, uit, specs = sys.argv[1], sys.argv[2], [s.split(':') for s in sys.argv[3:]]
srv=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(http.server.SimpleHTTPRequestHandler,directory=D)); srv.RequestHandlerClass.log_message=lambda *a:None
threading.Thread(target=srv.serve_forever,daemon=True).start()
U=f"http://127.0.0.1:{srv.server_port}/index.html"
zet="(el, v) => { const s = Object.getOwnPropertyDescriptor(HTMLInputElement.prototype,'value').set; s.call(el, v); el.dispatchEvent(new Event('input', {bubbles:true})) }"
f=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',18)
rows=[]
with sync_playwright() as p:
    b=p.chromium.launch(args=['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader'])
    pg=b.new_page(viewport={'width':420,'height':900}, device_scale_factor=2)
    pg.goto(U); pg.evaluate("localStorage.setItem('padel-app-v1', JSON.stringify({versie:1,hand:'"+os.environ.get('HAND','rechts')+"',posities:{},voortgang:{},training:[],uitlegGezien:true}))")
    for tid,lv,fase,view,offs in specs:
        pg.goto(U+f"#t={tid}&l={lv}"); pg.reload(); pg.wait_for_timeout(1300)
        pg.locator('.aanzichten .chip', has_text=view).click(); pg.wait_for_timeout(300)
        pg.locator('.tijdlijn').evaluate(zet,'0'); pg.wait_for_timeout(150)
        for _ in range(int(fase)): pg.get_by_label('Volgende fase').click(); pg.wait_for_timeout(120)
        t0=int(float(pg.locator('.tijdlijn').input_value()))
        row=[]
        for o in offs.split(','):
            pg.locator('.tijdlijn').evaluate(zet,str(max(0,t0+int(o)))); pg.wait_for_timeout(250)
            im=Image.open(io.BytesIO(pg.locator('.beeld3d').screenshot())).convert('RGB')
            if os.environ.get('CROP'):
                x0,y0,x1,y1=[float(v) for v in os.environ['CROP'].split(',')]; W,H=im.size; im=im.crop((int(x0*W),int(y0*H),int(x1*W),int(y1*H)))
            im.thumbnail((500,500)); ImageDraw.Draw(im).text((6,4),f"{tid} {lv} {view} {o:+}" if False else f"{tid}{lv} {view} {int(o):+d}ms",fill='black',font=f)
            row.append(im)
        rows.append(row)
    b.close()
w=max(sum(i.width for i in r) for r in rows); h=sum(max(i.height for i in r) for r in rows)
o=Image.new('RGB',(w,h),'white'); y=0
for r in rows:
    x=0
    for i in r: o.paste(i,(x,y)); x+=i.width
    y+=max(i.height for i in r)
o.save(uit); print(uit,o.size)
