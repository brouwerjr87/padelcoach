"""Codepatches op de gebouwde app (de broncode is verloren; dit past de bundel aan).

Gebruik: python3 codepatch.py index.html [index.html ...]
Idempotent: een patch die al is toegepast wordt overgeslagen.
"""
import sys

HAND = ("M17 44L15.5 34L9.5 26.5a2.6 2.6 0 0 1 4-3.3L17 27V12a2.5 2.5 0 0 1 5 0V23V9"
        "a2.5 2.5 0 0 1 5 0V23V11a2.5 2.5 0 0 1 5 0V24V15a2.5 2.5 0 0 1 5 0V30"
        "C37 37 34.5 41.5 31 44")

PATCHES = []
def patch(naam, oud, nieuw):
    PATCHES.append((naam, oud, nieuw))

# 0. Baanoverzicht-camera: alle vier spelers in beeld (nov 2026, al live)
patch('baancamera',
 "function ln(e,t,n=0){switch(e){case`achter`:return{az:n,el:56,afstand:26,doel:[10,0,0]};case`zij`:return{az:t*90+n,el:50,afstand:24,doel:[10,0,0]};case`voor`:return{az:180+n,el:56,afstand:26,doel:[10,0,0]};case`boven`:return{az:n,el:86,afstand:26,doel:[10,0,0]};default:return{az:t*30+n,el:58,afstand:27,doel:[10,0,0]}}",
 "function ln(e,t,n=0){switch(e){case`achter`:return{az:n,el:56,afstand:28,doel:[8,0,0]};case`zij`:return{az:t*90+n,el:50,afstand:29,doel:[8.5,0,0]};case`voor`:return{az:180+n,el:56,afstand:26,doel:[10,0,0]};case`boven`:return{az:n,el:86,afstand:29,doel:[8.5,0,0]};default:return{az:t*30+n,el:58,afstand:29,doel:[8,0,0]}}")

# 1. Terugknop van telefoon/browser blijft in de app
patch('terugknop',
 "(0,e.useEffect)(()=>v(t),[t]);let s=a[r][a[r].length-1]",
 "(0,e.useEffect)(()=>v(t),[t]);"
 "let Hq=(0,e.useRef)({d:0,neg:0}),Rq=(0,e.useRef)(r),Aq=(0,e.useRef)(a);Rq.current=r,Aq.current=a;"
 "(0,e.useEffect)(()=>{let D=a[r].length-1+(r!==`leren`?1:0),h=Hq.current;"
 "if(D>h.d)for(;h.d<D;)h.d++,history.pushState({pc:h.d},``);"
 "else D<h.d&&(h.neg++,history.go(D-h.d),h.d=D)},[a,r]);"
 "(0,e.useEffect)(()=>{let q=()=>{let h=Hq.current;if(h.neg>0){h.neg--;return}h.d>0&&h.d--;"
 "let k=Rq.current;Aq.current[k].length>1?o(e=>({...e,[k]:e[k].slice(0,-1)})):k!==`leren`&&i(`leren`)};"
 "return addEventListener(`popstate`,q),()=>removeEventListener(`popstate`,q)},[]);"
 "let s=a[r][a[r].length-1]")

# 2a. Welkom: één scherm, slaghand met handjes, link Over de app, knop Aan de slag
def welkom(s):
    i = s.index('function zi(){')
    j = s.index('var Bi={leren')
    nieuw = (
     "function zi(){let{state:t,zetHand:n,uitlegKlaar:r,ga:i}=f(),a=e.default.createElement;"
     "return a(`div`,{className:`welkom`,role:`dialog`,\"aria-modal\":`true`,\"aria-label\":`Welkom bij je padelcoach`},"
     "a(`div`,{className:`welkom-kaart`},"
     "a(`h1`,null,`Welkom bij je padelcoach`,` `,a(ve,null)),"
     "a(`p`,null,`Stap voor stap de juiste techniek, met 3D-beelden die je kunt afspelen en draaien. Met welke hand speel je?`),"
     "a(`div`,{className:`hand-keuze`,role:`group`,\"aria-label\":`Speelhand`},[`rechts`,`links`].map(h=>"
     "a(`button`,{key:h,className:`hand-tegel${t.hand===h?` aan`:``}`,\"aria-pressed\":t.hand===h,onClick:()=>n(h)},"
     "a(`svg`,{viewBox:`0 0 48 48`,\"aria-hidden\":`true`,style:h===`links`?{transform:`scaleX(-1)`}:void 0},a(`path`,{d:`" + HAND + "`})),"
     "a(`span`,null,h===`rechts`?`Rechtshandig`:`Linkshandig`)))),"
     "a(`p`,{className:`klein`},`Alle beelden en teksten draaien mee. Je kunt dit later wijzigen bij Instellingen.`),"
     "a(`button`,{className:`link welkom-over`,onClick:()=>{r(),i({naam:`gids`,id:`app`})}},`Over de app`),"
     "a(`button`,{className:`knop-primair welkom-start`,onClick:r},`Aan de slag`)))}"
    )
    return s[:i] + nieuw + s[j:]
PATCHES.append(('welkom', welkom, 'className:`hand-keuze`'))

# 2b. Animatie start vanzelf (niet bij 'minder beweging')
patch('autostart',
 "I?e.default.createElement(Xr,{reeks:A,camera:F,onDraai:T,sprong:y,onActief:w,boven:",
 "I?e.default.createElement(Xr,{reeks:A,camera:F,onDraai:T,sprong:y,onActief:w,autoStart:!matchMedia(`(prefers-reduced-motion: reduce)`).matches,boven:")

# 3. Tip beginscherm na een nieuw beheerst level
patch('zetVlag',
 "uitlegKlaar:()=>n(e=>({...e,uitlegGezien:!0}))",
 "uitlegKlaar:()=>n(e=>({...e,uitlegGezien:!0})),zetVlag:e=>n(t=>({...t,[e]:!0}))")
patch('tipfunctie',
 "var Bi={leren",
 "function TipBs(){let{state:t,zetVlag:n}=f(),a=e.default.createElement,o=navigator.userAgent||``;"
 "if(t.tipBeginscherm)return null;"
 "try{if(matchMedia(`(display-mode: standalone)`).matches||navigator.standalone||!matchMedia(`(pointer: coarse)`).matches)return null}catch{}"
 "let s=/LinkedInApp|FBAN|FBAV|Instagram/i.test(o),c=/iPhone|iPad|iPod/i.test(o);"
 "return a(`div`,{className:`tip-beginscherm`,role:`note`},a(`h4`,null,`Bewaar je voortgang`),"
 "a(`p`,null,`Je voortgang staat alleen in deze browser op je telefoon. Zet de app op je beginscherm, dan open je hem altijd op dezelfde plek.`),"
 "s?a(`p`,null,`Je zit nu in de browser van een andere app. Open deze pagina eerst in `,c?`Safari`:`Chrome`,` (via de drie puntjes) en zet hem daar op je beginscherm. Je voortgang neem je mee met de code bij Instellingen.`)"
 ":a(`p`,null,c?`Tik op het deelicoon (vierkantje met pijl omhoog) en kies \"Zet op beginscherm\".`:`Tik op de drie puntjes en kies \"App installeren\" of \"Toevoegen aan startscherm\".`),"
 "a(`button`,{className:`knop-secundair`,onClick:()=>n(`tipBeginscherm`)},`Begrepen`))}"
 "var Bi={leren")
patch('tipplek',
 "_?e.default.createElement(vi,{sleutel:s}):",
 "_?e.default.createElement(e.default.Fragment,null,e.default.createElement(vi,{sleutel:s}),e.default.createElement(TipBs,null)):")

# 4. Volgende stap: zelf markeren als beheerst, met ongedaan maken
patch('kanal-state',
 "function xe(){let{state:t,ga:n}=f(),r=",
 "function xe(){let{state:t,ga:n,zetVoortgang:Zv}=f(),[Uv,Wv]=(0,e.useState)(null),r=")
patch('kanal-knop',
 "`Start deze stap`),e.default.createElement(`button`,{className:`link`,onClick:()=>n({naam:`leerpad`})},`Hele leerpad`)))}",
 "`Start deze stap`),e.default.createElement(`button`,{className:`link`,onClick:()=>n({naam:`leerpad`})},`Hele leerpad`)),"
 "Uv?e.default.createElement(`p`,{className:`klein kan-al`},`✓ `,Uv.naam,` staat op beheerst. `,e.default.createElement(`button`,{className:`link`,onClick:()=>{Zv(Uv.id,Uv.level,null),Wv(null)}},`Ongedaan maken`))"
 ":e.default.createElement(`p`,{className:`klein kan-al`},`Haal je het criterium van deze stap al? `,e.default.createElement(`button`,{className:`link`,onClick:()=>{Zv(r.techniek.id,r.level,x()),Wv({id:r.techniek.id,level:r.level,naam:r.techniek.naam+(r.techniek.levels.length>1?` · level ${r.level}`:``)})}},`Markeer als beheerst`)))}")

# 5. Fouten: 'met beeld' waar een beeld is, eerlijke hint
patch('fout-hint',
 "e.default.createElement(`span`,{className:`sectie-hint`},`tik voor fout naast goed`)),e.default.createElement(`div`,{className:`fouten`},k.fouten.map((t,n)=>e.default.createElement(hi,{key:n,fout:t,hand:l.hand,aanzicht:b,positie:D})))",
 "e.default.createElement(`span`,{className:`sectie-hint`},k.fouten.every(t=>t.houding||t.plaatsing||t.diagram)?`tik voor fout naast goed`:`tik voor uitleg`)),e.default.createElement(`div`,{className:`fouten`},k.fouten.map((t,n)=>e.default.createElement(hi,{key:n,fout:t,hand:l.hand,aanzicht:b,positie:D,gemengd:!k.fouten.every(t=>t.houding||t.plaatsing||t.diagram)})))")
patch('fout-label',
 "function hi({fout:t,hand:n,aanzicht:r,positie:i}){",
 "function hi({fout:t,hand:n,aanzicht:r,positie:i,gemengd:Gq}){")
patch('fout-summary',
 "e.default.createElement(`summary`,null,z(t.titel,n))",
 "e.default.createElement(`summary`,null,e.default.createElement(`span`,null,z(t.titel,n)),Gq&&(t.houding||t.plaatsing||t.diagram)&&e.default.createElement(`span`,{className:`fout-beeld`},`met beeld`))")

# Greep: eigen foto bij "Zo zit hij goed" (fase.foto = 'greep-goed') en tekst in het handdruk-diagram
import base64 as _b64, os as _os
_fp = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), 'foto', 'greep-goed.jpg')
_fd = 'data:image/jpeg;base64,' + _b64.b64encode(open(_fp, 'rb').read()).decode()
import re as _re
_KR = "Kr={'greep-goed':{src:'" + _fd + "',alt:'Continentale greep (pistoolgreep): V tussen duim en wijsvinger bovenop de greep, koord om de pols',ar:'1 / 1',w:900,h:900}};"
def _kr(s):
    n = len(_re.findall(r"Kr=\{(?:'greep-goed':\{src:'data:[^']*',[^}]*\})?\};", s))
    if n != 1: raise SystemExit(f'greep-foto: Kr gevonden {n}x')
    return _re.sub(r"Kr=\{(?:'greep-goed':\{src:'data:[^']*',[^}]*\})?\};", lambda m: _KR, s)
patch('greep-foto', _kr, _KR)
patch('foto-verhouding',
 "className:`plaatje foto`,style:{aspectRatio:`4 / 3`}},e.default.createElement(`img`,{src:Kr[a.foto].src,alt:Kr[a.foto].alt,width:960,height:720,",
 "className:`plaatje foto`,style:{aspectRatio:Kr[a.foto].ar||`4 / 3`}},e.default.createElement(`img`,{src:Kr[a.foto].src,alt:Kr[a.foto].alt,width:Kr[a.foto].w||960,height:Kr[a.foto].h||720,")
patch('greep-handdruk-tekst',
 "`Geef het racket`),e.default.createElement($,{x:188,y:128,gewicht:600},`een hand`)",
 "`Langs de rand`),e.default.createElement($,{x:188,y:128,gewicht:600},`naar de greep`)")

# Terug: scrollpositie per scherm onthouden en herstellen (in plaats van altijd bovenaan)
patch('terug-scroll',
 "(0,e.useEffect)(()=>{c.current&&(c.current.scrollTop=0)},[s]);",
 "let Zsc=(0,e.useRef)(new WeakMap),Zsr=(0,e.useRef)(s);Zsr.current=s;(0,e.useEffect)(()=>{let m=c.current;if(!m)return;let f=()=>{Zsr.current&&typeof Zsr.current==`object`&&Zsc.current.set(Zsr.current,m.scrollTop)};m.addEventListener(`scroll`,f,{passive:!0});return()=>m.removeEventListener(`scroll`,f)},[]);(0,e.useEffect)(()=>{let m=c.current;if(!m)return;let y=s&&typeof s==`object`?Zsc.current.get(s)||0:0;m.scrollTop=y;if(y)requestAnimationFrame(()=>{m.scrollTop=y})},[s]);")

# Over de app: korte disclaimer onderaan
patch('over-disclaimer',
 'gelden de regels van YouTube."],"stijl":"klein"}]}',
 'gelden de regels van YouTube."],"stijl":"klein"},{"kop":"Goed om te weten","tekst":["Dit is een hobbyproject, voor de lol gemaakt. De uitleg en oefeningen zijn met zorg samengesteld, maar ze vervangen geen trainer en je kunt er geen rechten aan ontlenen.","Oefenen doe je op eigen risico. Warm goed op, bouw rustig op en stop als iets pijn doet."],"stijl":"klein"}]}')

# Over de app: teksten bij de nieuwe werking
patch('over-kijk',
 '["Kijk","Speel de animatie af op 0,25× en sleep over het beeld om rond te draaien.',
 '["Kijk","De animatie start vanzelf. Pauzeer, zet hem op 0,25× en sleep over het beeld om rond te draaien.')
patch('over-vergelijk',
 'op een fout en je ziet fout naast goed. Dit zijn',
 'op een fout voor het gevolg en het herstel. Staat er \\\\"met beeld\\\\" bij, dan zie je ook fout naast goed. Dit zijn')

# 6. Eindstand na de laatste fase (level.eind = [{houding, ms}, ...]), geen extra fase
patch('eindstand-beweging',
 "beweging:f===`3d`&&M.length>1&&Ut(e.id)?Bt(tn(M,I),n):void 0",
 "beweging:f===`3d`&&M.length>1&&Ut(e.id)?Bt(Array.isArray(t.eind)&&t.eind.length?t.eind.reduce((a,q)=>(a.push({t:a[a.length-1].t+(q.ms||600),pose:A[q.houding]||A.klaar,offset:M[M.length-1].offset,raak:!1}),a),tn(M,I)):tn(M,I),n):void 0")
patch('eindstand-totaal',
 "totaal:(u=I[I.length-1])==null?0:u,baan:j",
 "totaal:((u=I[I.length-1])==null?0:u)+(f===`3d`&&M.length>1&&Ut(e.id)&&Array.isArray(t.eind)?t.eind.reduce((s,q)=>s+(q.ms||600),0):0),baan:j")

# 7. Startpositie per level (baanPad.startX): beginpositie ligt vast, ook voor linkshandigen
patch('startX',
 "_=(i=g==null?void 0:g.speler[0])==null?7.5:i",
 "_=g&&g.startX!=null?(F0=>g.startX-(F0&&F0.baan&&F0.baan.verschuiving?h*F0.baan.verschuiving[0]:0)-(F0&&A[F0.houding]?(n===`links`?-1:1)*A[F0.houding].bekken[2]:0))(t.fases[0]):(i=g==null?void 0:g.speler[0])==null?7.5:i")

# 8. Onderarmdraai anatomisch meten (t.o.v. de bovenarm) in plaats van t.o.v. een vaste richting in de romp.
#    De oude referentie sloeg om als de onderarm naar achter-beneden wees (uitzwaai smash/víbora): racket draaide 360°.
patch('onderarm-frame',
 "function lt(e,t){let n=it(t,st)",
 "function lt(e,t,u){if(u){let w=H(u,U(e,W(u,e))),m=Te(w);if(m>.12){let o=U(w,1/m);return[e,o,G(e,o)]}}let n=it(t,st)")
patch('onderarm-frame-sleutel',
 "o=lt(K(H(e.handR,e.elleboogR)),n);return{elleboog:",
 "o=lt(K(H(e.handR,e.elleboogR)),n,K(H(e.elleboogR,e.schouderR)));return{elleboog:")
patch('onderarm-frame-afspelen',
 "let n=lt(K(H(C,O)),t),r=ht(n,e.arm.pols)",
 "let n=lt(K(H(C,O)),t,K(H(O,p))),r=ht(n,e.arm.pols)")

CSS = (".hand-keuze{display:grid;grid-template-columns:1fr 1fr;gap:12px}"
 ".hand-tegel{display:grid;justify-items:center;gap:6px;padding:14px 8px 12px;border:2px solid var(--line);border-radius:14px;background:var(--surface);color:var(--muted);font-weight:600;font-size:16px}"
 ".hand-tegel svg{width:64px;height:64px;fill:none;stroke:currentColor;stroke-width:2.2;stroke-linecap:round;stroke-linejoin:round}"
 ".hand-tegel.aan{border-color:var(--accent);background:var(--accent-zacht);color:var(--accent)}"
 ".welkom-over{justify-self:start}"
 ".fout-beeld{margin-left:auto;font-family:var(--f-body);font-size:12px;font-weight:600;color:var(--accent);background:var(--accent-zacht);border-radius:999px;padding:2px 8px;white-space:nowrap}"
 ".fout summary:has(.fout-beeld):after{margin-left:6px}"
 ".tip-beginscherm{background:var(--accent-zacht);color:var(--fg);border-radius:var(--r);padding:14px 16px;display:grid;gap:6px;margin-top:12px;text-align:left}"
 ".tip-beginscherm h4{font-family:var(--f-display);font-size:20px;font-weight:600;margin:0}"
 ".tip-beginscherm p{margin:0}"
 ".kan-al .link{color:inherit;margin-right:0}")
CSS_MERK = "/*codepatch-css*/"

# Greep: eigen tekening 'Zo zit hij goed' (hand aan de greep, spiegelt voor links) (nov 2026)
GREEP_IDEAAL = 'case`greep-ideaal`:a=e.default.createElement(`g`,{dangerouslySetInnerHTML:{__html:i?"<g transform=\\"translate(184 0) scale(-1 1)\\"><ellipse cx=\\"93\\" cy=\\"14\\" rx=\\"25\\" ry=\\"90\\" fill=\\"var(--diag-blad)\\" stroke=\\"var(--fg)\\" stroke-width=\\"2.5\\"/><circle cx=\\"86\\" cy=\\"-24\\" r=\\"1.7\\" fill=\\"var(--fg)\\" fill-opacity=\\".28\\"/><circle cx=\\"93\\" cy=\\"-24\\" r=\\"1.7\\" fill=\\"var(--fg)\\" fill-opacity=\\".28\\"/><circle cx=\\"100\\" cy=\\"-24\\" r=\\"1.7\\" fill=\\"var(--fg)\\" fill-opacity=\\".28\\"/><circle cx=\\"89\\" cy=\\"-11\\" r=\\"1.7\\" fill=\\"var(--fg)\\" fill-opacity=\\".28\\"/><circle cx=\\"96\\" cy=\\"-11\\" r=\\"1.7\\" fill=\\"var(--fg)\\" fill-opacity=\\".28\\"/><circle cx=\\"103\\" cy=\\"-11\\" r=\\"1.7\\" fill=\\"var(--fg)\\" fill-opacity=\\".28\\"/><circle cx=\\"86\\" cy=\\"2\\" r=\\"1.7\\" fill=\\"var(--fg)\\" fill-opacity=\\".28\\"/><circle cx=\\"93\\" cy=\\"2\\" r=\\"1.7\\" fill=\\"var(--fg)\\" fill-opacity=\\".28\\"/><circle cx=\\"100\\" cy=\\"2\\" r=\\"1.7\\" fill=\\"var(--fg)\\" fill-opacity=\\".28\\"/><circle cx=\\"89\\" cy=\\"15\\" r=\\"1.7\\" fill=\\"var(--fg)\\" fill-opacity=\\".28\\"/><circle cx=\\"96\\" cy=\\"15\\" r=\\"1.7\\" fill=\\"var(--fg)\\" fill-opacity=\\".28\\"/><circle cx=\\"103\\" cy=\\"15\\" r=\\"1.7\\" fill=\\"var(--fg)\\" fill-opacity=\\".28\\"/><circle cx=\\"86\\" cy=\\"28\\" r=\\"1.7\\" fill=\\"var(--fg)\\" fill-opacity=\\".28\\"/><circle cx=\\"93\\" cy=\\"28\\" r=\\"1.7\\" fill=\\"var(--fg)\\" fill-opacity=\\".28\\"/><circle cx=\\"100\\" cy=\\"28\\" r=\\"1.7\\" fill=\\"var(--fg)\\" fill-opacity=\\".28\\"/><circle cx=\\"89\\" cy=\\"41\\" r=\\"1.7\\" fill=\\"var(--fg)\\" fill-opacity=\\".28\\"/><circle cx=\\"96\\" cy=\\"41\\" r=\\"1.7\\" fill=\\"var(--fg)\\" fill-opacity=\\".28\\"/><circle cx=\\"103\\" cy=\\"41\\" r=\\"1.7\\" fill=\\"var(--fg)\\" fill-opacity=\\".28\\"/><circle cx=\\"86\\" cy=\\"54\\" r=\\"1.7\\" fill=\\"var(--fg)\\" fill-opacity=\\".28\\"/><circle cx=\\"93\\" cy=\\"54\\" r=\\"1.7\\" fill=\\"var(--fg)\\" fill-opacity=\\".28\\"/><circle cx=\\"100\\" cy=\\"54\\" r=\\"1.7\\" fill=\\"var(--fg)\\" fill-opacity=\\".28\\"/><circle cx=\\"89\\" cy=\\"67\\" r=\\"1.7\\" fill=\\"var(--fg)\\" fill-opacity=\\".28\\"/><circle cx=\\"96\\" cy=\\"67\\" r=\\"1.7\\" fill=\\"var(--fg)\\" fill-opacity=\\".28\\"/><circle cx=\\"103\\" cy=\\"67\\" r=\\"1.7\\" fill=\\"var(--fg)\\" fill-opacity=\\".28\\"/><circle cx=\\"86\\" cy=\\"80\\" r=\\"1.7\\" fill=\\"var(--fg)\\" fill-opacity=\\".28\\"/><circle cx=\\"93\\" cy=\\"80\\" r=\\"1.7\\" fill=\\"var(--fg)\\" fill-opacity=\\".28\\"/><circle cx=\\"100\\" cy=\\"80\\" r=\\"1.7\\" fill=\\"var(--fg)\\" fill-opacity=\\".28\\"/><path d=\\"M81 124 L79 100 Q93 92 107 100 L105 124 Z\\" fill=\\"var(--diag-blad)\\" stroke=\\"var(--fg)\\" stroke-width=\\"2.5\\" stroke-linejoin=\\"round\\"/><rect x=\\"82\\" y=\\"118\\" width=\\"22\\" height=\\"108\\" rx=\\"4\\" fill=\\"var(--diag-greep)\\" stroke=\\"var(--fg)\\" stroke-width=\\"2.5\\"/><path d=\\"M83 130 L103 126\\" stroke=\\"var(--fg)\\" stroke-opacity=\\".18\\" stroke-width=\\"1.5\\"/><path d=\\"M83 137 L103 133\\" stroke=\\"var(--fg)\\" stroke-opacity=\\".18\\" stroke-width=\\"1.5\\"/><path d=\\"M83 144 L103 140\\" stroke=\\"var(--fg)\\" stroke-opacity=\\".18\\" stroke-width=\\"1.5\\"/><path d=\\"M83 151 L103 147\\" stroke=\\"var(--fg)\\" stroke-opacity=\\".18\\" stroke-width=\\"1.5\\"/><rect x=\\"79\\" y=\\"224\\" width=\\"28\\" height=\\"9\\" rx=\\"4\\" fill=\\"var(--diag-blad)\\" stroke=\\"var(--fg)\\" stroke-width=\\"2.5\\"/><path d=\\"M102 206 L142 192 L214 236 L214 250 L124 250 Z\\" fill=\\"#e8c2a2\\" stroke=\\"#8a5a44\\" stroke-width=\\"1.8\\" stroke-linejoin=\\"round\\"/><path d=\\"M93 233 C 95 246, 112 244, 116 212\\" fill=\\"none\\" stroke=\\"var(--fg)\\" stroke-width=\\"3\\" stroke-linecap=\\"round\\"/><path d=\\"M106 214 C 120 210, 134 204, 146 197\\" fill=\\"none\\" stroke=\\"var(--fg)\\" stroke-width=\\"4.5\\" stroke-linecap=\\"round\\"/><rect x=\\"70\\" y=\\"168\\" width=\\"30\\" height=\\"17\\" rx=\\"8.5\\" fill=\\"#e8c2a2\\" stroke=\\"#8a5a44\\" stroke-width=\\"1.8\\" stroke-linejoin=\\"round\\"/><rect x=\\"72\\" y=\\"185\\" width=\\"28\\" height=\\"16\\" rx=\\"8.0\\" fill=\\"#e8c2a2\\" stroke=\\"#8a5a44\\" stroke-width=\\"1.8\\" stroke-linejoin=\\"round\\"/><rect x=\\"75\\" y=\\"201\\" width=\\"25\\" height=\\"14\\" rx=\\"7.0\\" fill=\\"#e8c2a2\\" stroke=\\"#8a5a44\\" stroke-width=\\"1.8\\" stroke-linejoin=\\"round\\"/><path d=\\"M102 146 C 92 136, 74 137, 67 147 C 62 155, 66 163, 75 162 C 84 161, 92 156, 102 158 Z\\" fill=\\"#e8c2a2\\" stroke=\\"#8a5a44\\" stroke-width=\\"1.8\\" stroke-linejoin=\\"round\\"/><path d=\\"M80 140 C 79 146, 79 154, 81 161\\" fill=\\"none\\" stroke=\\"#8a5a44\\" stroke-width=\\"1.2\\" stroke-opacity=\\".6\\"/><path d=\\"M106 210 C 96 202, 86 188, 80 173 C 76 164, 82 156, 90 160 C 94 162, 96 158, 96 150 C 102 137, 124 133, 135 141 C 144 155, 148 178, 144 194 C 138 206, 122 213, 106 210 Z\\" fill=\\"#e8c2a2\\" stroke=\\"#8a5a44\\" stroke-width=\\"1.8\\" stroke-linejoin=\\"round\\"/><path d=\\"M106 210 C 96 202, 86 188, 80 173 C 76 164, 82 156, 90 160 C 94 162, 96 160, 97 158 C 102 172, 110 186, 122 196 C 116 204, 112 209, 106 210 Z\\" fill=\\"#c8957a\\" fill-opacity=\\".55\\"/><path d=\\"M97 158 C 102 172, 110 186, 122 196\\" fill=\\"none\\" stroke=\\"#8a5a44\\" stroke-width=\\"1.3\\" stroke-opacity=\\".7\\" stroke-linecap=\\"round\\"/><path d=\\"M82 168 C 81 163, 85 160, 88 162 L 92 167 C 89 170, 84 171, 82 168 Z\\" fill=\\"#f3dccb\\" stroke=\\"#8a5a44\\" stroke-width=\\"1\\"/><path d=\\"M108 140 q5 -3 9 0 M120 138 q5 -2 9 1\\" fill=\\"none\\" stroke=\\"#8a5a44\\" stroke-width=\\"1.2\\" stroke-opacity=\\".6\\"/></g><path d=\\"M81 140 L89 150 L97 140\\" fill=\\"none\\" stroke=\\"var(--accent)\\" stroke-width=\\"4.5\\" stroke-linecap=\\"round\\" stroke-linejoin=\\"round\\"/><circle cx=\\"123\\" cy=\\"151\\" r=\\"6\\" fill=\\"var(--bal)\\" stroke=\\"var(--bal-rand)\\" stroke-width=\\"2\\"/><path d=\\"M198 96 L204 103 L210 96\\" fill=\\"none\\" stroke=\\"var(--accent)\\" stroke-width=\\"4\\" stroke-linecap=\\"round\\" stroke-linejoin=\\"round\\"/><text x=\\"220\\" y=\\"105\\" font-size=\\"12\\" font-weight=\\"500\\" fill=\\"var(--fg)\\" font-family=\\"var(--f-body)\\">V bovenop</text><circle cx=\\"204\\" cy=\\"134\\" r=\\"6\\" fill=\\"var(--bal)\\" stroke=\\"var(--bal-rand)\\" stroke-width=\\"2\\"/><text x=\\"220\\" y=\\"139\\" font-size=\\"12\\" font-weight=\\"500\\" fill=\\"var(--fg)\\" font-family=\\"var(--f-body)\\">Wijsvinger iets los,</text><text x=\\"220\\" y=\\"155\\" font-size=\\"12\\" font-weight=\\"500\\" fill=\\"var(--fg)\\" font-family=\\"var(--f-body)\\">als een trekker</text>":"<ellipse cx=\\"93\\" cy=\\"14\\" rx=\\"25\\" ry=\\"90\\" fill=\\"var(--diag-blad)\\" stroke=\\"var(--fg)\\" stroke-width=\\"2.5\\"/><circle cx=\\"86\\" cy=\\"-24\\" r=\\"1.7\\" fill=\\"var(--fg)\\" fill-opacity=\\".28\\"/><circle cx=\\"93\\" cy=\\"-24\\" r=\\"1.7\\" fill=\\"var(--fg)\\" fill-opacity=\\".28\\"/><circle cx=\\"100\\" cy=\\"-24\\" r=\\"1.7\\" fill=\\"var(--fg)\\" fill-opacity=\\".28\\"/><circle cx=\\"89\\" cy=\\"-11\\" r=\\"1.7\\" fill=\\"var(--fg)\\" fill-opacity=\\".28\\"/><circle cx=\\"96\\" cy=\\"-11\\" r=\\"1.7\\" fill=\\"var(--fg)\\" fill-opacity=\\".28\\"/><circle cx=\\"103\\" cy=\\"-11\\" r=\\"1.7\\" fill=\\"var(--fg)\\" fill-opacity=\\".28\\"/><circle cx=\\"86\\" cy=\\"2\\" r=\\"1.7\\" fill=\\"var(--fg)\\" fill-opacity=\\".28\\"/><circle cx=\\"93\\" cy=\\"2\\" r=\\"1.7\\" fill=\\"var(--fg)\\" fill-opacity=\\".28\\"/><circle cx=\\"100\\" cy=\\"2\\" r=\\"1.7\\" fill=\\"var(--fg)\\" fill-opacity=\\".28\\"/><circle cx=\\"89\\" cy=\\"15\\" r=\\"1.7\\" fill=\\"var(--fg)\\" fill-opacity=\\".28\\"/><circle cx=\\"96\\" cy=\\"15\\" r=\\"1.7\\" fill=\\"var(--fg)\\" fill-opacity=\\".28\\"/><circle cx=\\"103\\" cy=\\"15\\" r=\\"1.7\\" fill=\\"var(--fg)\\" fill-opacity=\\".28\\"/><circle cx=\\"86\\" cy=\\"28\\" r=\\"1.7\\" fill=\\"var(--fg)\\" fill-opacity=\\".28\\"/><circle cx=\\"93\\" cy=\\"28\\" r=\\"1.7\\" fill=\\"var(--fg)\\" fill-opacity=\\".28\\"/><circle cx=\\"100\\" cy=\\"28\\" r=\\"1.7\\" fill=\\"var(--fg)\\" fill-opacity=\\".28\\"/><circle cx=\\"89\\" cy=\\"41\\" r=\\"1.7\\" fill=\\"var(--fg)\\" fill-opacity=\\".28\\"/><circle cx=\\"96\\" cy=\\"41\\" r=\\"1.7\\" fill=\\"var(--fg)\\" fill-opacity=\\".28\\"/><circle cx=\\"103\\" cy=\\"41\\" r=\\"1.7\\" fill=\\"var(--fg)\\" fill-opacity=\\".28\\"/><circle cx=\\"86\\" cy=\\"54\\" r=\\"1.7\\" fill=\\"var(--fg)\\" fill-opacity=\\".28\\"/><circle cx=\\"93\\" cy=\\"54\\" r=\\"1.7\\" fill=\\"var(--fg)\\" fill-opacity=\\".28\\"/><circle cx=\\"100\\" cy=\\"54\\" r=\\"1.7\\" fill=\\"var(--fg)\\" fill-opacity=\\".28\\"/><circle cx=\\"89\\" cy=\\"67\\" r=\\"1.7\\" fill=\\"var(--fg)\\" fill-opacity=\\".28\\"/><circle cx=\\"96\\" cy=\\"67\\" r=\\"1.7\\" fill=\\"var(--fg)\\" fill-opacity=\\".28\\"/><circle cx=\\"103\\" cy=\\"67\\" r=\\"1.7\\" fill=\\"var(--fg)\\" fill-opacity=\\".28\\"/><circle cx=\\"86\\" cy=\\"80\\" r=\\"1.7\\" fill=\\"var(--fg)\\" fill-opacity=\\".28\\"/><circle cx=\\"93\\" cy=\\"80\\" r=\\"1.7\\" fill=\\"var(--fg)\\" fill-opacity=\\".28\\"/><circle cx=\\"100\\" cy=\\"80\\" r=\\"1.7\\" fill=\\"var(--fg)\\" fill-opacity=\\".28\\"/><path d=\\"M81 124 L79 100 Q93 92 107 100 L105 124 Z\\" fill=\\"var(--diag-blad)\\" stroke=\\"var(--fg)\\" stroke-width=\\"2.5\\" stroke-linejoin=\\"round\\"/><rect x=\\"82\\" y=\\"118\\" width=\\"22\\" height=\\"108\\" rx=\\"4\\" fill=\\"var(--diag-greep)\\" stroke=\\"var(--fg)\\" stroke-width=\\"2.5\\"/><path d=\\"M83 130 L103 126\\" stroke=\\"var(--fg)\\" stroke-opacity=\\".18\\" stroke-width=\\"1.5\\"/><path d=\\"M83 137 L103 133\\" stroke=\\"var(--fg)\\" stroke-opacity=\\".18\\" stroke-width=\\"1.5\\"/><path d=\\"M83 144 L103 140\\" stroke=\\"var(--fg)\\" stroke-opacity=\\".18\\" stroke-width=\\"1.5\\"/><path d=\\"M83 151 L103 147\\" stroke=\\"var(--fg)\\" stroke-opacity=\\".18\\" stroke-width=\\"1.5\\"/><rect x=\\"79\\" y=\\"224\\" width=\\"28\\" height=\\"9\\" rx=\\"4\\" fill=\\"var(--diag-blad)\\" stroke=\\"var(--fg)\\" stroke-width=\\"2.5\\"/><path d=\\"M102 206 L142 192 L214 236 L214 250 L124 250 Z\\" fill=\\"#e8c2a2\\" stroke=\\"#8a5a44\\" stroke-width=\\"1.8\\" stroke-linejoin=\\"round\\"/><path d=\\"M93 233 C 95 246, 112 244, 116 212\\" fill=\\"none\\" stroke=\\"var(--fg)\\" stroke-width=\\"3\\" stroke-linecap=\\"round\\"/><path d=\\"M106 214 C 120 210, 134 204, 146 197\\" fill=\\"none\\" stroke=\\"var(--fg)\\" stroke-width=\\"4.5\\" stroke-linecap=\\"round\\"/><rect x=\\"70\\" y=\\"168\\" width=\\"30\\" height=\\"17\\" rx=\\"8.5\\" fill=\\"#e8c2a2\\" stroke=\\"#8a5a44\\" stroke-width=\\"1.8\\" stroke-linejoin=\\"round\\"/><rect x=\\"72\\" y=\\"185\\" width=\\"28\\" height=\\"16\\" rx=\\"8.0\\" fill=\\"#e8c2a2\\" stroke=\\"#8a5a44\\" stroke-width=\\"1.8\\" stroke-linejoin=\\"round\\"/><rect x=\\"75\\" y=\\"201\\" width=\\"25\\" height=\\"14\\" rx=\\"7.0\\" fill=\\"#e8c2a2\\" stroke=\\"#8a5a44\\" stroke-width=\\"1.8\\" stroke-linejoin=\\"round\\"/><path d=\\"M102 146 C 92 136, 74 137, 67 147 C 62 155, 66 163, 75 162 C 84 161, 92 156, 102 158 Z\\" fill=\\"#e8c2a2\\" stroke=\\"#8a5a44\\" stroke-width=\\"1.8\\" stroke-linejoin=\\"round\\"/><path d=\\"M80 140 C 79 146, 79 154, 81 161\\" fill=\\"none\\" stroke=\\"#8a5a44\\" stroke-width=\\"1.2\\" stroke-opacity=\\".6\\"/><path d=\\"M106 210 C 96 202, 86 188, 80 173 C 76 164, 82 156, 90 160 C 94 162, 96 158, 96 150 C 102 137, 124 133, 135 141 C 144 155, 148 178, 144 194 C 138 206, 122 213, 106 210 Z\\" fill=\\"#e8c2a2\\" stroke=\\"#8a5a44\\" stroke-width=\\"1.8\\" stroke-linejoin=\\"round\\"/><path d=\\"M106 210 C 96 202, 86 188, 80 173 C 76 164, 82 156, 90 160 C 94 162, 96 160, 97 158 C 102 172, 110 186, 122 196 C 116 204, 112 209, 106 210 Z\\" fill=\\"#c8957a\\" fill-opacity=\\".55\\"/><path d=\\"M97 158 C 102 172, 110 186, 122 196\\" fill=\\"none\\" stroke=\\"#8a5a44\\" stroke-width=\\"1.3\\" stroke-opacity=\\".7\\" stroke-linecap=\\"round\\"/><path d=\\"M82 168 C 81 163, 85 160, 88 162 L 92 167 C 89 170, 84 171, 82 168 Z\\" fill=\\"#f3dccb\\" stroke=\\"#8a5a44\\" stroke-width=\\"1\\"/><path d=\\"M108 140 q5 -3 9 0 M120 138 q5 -2 9 1\\" fill=\\"none\\" stroke=\\"#8a5a44\\" stroke-width=\\"1.2\\" stroke-opacity=\\".6\\"/><path d=\\"M87 140 L95 150 L103 140\\" fill=\\"none\\" stroke=\\"var(--accent)\\" stroke-width=\\"4.5\\" stroke-linecap=\\"round\\" stroke-linejoin=\\"round\\"/><circle cx=\\"61\\" cy=\\"151\\" r=\\"6\\" fill=\\"var(--bal)\\" stroke=\\"var(--bal-rand)\\" stroke-width=\\"2\\"/><path d=\\"M198 96 L204 103 L210 96\\" fill=\\"none\\" stroke=\\"var(--accent)\\" stroke-width=\\"4\\" stroke-linecap=\\"round\\" stroke-linejoin=\\"round\\"/><text x=\\"220\\" y=\\"105\\" font-size=\\"12\\" font-weight=\\"500\\" fill=\\"var(--fg)\\" font-family=\\"var(--f-body)\\">V bovenop</text><circle cx=\\"204\\" cy=\\"134\\" r=\\"6\\" fill=\\"var(--bal)\\" stroke=\\"var(--bal-rand)\\" stroke-width=\\"2\\"/><text x=\\"220\\" y=\\"139\\" font-size=\\"12\\" font-weight=\\"500\\" fill=\\"var(--fg)\\" font-family=\\"var(--f-body)\\">Wijsvinger iets los,</text><text x=\\"220\\" y=\\"155\\" font-size=\\"12\\" font-weight=\\"500\\" fill=\\"var(--fg)\\" font-family=\\"var(--f-body)\\">als een trekker</text>"}});break;'
patch('greep-ideaal', "case`greep-v-controle`:a=", GREEP_IDEAAL+"case`greep-v-controle`:a=")

# Shirt: hangt recht over de onderrug en billen: geen dijbeen-invloed (volgt de bilnaad niet meer) en de holte opgevuld (nov 2026)
SHIRT_RECHT = 'e===`lichaam`&&h.length&&((P,N,G,B,V,F,W,NM)=>{let M=wn.maten,ty=M.taille,lo=ty-.1,hi=(M.schouderY||ty+.45)-.16,sp=NM.indexOf(`spine`),pak=[],hel=new Map;for(let i=0;i<G.length;i++){if(G[i]!==1)continue;let a=B+i;if(sp>=0)for(let j=0;j<4;j++){let nm=NM[F[a*4+j]]||``;if(/^thigh/.test(nm)&&W[a*4+j]>0){let w=W[a*4+j];W[a*4+j]=0;let k=-1;for(let q=0;q<4;q++)F[a*4+q]===sp&&q!==j&&(k=q);k<0&&(k=j,F[a*4+j]=sp);W[a*4+k]+=w}}let y=V[a*3+1];if(y<lo||y>hi||N[a*3]>-.2)continue;pak.push(a)}let romp=(lijst,as1)=>{let bak=new Map;for(let a of lijst){let k=Math.round(P[a*3+as1]/.012);bak.has(k)||bak.set(k,[]);bak.get(k).push(a)}for(let[,r]of bak){if(r.length<3)continue;let as2=as1===1?2:1,pt=r.map(a=>[P[a*3+as2],-P[a*3]]).sort((p,q)=>p[0]-q[0]),h=[];for(let p of pt){for(;h.length>=2;){let o=h[h.length-2],q=h[h.length-1];if((q[0]-o[0])*(p[1]-o[1])-(q[1]-o[1])*(p[0]-o[0])>=0)h.pop();else break}h.push(p)}for(let a of r){let z=P[a*3+as2],d=-P[a*3],t=d,sl=0;for(let j=0;j+1<h.length;j++){let p=h[j],q=h[j+1];if(z>=p[0]&&z<=q[0]){q[0]>p[0]?(sl=(q[1]-p[1])/(q[0]-p[0]),t=p[1]+sl*(z-p[0])):t=Math.max(p[1],q[1]);break}}if(t>d+1e-4){P[a*3]=-t;let o=hel.get(a)||[-N[a*3+1]/N[a*3],-N[a*3+2]/N[a*3]];o[as2-1]=-sl;hel.set(a,o)}}}};romp(pak.filter(a=>V[a*3+1]<ty+.12),1);romp(pak,2);romp(pak.filter(a=>V[a*3+1]<ty+.12),1);for(let[a,[sy,sz]]of hel){let x=-1,y=sy,z=sz,L=Math.hypot(x,y,z);N[a*3]=x/L,N[a*3+1]=y/L,N[a*3+2]=z/L}for(let ronde=0;ronde<3;ronde++){let nw=pak.map(a=>{let sx=0,sy=0,sz=0;for(let c of pak){let d=Math.hypot(P[a*3]-P[c*3],P[a*3+1]-P[c*3+1],P[a*3+2]-P[c*3+2]);if(d<.05){let w=1-d/.05;sx+=N[c*3]*w,sy+=N[c*3+1]*w,sz+=N[c*3+2]*w}}let L=Math.hypot(sx,sy,sz)||1;return[sx/L,sy/L,sz/L]});pak.forEach((a,i)=>{N[a*3]=nw[i][0],N[a*3+1]=nw[i][1],N[a*3+2]=nw[i][2]})}})(s,l,g,_,v,f,p,r.namen);'
patch('shirt-recht', "let T=new n.BufferGeometry;if(T.setAttribute(`position`", SHIRT_RECHT+"let T=new n.BufferGeometry;if(T.setAttribute(`position`")

# Broek: geen stoflaag boven de zoom van het shirt, zodat de broeksband niet door het shirt prikt (nov 2026)
patch('broek-onder-shirt', "else if (vLaag < 2.5) { if (b.y < ${o(s.knie+.09)}) discard; }", "else if (vLaag < 2.5) { if (b.y < ${o(s.knie+.09)} || b.y > ${o(s.taille-.06)}) discard; }")

def pas_toe(pad):
    s = open(pad, encoding='utf-8').read()
    for naam, oud, nieuw in PATCHES:
        if callable(oud):
            if nieuw in s: print(' =', naam); continue
            s = oud(s); print(' +', naam); continue
        if nieuw in s: print(' =', naam); continue
        n = s.count(oud)
        if n != 1: raise SystemExit(f'{pad}: patch {naam} gevonden {n}x')
        s = s.replace(oud, nieuw); print(' +', naam)
    if CSS_MERK not in s:
        k = s.index('</style>'); s = s[:k] + CSS_MERK + CSS + s[k:]; print(' + css')
    open(pad, 'w', encoding='utf-8').write(s)

if __name__ == '__main__':
    for p in sys.argv[1:]:
        print(p); pas_toe(p)
