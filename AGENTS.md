# OpenMontage

**MANDATORY: Read `AGENT_GUIDE.md` before responding to ANY user message.**

Do not act on the user's request until you have read AGENT_GUIDE.md.
It contains routing rules that determine your first action based on what the user asked.
Skipping it WILL cause you to take the wrong action.

All core pipeline and routing instructions are in AGENT_GUIDE.md.

## Automatic Post-Production Deliverables: `publish.txt` + `thumbnail.png`

Whenever a video production finishes, the agent must **always automatically create both deliverables** inside the project's `renders/` folder (`projects/<project-name>/renders/`) without waiting for the user to prompt for it.

### 1. `publish.txt` — Publishing Kit

Write a complete, platform-ready publishing kit. Every field must be crafted from the actual video content — no filler, no placeholders, no generic copy.

**Required sections:**

1. **Optimized Titles** — At least **5** variations, each targeting a different platform context or audience intent:
   - `Punchy / Shorts` — ≤60 chars, hook-first, mobile-scroll attention grab
   - `High-CTR / Curiosity gap` — open loop that makes clicking feel compelled
   - `Technical / Developer` — precise, keyword-rich, earns trust from experts
   - `LinkedIn / Professional` — outcome-focused, professional framing
   - `SEO / Long-tail` — full-phrase title built around searchable terms

2. **Post Descriptions** — **2 distinct versions**:
   - `Short (Shorts/Reels/TikTok)` — 3–5 punchy sentences, hook → payoff → CTA. Under 150 words.
   - `Long (YouTube/LinkedIn)` — Full story arc: opening hook, context, what the viewer learns, 3–5 bullet key insights, closing CTA. 200–400 words. No timestamps.

3. **Platform Tags** — 20–30 comma-separated tags for YouTube Studio / meta fields. Mix broad discovery tags with niche long-tail and brand tags.

4. **Hashtags** — 15–25 hashtags in `#Format`. Group in 3 tiers:
   - Broad reach (3–5): `#AI #Tech #Science`
   - Mid-niche (6–10): topic-specific, algorithm-friendly
   - Brand / series (3–5): `#Refactorian #Shorts #Reels`

5. **Pinned Comment** — One carefully crafted engagement-seed comment. Options: a provocative question that splits opinion, a teaser for the next video in the series, a "timestamp guide" if the video is long, or a bold claim that invites debate. Must feel like the creator wrote it, not an AI.

6. **Chapters** *(if video is 3 min+)* — Timestamped chapter list in `00:00 Chapter Name` format, derived from the scene_plan. Skip for Shorts/Reels under 60 seconds.

7. **A/B Hook Lines** — 3 alternative first-sentence hooks for the description, so the creator can test which performs best.

**Quality rules:**
- Pull every title, stat, and claim directly from the `script` and `brief` artifacts — never invent facts
- Match the video's tone: dry/technical, hype/cinematic, educational/calm — no one-size-fits-all voice
- Titles must be unique; no two should feel like variations of the same phrase
- The pinned comment must spark a reply, not just acknowledge the video

### 2. `thumbnail.png` — Video Thumbnail

Generate a **visually striking 1280×720 PNG thumbnail** using an available image generation tool (e.g., `flux_image`, `imagen`, `gpt_image`). The thumbnail must:

1. **Reflect the video's core hook** — dominant visual (a dramatic frame, concept illustration, or hero graphic) that communicates the topic at a glance.
2. **Include bold, readable text overlay** — 2-5 words max, high-contrast font, legible at small sizes (YouTube thumbnail grid). Use a color that pops against the background.
3. **Follow the video's visual style** — match the palette, tone, and energy of the production (cinematic, tech-minimal, vibrant, etc.).
4. **Be 16:9 aspect ratio, 1280×720 px** — the standard for YouTube, LinkedIn, and social previews.
5. **Avoid clutter** — one clear focal point, minimal elements. The best thumbnails are simple and bold.

**Thumbnail generation workflow (preferred: HyperFrames HTML):**
- **Primary method — HyperFrames**: Author a bespoke `thumbnail-hf/index.html` composition (1280×720, `data-duration="1"`) that exactly matches the video's visual language (palette, grid, typography, accent colours). Use pure SVG for diagrams and icons — no external images required. Run `npx hyperframes snapshot --at 0 --output snapshot_0.png` from inside the folder, then copy `snapshot_0.png/frame-00-at-0s.png` → `renders/thumbnail.png`.
- **Design rules**: Off-white `#F5F5F1` background; architectural grid with thin `rgba(17,24,39,0.045)` lines (0.65px), delicate dot intersections, and 192px module rules; corner registration marks in `#94A3B8`; Inter (sans) + JetBrains Mono; bold headline ≤5 words at high contrast; 4–6 stat chips grounding the hook in data; REFACTORIAN brand signature.
- **Fallback — image generation**: If HyperFrames isn't available, use `flux_image`, `imagen`, or `gpt_image`. Write the prompt to explicitly request: bold text overlay, high contrast, 16:9, thumbnail composition at 1280×720.
- **Fallback — FFmpeg**: If no generation tool is available, extract a compelling still frame from `renders/final.mp4` at the most visually impactful timestamp: `ffmpeg -ss <timestamp> -i final.mp4 -frames:v 1 -vf scale=1280:720 renders/thumbnail.png`.
