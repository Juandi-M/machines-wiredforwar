# Working agreement for Juan's Machines project

## Purpose and two working copies

We have two distinct workstreams, intended to run in separate working copies:

| Copy | Purpose | Branch convention |
| --- | --- | --- |
| Upstream contribution copy | Focused fixes, features, tests, and documentation suitable for WiredForWar/machines. | `upstream/<topic>` |
| Juan's experimental copy | Our Vulkan port, architecture experiments, preservation work, and project-specific documentation. | Local `dev` |

Use descriptive project names for branches and contributions. Do not add tool or
AI-provider branding to branch names, commit messages, or contribution prose.

Keep their code changes, commits, pushes, runtime state, and PRs separate.
An experimental change is not automatically an upstream contribution.

**Current physical setup:** two independent clones live under
`C:/Users/juanm/OneDrive/Documents/github/`:

- `machines-wiredforwar`: the sibling upstream contribution checkout, currently
  on `upstream/display-scaling-preferences`.
- `machines-juan-experiments`: this personal experiment checkout, initially on
  `experiment/ground-zero`, based on upstream `dev` at `104862d6`; ongoing personal
  work now uses local `dev` at the user's request. Earlier experiment branches
  remain as historical references; do not resume work on them by default.

Both use Juan's fork as `origin` and WiredForWar/machines as `upstream`, with the
URLs below. This experimental clone contains the authoritative private documents
in `juans-custom-implementation/`. The user requested this move; all 20 files
were verified by SHA-256 after moving. Community changes and existing runtimes
remain in the contribution checkout. The personal HD HUD pack, native image
checker, and isolated `build/hd-hud/play/machines` runtime are now provisioned.
The latter deliberately reuses community executable SHA-256 `d321a22c...` and
immutable base assets, with separate configuration/saves/logs. It is not a full
game build from this clone's engine source. See migration record 0011. Do not recreate
or clean up the retired `machines-game-experiment` workspace.

When provisioning the experimental copy, use a separate clone or managed
worktree outside this checkout. Do not put another Git repository inside this
one. Update this setup section with its actual path, branch, and remotes. Do not
move the existing documents or change their authoritative location silently.

## Identify the destination before changing anything

- Determine whether the task is an upstream contribution, a private experiment,
  or shared planning/documentation. If unclear, perform useful read-only work
  and clarify the destination before mixing implementation changes.
- Check the working directory, `git status --short`, current branch, remotes,
  and the intended base commit. Inspect existing changes and preserve unrelated
  work. A folder name alone does not prove which repository or branch is active.
- Use local `dev` for ongoing personal work. Keep upstream contributions on
  topic branches in the separate contribution checkout. The upstream default
  branch is currently `dev`; verify that when starting a new contribution.
- Do not update remote shared/default branches without explicit authorization.
  Keep one topic per contribution branch and record the starting upstream
  revision for experiments.
- Give parallel tasks separate working copies and branches. Do not let two
  workers edit the same checkout concurrently. These workstreams do not by
  themselves request sub-agents or authorize starting other workers.

## Remotes, commits, and pushes

Current remotes:

- `origin`: `https://github.com/Juandi-M/machines-wiredforwar.git` — Juan's fork.
- `upstream`: `https://github.com/WiredForWar/machines.git` — community project.

Before every commit, inspect the complete staged diff and its file list. Stage
specific paths; do not use a blanket `git add .` or `git add -A` when the checkout
contains unrelated work, private documents, or experiments. Keep commits focused
and independently understandable. Use a concrete subject describing the change;
explain the reason and material validation in the body when useful. Do not put
generated logs, downloaded assets, executables, DLLs, build outputs, debug
symbols, or local caches into source commits.

Before every push, verify the repository URL, local branch, remote branch, and
commits being published. Push explicitly to the named topic branch on Juan's
`origin`. Treat `upstream` as read-only unless the user explicitly requests a
direct upstream push and access is available. Do not force-push, merge a PR,
rewrite shared history, or update shared/default branches without specific
authorization.

User authorization to commit, push, or open a PR applies to the stated scope and
destination; do not repeatedly request it. A request to investigate, build, fix,
or write documentation alone does not request publication. Complete the local
work and relevant checks so any requested review concerns a concrete result.

## Upstream contributions and PR contents

- Base an upstream contribution on the appropriate upstream branch. Keep our
  private Vulkan work, project roadmap, migration diary, this local working
  agreement, and unrelated changes out of the upstream PR by default.
- Follow upstream's current contribution instructions, conventions, supported
  build paths, and relevant tests. Inspect any PR template before writing the PR.
- Check the full PR diff against its intended base, not just the last commit.
  Review both file names and commit history for accidental experimental content.
- Public documentation directly explaining the contributed behavior belongs
  with the contribution, using upstream's existing locations and style.

Each PR description should provide the information relevant to that change:

1. The problem and reproduction steps, linked issue, or reason for the feature.
2. The resulting behavior, approach, and important tradeoffs.
3. Validation actually performed: commands, results, and relevant environment
   details, including source/data revisions or toolchain when they matter.
4. Known limitations, untested cases, and compatibility or behavior changes.
5. Before/after screenshots or a short capture for visual changes, when useful;
   concise reproduction instructions for timing, audio, or multiplayer changes.

Scale this to the change. A small fix needs a short clear description, not a
ceremony. Do not claim a build, automated test, manual play test, or comparison
passed unless it actually did. Distinguish assistant observations from user
reports. Avoid uploading raw private logs, personal paths, credentials, or
unrelated screenshots. Opening a PR does not authorize posting other messages
or contacting maintainers through another channel.

## Our documentation and experiments

Our authoritative project documentation is currently under
`juans-custom-implementation/docs/`, indexed by
`juans-custom-implementation/README.md`:

- `PROJECT_BRIEF.md`: purpose, problem, scope, preservation policy, open decisions.
- `ROADMAP.md`: stages, intended outcomes, and acceptance criteria.
- `ARCHITECTURE.md`: current design, proposed boundaries, and technical decisions.
- `guides/`: reproducible build, setup, testing, and maintenance procedures.
- `migration/`: changes, rationale, alternatives, provenance, evidence, and lessons.

Keep documents synchronized when their subject changes. Separate historical
results from current facts and proposed work. The imported two-source-tree and
2020-port notes describe the retired experiment; they are not current setup
instructions. Do not copy them into an upstream PR as evidence for another build.

For a meaningful experiment, record what changed, why, the base revision and
relevant dependencies/assets/settings, how it was checked, and what remains
uncertain. Keep raw/generated artifacts in ignored local build directories and
summarize useful findings in the documentation. Do not require a separate report
for every trivial edit.

Our agreed stages remain:

1. The whole game playable on Windows 11 with Vulkan, including multiplayer;
   known bugs are allowed, missing functionality is not.
2. Stable behavior faithful to the 1999 retail experience. Preserve inherited
   retail quirks by default; fix our regressions and document uncertain origins.
3. Modern C++, dependencies, and architecture while preserving that experience.

The community fork intentionally contains changes beyond retail behavior.
Distinguish those from our changes and from verified retail quirks. Its OpenGL
play test passes an initial ground-zero checkpoint, not stage one. Native
Windows source compilation passed in the contribution checkout; complete feature
coverage remains a separate check. Do not reuse its absolute-path CMake cache here.

## Reusing changes between copies

Transfer only deliberately selected changes. Prefer focused, attributable
commits over copying a whole source tree or merging all experimental history
into an upstream contribution. Revalidate a fix in the receiving copy and
record its source commit. Rework or extract an experimental change onto a clean
upstream topic branch before proposing it publicly.

Use separate build directories and writable runtime folders, configurations,
saves, mods, and logs for the two copies. Do not reuse a CMake cache across
working copies; it contains absolute paths. Shared immutable asset archives are
fine, but concurrent tests must not share writable game state.

## Running and cleaning up

Use a native Windows C++ toolchain for this project. Do not use Docker or WSL
for builds, tests, or dependency installation unless the user explicitly requests
that approach. Install and maintain the native tools within the authorized task
scope; discuss a different build environment before introducing it.

Do not launch an interactive game, take screen control, or change display state
without the user's authorization for that test session. Establish whether local
runners are active before an interactive test; once the user confirms the test
is authorized and runners are off, proceed within that scope without asking
again. Stop screen automation immediately if the user stops it, and yield when
they take over the controls. A documentation task does not require launching.

Preserve the known working runtime and required game files during cleanup.
Verify resolved paths before recursive deletion or moving, and keep operations
inside the named workspace. Remove only task-owned containers/images; never
globally prune shared Docker resources, caches, or volumes. If an action is
blocked, report it accurately and use only permitted safer alternatives; do not
claim quarantined files were permanently deleted. The Windows game runs without
Docker; the source still supports Docker as one build option.

## Handoff

State which copy and branch changed, what changed and why, relevant checks and
their limits, and whether anything was committed, pushed, or proposed upstream.
Include the commit or PR link when applicable. Explicitly identify pending work
and cross-copy transfers so the next task starts with the correct context.
