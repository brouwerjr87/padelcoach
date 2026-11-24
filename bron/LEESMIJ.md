# Inhoud van de app

De programmacode van de app staat (in samengeperste vorm) in `index.html` en `beta/index.html`.
De inhoud staat hier los, zodat hij te bewerken is:

- `technieken.json`: alle technieken, levels, fases, teksten en fouten
- `houdingen3d.json`: alle 3D-houdingen voor de animaties

Inhoud terugzetten in de app:

    node bron/bouw.js index.html index.html bron/technieken.json bron/houdingen3d.json
    node bron/bouw.js beta/index.html beta/index.html bron/technieken.json bron/houdingen3d.json

Pas daarna het versienummer in `sw.js` en `beta/sw.js` aan, zodat telefoons de nieuwe versie ophalen.

`frames.py` maakt controlebeelden uit de app, `vel2.py` maakt een beoordelingsvel (pdf) per techniek.


## Codewijziging buiten de inhoud (bèta en live, nov 2026)
In `beta/index.html` is de camera van de baanoverzichten (functie `ln`, positie/tactiek) aangepast: camera iets verder weg en gericht op de eigen helft (`doel` 8–8,5 i.p.v. 10), zodat alle vier spelers in elk aanzicht in beeld zijn. Staat sinds 13 nov 2026 ook live. `bouw.js` raakt deze code niet.

## Codepatches (codepatch.py)
De broncode van de app is verloren; codewijzigingen gaan als tekstvervanging op de gebouwde `index.html`.
Alle codewijzigingen staan in `bron/codepatch.py` (idempotent, faalt als een stuk code niet precies één keer gevonden wordt).

Volgorde bij bouwen:
1. `node bouw.js <in.html> <uit.html> technieken.json houdingen3d.json` (inhoud)
2. `python3 codepatch.py <uit.html>` (code)
3. versie in `sw.js` bijwerken (sha256 van index.html, eerste 12 tekens)

Patches: baancamera (live), terugknop, één welkomscherm met handjes en link Over de app, animatie start vanzelf,
tip beginscherm na een nieuw beheerst level, 'Markeer als beheerst' op de volgende-stapkaart, 'met beeld' bij fouten
en eerlijke hint, teksten Over de app. Stand 18 nov 2026: alle patches staan live en in bèta.
Nieuw 16 nov: eindstand (level.eind = lijst {houding, ms}, geen extra fase) en startX (baanPad.startX: vaste beginpositie, ook voor linkshandigen).

## Slice-slagen (slicepatch.py, 24 nov 2026)
Bandeja, víbora, bajada (fh/bh), backhandvolley, dejada, cortado en backhandslice: het racket draait van boven naar beneden om de dwarsas (zwaaivlak door de doelrichting), niet om de verticale as. Controle met `swinganalyse.py` (draaias per slag). Alleen bèta tot akkoord.

## Stevige pols en geen arm door de romp (polsfix.py, 24 nov 2026)
`rigmeting.py` meet met de rig van de app zelf per houding de polshoek (th, ph), of de racketstand geklemd wordt en of de slagarm door de romp gaat. `polsfix.py` zet het racket vanuit een stevige pols in de onderarm en draait de onderarm tot het slagvlak zo dicht mogelijk bij de gewenste stand staat; varianten voor hand, romp en elleboog kiezen de stand zonder arm door de romp. Beide hebben een testkopie nodig waarin `function vt(e){` is voorafgegaan door `window.__rig={vt,Ye,Ie,yt}`. Opdrachten staan in `polsopdrachten.py`.

## Vaste pols en anatomische onderarmdraai (24 nov 2026)
- Alle houdingen met racket zijn opnieuw opgelost met een vaste pols (th 42–48, ph 15–21: licht gestrekt, ‘vastgezet’). De onderarmdraai (pronatie/supinatie, gemeten met de app-functie Ue) blijft binnen −80..90°.
- Codepatch `onderarm-frame`: de app mat de draai van de onderarm t.o.v. een vaste richting in de romp; die sloeg om als de onderarm naar achter-beneden wees, waardoor het racket bij smash en víbora 360° draaide. Nu t.o.v. de bovenarm (anatomisch).
- `afspeelscan.py` controleert per techniek de afgespeelde beweging (polsbereik, onderarmdraai, draaisnelheid, elleboog). `afspeelmeting.py` geeft het verloop per tijdstap. Beide hebben de diag-kopie met `window.__rig` en `window.__mot` nodig.
