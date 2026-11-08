# OpenMontage

**MANDATORY: Read `AGENT_GUIDE.md` before responding to ANY user message.**

Do not act on the user's request until you have read AGENT_GUIDE.md.
It contains routing rules that determine your first action based on what the user asked.
Skipping it WILL cause you to take the wrong action.

All core pipeline and routing instructions are in AGENT_GUIDE.md.

## Automatic Post-Production Deliverable: `publish.txt`

Whenever a video production finishes, the agent must **always automatically create a simple `publish.txt` file** at the root of the project workspace (`projects/<project-name>/publish.txt`) without waiting for the user to prompt for it.

This file keeps things simple and ready to post:
1. **Optimized Titles**: 3-4 title variations (e.g., Punchy/Shorts, High-CTR/Curiosity, Technical/Developer, Facebook/LinkedIn).
2. **Post Description**: Clean, engaging post copy with the story hook, core breakdown, and call to action (no timestamps needed).
3. **Platform Tags**: Comma-separated tags ready to copy-paste into YouTube Studio or meta fields.
4. **Hashtags**: Formatted hashtags (`#Topic #TechNews #Shorts...`) for Shorts, Reels, and TikTok.
5. **Pinned Comment**: A short question or call-to-action for comments.
