# OpenMontage

**MANDATORY: Read `AGENT_GUIDE.md` before responding to ANY user message.**

Do not act on the user's request until you have read AGENT_GUIDE.md.
It contains routing rules that determine your first action based on what the user asked.
Skipping it WILL cause you to take the wrong action.

All core pipeline and routing instructions are in AGENT_GUIDE.md.

## Automatic Post-Production Tasks

**MANDATORY: Read `AGENT_TASKS.md` after every video production completes.**

After `compose` finishes and `renders/final.mp4` exists, the agent must run all tasks defined in `AGENT_TASKS.md` automatically — without waiting for the user to ask. That file is the single source of truth for post-production behaviour.

Currently defined tasks:
- **Task 1 — `publish.txt`**: Complete platform-ready publishing kit (titles, descriptions, tags, hashtags, pinned comment, chapters, A/B hooks).
- **Task 2 — `thumbnail.png`**: video thumbnail in the same orientation as the video (1280×720 horizontal, 1080×1920 vertical) via HyperFrames HTML (preferred), image generation, or FFmpeg fallback.

Both outputs go into `projects/<project-name>/renders/`. Full specs and workflows are in `AGENT_TASKS.md`.
