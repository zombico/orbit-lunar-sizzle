# Handoff: Orbit lunar sizzle

A 9-second, text-free concept loop for [Orbit Studio 3D](https://orbitstudio3d.com/): a 3D moon turns, a hex reticle
captures a site on its surface, and the hexagon becomes a white, cratered "moon rock slab" seen at three-quarter view.

- **Live:** the GitHub Pages site serves `index.html` from this repo's root.
- **Scrub to any moment:** add `?t=<seconds>` (e.g. `?t=5.5`) to freeze the timeline — the fastest way to check a change.

## What's in here

| File | What it is |
|---|---|
| `index.html` | The whole animation: three.js (0.169, from jsDelivr) + an SVG reticle overlay. No build step. |
| `hex.glb` | The slab model, exported from mojulo (lit PBR, quantized). Loaded by `index.html`. |
| `mojulo/hex-slab.recipe.json` | The slab's **source**: the mojulo recipe `hex.glb` was generated from. |
| `build.py` | Inlines `hex.glb` into one portable file, `dist/lunar-sizzle.html` (for email/decks; not needed for Pages). |

Run locally (a server is needed because the page fetches `hex.glb`):

```bash
python3 -m http.server 4518
```

then open http://localhost:4518/?t=5.5

---

## Path A — any AI agent (no mojulo)

Everything except the slab's geometry is plain code in `index.html`. Edit it directly.

**Timing** (top of the module script):
- `T = 9` — loop length in seconds.
- `SWAP = 3.4` — the moment the captured hexagon becomes the slab. Moon/reticle/push-in happen before it,
  the slab orbit after. The comment block above `T` lists every beat; keep it in sync when you retime.

**The moon** (procedural, painted at load — not real lunar data):
- `moonMaps()` paints the colour (`#aba79f` base, dark maria blobs) and a bump map (the `2400` crater loop).
- `MOON_R` radius; `LAT` / `U0` pick the captured site on the texture.
- It is a smooth sphere with a bump map: relief is lighting only, the silhouette stays round.

**The slab** (look, not shape):
- `TONE` — per-part brightness, keyed by mesh name (`vesiclespbr`, `craterpbr`, `rimpbr`).
  GLTFLoader strips the `:` from mojulo's `part:pbr` node names, so `crater:pbr` arrives as `craterpbr`.
- `poseSlab(t)` — its rotation (three-quarter view) and slow push-in.
- `RAKE` — the low sun direction in slab space; lower = longer crater shadows.
- Material roughness/colour are set where the GLB is traversed after `loadAsync`.

**The reticle** — the SVG `#retHex` polygon; it tracks the moon target, then morphs onto the slab's top face
(`measureSwap()` / `slabTopOnScreen()`), then fades by `SWAP + 0.8`.

**Swapping the model:** any GLB works — set `const GLB = { slab: '<file>.glb' }`. Update `HEX_R` / `TILE_H`
(the slab's half-width and height in the model's units) and `SCALE` if the new model's size differs.
A non-mojulo GLB is z-up/y-up dependent; mojulo GLBs already import upright.

**Ground rules that keep it on-brief:** no text on screen; white, smooth specimen (not pixelated or rough);
the hexagon is already determined — don't add a "carving" or "hexagonizing" step.

**Verify:** load `?t=1.8`, `?t=3.1`, `?t=3.6`, `?t=5.5`, `?t=7.5`, `?t=8.1` and check the console is clean.

**Ship:** commit and push to `main`; Pages redeploys. Run `python3 build.py` only if you also need the single file.

---

## Path B — agents with mojulo

Use mojulo when you want to change the slab's **geometry** (craters, rims, pores, terrain, proportions).
The GLB is derived; the recipe is the source. Never hand-edit `hex.glb`.

1. **Load the recipe.** If your mojulo host still has sketch `sk_4tr1ovzadu`, use it. Otherwise store
   `mojulo/hex-slab.recipe.json` as a new sketch (its `kind` is `workbench`, so mint it with
   `mint_solid({ kind: 'workbench', ... })`) and note the new ref. Start every session with `forward_context`.
2. **Edit in place** with `update_sketch` (JSON-Pointer patches), not a re-mint. The recipe is one `fields`
   entry: `cells` (≤ 128; resolution) and a `terms` list of signed-distance terms:
   - `hex` — the body: an `expr` hexagonal prism (`r` = half-width 2.6, `hz` = half-height) with low terrain
     noise (`g` amplitude, `gs` scale). Keep `r` fixed if the animation should line up without touching `index.html`.
   - `crater` (subtract, sphere) + `rim` (add, torus `expr`) pairs — five large craters, then smaller secondaries.
     Raise a rim's `zt` if it gets buried by the terrain noise.
   - `peak` — a central-peak sphere in the main crater.
   - `vesicles` — the porous texture: `noise3` thresholded; `thr` controls how many pores, `sc` their size
     (in `noise3` the scale argument acts like feature size).
   - Every term's `id` becomes a GLB node/material group (`id:pbr`), which is what `TONE` keys on.
3. **Export** with `export_model({ ref, format: 'glb', lit: true, quantize: true })`.
   `lit: true` matters: the default bakes lighting into vertex colours and the page's own lights then double up
   (black side walls). Copy the resulting `model.glb` over `hex.glb`.
4. **Refresh the source copy:** copy the outcome's `recipe.json` over `mojulo/hex-slab.recipe.json`
   so the repo's recipe always matches its GLB.
5. Verify with the `?t=` frames above and push.

**Exploring further with mojulo** (not wired into this page yet):
- A real 3D cratered moon to replace the painted sphere, and capturing the slab from that same surface —
  so the specimen is literally cut from the moon shown.
- Walkable / drivable / flyable lunar terrain at multiple scales, from mojulo's planet terrain worlds.
These are being explored on mojulo's `1004-lunar-explorer` branch.
