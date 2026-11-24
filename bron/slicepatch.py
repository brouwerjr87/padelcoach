"""Slice-slagen: racket draait van boven naar beneden (om de dwarsas), niet om de verticale as.

Model per slag: een zwaaivlak door de doelrichting f en een (iets gekantelde) opwaartse as U.
Kopricht r(phi) = sin(phi)*f + cos(phi)*U, slagvlak naar het net n(phi) = cos(phi)*f - sin(phi)*U.
phi < 0: kop naar achter, blad open. phi = 90: kop wijst naar het doel. phi > 90: kop naar voren-omlaag.
"""
import json, math
T = json.load(open('technieken.json')); H = json.load(open('houdingen3d.json'))

def n(v): l = math.sqrt(sum(x*x for x in v)); return [x/l for x in v]
def dot(a, b): return sum(x*y for x, y in zip(a, b))
def r3(v): return [round(x, 3) for x in v]
def orth(v, r): d = dot(v, r); return n([v[i]-d*r[i] for i in range(3)])

def vlak_basis(doel_links_graden, kantel_graden, kant):
    """kant: +1 = vlak leunt naar rechts (forehandkant), -1 = naar links (backhandkant)."""
    a = math.radians(doel_links_graden); f = [math.cos(a), 0, -math.sin(a)]
    R = [-f[2], 0, f[0]]
    t = math.radians(kantel_graden)
    U = n([math.cos(t)*[0, 1, 0][i] + kant*math.sin(t)*R[i] for i in range(3)])
    return f, U

def zet(p, basis, phi, backhand=False, hand=None):
    f, U = basis; a = math.radians(phi)
    r = n([math.sin(a)*f[i] + math.cos(a)*U[i] for i in range(3)])
    nn = n([math.cos(a)*f[i] - math.sin(a)*U[i] for i in range(3)])
    p['racket'] = {'richting': r3(r), 'vlak': r3([-x for x in nn] if backhand else nn)}
    if hand: p['handR'] = hand
    return r, nn

def raak(p, basis, phi, backhand=False, hand=None):
    r, nn = zet(p, basis, phi, backhand, hand)
    p['bal'] = r3([p['handR'][i] + 0.3*r[i] + 0.07*nn[i] for i in range(3)])

# Bandeja: dienblad -> open blad bij het raken -> kop naar voren-omlaag richting doel
B = vlak_basis(21, 20, +1)
zet(H['bandeja-laden'], B, -82)
raak(H['bandeja-raak'], B, -25)
zet(H['bandeja-door'], B, 40, hand=[0.55, 1.45, 0.2])
zet(H['bandeja-uit'], B, 112, hand=[0.66, 1.22, -0.12])

# Víbora: schuiner vlak (zijwaartse slice), blad rechter bij het raken
V = vlak_basis(33, 40, +1)
zet(H['vibora-laden'], V, -75)
raak(H['vibora-raak'], V, -12)
zet(H['vibora-uit'], V, 125)

# Bajada forehand
BJ = vlak_basis(16, 15, +1)
raak(H['bajada-raak'], BJ, -20)
zet(H['bajada-uit'], BJ, 118)

# Bajada backhand: vlak aan de linkerkant
BB = vlak_basis(16, 18, -1)
zet(H['bh-bajada-laden'], BB, -70, backhand=True)
raak(H['bh-bajada-raak'], BB, -20, backhand=True)
zet(H['bh-bajada-uit'], BB, 112, backhand=True)

# Backhandvolley: korte stoot van hoog naar laag, kop schuin omhoog
BV = vlak_basis(24, 40, -1)
zet(H['bh-volley-voor'], BV, -35, backhand=True)
raak(H['bh-volley-raak'], BV, -15, backhand=True)
zet(H['bh-volley-uit'], BV, 8, backhand=True, hand=[0.82, 0.86, -0.32])

# Dejada: zelfde open blad, korte duw naar voren-omlaag (geen draai om de lengteas)
p = H['dejada-raak']; r = n(p['racket']['richting']); nn = orth(p['racket']['vlak'], r)
p['bal'] = r3([p['handR'][i] + 0.3*r[i] + 0.07*nn[i] for i in range(3)])
v = H['dejada-voor']; v['racket'] = {'richting': r3(r), 'vlak': r3(orth([nn[0]+0.15, nn[1]-0.2, nn[2]], r))}
v['handR'] = r3([p['handR'][0]-0.2, p['handR'][1]+0.12, p['handR'][2]+0.02])
u = H['dejada-uit']; u['racket'] = {'richting': r3(r), 'vlak': r3(orth([nn[0]-0.1, nn[1]+0.15, nn[2]], r))}
u['handR'] = r3([p['handR'][0]+0.13, p['handR'][1]-0.06, p['handR'][2]-0.02])

# Forehand cortado (laag): uitzwaai naar voren, kop blijft opzij, blad open
p = H['fh-laag-uitzwaai']; r = n([0.55, 0.08, 0.83]); p['handR'] = [0.95, 0.9, 0.12]
p['racket'] = {'richting': r3(r), 'vlak': r3(orth([0.7, 0.7, -0.1], r))}
a, b = H['fh-laag-raak'], p; d = H['fh-door-laag']
d['handR'] = r3([(a['handR'][i]+b['handR'][i])/2 for i in range(3)])
rm = n([n(a['racket']['richting'])[i]+r[i] for i in range(3)])
d['racket'] = {'richting': r3(rm), 'vlak': r3(orth([a['racket']['vlak'][i]+b['racket']['vlak'][i] for i in range(3)], rm))}

# Backhand slice: uitzwaai naar voren op borsthoogte, kop blijft opzij, blad open
p = H['bh-slice-uitzwaai']; r = n([0.5, 0.12, -0.86]); p['handR'] = [1.0, 1.0, -0.25]
p['racket'] = {'richting': r3(r), 'vlak': r3([-x for x in orth([0.75, 0.65, 0.1], r)])}

json.dump(T, open('technieken.json', 'w'), ensure_ascii=False); json.dump(H, open('houdingen3d.json', 'w'), ensure_ascii=False)
print('ok')
