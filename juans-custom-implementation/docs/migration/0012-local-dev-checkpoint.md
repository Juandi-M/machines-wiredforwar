# Local development checkpoint

Date: 2026-11-08.

The user requested local commits of the pending project work, with ongoing
personal development on one `dev` branch. No merge or push was requested.

The authoritative personal checkout is `machines-juan-experiments`. Its existing
local `dev` branch and both earlier experiment branches started at `104862d6`, so
switching to `dev` preserved all working files without a merge. Ongoing personal
work uses local `dev`; `experiment/ground-zero` and `experiment/hd-hud` remain
unchanged as historical references. Local `dev` no longer tracks upstream's
shared `dev` branch.

The personal checkpoint includes all 15 HD artwork masters and their prompts,
references, 516 exported textures, manifests, offline review materials, exporter
and preview scripts, native image checker source, the working agreement, and
project documentation. Build outputs, downloaded game assets, executable files,
runtime configuration, saves, and logs remain in ignored local directories.

The separate contribution checkout, `machines-wiredforwar`, retains its focused
branch `upstream/display-scaling-preferences`. Its existing engine changes and
tests were saved in local commit
`6a7a62f9cce8808d58ca2a68c87e4a98f4506672`. Its local `dev` remains unchanged.
This is the source work behind the reused HD preview executable described in
record 0011; it has not been transferred into the personal checkout or published.

Checkpoint validation:

- All 15 master hashes and matching prompt files verified.
- All 129 source entries and 516 exported PNG hashes, byte sizes, and dimensions
  verified against the manifests.
- All 516 textures decoded and converted by the existing native SDL3 image checker.
- The existing native contribution test binaries passed 42 focused cases across
  display preferences, dropdown placement, bitmap caching, HUD layout, loading
  layout, and scale selection. This checkpoint did not rebuild the game.
- Staged whitespace checks passed. No interactive game was launched.

The retired `machines-game-experiment` workspace was inspected but left
unchanged. This chat still reported that old working directory, while the app's
project named `machines-game-experiment` reported `machines-wiredforwar` as its
folder. The app naming/location mismatch is separate from the saved source and
artwork; no project entry, chat location, or folder was deleted or recreated.

The separately reported menu issue remains pending. Nothing was merged, pushed,
or proposed upstream by this checkpoint.
