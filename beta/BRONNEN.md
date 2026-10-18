# Bronnen

## 3D-mensmodel

- **Model:** samengesteld uit de vrije bestanden van MakeHuman (basismodel hm08, vormdoelen voor man/leeftijd/spiermassa/gewicht/lengte/proporties, game-engine-skelet en -gewichten)
- **Bron:** MakeHuman / MPFB2 — https://github.com/makehumancommunity/mpfb2 (versie in `bronnen/makehuman/VERSIE.txt`)
- **Licentie:** CC0 1.0 Universal (publiek domein): vrij te gebruiken, aan te passen en te verspreiden, ook commercieel, zonder naamsvermelding. Volledige tekst: `bronnen/makehuman/LICENSE.ASSETS.md`. Alleen de bestanden (assets) zijn gebruikt, geen programmacode van MakeHuman.
- **Gebruikte bestanden** (in `bronnen/makehuman/data/`): `base.obj`, `rig.game_engine.json`, `weights.game_engine.json`, `macro.json` en de benodigde vormdoelen (`targets/`)
- **Aanpassingen:** samengesteld als gewone man (jong volwassen, gemiddeld gewicht, iets minder spiermassa dan gemiddeld), geschaald naar 1,80 m en omgezet naar een eigen compact formaat (`scripts-makehuman.py` → `src/lib/mensmodel.ts`). Huid effen gekleurd, ogen gekleurd per punt. Kleding (als eigen stoflaag over het lichaam), haar, logo en beeldmerk worden in de app zelf gemaakt; de bewegingen komen uit de eigen houdingen van de app.

Er zijn geen video's, foto's of bewegingsopnames van derden in de app verwerkt.
