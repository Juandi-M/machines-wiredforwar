# Display preferences and larger UI scales

Date: 2026-11-08. Upstream contribution checkout: `machines-wiredforwar`.
Branch: `upstream/display-scaling-preferences`.
Base: upstream `dev`, `104862d63b7a09b95d318a2014f05120060ed80d`.

## Problem and intended contributions

[Issue #39](https://github.com/WiredForWar/machines/issues/39) asks the game to
follow the current desktop resolution across launches unless the player
explicitly selects a resolution. Startup already supports this: width and
height default to zero. However, accepting Options unconditionally writes the
displayed size and refresh rate, converting detection into a saved preference
even when only sound was changed. The screen also reads actual runtime settings
instead of saved intent, which can overwrite a temporarily unavailable mode.

[Issue #70](https://github.com/WiredForWar/machines/issues/70) requests larger
UI scales for 4K displays. Options and automatic startup scaling stop at 200%.
Simply exposing 300% and 400% is insufficient: bitmap fonts try to load absent
prebuilt atlases, menu heading sizes stop growing after 200%, and first-person
radar backgrounds bypass the image loader's scaling fallback.

These are related issues, not duplicates. Keep the eventual contributions
separate: first resolution-preference persistence, then UI scaling and its
rendering dependencies. This local branch develops both together for inspection;
no PR, commit, push, or maintainer message is authorized by this implementation
request. Private planning documents and the local working agreement stay out of
upstream contribution diffs.

## Proposal

### Resolution intent

- Reuse the existing `config.xml`; no parallel INI format or new settings store.
- An **Auto** resolution means follow the desktop on each launch. Store a zero
  width/height when a player explicitly returns to Auto. Merely opening or
  accepting Options must not write detected dimensions.
- List Auto separately from the native resolution. Choosing the native size
  explicitly is different from choosing Auto, even when both look identical now.
- Save resolution and refresh choices only after deliberate interaction, not
  after a dependent list is rebuilt. Keep a saved mode when it is temporarily
  unavailable and a fallback is displayed.
- Borderless follows the desktop without erasing the saved explicit mode for a
  later return to fullscreen. Cancel must not persist display changes.
- Include refresh-only changes in the existing restart notice.

Existing nonzero preferences cannot reliably be classified as deliberate or
accidentally saved by older versions. Preserve them; the player can choose Auto
to opt back into desktop following.

### Scaling and appearance

Render the 3D world at the chosen display resolution. Scale the interface
independently, retaining original art and proportions. Avoid stretching the
entire low-resolution framebuffer across a widescreen display.

Offer 100%, 200%, 300%, and 400%, plus Auto. Auto selects the largest supported
whole-number scale for which the complete 640x480 menu fits in both dimensions.
An explicit smaller scale is honoured. If a saved scale cannot fit after moving
to a smaller display, use a fitting scale for that launch.

| Display | Automatic scale | Scaled 640x480 menu |
| --- | --- | --- |
| 1280x720 | 100% | 640x480 |
| 1920x1080 | 200% | 1280x960 |
| 2560x1440 | 300% | 1920x1440 |
| 3440x1440 | 300% | 1920x1440 |
| 3840x2160 | 400% | 2560x1920 |

Integer enlargement makes each original pixel occupy a regular block of display
pixels. This preserves the shapes but exposes the artwork's original detail
limit. It does not create high-resolution textures. Bilinear filtering can make
small bitmap text and outlines soft; stretching to another aspect ratio distorts
them. The first pass uses the existing offscreen nearest-neighbour scaling path.
Headings already use an outline font, which can be rendered at an appropriate
size rather than magnifying a low-resolution text image.

Prefer a matching prebuilt scaled image where available. Otherwise derive the
image in memory from the original. For bitmap fonts, parse the original glyph
boundaries first and enlarge the atlas and measurements together; rescanning
enlarged white separator pixels would create incorrect glyph indices. Cache the
derived font under its requested path without writing generated 3x/4x assets.

SDL already enumerates display modes. This contribution does not need a
hardcoded 1080p/1440p/4K list, a new renderer, new models, asset replacement, or
gameplay changes. Native mode availability depends on the display/driver and
selected window mode. Wider screens should retain the UI's proportions and
appropriate anchors; remaining space belongs to the world view/background.

## First implementation

- Added a testable display-preference policy and guarded UI callbacks so
  programmatic selection changes are not mistaken for user intent.
- Added Auto to resolution and refresh controls, and loaded saved preferences
  rather than copying detected runtime dimensions into the controls.
- Centralized the supported scales and startup choice, including a safe fallback
  and overflow-safe fit checks.
- Added an in-memory bitmap-font enlargement path, proportional menu/HUD font
  sizing, and the missing radar-image fallback.
- Updated the local branch convention to use descriptive project names.

## Validation and limits

The first headless run passed 18 GoogleTest cases: 11 scale-fit/selection cases
and 7 display-preference cases. These compile the actual production policy
sources with GCC 13 in a temporary Ubuntu 24.04 container. They cover desktop
following, deliberate native-size selection, return to Auto, unavailable saved
modes, borderless preservation, refresh-only changes, common monitor shapes,
and smaller-display fallback. They do not exercise SDL, GPU rendering, XML
serialization, or real mouse input.

A Windows cross-build was started using the previous MinGW/container approach.
The user rejected further Docker use and explicitly requested a native Windows
C++ compiler. The task's container was stopped and removed before the build
finished; that attempt produced no validated Windows executable. Native MSVC,
Windows SDK, CMake, and Conan are the chosen path from here. Do not use Docker
or WSL for future work unless the user explicitly requests it. The known working
`build/ground-zero/play` runtime is not modified.

The user subsequently requested a complete local Docker reset while keeping the
software installed. Removed all 200 volumes and 4 remaining images; verified zero
containers, images, volumes, and build cache. Reset the Docker/containerd data
directories, verified the recreated engine, then stopped both services and the
Docker socket. No local Kubernetes cluster/PVC store was found. The shared WSL
distribution/disk was preserved. Future game work uses the native toolchain.

Native prerequisites installed successfully: Visual Studio Build Tools 2022
17.14.44, MSVC 14.44, Windows 11 SDK, CMake 3.31.6-msvc6, Ninja 1.12.1, and Conan
2.34.0 in `build/native-tools`. Conan detects Windows x86_64/MSVC 194. All 18
policy tests also passed natively on Windows with MSVC, compiling the actual
production sources and GoogleTest into `build/native-policy-tests`. Results are
in `build/display-scaling/native-policy-results.log`.

Full native game configuration passed in the fresh `build/native-display`
directory through the upstream Conan provider. Conan obtained the pinned MSVC
dependencies and built missing FFmpeg/SDL_image packages. All 1,208 native build
steps completed, including linking the game and four repository test targets.
CTest passed all four suites (32 cases): display preferences (7), scale factors
(11), GUI baselines (6), and dropdown placement (8). Build warnings were emitted,
including the existing GCC-only pragmas in test overrides; this was not a
warning-free build. This was a Release configuration with DEV_BUILD=ON,
BUILD_TESTS=ON, and optional SWScale disabled.

Executable: `build/native-display/machines.exe`.
SHA-256: `0f23e861be1ecf22de9c7abed1f0c59592a66affab73923b3c035e1f1be6f9ec`.
Build/test logs and preview provenance are retained under
`build/display-scaling`. No game launch, commit, push, or PR was performed.

No interactive game launch is part of this task. Rendering quality, animation
alignment, actual font appearance, and input accuracy remain manual-test items.
This is an initial contribution prototype, not evidence that both issues are
resolved in every mode or that a preservation-project stage is complete.

## Shared-test checklist

Use an isolated runtime/config so the known working build stays reproducible.

1. With no saved width/height, start at desktop resolution. Change only volume
   and accept Options; confirm no explicit width/height was introduced.
2. Change the desktop mode between launches; Auto must follow it. Also test a
   deliberately selected mode, deliberate native size, and return to Auto.
3. Exercise Fullscreen, Borderless, and Windowed. Check a temporarily unavailable
   saved mode and ensure accepting unrelated settings does not replace it.
4. Change resolution/refresh, then Cancel. Verify configuration and subsequent
   launch. Check a refresh-only selection produces the restart notice.
5. At 1080p, 1440p, and 4K, inspect available scales, Auto, and explicit smaller
   choices. At ultrawide sizes, test height limits as well as width. Repeat at
   Windows desktop scaling of 100%, 150%, and 200% to catch any confusion between
   window coordinates and physical display pixels.
6. Inspect main menu, Options, campaign/skirmish selection, lobby, message boxes,
   scrolling dropdowns, hotkeys, and load/save screens. Verify labels, animations,
   hover effects, clipping, and click targets coincide at every scale.
7. In a match, inspect the HUD, icons, tooltips, minimap, first-person radar,
   selection and cursor hotspots, chat, and console. Confirm world rendering and
   gameplay still behave normally.

## Remaining review questions

- Confirm the maintainer agrees with Auto choosing up to 400% by default and
  with a separate Auto resolution entry. Both are user-visible policy choices.
- Audit bitmap-font reload after changing mods: the existing font cache already
  retains font objects, and this work must not promise new live-reload behavior.
- The loading backdrop deliberately uses 100% in upstream because scaling caused
  glitches; this prototype retains that exception rather than claiming every
  legacy screen has already been converted.
