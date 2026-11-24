"""Zet racketstanden vanuit een stevige pols: racket volgt de onderarm (polshoek th/ph vast),
de onderarm draait (pronatie/supinatie) tot het slagvlak zo dicht mogelijk bij de gewenste stand staat.
Gebruikt de rig van de app zelf (diag/index.html met window.__rig).

python3 polsfix.py diag houdingen3d.json opdrachten.json  -> schrijft houdingen3d.json bij
"""
import json, sys, threading, http.server, functools
from playwright.sync_api import sync_playwright
D, HP, OP = sys.argv[1], sys.argv[2], sys.argv[3]
H = json.load(open(HP)); OPD = json.load(open(OP)); import os; STIL = os.environ.get('STIL')
srv = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(http.server.SimpleHTTPRequestHandler, directory=D)); srv.RequestHandlerClass.log_message = lambda *a: None
threading.Thread(target=srv.serve_forever, daemon=True).start()
JS = r"""([H, OPD]) => {
const R = window.__rig, K = e => { const l = Math.hypot(...e) || 1; return e.map(x => x / l) },
 S = (a, b) => a.map((x, i) => x - b[i]), A = (a, b) => a.map((x, i) => x + b[i]), M = (a, s) => a.map(x => x * s),
 D = (a, b) => a.reduce((s, x, i) => s + x * b[i], 0), X = (a, b) => [a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0]],
 hoek = (a, b) => Math.acos(Math.max(-1, Math.min(1, D(K(a), K(b))))) * 180 / Math.PI, rad = x => x * Math.PI / 180;
const uit = {};
const los = (o, zet) => {
  const p = JSON.parse(JSON.stringify(H[o.van || o.naam]));
  Object.assign(p, o.zet || {}, zet || {}); const bal = p._bal || o.bal; delete p._bal;
  const thL = o.ths || [o.th], phL = o.phs || [o.ph];
  const frames = []; for (const T0 of thL) for (const P0 of phL) { const th = rad(T0), ph = rad(P0), af = [Math.cos(ph)*Math.cos(th), Math.cos(ph)*Math.sin(th), Math.sin(ph)];
    const bf = Math.abs(af[2]) < 0.9 ? K(X(af, [0,0,1])) : K(X(af, [1,0,0])); frames.push({ af, bf, cf: X(af, bf), straf: 0.15 * (Math.abs(T0 - (o.thDoel ?? 45)) + Math.abs(P0 - (o.phDoel ?? 18))) }); }
  let log = [];
  for (let it = 0; it < (o.iter || 8); it++) {
    const j = R.vt(p), a = K(S(j.handR, j.elleboogR));
    let q1 = Math.abs(a[1]) < 0.9 ? K(X(a, [0,1,0])) : K(X(a, [1,0,0])); const q2 = X(a, q1);
    let best = null;
    for (const F of frames) for (let r = 0; r < 360; r += 3) {
      const b = A(M(q1, Math.cos(rad(r))), M(q2, Math.sin(rad(r)))), c = X(a, b);
      const col = i => A(A(M(a, F.af[i]), M(b, F.bf[i])), M(c, F.cf[i]));
      const t = col(0), n = col(2), hit = o.backhand ? M(n, -1) : n;
      const pro = R.Ue(j.schouderR, j.elleboogR, j.handR, n, 1), proStraf = isNaN(pro) ? 0 : 5 * (Math.max(0, (o.proMin ?? -80) - pro) + Math.max(0, pro - (o.proMax ?? 90)));
      const sc = proStraf + (o.wN ?? 1) * hoek(hit, o.N) + (o.T ? (o.wT ?? 0.5) * hoek(t, o.T) : 0) + F.straf;
      if (!best || sc < best.sc) best = { sc, t, n, hit };
    }
    p.racket = { richting: best.t.map(x => +x.toFixed(3)), vlak: best.n.map(x => +x.toFixed(3)) };
    if (bal) { p.handR = S(S(bal, M(best.t, 0.3)), M(best.hit, 0.07)).map(x => +x.toFixed(3)); p.bal = bal; }
    log.push(+best.sc.toFixed(1));
  }
  const j = R.vt(p), a = K(S(j.handR, j.elleboogR)), w = K(p.racket.richting), pl = K(S(p.racket.vlak, M(w, D(p.racket.vlak, w))));
  const ie = R.Ie(a, w, pl), romp = { bekken: j.bekken, borst: j.borst, op: j.rugRichting, voor: j.rompVoor, rechts: j.rompRechts };
  const hit = o.backhand ? M(pl, -1) : pl;
  return { pose: p, score: log[log.length-1], meting: { th: Math.round(ie.th), ph: Math.round(ie.ph), klem: Math.round(hoek(j.racketAs, w)), door: +R.Ye(j.schouderR, j.elleboogR, j.handR, romp).toFixed(3),
    vlakAfwijking: Math.round(hoek(hit, o.N)), asAfwijking: o.T ? Math.round(hoek(w, o.T)) : null, pro: Math.round(R.Ue(j.schouderR, j.elleboogR, j.handR, pl, 1)), elb: Math.round(180 - hoek(S(j.elleboogR, j.schouderR), a)), elZij: +D(S(j.elleboogR, j.schouderR), j.rompRechts).toFixed(2), elOp: +(j.elleboogR[1] - j.schouderR[1]).toFixed(2), hoofd: j.hoofd.map(x => +x.toFixed(2)), schouderR: j.schouderR.map(x => +x.toFixed(2)), log } };
};
for (const o of OPD) { let best = null;
  for (const v of (o.varianten || [null])) { const r = los(o, v); const mm = r.meting, elbS = o.elb ? 4 * (Math.max(0, o.elb[0] - mm.elb) + Math.max(0, mm.elb - o.elb[1])) : 0, proS = isNaN(mm.pro) ? 0 : 10 * (Math.max(0, (o.proMin ?? -80) - mm.pro) + Math.max(0, mm.pro - (o.proMax ?? 90))), ell = elbS + proS + o.elleboog ? 100*Math.max(0, o.elleboog.zij - mm.elZij) + 100*Math.max(0, o.elleboog.op - mm.elOp) : 0, pols = ell + 3*Math.max(0, Math.abs(mm.ph) - (o.phMax ?? 35)) + 3*Math.max(0, 30 - mm.th) + 3*Math.max(0, mm.th - 70) + 5*mm.klem; const tot = r.score + 60 * mm.door + pols + (isNaN(mm.th) ? 1000 : 0); if (!best || tot < best.tot) best = { ...r, tot, v }; }
  best.meting.variant = best.v; uit[o.naam] = best; }
return uit }"""
with sync_playwright() as p:
    b = p.chromium.launch(args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'])
    pg = b.new_page(); pg.goto(f"http://127.0.0.1:{srv.server_port}/index.html"); pg.wait_for_function('window.__rig')
    res = pg.evaluate(JS, [H, OPD]); b.close()
for naam, r in res.items():
    H[naam] = r['pose']; m = r['meting']
    if STIL: continue
    print(f"{naam:20s} pro {m['pro']} elb {m['elb']} | elleboog zij {m['elZij']} op {m['elOp']} | th {m['th']!s:>4} ph {m['ph']!s:>4} klem {m['klem']!s:>3} door {m['door']!s:>5} vlak±{m['vlakAfwijking']!s:>3}° as±{m['asAfwijking']}° hoofd {m['hoofd']} schouder {m['schouderR']} hand {[round(x,2) for x in r['pose']['handR']]} {('variant '+json.dumps(m.get('variant'))) if m.get('variant') else ''}")
json.dump(H, open(HP, 'w'), ensure_ascii=False)
