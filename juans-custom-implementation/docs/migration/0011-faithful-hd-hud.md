# Faithful HD HUD artwork experiment

Date: 2026-11-08. Personal clone: `machines-juan-experiments`.
Branch: `experiment/hd-hud`. Source baseline: upstream `dev` at
`104862d63b7a09b95d318a2014f05120060ed80d`.

## Request and separation

The user supplied three photographs of the 400% HUD and requested genuinely
re-rendered high-quality artwork, with compression and engine-compatible
conversion. They explicitly chose faithful high-resolution versions of the
original designs. Simply enlarging old pixels did not meet this request.

Created the personal artwork branch and an optional `mods/faithful-hd-hud` pack.
No generated art or new source changes were added to the community contribution
checkout. The community branch and its existing preview remain separate.
The red circular markings and bars in the photos are original panel decals;
they were traced to the source images and redrawn along with the controls.

## Artwork and production files

The built-in image-generation tool produced 15 saved masters: four individual
faction emblems, nine sprite atlases, and two panel surfaces. References preserve
the original designs, positions, silhouettes, colors, glyphs and control states
as far as the small source artwork permits. These are artistic redraws rather
than pixel-identical retail assets. User review of the result remains appropriate.

| Covered assets | Count |
| --- | --- |
| Four faction emblems | 4 |
| Faction navigation tabs, X/return and camera/tool buttons | 16 |
| Requested command buttons, eight self-destruct frames, seven initiative states | 25 |
| Left/right/up/down scroll controls and hover variants | 20 |
| Four panel decals per faction | 16 |
| Counter digits/slash in the original size groups | 41 |
| Shared trim, ornaments, slider and slider slot | 5 |
| Gray backing tile and sidebar panel | 2 |
| Total | 129 |

Unit portraits and the rest of the game's artwork were not replaced. The pack
does not change gameplay, command functions, hit boxes, engine code, or intro
timing. Initiative LED states and self-destruct frame order were inspected
against the reference sheet. Runtime animation/input behavior still needs an
in-game test with the new art installed.

Selected masters, exact prompts, prepared references, source dimensions/hashes,
and crop geometry are saved under `art/hd-hud`. Original generated outputs were
also retained in the session's generated-images folder. No model/API CLI fallback
was used. Generation is nondeterministic; export is reproducible from the saved
masters and pinned Pillow 13.0.0/Zopfli 0.4.3 tools.

## Engine-safe conversion and compression

`scripts/hd_hud_assets.py` assembles references, extracts atlas rectangles,
resamples to exact original dimensions times 1/2/3/4, and writes standard PNG
companions using the existing lookup names (`name.png`, `name_2x.png`, etc.).
The script does not draw replacements in place of generated art.

The original BMP magenta color key is normalized to PNG alpha for references.
Zero-alpha RGB is normalized before export; it is invisible and otherwise
wastes compression space. Alpha is retained, opaque images can omit the alpha
plane, and no lossy palette reduction or JPEG conversion is used. Each PNG is
encoded at level 9, optimized with Zopfli (15 iterations), and decoded again to
verify identical pixels after compression. Only the smaller valid encoding is
retained.

| Measurement | Result |
| --- | --- |
| Master PNGs outside the runtime | 21,525,808 bytes |
| Runtime PNG variants | 516 |
| Runtime PNG bytes before Zopfli | 6,924,919 |
| Final runtime PNG bytes | 6,528,607 (about 6.23 MiB) |
| 400% PNG bytes alone | 3,304,717 |
| Decoded RGBA pixels, all scales combined | 19,676,040 bytes |
| Decoded RGBA pixels at 400% | 10,493,888 bytes (about 10.01 MiB) |
| Largest texture edge | 676 pixels |

The decoded figures describe one RGBA copy of the textures, not total engine
RAM/VRAM use: derived surfaces and mipmaps can add allocations. The engine loads
the selected scale, not a 4K master for each icon. The exporter limits each edge
to 2048 and aggregate decoded pixel data to 64 MiB; current outputs fit well
within those project budgets. These budgets are not claims about a queried GPU
limit. `manifest.json` records individual dimensions, hashes and byte counts.

## Native compatibility check and review

Built `tools/hd-hud-check` natively with MSVC using the same installed SDL3 and
SDL3_image packages as the community native build, with a fresh CMake build
directory in this clone. No game build cache was copied.

All 516 exported PNGs passed native `IMG_Load`, exact dimension checks, RGBA8888
conversion, magenta color-key setup, and RGBA32 surface blitting. That reproduces
the CPU image-conversion portion of `RenISurfBody::copyWithColourKeyEmulation`.
It did not create a video window, upload GPU textures, or launch the game.
Logs are in `build/asset-tools/{check-*,native-image-check.log,pack.log}`.

An opaque comparison proof was composed from the actual exported textures at
400%, including the X, tool symbol, navigation tabs, arrows, command labels, and
red panel decal. Their contours and lettering are visibly cleaner than enlarged
source pixels. The offline `art/hd-hud/preview.html` permits inspecting all 129
assets at 100/200/300/400%. Pixel-level and native-decoder checks do not establish
every in-game blend, texture upload, animation transition, or click target.

## Isolated runtime

Prepared `build/hd-hud/play/machines` with its own configuration and writable game
state. Base assets were copied from the known working ground-zero package;
the optional HD mod is installed under that runtime's `mods` directory.

The executable was deliberately reused from the community native preview:
`d321a22c29effadec45ca5075ed416134c42b410925176ab95da78985d81055a`.
It includes the still-uncommitted community display/intro changes and supports
400% UI scaling. This is not a newly compiled personal engine and is not claimed
to match the personal clone's otherwise unmodified engine source. The original
community checkout retains the source for that executable. Asset experiments
remain separate, and there is no shared writable runtime state between copies.

`Play HD HUD Preview.cmd` uses the correct working directory, clears `MACH_ROOT`
in its child environment, and keeps the normal intro enabled. This new runtime
was not launched during artwork production. The next shared test should inspect
the HUD in a match at 4K/400%, then smaller UI scales/resolutions, including all
faction tabs, X/camera controls, hover highlights, scrolling, counters, initiative
states and the self-destruct animation. Preserve the original runtime for
comparison. Nothing was committed, pushed, or proposed upstream.

## First shared in-game test

The user requested launch for a shared test. Launched the isolated personal HD
runtime normally, with the installed 516-texture mod and intro enabled (PID 28428).
Startup logs confirmed registration of `mods/faithful-hd-hud`, a 400% UI scale,
and completed client startup. The process was responsive at the observed check.

The user answered the Skirmish HUD question: **"New artwork appears and the
controls work."** This confirms the first manual in-game appearance/input check
for the new pack. The assistant's native captures continued to show the loading
image, so the in-game HUD result is attributed to the user, not those captures.

This does not establish a full review of every faction, hover/animation state,
resolution, gameplay feature, or multiplayer mode. The user also mentioned a
separate menu bug whose report had not arrived; that issue remains pending and
is not classified as fixed by the successful HD HUD check. No new source or art
changes, commits, pushes, or upstream messages were made during this test.
