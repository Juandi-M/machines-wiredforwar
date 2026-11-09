# Faithful high-resolution HUD masters

This is the editable/provenance side of the personal HD HUD experiment. The
engine receives only `mods/faithful-hd-hud/gui/**/*.png`, not these large masters.

The first-person HUD extension is exported and checked: 211 source assets and
844 PNG variants in total, including 82 additions from the five supplied photos.
See [extension status](EXTENSION_STATUS.md) for scope and validation limits.

- `masters/`: 25 saved HUD masters and their exact render prompts.
- `references/`: source images and prepared sprite sheets used for generation.
- `source-manifest.json`: original paths, dimensions, SHA-256, and atlas crop rectangles.
- `requirements.txt`: pinned export-tool dependencies.
- `preview.html`: offline review page with 100–400% selection and original/HD comparisons.
- `review-400.png`: a representative exported-texture comparison on a gray backing.
- `review-first-person-400.png`: the new panel and first-person comparisons.

The built-in image-generation tool rendered the artwork from the original
references. No CLI model/API fallback was used. The original generated files are
also retained in the session's generated-images directory; selected copies are
saved here. The `*.prompt.txt` files are the final prompt set, not instructions
for game execution. Image generation is not deterministic; packaging is
reproducible from the saved masters and pinned tools.

## Export again

From the root of `machines-juan-experiments`, with the native Python environment:

```powershell
& ./build/asset-tools/Scripts/python.exe scripts/hd_hud_assets.py pack --iterations 15
& ./build/asset-tools/Scripts/python.exe scripts/preview_hd_hud.py
```

To create that environment in a fresh checkout:

```powershell
py -3 -m venv build/asset-tools
& ./build/asset-tools/Scripts/python.exe -m pip install -r art/hd-hud/requirements.txt
```

`prepare --source <game-runtime>` rebuilds references and the source manifest from
the original installed assets; it does not regenerate the master artwork.
Run `scripts/extend_hd_hud.py` after `prepare` to add the shared first-person
references before exporting. The final line-art masters use a magenta-keyed
format; the exporter decodes that to clean RGBA before lossless PNG compression.

## Native image-loader check

The checker in `tools/hd-hud-check` uses the same SDL3 and SDL3_image packages as
the existing native game build. It has its own fresh CMake build directory under
this clone. For this machine the cached package configuration is available at:

```powershell
& 'C:/Program Files (x86)/Microsoft Visual Studio/2022/BuildTools/Common7/Tools/Launch-VsDevShell.ps1' `
    -Arch amd64 -HostArch amd64 -SkipAutomaticLocation
cmake -S tools/hd-hud-check -B build/hd-hud-check -G Ninja `
    '-DCMAKE_BUILD_TYPE=Release' `
    '-DCMAKE_PREFIX_PATH=C:/Users/juanm/OneDrive/Documents/github/machines-wiredforwar/build/native-display/conan/build/Release/generators'
cmake --build build/hd-hud-check -j 4
& ./build/hd-hud-check/hud-asset-check.exe (Resolve-Path mods/faithful-hd-hud).Path
```

This reuses installed immutable dependency packages, not the other clone's CMake
cache. On another machine, point CMake at locally installed SDL3/SDL3_image package
configuration files instead. It checks image dimensions, PNG decoding, and the
same RGBA/color-key surface conversion as the engine; it does not prove rendered
GPU output or click-target behavior.
