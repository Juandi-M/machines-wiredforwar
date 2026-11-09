# Machines workspace

This workspace has two project folders:

| Folder | Purpose | Git |
| --- | --- | --- |
| [project/](project/README.md) | Community game source and contribution work | Tracked by the outer repository |
| [experiment/](experiment/LOCAL_WORKSPACE.md) | Personal implementation, HD artwork, documentation and roadmap | Independent local `dev`; ignored by the outer repository |

The outer `.git` and remotes remain here. Run contribution build commands from
`project/` and experimental commands from `experiment/`.

Our [roadmap](experiment/juans-custom-implementation/docs/ROADMAP.md),
[project brief](experiment/juans-custom-implementation/docs/PROJECT_BRIEF.md), and
[architecture](experiment/juans-custom-implementation/docs/ARCHITECTURE.md) live
only in the experiment folder. The three agreed stages are complete playable
Vulkan functionality, faithful stabilization, then internal modernization.

Recovery archives are under `project/build/consolidation/2026-11-09/` and remain
local. The latest layout checkpoint is in its `two-folder-layout/` subfolder.

The `project/` prefix is this user's workspace arrangement. Review and extract
selected changes into the upstream layout before preparing a community PR;
do not submit the workspace reorganization as an upstream game fix.
