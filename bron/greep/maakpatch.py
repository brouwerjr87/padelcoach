import json, importlib.util, sys
spec=importlib.util.spec_from_file_location('t','teken.py'); t=importlib.util.module_from_spec(spec)
src=open('teken.py').read().split("open('t.html'")[0]; exec(src, t.__dict__)
V=dict(paneel='var(--paneel)',fg='var(--fg)',muted='var(--muted)',line='var(--line)',accent='var(--accent)',bal='var(--bal)',balrand='var(--bal-rand)',blad='var(--diag-blad)',greep='var(--diag-greep)')
def binnen(links):
    p=t.plaatje(V)
    if links: p=f'<g transform="translate(184 0) scale(-1 1)">{p}</g>'
    return (p+t.labels(V,links)).replace('Barlow,sans-serif','var(--f-body)').replace('\n','')
R,L=binnen(False),binnen(True)
code="case`greep-ideaal`:a=e.default.createElement(`g`,{dangerouslySetInnerHTML:{__html:i?"+json.dumps(L)+":"+json.dumps(R)+"}});break;"
open('greep-ideaal.js','w').write(code); print(len(code))
