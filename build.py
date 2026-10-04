# Inline the mojulo slab GLB so the sizzle is one portable file: dist/lunar-sizzle.html
import base64, pathlib
root = pathlib.Path(__file__).parent
s = (root / 'index.html').read_text()
uri = lambda f: 'data:model/gltf-binary;base64,' + base64.b64encode((root / f).read_bytes()).decode()
s = s.replace("const GLB = { slab: 'hex.glb' };", f"const GLB = {{ slab: '{uri('hex.glb')}' }};")
(root / 'dist').mkdir(exist_ok=True)
(root / 'dist' / 'lunar-sizzle.html').write_text(s)
print('wrote', root / 'dist' / 'lunar-sizzle.html', round(len(s) / 1e6, 1), 'MB')
