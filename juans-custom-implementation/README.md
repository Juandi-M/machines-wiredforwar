# Juan's custom implementation

This folder contains our project brief, architecture, decisions, roadmap, and
migration history. It now lives in the independent personal experiment clone,
`machines-juan-experiments`, beside the community contribution clone,
`machines-wiredforwar`. Both start from
[WiredForWar/machines](https://github.com/WiredForWar/machines) and use
[Juan's fork](https://github.com/Juandi-M/machines-wiredforwar) as `origin`.

The repository's [working agreement](../AGENTS.md) separates upstream
contributions from our experiments and defines commit, push, PR, and
documentation rules. The personal clone now uses local `dev`; community
fixes remain on `upstream/display-scaling-preferences` in the other clone. This
documentation folder itself is not another nested Git repository.

- [Project brief](docs/PROJECT_BRIEF.md)
- [Roadmap and stages](docs/ROADMAP.md)
- [Architecture and audio direction](docs/ARCHITECTURE.md)
- [Decisions and migration history](docs/migration/README.md)
- [Practical guides](docs/guides/README.md)
- [Current community-fork ground zero](docs/migration/0007-community-ground-zero.md)
- [Display preferences and larger UI scales](docs/migration/0008-display-preferences-and-ui-scaling.md)
- [Upscaling review and isolated Windows preview](docs/migration/0009-upscaling-preview.md)
- [Separate experiment clone, loading scaling, and robot audio](docs/migration/0010-loading-screen-and-separated-experiments.md)
- [Personal HD HUD artwork and packaging](docs/migration/0011-faithful-hd-hud.md)
- [Local commits and the personal dev branch](docs/migration/0012-local-dev-checkpoint.md)

## Current evidence

The unmodified `dev` source at `104862d6` has compiled into a Windows executable
through the upstream MinGW/packager path. Windows loaded it successfully; intro
and menu rendering work, and the user confirmed continuous intro audio and a
Skirmish match that loaded and played without a reported crash. Complete-game
coverage and multiplayer remain unverified. The display contribution branch now
also builds natively on Windows with MSVC and passes 48 focused test cases. Its
previous build displayed the enlarged 4K main menu; the user closed it manually.
The latest loading-screen scaling build includes the requested three-second
minimum robot sequence and has now been launched with runners off. Enlarged
loading artwork was observed; the user confirmed audible gunfire, roughly three
seconds of visibility, and continued startup into the intro or menu.
See the [latest record](docs/migration/0010-loading-screen-and-separated-experiments.md).
The personal `dev` branch now contains an optional pack with 129
re-rendered HUD assets and 516 losslessly optimized scale variants. All passed
native SDL image decoding/conversion. Its separate runtime at
`build/hd-hud/play/machines` reuses the community preview executable. In its first
shared test at 400%, the user confirmed that the new artwork appears and the
controls work. The separate menu-bug report is still pending. See the
[HD HUD record](docs/migration/0011-faithful-hd-hud.md).
Vulkan has not been implemented in either checkout.

Runtime paths in these records belong to the community checkout unless stated
otherwise. Its proven baseline is `build/ground-zero/play/machines/machines.exe`;
the native preview is `build/display-scaling/play/machines/machines.exe`. Both
run directly on Windows. The personal clone now has its own HD HUD test runtime
and native image-checker build; it has no separate full-game build yet. Build
directories, configurations, saves, and logs remain separate between clones.

## Current layout

The game source lives at the repository root, with its upstream README and build
files. This custom folder contains documentation only. The independent personal
clone starts from upstream's `dev` at `104862d6`; no community display patches,
old experiment patches, build caches, or Vulkan prototype code were copied here.

The preserved documents describe the earlier experiment and its original
two-source-tree layout. Those paths, old build commands, dependency workarounds,
and claims of implemented prototype functionality are historical. This layout
and the upstream fork replace those implementation assumptions. The project
goals remain: stage one is the whole game on Windows 11 with Vulkan, including
multiplayer; stage two establishes stability and original fidelity; stage three
modernizes internals while preserving the experience.

All 20 private documentation files were moved here at the user's request and
verified by SHA-256 before updating the current setup notes. The retired project's
README and source metadata remain under `docs/migration/previous-workspace-*`.
Nothing from the retired workspace was deleted during this move.
