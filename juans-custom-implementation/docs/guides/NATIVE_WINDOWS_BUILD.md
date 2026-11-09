# Native Windows C++ build

This guide applies to the current community-fork checkout. Build and test on
Windows with MSVC; do not introduce Docker or WSL unless explicitly requested.
The older container/MinGW records describe historical experiments.

Run the commands from `machines-wiredforwar`. This guide now lives in the sibling
`machines-juan-experiments` clone, which has no build or runtime yet. For a future
personal build, configure a fresh build directory there; never copy a CMake cache
between clones.

## Installed prerequisites

On 2026-11-08, installed Visual Studio Build Tools 2022 17.14.44 with the x64/x86
C++ tools, Windows 11 SDK 26100, and C++ CMake tools. These provide MSVC 14.44,
CMake 3.31.6-msvc6, and Ninja 1.12.1. The full Visual Studio editor is not needed.
Conan 2.34.0 is installed in the ignored `build/native-tools` Python environment.
The toolchain installation completed without requiring a reboot.

From PowerShell in the repository root, enter the compiler environment:

```powershell
$machinesVswhere = "${env:ProgramFiles(x86)}/Microsoft Visual Studio/Installer/vswhere.exe"
$machinesVsRoot = & $machinesVswhere -latest -products '*' `
    -requires Microsoft.VisualStudio.Component.VC.Tools.x86.x64 -property installationPath
& "$machinesVsRoot/Common7/Tools/Launch-VsDevShell.ps1" `
    -Arch amd64 -HostArch amd64 -SkipAutomaticLocation
$env:PATH = (Join-Path $PWD 'build/native-tools/Scripts') + ';' + $env:PATH
```

For a new checkout, create the Python environment before adding it to PATH:

```powershell
py -3 -m venv build/native-tools
& ./build/native-tools/Scripts/python.exe -m pip install 'conan>=2,<3'
& ./build/native-tools/Scripts/conan.exe profile detect
```

The profile should identify Windows, x86_64, MSVC 194, and the dynamic runtime.
The project's CMake configuration requests C++20. Do not reuse the old Linux or
MinGW CMake cache; native builds use their own directory.

## Game configuration and build

The upstream README recommends its bundled Conan provider for MSVC. It obtains
the dependency versions in `conanfile.py`, downloading binaries where available
and compiling missing packages. The first configure can therefore take longer
than subsequent cached builds. FFmpeg's recipe can use Windows-native MSYS2
tools to run its configure script while compiling with MSVC.

The following configuration command completed successfully:

```powershell
cmake -S . -B build/native-display -G Ninja `
    '-DCMAKE_BUILD_TYPE=Release' '-DDEV_BUILD=ON' '-DBUILD_TESTS=ON' `
    '-DBUILD_WITH_SWSCALE=OFF' `
    '-DCMAKE_PROJECT_TOP_LEVEL_INCLUDES=cmake/conan_provider.cmake' `
    '-DCONAN_INSTALL_ARGS=--build=missing;-c;tools.build:jobs=4'
```

Quote complete `-D...` arguments in PowerShell, especially those containing a
filename or semicolon-separated list. An unquoted provider filename was split
on the first attempt and prevented compiler detection; correcting the quoting
allowed MSVC detection and dependency installation to proceed.

These build/test commands also completed successfully:

```powershell
cmake --build build/native-display -j 4 --target machines ScaleFactorTests `
    DisplayPreferencesTests GuiBaselineTests DropDownPlacementTests GuiRootSharedBitmapsTests `
    HudLayoutTests LoadingScreenLayoutTests
ctest --test-dir build/native-display --output-on-failure `
    -R '^(ScaleFactorTests|DisplayPreferencesTests|GuiBaselineTests|DropDownPlacementTests|GuiRootSharedBitmapsTests|HudLayoutTests|LoadingScreenLayoutTests)$'
```

`BUILD_WITH_SWSCALE=OFF` matches the optional-scaling setting used for ground
zero. The current Conan recipe still requires FFmpeg even with that CMake option;
the recipe is not being changed as part of the display contribution.

## Evidence and runtime separation

All 18 display-policy tests have already compiled and passed natively with MSVC
through an isolated, ignored harness in `build/native-policy-tests`. The harness
uses the actual production source files and test cases; it does not open SDL or
the game. Results are in `build/display-scaling/native-policy-results.log`.
The complete game then linked successfully with MSVC. The current seven focused
repository test suites pass all 48 cases. The native executable is
`build/native-display/machines.exe`. Configuration/build/test logs are retained
under `build/display-scaling`; the latest logs are `loading-minimum-build.log`
and `loading-minimum-ctest.log`. Earlier builds emitted warnings. The previous native
preview showed the enlarged 4K main menu and was closed manually by the user.
The latest loading-screen build has now been launched with authorization and
runners off. Native captures show enlarged loading artwork. The user confirmed
audible gunfire, roughly three seconds of visibility, and startup continuing
into the intro or menu. Duration was assessed manually, not instrumented.
Automated geometry tests and decoded audio alone do not verify those results.

The established playable ground-zero runtime remains in
`build/ground-zero/play/machines`. Do not overwrite it while experimenting.
A separate native test runtime is now prepared at
`build/display-scaling/play/machines`, with its own configuration and launcher.
Its metadata-only `--version` check exits successfully before video startup.
See the [preview record](../migration/0009-upscaling-preview.md) for exact settings,
asset provenance, and launch history. The [latest loading-screen record](../migration/0010-loading-screen-and-separated-experiments.md)
contains the current executable hash and remaining shared tests.

The preview launcher sets its working directory, clears `MACH_ROOT` in its child
environment, and starts `machines.exe` without `--skip-intro`. That option also
skips the short loading robot animation and its embedded audio. Leave it off
when testing the machine-gun sound. For a metadata-only `--version` check from
PowerShell, use `Start-Process -Wait -PassThru -WindowStyle Hidden` and inspect
the returned process's `ExitCode`; the GUI executable does not reliably update
`$LASTEXITCODE` when invoked directly.

Launching the game and changing display state require authorization for the
shared test session. The [display contribution record](../migration/0008-display-preferences-and-ui-scaling.md)
contains the visual/input/configuration checklist and current limitations.
