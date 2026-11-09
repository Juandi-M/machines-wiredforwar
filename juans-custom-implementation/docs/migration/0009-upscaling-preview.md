# Upscaling review and isolated Windows preview

Date: 2026-11-08. Checkout: `machines-wiredforwar`.
Branch: `upstream/display-scaling-preferences`.
Base: upstream `dev`, `104862d63b7a09b95d318a2014f05120060ed80d`.
This continues the [display-preferences and UI-scaling work](0008-display-preferences-and-ui-scaling.md).

The sections below record the initial preview preparation. See the follow-up at
the end for actual launch results and the subsequent loading-screen work.

## Problems found in the second pass

### Dropdowns used space that was outside the window

The startup GUI root retains the window's full dimensions when the menu is
centered. At 400% on 3840x2160, the 2560x1920 menu starts at (640,120), while the
root still reports 3840x2160. Treating all that root space as visible can place a
long resolution list below the physical window.

Added a small geometry helper that intersects the root with the real window and
expresses the visible area in root-local coordinates. Options dropdowns and the
multiplayer player-selection dropdown now use those bounds. The lobby dropdown
also uses the actual root origin and scales the shared row-border spacing;
player-colour outlines scale with the rest of the control.

Regression cases cover a long list on a centered 4K menu, a root overlapping the
top-left, and roots entirely outside the window vertically or horizontally.
Zero-width visible areas offer no dropdown rows.

### The named-bitmap cache ignored scale

`GuiRootSharedBitmaps` cached an image by filename alone. Requesting the same file
at 1x and then 4x returned the same cached object. This can retain a loading-size
image when a larger menu needs it.

Added regression tests first: both changing from 1x to 4x and returning from 4x
to 1x failed before the fix. The cache now remembers the scale of its current
entry and reloads when that scale changes. Repeated requests at the same scale
still share the object. Named lookups expose the most recently requested scale;
existing owning references remain valid.

These cache tests use the repository's surface overrides and temporary file
placeholders. They verify cache identity and lifetime without a GPU or image
decoder; they do not establish rendered pixel quality.

## Native build and tests

The game and five focused repository suites build with the installed Windows
MSVC toolchain. All 42 cases pass:

| Suite | Cases |
| --- | --- |
| GUI baselines | 6 |
| Named-bitmap cache | 6 |
| Display preferences | 7 |
| Dropdown placement | 12 |
| Scale selection/fit | 11 |

Logs are in `build/display-scaling/upscaling-build*.log` and
`build/display-scaling/upscaling-ctest.log`. This is focused validation, not a run
of every upstream suite. No Docker or WSL build was used.

## Isolated preview

Prepared `build/display-scaling/play/machines` as a separate runtime. Copied
7,700 asset files from the proven ground-zero package, including planet data,
movies, GUI, models, sounds, metadata, and shaders. Did not copy old MinGW DLLs,
executables, logs, saved games, or the working build's configuration. The native
executable imports Windows system libraries and the MSVC runtime; its SDL,
OpenAL, and other game dependencies are linked into this build.

Initial configuration:

- Borderless, following the desktop resolution without saved width/height.
- Auto UI scale: up to 400% when the complete menu fits.
- Cursor grabbing disabled for the shared test.
- Separate writable configuration and logs.

The launcher `Play Upscaling Preview.cmd` sets its working directory and
`MACH_ROOT` to this preview and uses the existing `--skip-intro` option to reach
the menus sooner. It does not modify global environment variables.

The metadata-only `machines.exe --version` check exited 0 and reported MSVC
19.44.35229.0/x86_64. Source inspection confirms this argument returns before
`startup()` and SDL/video initialization. No interactive game window was opened.

Preview executable SHA-256:
`4345c778db62fb66c28951efabe9cefe6ace3c6dec5fcb5cb6e94cdfefe6ef2e`.
The matching manifest is `build/display-scaling/upscaling-preview.json`.

## Next shared test and limits

The next step is an authorized visual/input test with runners off: verify the
4K menu at Auto/400%, Options dropdowns, labels, highlights, click targets,
animations, message boxes, and a match/HUD including first-person radar. Then
compare 300%, 200%, smaller resolutions, Windows desktop DPI scaling, and saved
resolution/Auto behavior. The full checklist remains in the previous record.

The initial loading-screen exception and disabled hotkey-screen animation at
scales above 100% were inherited upstream behavior at this point. No claim was
made that every screen rendered correctly,
that gameplay or multiplayer passed in this preview, or that either issue is
ready to close. No commit, push, PR, or maintainer message was made.

## Shared launch follow-up

The user authorized launching with runners off. Three launch attempts exposed:

1. The initial launcher redundantly set `MACH_ROOT`. In the development build,
   an assertion diagnostic recursively called `SysPathName::pathname()` while
   checking whether the path was relative, causing stack overflow `0xc00000fd`.
   Matching native symbols established the cause; the last SDL log line alone
   had initially suggested the wrong subsystem. Clearing `MACH_ROOT` in the child
   environment and relying on the correct working directory resolved it without
   changing the path implementation or global environment.
2. At 400%, the squadron-bank rows extended four pixels below their parent and
   hit the GUI containment assertion. One-pixel row overlaps had not scaled.
   Scaling the overlaps and numeric-label border restored the original geometry.
   Two added HUD regression cases failed before this fix and passed afterward,
   bringing the focused total to 44. Logs: `hud-before.log` and `hud-fix-ctest.log`.
3. The repaired build displayed the enlarged main menu at 3840x2160/400%. The
   assistant observed aligned menu text/buttons in a native screen capture.
   The user then closed it manually; this was confirmed explicitly and was not
   another crash. Options, gameplay, and audible output were not verified in
   this native preview session.

The third build's executable SHA-256 was
`8419cec892a1456027c7be8e31a6f4300469d5f577247466def595121a7536c6`.
The original failed preview executable/PDB and crash reports were retained for
symbolication. The corrected launcher clears `MACH_ROOT`; it does not set it to
the runtime path.

The user subsequently requested enlargement of the initial loading image and
reported missing robot gun audio. The continuation is recorded in
[0010](0010-loading-screen-and-separated-experiments.md). This document now lives
in the separate personal clone; the code and runtime evidence remain in the
community checkout. No source work was committed or published.
