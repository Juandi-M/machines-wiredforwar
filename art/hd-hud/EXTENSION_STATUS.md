# First-person HUD extension — work in progress

This snapshot preserves 47 additional source entries, bringing the preparation
manifest to 176 assets. It does not replace the completed 129-asset/516-texture
pack already saved under `mods/faithful-hd-hud` and tested in the personal runtime.

Saved new masters and prompts:

- `panel-extras`: panel-edge indicators and faction first-person buttons.
- `fp-radar`: first-person radar assembly.
- `fp-command-widget`: first-person command widget.
- `fp-blank-grid`: first-person machine-panel background.

Prepared references with masters still pending:

- `fp-compass`
- `fp-command-labels`
- `fp-reticles`
- `fp-status`

`scripts/extend_hd_hud.py` prepares these references and extends the source
manifest. Do not interpret this preparation snapshot as a completed exported or
play-tested first-person pack. The full exporter currently requires the four
pending masters before this expanded manifest can be packaged successfully.
The earlier complete export inputs are preserved in commit `24e5eb91`.

Validation for this snapshot: Python syntax compilation, unique source paths,
JSON parsing, PNG integrity for all 12 new reference/master images, and staged
whitespace review. No new GPU rendering or gameplay result is claimed.
