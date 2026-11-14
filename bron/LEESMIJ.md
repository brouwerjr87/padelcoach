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
en eerlijke hint, teksten Over de app. Stand 15 nov 2026: alles behalve baancamera alleen in bèta.
