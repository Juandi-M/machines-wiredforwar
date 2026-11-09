# First-person HUD extension — exported and checked

Completed 2026-11-09 in `machines-juan-experiments`, local `dev`.

The five supplied photographs were mapped to 82 additional shared source assets,
rendered into ten new masters and exported as 328 PNGs across 100–400% scales.
The complete optional pack now contains 211 source assets and 844 PNG variants.
All earlier 516 PNGs remain byte-for-byte identical to the previous pack.

| Master | Shared assets |
| --- | ---: |
| `panel-extras`: two panel-edge light states and four faction control buttons | 6 |
| `fp-radar`: radar housing, hoses, gauge and display surround | 1 |
| `fp-command-widget`: command-display metal housing | 1 |
| `fp-blank-grid`: common empty monitor grid | 1 |
| `fp-command-labels`: move/follow/attack, three states each | 9 |
| `fp-reticles`: acquisition, normal and target-state animation frames | 19 |
| `fp-status`: health/armour states, narrow cursor bars and central dome | 9 |
| `fp-compass`: heading tape | 1 |
| `fp-radar-arrows`: shared heading directions | 16 |
| `fp-radar-blips`: faction contacts, ore, artifact and debris | 19 |

Robot/model-specific portraits are excluded. The only new image under
`gui/fstpersn/machines` is the common `backgrnd` grid, with four scale variants.
No construction portrait directory, weapon illustrations or radar-opening
animation frames were added. Existing engine code and animation timing remain
unchanged; the existing reticle sequences retain their original filenames.

The built-in image-generation tool rendered the saved masters. Exact final
prompts are beside them in `masters/*.prompt.txt`. The thin line graphics and
small radar contacts use a magenta-keyed master format after rejecting noisy
transparent renders. The exporter converts that format to antialiased RGBA and
removes the matte at boundaries; game PNGs contain no opaque magenta key pixels.
Other masters retain their generated transparency. This conversion is separate
from the lossless PNG compression verification.

`scripts/extend_hd_hud.py` prepares the shared references and source entries.
`scripts/hd_hud_assets.py pack --only <master names>` exports selected masters
while preserving the other packaged textures. Full export remains supported.
When rebuilding source references from scratch, run the original `prepare`
command first and `extend_hd_hud.py` afterward, then export the pack.

Validation: all 844 file hashes, dimensions, byte sizes and unique paths checked;
all 25 master hashes checked; all 516 earlier texture hashes unchanged; excluded
portrait families absent; keyed exports checked for transparency/magenta errors.
The rebuilt native SDL3_image checker decoded and converted all 844 files.
The full pack occupies 11,088,962 PNG bytes; its 400% textures contain 24,111,360
decoded RGBA bytes before renderer overhead. No interactive game test is claimed
for this extension.

Review `preview.html` for every asset at 100–400%, and
`review-first-person-400.png` for the actual exported additions beside the
originals. Artwork is an interpretation of tiny original images, especially the
small radar glyphs; in-game appearance, blending and alignment still need review.
