"""Prepare the photographed shared HUD additions without selecting unit portraits."""

import json
from pathlib import Path

from PIL import Image

from hd_hud_assets import ART, load_reference, sha


def prepare():
    manifest_path = ART / "source-manifest.json"
    manifest = json.loads(manifest_path.read_text())
    source = Path(manifest["source"])
    groups = {
        "fp-radar-arrows": ([f"gui/fstpersn/radar/arrow/point{i}.bmp" for i in range(1, 17)],
                            4, (256, 256), 5),
        "fp-radar-blips": ([p.relative_to(source).as_posix() for p in
                           sorted((source / "gui/fstpersn/radar/blips").glob("*.bmp"))],
                          5, (256, 256), 16),
        "fp-compass": (["gui/fstpersn/cursor/compass.bmp"], 1, (2048, 768), 8),
        "panel-extras": (["gui/misc/tplight1.bmp", "gui/misc/tplight2.bmp"]
                         + [f"gui/misc/{race}/inhead.bmp" for race in
                            ("red", "blue", "green", "yellow")], 3, (320, 384), 12),
        "fp-command-labels": ([f"gui/fstpersn/command/{command}_{state}.bmp"
                               for command in ("move", "follow", "attack")
                               for state in ("invalid", "valid", "activate")],
                              3, (512, 256), 6),
        "fp-reticles": ([f"gui/fstpersn/cursor/ping{i}.bmp" for i in range(1, 8)]
                        + [f"gui/fstpersn/cursor/targ{i}.bmp" for i in range(1, 9)]
                        + [f"gui/fstpersn/cursor/{name}{i}.bmp"
                           for name in ("targnv", "targv") for i in (1, 2)],
                       5, (272, 296), 3),
        "fp-status": ([f"gui/fstpersn/radar/{name}.bmp" for name in
                        ("rhealth", "rhealth2", "rhealth3", "rarmour", "rarmour2", "rarmour3")]
                      + ["gui/fstpersn/cursor/health.bmp", "gui/fstpersn/cursor/armour.bmp",
                         "gui/fstpersn/radar/dome.bmp"], 3, (256, 512), 6),
    }
    existing = {entry["path"] for entry in manifest["assets"]}
    additions = []
    for name, (files, columns, (cw, ch), scale) in groups.items():
        rows = (len(files) + columns - 1) // columns
        canvas = Image.new("RGBA", (columns * cw, rows * ch))
        for index, relative in enumerate(files):
            path = source / relative
            original_size = Image.open(path).size
            w, h = (dimension * scale for dimension in original_size)
            if w > cw - 16 or h > ch - 16:
                raise ValueError(f"Reference exceeds cell: {relative}")
            x = index % columns * cw + (cw - w) // 2
            y = index // columns * ch + (ch - h) // 2
            canvas.paste(load_reference(path).resize((w, h), Image.Resampling.NEAREST), (x, y))
            entry = {"path": relative, "size": original_size,
                     "atlas": name, "rect": [x, y, x + w, y + h],
                     "source_sha256": sha(path.read_bytes())}
            if name in ("fp-command-labels", "fp-reticles", "fp-compass",
                        "fp-radar-arrows", "fp-radar-blips"):
                entry["master_background"] = "magenta"
            if relative not in existing:
                manifest["assets"].append(entry)
                additions.append(relative)
            else:
                index = next(i for i, old in enumerate(manifest["assets"])
                             if old["path"] == relative)
                manifest["assets"][index] = entry
        canvas.save(ART / "references" / f"{name}.png", optimize=True)
        manifest["atlases"][name] = {"size": canvas.size, "columns": columns,
                                     "rows": rows, "cell": [cw, ch], "count": len(files)}
    singles = {
        "fp-radar": "gui/fstpersn/radar/rmmap.bmp",
        "fp-command-widget": "gui/fstpersn/command/widget.bmp",
        "fp-blank-grid": "gui/fstpersn/machines/backgrnd.bmp",
    }
    for name, relative in singles.items():
        path = source / relative
        load_reference(path).save(ART / "references" / f"{name}.png", optimize=True)
        if relative not in existing:
            manifest["assets"].append({"path": relative, "size": Image.open(path).size,
                                        "master": name, "source_sha256": sha(path.read_bytes())})
            additions.append(relative)
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"Prepared {len(additions)} new shared HUD assets; unit portraits excluded.")


if __name__ == "__main__":
    prepare()
