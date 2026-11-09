# Working agreement for Juan's Machines workspace

## Current layout: two project folders

Workspace: `C:/Users/juanm/OneDrive/Documents/github/machines-wiredforwar`.
The user's explicit two-folder choice on 2026-11-09 supersedes older layouts.

- `project/` contains all community game source, build files and contribution
  work. It is tracked by the OUTER repository. The outer `.git` remains at the
  workspace root on `upstream/display-scaling-preferences`.
- `experiment/` contains the full personal project, HD artwork, export tools,
  documentation, stages, roadmap, architecture and migration records. It keeps
  its own `.git`, local branch `dev`, and no remote. The outer `.gitignore`
  ignores the ENTIRE folder, including its Git metadata.
- Root files `README.md`, `AGENTS.md`, and `.gitignore` explain the workspace.
  Do not put another game source tree or documentation collection at the root.
- Do not recreate `local-experiments`, `machines-game-experiment`, or
  `machines-juan-experiments`. Historical records keep former paths as evidence.

Use `git -C` with the intended absolute repository path. Contribution Git
commands target the outer workspace; experimental Git commands target
`.../machines-wiredforwar/experiment`. `project/` is not another Git repository
or submodule. Do not force-add `experiment/` to the outer repository.

## Source, remotes, and publication

Outer remotes:
- `origin`: `https://github.com/Juandi-M/machines-wiredforwar.git`.
- `upstream`: `https://github.com/WiredForWar/machines.git`; read-only unless
  the user explicitly requests a direct upstream push.

Use descriptive contribution branches such as `upstream/<topic>`. Preserve
existing changes and check the intended repository, branch and status before
editing. Concurrent tasks must not edit the same files; do not create workers
or additional repositories without a request.

Before commits, inspect the staged diff and file list. Stage specific paths,
keep runtime binaries, downloaded assets, caches and build outputs ignored,
and describe the change and actual validation. Before pushes, verify the URL,
source/destination branches and commits. Do not push, merge, force-push or
rewrite shared history without authorization for that action and destination.

The outer repository now stores community files under the `project/` prefix.
This local workspace reorganization is not an upstream game contribution.
Extract selected changes into upstream's normal layout and revalidate before
preparing a community PR. Keep private artwork, roadmap, migration history,
and working agreements out of upstream PRs unless directly relevant.

`experiment/` has no push destination. Its local commits preserve its work but
are not uploaded by outer commits or pushes. Do not configure a remote without
an explicit request. Promote selected source changes into `project/`
deliberately; never overwrite the entire contribution project with experiments.

## Documents and agreed goals

The authoritative index is `experiment/juans-custom-implementation/README.md`.
Its `docs/ROADMAP.md`, `docs/PROJECT_BRIEF.md`, and `docs/ARCHITECTURE.md` retain
all plans and decisions. The agreed stages are:
1. The whole game playable on Windows 11 with Vulkan, including multiplayer;
   known bugs are allowed, missing functionality is not.
2. Faithful stabilization: preserve inherited retail behavior, fix migration
   regressions, and document uncertain cases.
3. Modernize C++, dependencies and architecture while preserving the experience.

The OpenGL build is ground zero, not completion of Vulkan. The requested HD pack
is at `experiment/mods/faithful-hd-hud/`, with 844 textures and 25 masters under
`experiment/art/hd-hud/`. Only the initial 516 textures were user-tested; the
full extension still requires interactive review. Never invent test results.

## Native Windows work and preservation

Build from `project/` or `experiment/` using native Windows C++ tools. Do not use
Docker or WSL unless explicitly requested. Builds stay under each project's
`build/`. Moved CMake caches contain historical absolute source paths; configure
fresh build directories rather than reusing them.

Do not launch the game, control the screen or change display state without
session authorization and a check for active local runners. Stop when the user
stops automation or takes over. File reorganization does not require a launch.

Preserve source, artwork, working runtimes, settings, saves and Git metadata.
Recovery archives and manifests are under
`project/build/consolidation/2026-11-09/`; the two-folder checkpoint is in
`two-folder-layout/`. Verify exact resolved paths before recursive moves or
deletion, preserve unique work first, and never erase experiments with git clean.

For handoff, state the affected folder, branch, actual checks and their limits,
commit/publication status, and remaining work. Keep this layout as the single
current source of truth.
