"""python3 vel3.py (overzicht/tactiek: stand per fase; greep: diagrammen)
python3 vel2.py site-map techniek[,techniek] uit.pdf : beoordelingsvel uit de gebouwde app (per fase drie aanzichten + tekst)"""
import sys, json, base64, io, html, threading, http.server, functools
from playwright.sync_api import sync_playwright
from PIL import Image
D, tids, uit = sys.argv[1], sys.argv[2].split(','), sys.argv[3]
T=json.load(open('/home/claude/herstel/technieken.json')); TS=[[x for x in T if x['id']==t][0] for t in tids]
VIEWS=['Schuin','Boven','Achter']
srv=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(http.server.SimpleHTTPRequestHandler,directory=D)); srv.RequestHandlerClass.log_message=lambda *a:None
threading.Thread(target=srv.serve_forever,daemon=True).start()
U=f"http://127.0.0.1:{srv.server_port}/index.html"
zet="(el, v) => { const s = Object.getOwnPropertyDescriptor(HTMLInputElement.prototype,'value').set; s.call(el, v); el.dispatchEvent(new Event('input', {bubbles:true})) }"
def tekst(s): return html.escape(s.replace('{linker}','linker').replace('{rechter}','rechter').replace('{Linker}','Linker').replace('{Rechter}','Rechter'))
beelden={}
with sync_playwright() as p:
    b=p.chromium.launch(args=['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader'])
    pg=b.new_page(viewport={'width':420,'height':900}, device_scale_factor=2)
    pg.goto(U); pg.evaluate("localStorage.setItem('padel-app-v1', JSON.stringify({versie:1,hand:'rechts',posities:{},voortgang:{},training:[],uitlegGezien:true}))")
    for t in TS:
        for LV in t['levels']:
            pg.goto(U+f"#t={t['id']}&l={LV['level']}"); pg.reload(); pg.wait_for_timeout(1500)
            if LV['fases'][0].get('diagram'):
                for i in range(len(LV['fases'])):
                    if i: pg.get_by_label('Volgende fase').click(); pg.wait_for_timeout(300)
                    el=pg.locator('svg').filter(has=pg.locator('text')).first
                    im=Image.open(io.BytesIO(el.screenshot())).convert('RGB'); im.thumbnail((700,700))
                    buf=io.BytesIO(); im.save(buf,'JPEG',quality=88); beelden[(t['id'],LV['level'],i,'diagram')]=base64.b64encode(buf.getvalue()).decode()
                continue
            mx=pg.locator('.tijdlijn').get_attribute('max')
            for v in VIEWS:
                pg.locator('.aanzichten .chip', has_text=v).click(); pg.wait_for_timeout(700)
                n=len(LV['fases'])
                for i in range(n):
                    pg.locator('.tijdlijn').evaluate(zet, '0'); pg.wait_for_timeout(200)
                    for _ in range(i): pg.get_by_label('Volgende fase').click(); pg.wait_for_timeout(150)
                    pg.wait_for_timeout(350)
                    im=Image.open(io.BytesIO(pg.locator('.beeld3d').screenshot())).convert('RGB'); W,H=im.size
                    im=im.crop((int(.02*W),int(.02*H),int(.98*W),int(.9*H))); im.thumbnail((640,640))
                    buf=io.BytesIO(); im.save(buf,'JPEG',quality=86); beelden[(t['id'],LV['level'],i,v)]=base64.b64encode(buf.getvalue()).decode()
    css="""@page{size:A4;margin:12mm} body{font-family:Arial,sans-serif;color:#2E2E2E;font-size:10.5pt}
    h1{color:#2B4B6F;font-size:18pt;margin:0 0 4px} h2{color:#2B4B6F;font-size:14pt;margin:14px 0 2px;page-break-before:always} h2.eerste{page-break-before:avoid} .intro{color:#6B7280;margin:0 0 8px}
    .fase{page-break-inside:avoid;border-top:2px solid #3AAFA9;padding-top:6px;margin-top:10px} .fase h3{margin:0 0 4px;font-size:11.5pt}
    .rij{display:flex;gap:4px} .rij figure{margin:0;flex:1} .rij img{width:100%;display:block;border-radius:3px} figcaption{font-size:8pt;color:#6B7280;text-align:center}
    ul{margin:3px 0 0 16px;padding:0} .doel{background:#F4F6F8;padding:6px 8px;border-radius:4px;margin:4px 0 6px} .fouten li{margin-bottom:2px}"""
    naam=' en '.join(t['naam'] for t in TS)
    h=[f"<style>{css}</style><h1>{html.escape(naam)}: beoordeling van de animatie</h1>",
       "<p class='intro'>Rechtshandige speler. Bij de greep zie je per stap het diagram uit de app. Bij positie en tactiek zie je per fase de <b>stand bij die fase</b> (waar de spelers en de bal staan op het moment dat de fase beschrijft; daarna bewegen ze naar de volgende fase), vanuit drie camerastandpunten, met eronder de tekst zoals de speler die in de app leest. Het 3D-model is eenvoudig: beoordeel posities, afstanden en timing, niet het uiterlijk.</p>",
       "<div class='doel'><b>Beeld.</b> De twee spelers onderin met witte ring zijn jij en je partner; de twee met oranje ring zijn de tegenstanders. Jij speelt aan de <i>rechter</i>kant (vanaf je eigen achterwand gezien). <i>Schuin</i>: schuin van achter boven de eigen helft. <i>Boven</i>: recht van boven, het net loopt horizontaal. <i>Achter</i>: vanachter de eigen achterwand, op ooghoogte. Lijnen op de vloer: servicelijnen (ongeveer 3 m voor de achterwand) en de middenlijn; een padelbaan heeft geen zijlijnen, de wanden zijn de grens. De baan is 10 bij 20 meter.</div>"]
    for t in TS:
        for LV in t['levels']:
            h.append(f"<h2{' class=eerste' if LV is TS[0]['levels'][0] else ''}>{html.escape(t['naam'])} · level {LV['level']}: {html.escape(LV['titel'])}</h2><div class='doel'>{tekst(LV['doel'])}</div>")
            for i,f in enumerate(LV['fases']):
                fig=(f"<figure style='flex:0 0 60%'><img src='data:image/jpeg;base64,{beelden[(t['id'],LV['level'],i,'diagram')]}'></figure>" if f.get('diagram') else ''.join(f"<figure><img src='data:image/jpeg;base64,{beelden[(t['id'],LV['level'],i,v)]}'><figcaption>{v}</figcaption></figure>" for v in VIEWS))
                lo=''.join(f"<li>{tekst(x)}</li>" for x in f.get('letOp',[]))
                h.append(f"<div class='fase'><h3>Fase {i+1}: {tekst(f['titel'])}</h3><div class='rij'>{fig}</div><p style='margin:5px 0 0'>{tekst(f['uitleg'])}</p><ul>{lo}</ul></div>")
            fo=''.join(f"<li><b>{tekst(x['titel'])}</b>: {tekst(x['gevolg'])} <i>Herstel:</i> {tekst(x['herstel'])}</li>" for x in LV.get('fouten',[]))
            h.append(f"<div class='fase'><h3>Veelgemaakte fouten in de app</h3><ul class='fouten'>{fo}</ul></div>")
    pg2=b.new_page(); pg2.set_content('<meta charset="utf-8">'+''.join(h)); pg2.wait_for_timeout(300)
    pg2.pdf(path=uit, format='A4', print_background=True); print(uit)
    b.close()
