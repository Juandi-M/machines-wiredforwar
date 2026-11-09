# Skirmish menu crash: absent custom category

Date: 2026-11-08. Branch: `feature/opengl-first-run`.

Follow-up: the [upstream runtime audit](0006-upstream-runtime-audit.md) found no
missing base files and identified the same absent-Custom-category condition
explicitly handled by community v1.7.1. That strengthens the diagnosis without
establishing the result of our pending manual retest.

## Reproduction and evidence

The user reported successful menus and animations, then a crash while opening
Skirmish from the single-player choice screen. A match had not started. The
game's stdout ended after successful preloading and stderr was empty.

Windows Application event 1000 recorded an access violation (`0xc0000005`) at
module-relative offset `0x367850` in `machines-opengl.exe`, process 21368, at
17:49:53 Costa Rica local time. The executable's preferred image base is
`0x400000`, making its link-time address `0x767850`.

Relinking the same patched-baseline objects with a linker map identified that
address as `MachGuiDbSystem::nPlanets() const`. The mapped executable's entire
`.text` section was compared with the crashed executable and matched byte for
byte. Relinking changed the overall file hash (the PE timestamp is regenerated),
so the code comparison, rather than an assumed identical file hash, establishes
that the address mapping applies.

`MachGuiCtxSkirmish::updateMapSizeList()` iterates SMALL through CUSTOM (indexes
0 through 3) and calls `nPlanets()` on each system. The default database creates
only three systems. A fourth is appended by `parseUserCampaignFile()` only when
`data/customscen.dat` exists. That optional file is absent in this runtime.
`skirmishSystem()` previously indexed the vector without checking its size.
The absent fourth entry is a concrete out-of-bounds path consistent with the
recorded fault. No crash dump with a full stack or register values was available;
manual retesting is still required to establish the symptom as resolved.

## Repair

Added `MachGuiDatabase::hasSkirmishSystem()` to check the index and pointer before
access. The Skirmish list now skips absent systems before dereferencing them.
Existing categories retain their order, and valid Custom entries remain usable.
No fake scenario files, changes to save/database formats, or resolution changes
are introduced. The code changes are confined to `conversion/`.

This unsafe path exists in the published source. Its relationship to the 1999
retail game remains unclassified; do not label it a retail bug or an audio-patch
regression without additional evidence.

## Build and verification limits

Extended `tools/build-intro-audio-experiment.py` to rebuild staged `database.cpp`
and `ctxskirm.cpp` as well as the two audio translation units. It emits a linker
map and restores the baseline objects/executable after linking. This continues
the incremental patched-baseline experiment, not a clean/native build of the
complete conversion tree. Baseline ANI and MACHGUI compiler definitions and
flags were compared and matched; the build completed successfully.

Artifact: `build/opengl/bin/machines-opengl-skirmish.exe`, SHA-256
`45145ffdd33822d6b895c7f5726eca330e548839267af201668c962ebfcb2780`.
Build log: `build/opengl/logs/skirmish-guard-build.log`. The earlier address-only
relink log is `skirmish-address-map-build.log`; the current generated map at
`intro-audio-link.map` describes the latest patched build, whose addresses may
differ from the crashed build.

The helper retains its historical output name `machines-opengl-intro-audio.exe`;
the new result was saved separately as `machines-opengl-skirmish.exe`, and the
original audio-only artifact was restored from the runtime copy afterward.
Staged files under `build/opengl/intro-audio-source` now include both repairs.

Verified no game process was running, backed up the previous runtime executable
as `machines-opengl-before-skirmish-fix.exe`, and staged the new executable as
`build/opengl/runtime-baseline/machines/machines-opengl.exe`. Preserved all assets,
settings, saves, and the untouched `original/` source. No game was launched during
this investigation or build.

Next manual check: enter Skirmish, inspect the size/terrain/scenario choices,
and start a match. Also check a runtime with valid custom scenarios when one is
available. Campaign, multiplayer, resolution availability, and complete gameplay
remain separate validation work; this build is not yet confirmed playable.
