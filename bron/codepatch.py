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
