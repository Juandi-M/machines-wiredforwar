# Faithful HD HUD

Personal artwork experiment for Machines: 211 shared HUD assets rendered anew
from original references, packaged as 844 PNGs at 100%, 200%, 300%, and 400%.

Includes the four faction emblems, faction navigation tabs, return/X and camera
buttons, scrolling arrows, the requested command buttons and their self-destruct
and initiative states, counters, gray panel surfaces, and faction decorations.
Also includes the panel-edge indicators and first-person entry controls, radar
housing/contacts/heading arrows, command-display housing and blank grid, command
button states, compass tape, targeting animation frames and health/armour bars.
Unit portrait thumbnails, weapon illustrations, radar opening animation frames,
and the rest of the game's artwork are outside this pack.

## Install and use

Place this entire `faithful-hd-hud` folder inside the game's `mods` folder. The
existing filesystem override mechanism discovers it at startup. Keep the base
game files: PNG companions override the corresponding UI images; this pack is
not a standalone game. Remove this one mod folder to return to the base artwork.

The prepared personal test runtime already has the pack installed at
`build/hd-hud/play/machines` in `machines-juan-experiments`. Its launcher clears
`MACH_ROOT` and uses normal startup, including the intro. It is a separate runtime
from the community contribution preview.

The prepared executable supports UI scales through 400%. Select the appropriate
UI scale for the resolution; 400% preserves the full 640x480 menu within 4K.
An unmodified upstream build may expose fewer scale choices.

## Packaging and validation

Every PNG retains the original logical bitmap dimensions multiplied by its scale.
The 1x name is `name.png`; other variants are `name_2x.png`, `name_3x.png`, and
`name_4x.png`. High-resolution masters are not installed into the game.

PNG compression is lossless (Pillow level 9 plus Zopfli optimization). Pixel data
was compared after compression. Transparent pixels retain their alpha; hidden
RGB data under zero alpha is normalized before encoding. No JPEG or lossy
palette conversion is used.

All 844 files passed a native SDL3_image decoding and engine-style surface
conversion check, with dimensions verified against `native-check.tsv`. This did
not create a graphics window or test GPU uploads or gameplay. In-game visual and
input review remains necessary. `manifest.json` records file hashes, exact sizes,
compressed bytes, master provenance, and decoded RGBA memory by scale.

This is an optional personal redraw, with artistic interpretation of tiny source
images. It is separate from community scaling fixes and is not a pixel-identical
retail reference. Original designs and source-asset provenance remain attributed
to Machines and the supplied WiredForWar asset set. Existing game notices and
licensing files have not been modified.
