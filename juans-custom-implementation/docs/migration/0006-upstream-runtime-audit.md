# Upstream README and runtime-file audit

Date: 2026-11-08. Branch: `feature/opengl-first-run`.

## Purpose and result

The user requested an audit of upstream setup requirements before further code
changes. This investigation did not change game source, replace runtime files,
modify settings/databases, or launch the game. Previously staged audio and
Skirmish repairs remain separate, uncommitted work.

No omitted base-archive file or reference-source data/model/sound file was found.
The missing optional custom-map file is absent from both supplied archives,
not an extraction mistake. More decisively, the community v1.7.1 source already
contains a fix for the same Custom-category assumption. This supports treating
the observed lookup as a problem in the older published port, without making
claims about the 1999 retail implementation.

Our assembled runtime is nevertheless a patched-baseline experiment, not a
complete installation of the newer community release. Those configurations must
not be described as interchangeable or as an exact reproduction of its README.

## Sources checked

- The [Nightdive README](https://github.com/NightDive-Studio/machines/blob/2c857564ac9145fa8913ed57e533a5069faf7662/README.md)
  lists Git LFS, build dependencies, Linux/MinGW commands, and diagnostics. It
  provides no complete playable-asset manifest or instruction to supply custom
  scenarios. The [original port author's README](https://github.com/markol/machines/blob/master/README.md)
  also documents building rather than a complete asset installation contract.
- The [current community README](https://github.com/WiredForWar/machines/blob/dev/README.md)
  explicitly distinguishes that fork from the original port. Its Windows setup
  calls for the base asset archive followed by a complete release overlay into
  the same directory, including replacement assets. Its default branch is `dev`.
- The [v1.7.1 README](https://github.com/WiredForWar/machines/blob/v1.7.1/README.md)
  describes packaging the source data, graphics, and binaries; it does not
  contain the newer README's Windows installation section. Do not attribute
  the newer instructions to the frozen 2024 README.
- The [v1.7.1 packaging configuration](https://github.com/WiredForWar/machines/blob/v1.7.1/CMakeLists.txt#L244)
  installs `data`, `sounds`, `gui`, `models`, `machstrg.xml`, and the executable.
- Actual local archives inspected: `machines-assets.7z` and
  `machines-win64-wfw-20240910.7z` (community v1.7.1). The archive contents, not
  just the documentation, were used for the file comparison.

## File checks

| Check | Result |
| --- | --- |
| Base archive inventory | All 6,816 file paths exist in the runtime; no omitted extraction paths. This is a presence check, not a byte comparison of every asset. |
| Reference-source runtime overlay | All 367 files under `original/data`, `original/models`, and `original/sounds` exist and match their runtime copies by SHA-256. |
| Scenario definitions | All 51 unique scenario names referenced by `data/sceninfo.dat` have corresponding `data/<name>.scn` files. |
| Planet folders | All 45 referenced planet folders exist under `models/planet`. Folder presence does not establish that every internal geometry/texture reference is valid. |
| Menu/campaign FLIC references | Every FLIC path directly listed in the scenario database exists. |
| Briefing/description text | All 84 referenced text entries have their supported `pdata/<name>.bin` representation. Missing `.txt` source counterparts are not automatically missing content. |
| Scenario database | `pdata/sceninfo.bin` is present, 27,667 bytes, and byte-identical to the copy extracted from the base archive. SHA-256: `5d9055a121ec9195e84f038d823b34e3b6fa7e93a193a8ee2c1c30b232d64177`. |
| Player database | `savegame/playinfo.bin` is absent. The source explicitly falls back to the supplied scenario database when this file does not exist. |
| Custom-map database | `data/customscen.dat` appears in neither archive nor the preserved source tree and is absent from the runtime. The source conditionally loads it if present. |
| Windows library archives | No unresolved Git LFS pointer files found among `original/windows/**/*.a`. |

The reference implementation's `MachGuiDbTextData::pNewTextData()` prefers
compiled `.bin` descriptions and only parses `.txt` when the compiled form is
absent. Do not delete the entire `pdata` directory as a generic cache reset:
some supplied descriptions have no text-source replacement in this setup.
Likewise, archive-identical binary data establishes provenance, not complete
serialization compatibility or successful gameplay.

`SysMetaFile::useMetaFile()` returns false in the reference source, so loose files
are required; merely having `mach1.met` would not replace the source overlay.
The audit confirms that overlay is present.

## Direct upstream evidence for the Custom-category failure

Community v1.7.1's
[Skirmish list implementation](https://github.com/WiredForWar/machines/blob/v1.7.1/src/libdev/machgui/ctxskirm.cpp#L409)
explicitly notes that the Custom system is absent without `customscen.dat`. It
chooses a maximum category of LARGE when custom scenarios do not exist, and
CUSTOM otherwise. The corresponding
[database implementation](https://github.com/WiredForWar/machines/blob/v1.7.1/src/libdev/machgui/database.cpp)
checks file existence before parsing user scenarios.

This is independent upstream confirmation of the condition found at our crash
address. Supplying a fabricated custom file is not an upstream-documented
installation requirement. Our pending guard checks the actual stored category
before accessing it; the community fix instead limits iteration based on file
existence. Both address the absent category, though our runtime result remains
unverified until another authorized test.

## Difference from a complete community installation

The community release archive contains 1,168 files. Relative to that release,
our runtime has 376 byte-identical files, 248 different files, and 544 absent
paths. Differences include the original shaders, tutorial script, GUI graphics,
planet textures, and string table. Absent paths include 2x UI graphics, shader
variants, newer command indicators, a movement-indicator texture, and
`machines.exe` (we use the separately named source-built executable).

These are material differences from the complete community installation, not
evidence that all 544 paths are required by our older source. Our runtime used
the base assets, the older source's matching metadata, selected community DLLs,
and some release resources. Blindly overlaying a newer release would change the
comparison and could add incompatible shaders or change visuals. No overlay
was applied during this audit.

## Evidence and next step

Local audit artifacts, ignored under `build/opengl`:

- `logs/assets-archive-manifest.txt` and `logs/community-1.7.1-manifest.txt`.
- `logs/runtime-layout-audit.json`, including complete missing/different lists.
- `audit-runtime-layout.py`, the local inventory/comparison probe.

The justified next step is a controlled retest of the already staged Skirmish
guard, with this same recorded asset set. A separate clean community installation
could provide additional comparison evidence, but must retain its matching
executable and data together and must not be confused with the preserved-source
baseline. No new launch was authorized or performed by this audit. Complete game
asset integrity, downstream references, binary parsing, campaign play, skirmish
matches, and multiplayer still require runtime validation.
