"""Beoordeling Merijn 16 nov 2026: inhoudspatch (technieken.json, houdingen3d.json)."""
import json, math, copy
T = json.load(open('technieken.json')); H = json.load(open('houdingen3d.json'))
arr = T if isinstance(T, list) else list(T.values())
tech = {t['id']: t for t in arr}

def n(v): l = math.sqrt(sum(x*x for x in v)); return [x/l for x in v]
def dot(a, b): return sum(x*y for x, y in zip(a, b))
def orth(v, r): d = dot(v, r); return n([v[i]-d*r[i] for i in range(3)])
def r3(v): return [round(x, 3) for x in v]
def kop(p): return [p['handR'][i]+0.3*n(p['racket']['richting'])[i] for i in range(3)]
def zet_racket(p, richting, netnormaal, backhand=False):
    """richting: kop-richting; netnormaal: slagvlak naar het net. vlak = palmkant (backhand: -slagvlak)."""
    nn = n(netnormaal); r = orth(richting, nn)
    p['racket'] = {'richting': r3(r), 'vlak': r3([-x for x in nn] if backhand else nn)}
def bal_op_blad(p, d=0.07):
    r = n(p['racket']['richting']); v = orth(p['racket']['vlak'], r)
    s = 1 if v[0] >= 0 else -1; v = [s*x for x in v]
    k = kop(p); rel = [p['bal'][i]-k[i] for i in range(3)]
    a = dot(rel, r); lat = [rel[i]-a*r[i]-dot(rel, v)*v[i] for i in range(3)]
    p['bal'] = r3([k[i]+a*r[i]+lat[i]+d*v[i] for i in range(3)])

# --- slagbewegingen (eerst, daarna bal op het blad leggen) ---
# Lob: hoog uitzwaaien zonder na te strekken
p = H['fh-lob-uit']; p['handR'] = [0.6, 1.55, 0.06]
p = H['bh-lob-uit']; p['handR'] = [0.7, 1.56, -0.1]
# Bajada forehand: slagvlak naar het doel en licht open, zwaai van hoog naar laag naar voren
p = H['bajada-raak']; zet_racket(p, [0.163, 0.92, 0.357], [0.9, 0.25, -0.28])
p['bal'] = r3([kop(p)[i] for i in range(3)])
p = H['bajada-uit']; p['handR'] = [0.92, 1.02, 0.02]; zet_racket(p, [0.78, 0.05, -0.62], [0.1, 0.75, -0.3])
# Bajada backhand: hoger raken, licht open, uitzwaai naar voren en omlaag
p = H['bh-bajada-laden']; p['handR'] = [-0.3, 1.62, -0.38]
p = H['bh-bajada-raak']; p['handR'] = [0.8, 1.48, -0.45]; zet_racket(p, [-0.1, 0.75, -0.65], [0.93, 0.3, -0.2], backhand=True)
p['bal'] = r3(kop(p))
p = H['bh-bajada-uit']; p['handR'] = [1.0, 0.98, -0.12]; zet_racket(p, [0.75, 0.45, -0.45], [0.2, 0.75, 0.3], backhand=True)
# Víbora: heup in bij het raken, blad rechter (niet plat) met zijwaartse slice
p = H['vibora-raak']; p['heupDraai'] = 20; p['rompDraai'] = 25
zet_racket(p, [0.2, 0.75, 0.6], [0.82, 0.1, -0.55]); p['bal'] = r3(kop(p))
# Backhand slice: vrije hand bij het raken naar buiten, niet voor de borst langs
H['bh-slice-raak']['handL'] = [-0.04, 1.02, -0.62]
# Backhand: tussenstand bij teruglopen, vrije hand komt langs de zij terug
q = copy.deepcopy(H['terugstap']); a, b = H['bh-uitzwaai'], H['terugstap']
q.update(rompDraai=-22, heupDraai=-14, handR=[0.72, 1.12, -0.12], handL=[0.12, 1.0, -0.36])
ra, rb = n(a['racket']['richting']), n(b['racket']['richting']); va, vb = n(a['racket']['vlak']), n(b['racket']['vlak'])
if dot(va, vb) < 0: vb = [-x for x in vb]
rm = n([ra[i]+rb[i] for i in range(3)]); q['racket'] = {'richting': r3(rm), 'vlak': r3(orth([va[i]+vb[i] for i in range(3)], rm))}
q['bal'] = None; H['bh-terug-tussen'] = q

# --- bal op de slagkant van het blad (niet half erdoor) ---
for k, p in H.items():
    if p.get('bal') and isinstance(p.get('handR'), list) and p.get('racket'):
        rel = [p['bal'][i]-kop(p)[i] for i in range(3)]
        if math.sqrt(dot(rel, rel)) < 0.3: bal_op_blad(p)

# --- racket niet voor het gezicht in klaarhoudingen ---
def kantel(p, graden, dy):
    t = math.radians(graden); c, s = math.cos(t), math.sin(t)
    rot = lambda v: [v[0]*c+v[1]*s, -v[0]*s+v[1]*c, v[2]]
    p['racket'] = {'richting': r3(n(rot(p['racket']['richting']))), 'vlak': r3(n(rot(p['racket']['vlak'])))}
    p['handR'] = r3([p['handR'][0], p['handR'][1]+dy, p['handR'][2]])
gekanteld = []
for k, p in H.items():
    if p.get('handL') != 'hals' or not isinstance(p.get('handR'), list): continue
    r = n(p['racket']['richting']); kp = kop(p)
    if r[1] > 0.8 and kp[0] - p['bekken'][0] > 0.25 and kp[1] > 1.15 and abs(kp[2]-p['bekken'][2]) < 0.35:
        kantel(p, 20 if r[0] < 0.3 else 15, -0.08 if p['handR'][1] > 1.1 else -0.05); gekanteld.append(k)
print('gekanteld:', gekanteld)
kantel(H['net-klaar'], 15, 0); H['net-klaar']['handR'] = [0.42, 1.04, 0.12]
H['fh-lob-uit']['handR'] = [0.72, 1.5, 0.1]

# --- techniekinhoud ---
def lvl(tid, nr): return tech[tid]['levels'][nr-1]
# Startpositie niet naast het glas
for tid, nr in [('forehand', 2), ('backhand', 2), ('voetenwerk', 1), ('voetenwerk', 2), ('wachtpositie', 2)]:
    lvl(tid, nr)['baanPad']['startX'] = 6.9
for tid in ['forehand', 'backhand']:
    f = lvl(tid, 2)['fases']; f[0]['baan']['verschuiving'] = [-1.2, 0.3]; f[1]['baan']['verschuiving'] = [-0.95, 0.2]; f[4]['baan']['verschuiving'] = [-1.2, 0.3]
lvl('backhand', 2)['fases'][4]['tussen'] = [{'houding': 'bh-door', 'ms': 110}, {'houding': 'bh-uitzwaai', 'ms': 300}, {'houding': 'bh-terug-tussen', 'ms': 540}]
f = lvl('backhand', 1)['fases'][5]; f['tussen'] = [{'houding': 'bh-terug-tussen', 'ms': 450}]
# Na de slag weer rechtop (eindstand, geen fase)
lvl('forehand', 3)['eind'] = [{'houding': 'klaar', 'ms': 900}]
lvl('backhand', 3)['eind'] = [{'houding': 'bh-terug-tussen', 'ms': 450}, {'houding': 'klaar', 'ms': 500}]
# Service: stuit achter de servicelijn
for nr in (1, 2):
    L = lvl('service', nr); L['spelerCy'] = 17.6; L['baanPad']['speler'] = [7.3, 17.6]
    L['balbaan'] = {'tussen': [[0.35, 0, 0.42]], 'toppen': [0.55, 1.0]}
    f = L['fases'][1]
    f['uitleg'] = 'Laat de bal naast je, iets voor je lichaam en achter de servicelijn, op de grond stuiten. Tegelijk gaat je racket compact naar achter.'
    f['letOp'] = ['Bal laten vallen, niet gooien', 'Stuit achter de servicelijn, naast je {linker}voet']
# Smash por tres: dichter bij het net, steiler, stuit voor de servicelijn
L = lvl('smash', 2); L['spelerCy'] = 12.8; L['baanPad']['speler'] = [7.5, 12.8]; L['baanPad']['doel'] = [4.2, 5.2]
L['fases'][3]['uitleg'] = 'Raak de bal op het hoogste punt, met veel kracht en een plat blad, en sla steil naar beneden. Zo springt de bal na de stuit hoog op.'
L['fases'][3]['letOp'] = ['Arm helemaal gestrekt', 'Raakpunt iets voor je hoofd', 'Hoe dichter bij het net, hoe steiler']
L['fases'][4]['uitleg'] = 'Zwaai krachtig door. De bal stuit tussen het net en de servicelijn en springt over de achterwand. Alleen doen als je echt goed onder de bal staat.'
# Bajada: van hoog naar laag; naar voren alleen na een goede bajada
for nr, uitzwaai in [(1, 'Zwaai door van hoog naar laag, naar voren richting je doel, en stap door met je {rechter}voet.'), (2, None)]:
    L = lvl('bajada', nr); f = L['fases'][-1]
    if uitzwaai: L['fases'][-2]['uitleg'] = uitzwaai
    f['uitleg'] = 'Was je bajada laag en diep? Loop dan samen met je partner een paar passen naar voren. Was hij te hoog of te kort, blijf dan staan en wacht de volgende bal af.'
    f['letOp'] = ['Samen met je partner', 'Alleen na een goede bajada']
    f['baan']['verschuiving'] = [0, -1.6]
lvl('bajada', 2)['fases'][-2]['uitleg'] = 'Zwaai door van hoog naar laag, naar voren richting je doel. Je {linker}arm gaat naar achter voor balans.'
# Víbora: heup indraaien
f = lvl('vibora', 1)['fases'][3]
f['uitleg'] = 'Raak de bal {rechts} naast je, op hoofdhoogte. Draai je heup in en snijd met een rechtopstaand blad zijwaarts langs de bal. Zo krijgt hij zijwaartse slice.'
f['letOp'] = ['Raakpunt opzij, niet boven je hoofd', 'Heup draait in', 'Blad rechtop, niet plat']
# Chiquita: nadruk op de slag, samen naar voren en afmaken
C = lvl('chiquita', 1)
C['fases'] = [
 {'id': 'ch-1', 'titel': 'Tegenstanders aan het net', 'uitleg': 'Jullie staan achterin, de tegenstanders aan het net. Jij hebt de bal.', 'letOp': ['Kies: lob of chiquita', 'Zelfde voorbereiding als je lob'], 'duurMs': 1100,
  'plaatsing': {'wij': [[7, 18.2], [3, 18.2]], 'zij': [[3, 7.2], [7, 7.2]], 'bal': [7, 17.9, 0.9]}},
 {'id': 'ch-2', 'titel': 'Zacht en laag naar de voeten', 'uitleg': 'Speel een zachte, lage bal schuin naar de voeten van de netspeler. Hij moet de bal van onderen raken.', 'letOp': ['Zacht, niet hard', 'Laag over het net, dalend bij zijn voeten'], 'duurMs': 1200,
  'plaatsing': {'wij': [[7, 17.8], [3, 17.8]], 'zij': [[3, 7.2], [7, 7.2]], 'bal': [3.3, 7.6, 0.2]}},
 {'id': 'ch-3', 'titel': 'Samen naar voren', 'uitleg': 'De netspeler moet de bal omhoog volleyen. Op dat moment lopen jij en je partner samen naar voren.', 'letOp': ['Samen en even snel', 'Split-step als de tegenstander raakt'], 'duurMs': 1100,
  'plaatsing': {'wij': [[7, 14.8], [3, 14.8]], 'zij': [[3, 7.4], [7, 7.2]], 'bal': [3.6, 9.2, 1.5]}},
 {'id': 'ch-4', 'titel': 'Aan het net', 'uitleg': 'Jullie staan aan het net. De bal komt hoog en langzaam terug: dat is jullie kans.', 'letOp': ['De rollen zijn omgedraaid', 'Wie de bal het best ziet, neemt hem'], 'duurMs': 1200,
  'plaatsing': {'wij': [[6.8, 12.8], [3.4, 12.8]], 'zij': [[3, 7.6], [7, 7.6]], 'bal': [3.7, 12.4, 1.9]}},
 {'id': 'ch-5', 'titel': 'Afmaken', 'uitleg': 'Volley de hoge bal stevig naar beneden, tussen de tegenstanders door of naar hun voeten.', 'letOp': ['Naar beneden, niet hard naar achter', 'Midden tussen de twee'], 'duurMs': 900,
  'plaatsing': {'wij': [[6.8, 12.6], [3.4, 12.6]], 'zij': [[3, 7.8], [7, 7.8]], 'bal': [5.1, 6.4, 0.1]}},
]

json.dump(T, open('technieken.json', 'w'), ensure_ascii=False); json.dump(H, open('houdingen3d.json', 'w'), ensure_ascii=False)
print('ok')
