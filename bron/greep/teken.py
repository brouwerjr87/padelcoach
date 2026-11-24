import sys
LICHT=dict(paneel='#f6f8fa',fg='#12202b',muted='#566673',line='#d3dce3',accent='#1c5a8e',bal='#d4ee2e',balrand='#8a9a10',blad='#9fb3c2',greep='#e2e9ee')
DONKER=dict(paneel='#111c25',fg='#e4ecf1',muted='#93a4b1',line='#273744',accent='#6fb0e6',bal='#d4ee2e',balrand='#8a9a10',blad='#4a6072',greep='#1d2c38')
HUID='#e8c2a2'; HUIDD='#c8957a'; LIJN='#8a5a44'
def plaatje(c):
    s=[]
    H=f'fill="{HUID}" stroke="{LIJN}" stroke-width="1.8" stroke-linejoin="round"'
    s.append(f'<ellipse cx="93" cy="14" rx="25" ry="90" fill="{c["blad"]}" stroke="{c["fg"]}" stroke-width="2.5"/>')
    for y in range(-24,84,13):
        for dx in (-7,0,7):
            s.append(f'<circle cx="{93+dx+(3 if (y//13)%2 else 0)}" cy="{y}" r="1.7" fill="{c["fg"]}" fill-opacity=".28"/>')
    s.append(f'<path d="M81 124 L79 100 Q93 92 107 100 L105 124 Z" fill="{c["blad"]}" stroke="{c["fg"]}" stroke-width="2.5" stroke-linejoin="round"/>')
    s.append(f'<rect x="82" y="118" width="22" height="108" rx="4" fill="{c["greep"]}" stroke="{c["fg"]}" stroke-width="2.5"/>')
    for y in range(126,150,7): s.append(f'<path d="M83 {y+4} L103 {y}" stroke="{c["fg"]}" stroke-opacity=".18" stroke-width="1.5"/>')
    s.append(f'<rect x="79" y="224" width="28" height="9" rx="4" fill="{c["blad"]}" stroke="{c["fg"]}" stroke-width="2.5"/>')
    # onderarm
    s.append(f'<path d="M102 206 L142 192 L214 236 L214 250 L124 250 Z" {H}/>')
    # koord
    s.append(f'<path d="M93 233 C 95 246, 112 244, 116 212" fill="none" stroke="{c["fg"]}" stroke-width="3" stroke-linecap="round"/>')
    s.append(f'<path d="M106 214 C 120 210, 134 204, 146 197" fill="none" stroke="{c["fg"]}" stroke-width="4.5" stroke-linecap="round"/>')
    # middel-, ring- en pink (achter de greep om, links zichtbaar)
    for (y,h,x0) in [(168,17,70),(185,16,72),(201,14,75)]:
        s.append(f'<rect x="{x0}" y="{y}" width="{100-x0}" height="{h}" rx="{h/2}" {H}/>')
    # wijsvinger als trekker: iets losser en hoger
    s.append(f'<path d="M102 146 C 92 136, 74 137, 67 147 C 62 155, 66 163, 75 162 C 84 161, 92 156, 102 158 Z" {H}/>')
    s.append(f'<path d="M80 140 C 79 146, 79 154, 81 161" fill="none" stroke="{LIJN}" stroke-width="1.2" stroke-opacity=".6"/>')
    # handrug + duim als een silhouet
    s.append(f'<path d="M106 210 C 96 202, 86 188, 80 173 C 76 164, 82 156, 90 160 C 94 162, 96 158, 96 150 C 102 137, 124 133, 135 141 C 144 155, 148 178, 144 194 C 138 206, 122 213, 106 210 Z" {H}/>')
    s.append(f'<path d="M106 210 C 96 202, 86 188, 80 173 C 76 164, 82 156, 90 160 C 94 162, 96 160, 97 158 C 102 172, 110 186, 122 196 C 116 204, 112 209, 106 210 Z" fill="{HUIDD}" fill-opacity=".55"/>')
    s.append(f'<path d="M97 158 C 102 172, 110 186, 122 196" fill="none" stroke="{LIJN}" stroke-width="1.3" stroke-opacity=".7" stroke-linecap="round"/>')
    s.append(f'<path d="M82 168 C 81 163, 85 160, 88 162 L 92 167 C 89 170, 84 171, 82 168 Z" fill="#f3dccb" stroke="{LIJN}" stroke-width="1"/>')
    s.append(f'<path d="M108 140 q5 -3 9 0 M120 138 q5 -2 9 1" fill="none" stroke="{LIJN}" stroke-width="1.2" stroke-opacity=".6"/>')
    return '\n'.join(s)
def labels(c,links):
    t=[]
    m=lambda x:184-x if links else x
    vx,vy=m(95),150
    t.append(f'<path d="M{vx-8} {vy-10} L{vx} {vy} L{vx+8} {vy-10}" fill="none" stroke="{c["accent"]}" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round"/>')
    t.append(f'<circle cx="{m(61)}" cy="151" r="6" fill="{c["bal"]}" stroke="{c["balrand"]}" stroke-width="2"/>')
    T=lambda x,y,tekst,kl=None,gw=500,gr=12: f'<text x="{x}" y="{y}" font-size="{gr}" font-weight="{gw}" fill="{kl or c["fg"]}" font-family="Barlow,sans-serif">{tekst}</text>'
    t.append(f'<path d="M198 96 L204 103 L210 96" fill="none" stroke="{c["accent"]}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>')
    t.append(T(220,105,'V bovenop'))
    t.append(f'<circle cx="204" cy="134" r="6" fill="{c["bal"]}" stroke="{c["balrand"]}" stroke-width="2"/>')
    t.append(T(220,139,'Wijsvinger iets los,'))
    t.append(T(220,155,'als een trekker'))
    return ''.join(t)
def svg(c,links=False):
    p=plaatje(c)
    if links: p=f'<g transform="translate(184 0) scale(-1 1)">{p}</g>'
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 240" width="640" height="480"><rect width="320" height="240" fill="{c["paneel"]}"/><g>{p}</g>{labels(c,links)}</svg>'
open('t.html','w').write('<html><body style="margin:0;display:flex;flex-wrap:wrap;gap:8px;background:#888">'+svg(LICHT)+svg(LICHT,True)+svg(DONKER)+'</body></html>')
