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
