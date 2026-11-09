"""Create an offline review page and a comparison proof from exported textures."""
import base64
import io
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from hd_hud_assets import ART, PACK

manifest = json.loads((ART / "source-manifest.json").read_text())
source = Path(manifest["source"])
entries = []
for asset in manifest["assets"]:
    original = Image.open(source / asset["path"]).convert("RGBA")
    original.putdata([(0, 0, 0, 0) if (r, g, b) == (255, 0, 255) else (r, g, b, a)
                      for r, g, b, a in original.get_flattened_data()])
    buffer = io.BytesIO()
    original.save(buffer, format="PNG", optimize=True)
    entries.append({"path": asset["path"], "size": asset["size"],
                    "group": asset.get("atlas", "emblems" if "/map/" in asset["path"] else "panels"),
                    "before": "data:image/png;base64," + base64.b64encode(buffer.getvalue()).decode()})

template = r'''<!doctype html><html lang="en"><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Machines — Faithful HD HUD review</title>
<style>
body{margin:0;background:#15191c;color:#e6edf2;font:16px system-ui}header{position:sticky;top:0;background:#20272df5;padding:20px 28px;border-bottom:1px solid #43505b;z-index:1}
h1{margin:0 0 8px;font-size:23px}p{margin:6px 0;color:#b3c0ca}label{margin-right:18px}select{font:inherit;color:#fff;background:#34434e;border:1px solid #60798b;border-radius:5px;padding:7px;margin:8px}
main{padding:24px;max-width:1500px;margin:auto}article{margin-bottom:22px;border:1px solid #43505b;border-radius:8px;overflow:auto;background:#242c32}h2{font-size:15px;font-weight:500;padding:13px 18px;margin:0;color:#c4d5e2}
.pair{display:grid;grid-template-columns:1fr 1fr;min-width:max-content}.item{padding:14px 20px 22px;min-width:290px;display:flex;flex-direction:column;gap:12px}.item span{color:#cbd6df;font-size:13px}.stage{background:#858b8c;display:flex;justify-content:center;align-items:center;padding:12px;min-height:56px}.before{image-rendering:pixelated}img{display:block}
</style><header><h1>Machines · Faithful HD HUD</h1><p>129 assets · 516 PNG variants · Original layout and dimensions</p>
<label>Category<select id="group"></select></label><label>UI scale<select id="scale"><option value="1">100%</option><option value="2">200%</option><option value="3">300%</option><option value="4" selected>400%</option></select></label>
<p>Original pixels and exported HD textures at their actual display sizes. In-game review remains separate.</p></header><main id="assets"></main>
<script>const assets=__ASSETS__;const group=document.querySelector('#group'),scale=document.querySelector('#scale'),main=document.querySelector('main');
for(const name of [...new Set(assets.map(a=>a.group))]){const o=new Option(name,name);group.add(o)}group.value='controls';
function render(){main.replaceChildren();const n=+scale.value;for(const a of assets.filter(x=>x.group===group.value)){const article=document.createElement('article'),heading=document.createElement('h2'),pair=document.createElement('div');heading.textContent=a.path;pair.className='pair';article.append(heading,pair);
for(const hd of [false,true]){const cell=document.createElement('div'),label=document.createElement('span'),stage=document.createElement('div'),image=document.createElement('img');cell.className='item';stage.className='stage';label.textContent=hd?'Faithful HD render':'Original pixels enlarged';image.width=a.size[0]*n;image.height=a.size[1]*n;image.alt=a.path;image.src=hd?'../../mods/faithful-hd-hud/'+a.path.replace(/\.bmp$/,n===1?'.png':'_'+n+'x.png'):a.before;if(!hd)image.className='before';stage.append(image);cell.append(label,stage);pair.append(cell)}main.append(article)}}
group.onchange=scale.onchange=render;render();</script></html>'''
(ART / "preview.html").write_text(template.replace("__ASSETS__", json.dumps(entries)), encoding="utf-8")

selected = ["gui/misc/return1.bmp", "gui/misc/zenith.bmp", "gui/navigate/red/machines.bmp",
            "gui/navigate/red/construc.bmp", "gui/misc/scrollr.bmp", "gui/commands/move.bmp",
            "gui/commands/stand.bmp", "gui/misc/red/decal4.bmp"]
assets = {a["path"]: a for a in manifest["assets"]}
height = sum(assets[p]["size"][1] * 4 + 46 for p in selected) + 52
proof = Image.new("RGBA", (1200, height), (133, 139, 140, 255))
draw = ImageDraw.Draw(proof)
font = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 18)
draw.text((20, 12), "Original pixels at 400%", font=font, fill="black")
draw.text((620, 12), "New exported textures at 400%", font=font, fill="black")
y = 52
for relative in selected:
    size = tuple(n * 4 for n in assets[relative]["size"])
    original = Image.open(io.BytesIO(base64.b64decode(next(a for a in entries if a['path'] == relative)['before'].split(',')[1]))).resize(size, Image.Resampling.NEAREST)
    path = Path(relative)
    new = Image.open(PACK / path.parent / f"{path.stem}_4x.png").convert("RGBA")
    draw.text((20, y), relative, font=font, fill="black")
    draw.text((620, y), relative, font=font, fill="black")
    proof.alpha_composite(original, (20, y + 30))
    proof.alpha_composite(new, (620, y + 30))
    y += size[1] + 46
proof.convert("RGB").save(ART / "review-400.png", optimize=True, compress_level=9)
print("Created art/hd-hud/preview.html and art/hd-hud/review-400.png")
