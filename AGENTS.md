# OpenMontage

**MANDATORY: Read `AGENT_GUIDE.md` before responding to ANY user message.**

Do not act on the user's request until you have read AGENT_GUIDE.md.
It contains routing rules that determine your first action based on what the user asked.
Skipping it WILL cause you to take the wrong action.

All core pipeline and routing instructions are in AGENT_GUIDE.md.

## Automatic Post-Production Deliverables: `publish.txt` + `thumbnail.png`

Whenever a video production finishes, the agent must **always automatically create both deliverables** inside the project's `renders/` folder (`projects/<project-name>/renders/`) without waiting for the user to prompt for it.

### 1. `publish.txt` — Publishing Kit

This file keeps things simple and ready to post:
1. **Optimized Titles**: 3-4 title variations (e.g., Punchy/Shorts, High-CTR/Curiosity, Technical/Developer, Facebook/LinkedIn).
2. **Post Description**: Clean, engaging post copy with the story hook, core breakdown, and call to action (no timestamps needed).
3. **Platform Tags**: Comma-separated tags ready to copy-paste into YouTube Studio or meta fields.
4. **Hashtags**: Formatted hashtags (`#Topic #TechNews #Shorts...`) for Shorts, Reels, and TikTok.
5. **Pinned Comment**: A short question or call-to-action for comments.

### 2. `thumbnail.png` — Video Thumbnail

Generate a **visually striking 1280×720 PNG thumbnail** using an available image generation tool (e.g., `flux_image`, `imagen`, `gpt_image`). The thumbnail must:

1. **Reflect the video's core hook** — dominant visual (a dramatic frame, concept illustration, or hero graphic) that communicates the topic at a glance.
2. **Include bold, readable text overlay** — 2-5 words max, high-contrast font, legible at small sizes (YouTube thumbnail grid). Use a color that pops against the background.
3. **Follow the video's visual style** — match the palette, tone, and energy of the production (cinematic, tech-minimal, vibrant, etc.).
4. **Be 16:9 aspect ratio, 1280×720 px** — the standard for YouTube, LinkedIn, and social previews.
5. **Avoid clutter** — one clear focal point, minimal elements. The best thumbnails are simple and bold.

**Thumbnail generation workflow:**
- Use the script's title/hook and scene_plan's hero visual moment as the prompt basis.
- If a generated hero image already exists in `assets/images/`, use it as the visual anchor (img2img or reference).
- Write the prompt to explicitly request: bold text, high contrast, 16:9, thumbnail composition.
- Save to `projects/<project-name>/renders/thumbnail.png`.
- If image generation is unavailable, extract a compelling still frame from `renders/final.mp4` using FFmpeg at the most visually impactful timestamp (use `ffmpeg -ss <timestamp> -i final.mp4 -frames:v 1 -vf scale=1280:720 thumbnail.png`).
