# Separate experiment clone, loading scaling, and robot audio

Date: 2026-11-08. Community code: `machines-wiredforwar`, branch
`upstream/display-scaling-preferences`. Source base:
`104862d63b7a09b95d318a2014f05120060ed80d`. Changes remain uncommitted.

## Independent personal project

At the user's request, cloned upstream `dev` into the sibling folder
`machines-juan-experiments` and created `experiment/ground-zero` at the same
source base. This is a full independent Git clone, not a nested repository or a
shared working tree. Both clones have these remotes:

- `origin`: `https://github.com/Juandi-M/machines-wiredforwar.git`.
- `upstream`: `https://github.com/WiredForWar/machines.git`.

Moved all 20 files from the community clone's `juans-custom-implementation/` to
the same relative location in the personal clone. Verified each relative path
and SHA-256 after moving, before updating current setup notes. Added a working
agreement to the personal clone and updated both copies' `AGENTS.md` to identify
the destinations and authoritative documentation location.

Community source edits, known working binaries, assets, configurations, saves,
and logs remain in `machines-wiredforwar`. No source patches or absolute-path
build caches were copied into the personal clone. It has no build/runtime yet.
No part of the retired `machines-game-experiment` folder was removed here.

## The tiny loading image

The screenshot shows the initial loading backdrop, `gui/menu/wait.bmp`, before
the short robot movie `flics/postload.smk`. This is separate from the longer
`animatic.smk` intro. Upstream explicitly forced the loading backdrop to 100%
with a comment about previous scaling glitches. Early startup also drew it at
unscaled 640x480 coordinates, while other UI elements already scaled.

Added a shared `LoadingScreenLayout` calculation for the centered backdrop,
animation offset, notice position, and initial progress bar. The early splash
and lobby splash now stretch to the selected menu scale. Both buffers retain
the existing clear/draw sequence. The later named loading backdrop uses that
same scale, and `postload.smk` scales both its position and its video frames.

At 3840x2160/400%, the complete backdrop occupies 2560x1920 at (640,120). The
572x184 robot movie is enlarged to 2288x736, beginning at (768,636). Black
margins and original proportions remain. This enlarges original pixels; it
does not create detail or replace assets. At 100%, original coordinates and
sizes are preserved.

Four added geometry cases cover original placement, exact 4K placement,
animation/progress containment across 100-400%, and consistent movement when
window dimensions change. These exercise production layout calculations without
a GPU; actual rendering still requires a shared test.

## Missing robot gun sound

Our preview launcher and the preceding menu test used `--skip-intro`. Source
inspection shows that `skipIntroScreens_` skips `CTX_POSTLOADINGANIMATION` as
well as the later logos and full intro. Thus the test displayed the static
loading picture but bypassed the robot movie and its sound. This was our preview
configuration, not evidence of a missing game asset or a defective audio DLL.

Removed `--skip-intro` from `Play Upscaling Preview.cmd`. The game's existing
skip option retains its behavior; no audio engine, decoder, codec, or volume
code changed for this finding.

A small headless inspector built natively with MSVC `/MD` and the game's bundled
libsmacker decoded the installed movie completely:

| Property | Result |
| --- | --- |
| Asset | `flics/postload.smk` |
| SHA-256 | `8d8a64599ab3e078cb1723a42612da4c31a7cc52e7572cbdeb53d7b813d4ab1a` |
| Video | 572x184, 45 frames, 2.25 seconds |
| Audio | Track 0, mono, 16-bit PCM, 22050 Hz |
| Decoded audio | 99,226 bytes, 25 nonempty chunks, 2.25 seconds |
| Non-silence evidence | Peak 16,465; RMS approximately 3,785 on the 16-bit scale |

The complete longer intro also decoded successfully (632x272, 2215 frames,
88.6 seconds, stereo 16-bit/44100 Hz). These are decoder checks, not listening
tests. Gunfire identity, Windows output volume, and synchronization remain to
be confirmed during normal startup.

Inspector source/executable and output remain ignored under
`build/display-scaling/`; the retained robot result is
`loading-audio-inspection.log`. No asset file was altered.

## Three-second minimum requested afterward

The user requested that the short robot sequence stay visible for at least
three seconds even on a very fast machine. Its video is already timed, rather
than played as quickly as the loading CPU allows. It starts in a separate
post-loading context; elapsed asset-loading time does not count toward it.

The movie and gunfire retain their original playback speed and duration. When
the movie finishes before the context has lasted three seconds, the startup
loop retains the player and leaves the last presented frame visible for the
remainder (approximately 0.75 seconds for the normal 2.25-second clip). Input
continues to be pumped each cycle; a one-millisecond yield prevents a busy spin
while holding the frame. The existing context timer supplies elapsed time. Slow
playback runs to completion, even if it exceeds three seconds. Escape/Space,
window events, and `--skip-intro` retain their existing skip paths; other movies
and menu transitions receive no minimum-duration change.

This is an intentional presentation preference requested by the user, not a
verified retail behavior or an established acceptance condition of upstream
issues #39/#70. Keep this change independently reviewable when preparing commits
and an upstream PR. No source change has yet been published.

## Build, preview, and limits

Built the game and seven focused suites natively on Windows using the previously
installed MSVC 19.44.35229.0/CMake/Ninja/Conan toolchain. All 48 cases pass:

| Suite | Cases |
| --- | --- |
| GUI baselines | 6 |
| Named-bitmap cache | 6 |
| Loading-screen layout | 4 |
| HUD layout | 2 |
| Display preferences | 7 |
| Dropdown placement | 12 |
| Scale selection/fit | 11 |

The initial logs are `build/display-scaling/loading-screen-build.log` and
`loading-screen-ctest.log`. After the minimum-duration change, the game and seven
suites rebuilt and all 48 existing cases passed again; the new logs are
`loading-minimum-build.log`, `loading-minimum-test-build.log`, and
`loading-minimum-ctest.log`. These cases cover layout/preferences, not the new
duration guard. The three-second hold still needs manual verification. No Docker
or WSL was used.

Updated only the isolated native preview at `build/display-scaling/play/machines`
with the new executable and matching PDB. Preserved the previous 44-case preview
under `build/display-scaling/preview-8419cec8`. The ground-zero executable's hash
remains `c08ecbc73b8f87199b305c2f98fe44ea62a53975e3d91e5b39eb95cf813f969d`.

Current preview executable SHA-256:
`d321a22c29effadec45ca5075ed416134c42b410925176ab95da78985d81055a`.
The preceding loading-scale build, hash
`26360f385b6c2c316331ed4d3854454aac4a58e68ae228767f7e922ec46bd8dc`,
is preserved with its PDB under `build/display-scaling/preview-26360f38`.
The metadata-only `--version` process exited 0 before SDL/game startup. The
manifests `upscaling-preview.json` and `native-provenance.json` now identify this
build and distinguish it from the previously observed menu build.

The previous preview displayed the enlarged 4K menu and was closed manually by
the user; see [0009](0009-upscaling-preview.md). At preparation time this latest
build had not been launched interactively. The shared test plan was normal startup with runners off,
checking enlarged loading art, notice/bar alignment, the robot firing animation
and sound, a three-second minimum from the robot sequence's start (including
the final-frame hold), explicit skipping, then menu transitions and Options.
Retest 100/200/300/400% and smaller
windows before claiming broad rendering compatibility. Gameplay, multiplayer,
and the separate inherited hotkey-animation exception remain unverified in this
modified preview. Nothing was committed, pushed, or posted upstream.

### Shared launch follow-up: user-confirmed results

The user explicitly requested launch and confirmed runners were off. Started
this exact preview executable normally, with no `--skip-intro` argument and with
the working directory/environment described above. The launched process was
PID 16380. Native window captures showed visibly enlarged, centered robot/loading
artwork; later captures continued to show that artwork. The user confirmed that
their monitor continued through the intro or reached the menu, so those captures
did not reflect continued progress on the actual display.

The user explicitly confirmed all three manual checks:

- Machine-gun fire was audible during the short loading animation.
- The robot sequence remained visible for roughly three seconds, including the
  brief hold at the end.
- Startup continued into the intro or reached the menu.

These audio, approximate duration, and progress results are user observations;
the assistant independently observed the enlarged loading artwork. The duration
was not instrumented, and no claim of sample-accurate audio synchronization or
complete-game coverage follows from this test. Left the game available for the
user instead of closing or relaunching it automatically. No additional code
changes, commits, pushes, or upstream messages were needed for this result.
