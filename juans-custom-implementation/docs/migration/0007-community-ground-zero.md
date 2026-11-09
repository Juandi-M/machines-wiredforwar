# Ground zero restarted on the community fork

Date: 2026-11-08. Initial source revision:
`104862d63b7a09b95d318a2014f05120060ed80d` on `dev`.

## Provenance and scope

The active workspace is `machines-wiredforwar`, a full clone of
[Juandi-M/machines-wiredforwar](https://github.com/Juandi-M/machines-wiredforwar).
GitHub identifies it as a fork of
[WiredForWar/machines](https://github.com/WiredForWar/machines). The local HEAD
matches that upstream's `dev` branch at the time of this audit. The old published
Nightdive source was also legitimate; this is a later community implementation,
not newly discovered 1999 source.

The checkout declares development version 1.7.6 and is 96 commits beyond the
latest published stable tag, v1.7.5. An available v1.7.5 executable would not
establish that this newer checkout builds or works. Ground zero builds this exact
source and follows its matching packaging process.

All previous documents were preserved under `juans-custom-implementation`.
Their old `original/`, `conversion/`, compiler paths, local patches, and Vulkan
prototype describe a discarded experiment. The current repository has one
source tree at its root; no earlier engine patches have been carried over.

## What upstream changed

The [changelog](../../../ChangeLog.md), source, build files, and upstream workflow
show substantial maintenance and behavioral changes:

| Area | Earlier baseline | Current checkout |
| --- | --- | --- |
| Language/build | C++11-era MinGW setup | C++20; Conan 2, MSVC/Clang and MinGW build paths |
| Window/input | SDL2 | SDL3 and SDL3_image; reorganized input/window integration |
| Music | ALURE plus dynamically loaded Vorbis library | Bundled stb_vorbis decoding and an OpenAL music mixer; ALURE removed |
| Cutscenes | Audio packets tied to video-frame submission | Separate audio-only Smacker decoder, prefilled audio buffers, correct microseconds conversion |
| Renderer | OpenGL operations across legacy rendering classes | `Ren::IRenderBackend`, surface/window interfaces, backend factory, GL21 backend |
| Display settings | Combined mode list and legacy filtering | Separate resolution/refresh settings and a display-mode catalogue |
| Skirmish | Unconditional Custom-category access | Category limit conditional on custom scenarios being present |
| Diagnostics/tests | Legacy diagnostic streams | spdlog, crash/hang reports, broader upstream test suites |

Only GL21 is registered by the current backend factory. A reusable interface is
useful for Vulkan investigation but is not an implemented Vulkan renderer.

Upstream also changes the experience: first-person squad commands, mouse-wheel
zoom, 2x UI scaling, pathfinding/AI fixes, music crossfades and resume behavior,
and starfield presentation are documented examples. Some are configurable, but
this review has not established a complete retail-equivalent configuration.
The 1999 retail game remains the fidelity authority; upstream changes must be
distinguished from our future regressions. Modern dependencies do not prove
unchanged sound, gameplay, timing, or assets.

A raw snapshot comparison with Nightdive commit
`2c857564ac9145fa8913ed57e533a5069faf7662` reports 6,901 changed paths, 706,195
insertions, and 823,700 deletions. Renames, formatting, and reorganized headers
inflate this count; it is not a measure of how much gameplay was rewritten.

## Build approach

The host has Python but no CMake, native C++ compiler, or discovered Visual Studio
installation. Avoid installing a large Windows toolchain as part of this first
experiment. Follow upstream's Ubuntu 24.04/MinGW cross-build and packaging path;
the result is a Windows executable to be tested on Windows 11. Native Windows
source compilation remains a later ground-zero checkpoint.

The README's generic dependency list still mentions SDL2. Actual CMake files
require SDL3. The upstream workflow additionally uses
`WiredForWar/machines-packager` for MinGW headers/libraries and runtime files,
and `WiredForWar/machines-data` for generated assets. Those are necessary context
missing from the short standalone README build command.

Source was exported directly from HEAD with `git archive`, then unpacked onto
the container's Linux filesystem. This avoids building through OneDrive and
keeps the working source unchanged. Configuration uses the upstream toolchain,
the packager's dependency directory, Release, DEV_BUILD=OFF, and four build jobs.
The dedicated container is `machines-community-ground-zero`; its only host
mount is the ignored `build/ground-zero` output directory. It does not expose
the working source to modification.

Packager revision: `f4bead0951223ac46d650a2b4756e168ec0efe4c`.
The cross-build dependencies differ from the versions pinned for native Conan
builds: dependency claims must identify which path was actually used.

## Runtime assembly and validation status

Runtime files must be assembled from the base asset archive, the compiled
checkout's installed files, the generated current data overlay, and the matching
packager's runtime libraries. Do not overlay the v1.7.5 executable onto a dev
source test or mix in our previous ALURE/FreeType patches.

The user explicitly authorized a shared launch once the build was ready and
confirmed runners were off. All 1,183 build steps completed successfully, followed
by installation. No game-source changes were required. Warnings were emitted;
this was not a warning-free build. The Release experiment disabled the upstream
unit-test suites; successful compilation is not a claim that those suites passed.

Actual tools: Ubuntu 24.04, CMake 3.28.3, MinGW GCC 13-posix (CMake reports
13.0.0), and Ninja. The packager supplies SDL 3.4.12 headers and FreeType 2.10.0;
these are not the same as the native Conan recipe's pinned versions. Optional
SWScale was not found and is disabled through the supported fallback.

Data-source revision: `2b5e9681174a924b1e4da7c6e6e5efb781da9f7c`. The base asset
archive SHA-256 is
`988a110402eba32c53166b668714425db608e65d58dcdfe43f202a58a7757cd3`.
The machine-readable digest in `build/ground-zero/provenance.json` is generated
from the downloaded file.

The temporary data helper scripts and `for-planets.txt` lists needed LF line
endings for execution/parsing on Linux; packaging scripts also needed executable
permissions after Windows tar staging. The initial attempt generated invalid
carriage-return folder names, and a retry copied a directory into an existing
destination, creating a nested `machines` folder. Corrected the temporary
packaging process using fresh build/install directories and content-copy syntax.
The final overlay's 1,276 paths were checked before extraction onto a newly
extracted base runtime. No malformed/partial runtime was used for the launch.

The final runtime is `build/ground-zero/play/machines`. It contains this checkout's
installed game/data, the current generated overlay, and the exact packager's
runtime files. The executable SHA-256 is
`c08ecbc73b8f87199b305c2f98fe44ea62a53975e3d91e5b39eb95cf813f969d`.
On Windows, `machines.exe --version` exited 0 and printed
`Machines 1.7.6 (build 104862d6)` and `Build: GCC 13.0.0 (MinGW), , Release`.
This verifies the executable's loader dependencies without opening SDL.

The authorized interactive launch then displayed the legal and developer intro
screens. Logs confirm GUI, models, textures, an OpenAL Soft device, and music
initialization. Runtime settings select Windowed, 1280 x 720, refresh 0 (desktop
rate), with cursor grabbing disabled for the shared test. The base config was
saved in the logs before those reversible test settings were applied. Intro
audio quality was subsequently confirmed continuous by the user through the
robot shooting sequence. The intro transitioned to the main menu, and the
assistant opened the single-player choices successfully. On detecting user
input in the window, the assistant yielded the controls; the attempted next
Skirmish click was not executed. The user subsequently confirmed that Skirmish
loaded and a match played, and later reported playing without crashes. This
passes the initial ground-zero play test. It does not establish all campaign
content, endurance, multiplayer, retail fidelity, or Vulkan functionality.

Runtime diagnostics identify SDL 3.4.12, an OpenAL Soft audio device, the GL21
backend on an RTX 4080 SUPER, and NVIDIA OpenGL driver 4.6. The game detects the
3840 x 2160 desktop at 60 Hz; this is not yet proof that the 4K option has been
selected or tested in the menu. The Windows kernel version logged as 10.0.26100
is consistent with the Windows 11 target and does not mean this is a Windows 10
build experiment.

## Reproduction and artifacts

Ignored output root: `build/ground-zero`. A fresh `git archive HEAD` source
snapshot was unpacked at `/work/source` inside the dedicated container; the
packager's dependency directory was staged as `/work/deps`.

```sh
cmake -S /work/source -B /work/build -G Ninja \
  -DCMAKE_TOOLCHAIN_FILE=/work/source/cmake/Toolchain-mingw64.cmake \
  -DWINDOWS_DEPENDENCIES_DIR=/work/deps \
  -DCMAKE_BUILD_TYPE=Release -DDEV_BUILD=OFF -DBUILD_TESTS=OFF \
  -DBUILD_PLANETED=OFF -DMachines_COMMIT_INFO=104862d6 \
  -DCMAKE_INSTALL_PREFIX=/work/install/machines
cmake --build /work/build --parallel 4
cmake --install /work/build --prefix /work/runtime-lf/machines
```

Generate the companion data with its upstream `scripts/install.sh`, setting
`SKIP_GRAYSCALE=y`; use the packager's supplied grayscale images as its workflow
does. Overlay generated data, then the packager's MinGW `bin` and
`win64-extra-files` directories, onto the installed source package, and extract
that overlay over the base archive's `machines` directory. Do not create another
`machines` directory inside it.

Logs include `toolchain-install.log`, `configure.log`, `build.log`,
`install-final.log`, `data-build-final.log`, `data-package-final.log`,
`game-imports.txt`, `version.stdout.log`, and `first-launch.*.log`.
Game diagnostics are under the runtime's `logs/machines.txt`. The provenance JSON
records the source and companion revisions. The build container initially held
the objects, symbols, and staged source; its later removal is recorded below.

## Cleanup after the successful play test

At the user's request, removed the three task-specific Docker containers:
`machines-opengl-baseline`, `machines-vulkan-build`, and
`machines-community-ground-zero`. Also removed the previous experiment's custom
image `machines-upstream-opengl:latest`. Shared base images, Docker itself, and
unrelated volumes were left intact. The Windows game does not depend on any of
those containers at runtime. A future rebuild needs a fresh build environment;
native Windows compiler setup remains pending.

Before removing the current container, exported the matching debug symbols to
`build/ground-zero/symbols/machines.exe.debug`, its CMake cache to
`logs/final-CMakeCache.txt`, and compiler/CMake version information to the logs.
The active output directory now contains only:

```text
build/ground-zero/
  play/machines/       Tested Windows executable, assets, runtime DLLs and state
  logs/                Build, packaging and launch logs
  symbols/             Matching debug symbols for crash analysis
  provenance.json      Source/dependency revisions and checksums
```

Automatic approval review rejected permanent deletion of the Windows staging
files with the reason "blocked by policy". Moved the downloads, companion
checkouts, failed runtime, and intermediate archives into the single ignored
folder `build/cleanup-trash`. They are inactive but still occupy disk space and
can be removed manually. Earlier paths to those temporary inputs are historical.
No alternate deletion mechanism was used.

Verified that the tested executable still has the recorded SHA-256 and that its
required non-system runtime DLLs remain present. The upstream game source and
its own supported build files, including `docker/`, were unchanged. No game
launch was performed during cleanup.
