# OpenMontage — Agent Tasks

This file defines the **automatic post-production tasks** every agent must run after a video production completes. Tasks are executed unconditionally — the agent does not wait for the user to ask.

**Read `AGENT_GUIDE.md` for the full pipeline contract. This file covers tasks only.**

Additional agent tasks will be added here over time. Each task is a top-level section below.

---

## Task Index

| # | Task | Trigger | Output |
|---|------|---------|--------|
| 1 | [Publishing Kit](#task-1-publishing-kit-publishtxt) | `compose` stage completes | `renders/publish.txt` |
| 2 | [Video Thumbnail](#task-2-video-thumbnail-thumbnailpng) | `compose` stage completes | `renders/thumbnail.png` |

Both outputs go into the project's `renders/` folder: `projects/<project-id>/renders/`.
Neither is optional. A production run is not complete until both files exist.

---

## Task 1 — Publishing Kit (`publish.txt`)

**Trigger:** Immediately after `renders/final.mp4` is confirmed to exist.
**Output:** `projects/<project-id>/renders/publish.txt`

Write a **complete, platform-ready publishing kit**. Draw every title, stat, and claim directly from the `script` artifact (hook, title, key claims) and `brief` artifact (tone, platform, target audience, style). **Never invent facts or use generic filler.** The tone must match the video's style — dry/technical, hype/cinematic, educational/calm — applied consistently across all sections.

Format: clearly sectioned plain-text using `================` banners and `---` sub-dividers. No markdown syntax, no asterisks, no backticks. The file must be copy-paste-ready out of a terminal.

Minimum total length: ~600 words. A thin `publish.txt` is a defect.

---

### Section 1 — Optimized Titles (minimum 5 variations)

One title per line, each preceded by its label. Each targets a distinct platform context or audience intent — no two titles should feel like paraphrases of each other.

| Label | Goal | Constraint |
|---|---|---|
| `Punchy / Shorts` | Stops the thumb on a mobile scroll, hook-first | ≤ 60 chars |
| `High-CTR / Curiosity Gap` | Opens a loop the viewer feels compelled to close | ≤ 70 chars |
| `Technical / Developer` | Precise, keyword-rich, earns expert trust | any length |
| `LinkedIn / Professional` | Outcome-framed, authoritative, results-first | ≤ 100 chars |
| `SEO / Long-tail` | Full search phrase built around discoverable terms | 60–100 chars |

Add a 6th (`Contrarian / Provocative`) when the content challenges conventional wisdom or is opinion-led.

---

### Section 2 — Post Descriptions (2 versions)

**Short version** *(Shorts / Reels / TikTok)*
- 3–5 sentences max. Under 150 words.
- Structure: bold opening hook → 1–2 sentences of context → payoff / key insight → CTA.
- No timestamps. No bullet lists. Must read like a human wrote it in one breath.

**Long version** *(YouTube / LinkedIn)*
- 200–400 words.
- Structure:
  1. Opening hook (1–2 sentences — same energy as the video's first line)
  2. Context / problem statement (2–3 sentences)
  3. What the viewer learns / sees (3–5 bullet key insights, each one sentence)
  4. Why it matters / broader significance (1–2 sentences)
  5. Closing CTA (subscribe / follow / comment prompt)
- No timestamps in the body. Add a `--- Chapters ---` block below when the video is 3 min+ (see Section 6).

---

### Section 3 — Platform Tags

20–30 comma-separated tags for YouTube Studio / social meta fields.

Mix strategy:
- **Broad discovery** (5–8 tags): wide-reach category terms a new viewer might search
- **Niche / long-tail** (10–15 tags): specific to the topic, boosts algorithm surfacing
- **Brand** (3–5 tags): `REFACTORIAN`, series name, recurring show identifiers

Output as a single comma-separated line, ready to paste directly into YouTube Studio's tag field.

---

### Section 4 — Hashtags (3-tier stack)

15–25 hashtags in `#CamelCase` format, ordered by tier on a single line:

- **Broad reach** (3–5 tags): e.g., `#AI #Tech #Science` — feeds the widest discovery funnel
- **Mid-niche** (8–12 tags): topic-specific, algorithm-friendly, used by the target community
- **Brand / series** (3–5 tags): `#Refactorian #Shorts #Reels` — builds channel identity over time

Output as a single space-separated line, ready to paste into a caption or description footer.

---

### Section 5 — Pinned Comment

One carefully crafted comment written **as the creator**, not as an AI assistant. It must do one of:

- Ask a **polarising or opinion-splitting question** ("Which of these three did you NOT expect?")
- Tease the **next video** in the series ("Part 2 is going to break your brain — it covers X")
- Surface a **surprising stat or fact** from the video that wasn't the main hook
- Provide a **"which one are you?"** identity anchor that reliably drives replies
- For videos 3 min+: a **quick timestamp guide** mapping key moments ("0:00 intro / 1:14 the twist / 2:30 the math")

Hard rules:
- Sounds human — ≤ 3 sentences
- Ends with a question or a strong statement that demands a reaction
- Never write "What do you think?" or "Let me know in the comments!" — these are banned phrases

---

### Section 6 — Chapters *(skip for videos under 3 min)*

Timestamped chapter list in `MM:SS Chapter Name` format, derived from the scene_plan scene boundaries.

- First chapter must always be `00:00`
- Chapter names: 3–5 words, title-case, tell the viewer exactly what they're walking into
- Minimum 4 chapters (YouTube requires 4+ for the chapter feature to surface in search)

---

### Section 7 — A/B Hook Lines

3 alternative **opening sentences** for the description — the creator can split-test which pulls best.

- Each is exactly 1–2 sentences
- Each uses a different rhetorical device:
  - `Hook A` — bold stat or hard claim
  - `Hook B` — provocative question
  - `Hook C` — story / scene-setting (drop the reader into a moment)
- Label them clearly as `Hook A`, `Hook B`, `Hook C`

---

## Task 2 — Video Thumbnail (`thumbnail.png`)

**Trigger:** Immediately after `renders/final.mp4` is confirmed to exist (run in parallel with Task 1).
**Output:** `projects/<project-id>/renders/thumbnail.png` — 1280×720 PNG

A great thumbnail has: one clear focal point, 2–5 words of high-contrast text legible at small sizes, palette and energy matching the video's visual style, and no clutter. Simple and bold wins every time.

---

### Method 1 — HyperFrames HTML (preferred)

Author a bespoke `thumbnail-hf/index.html` composition inside `renders/`:

```
projects/<project-id>/renders/thumbnail-hf/index.html
```

Composition spec:
- Root: `data-composition-id="thumbnail"`, `data-duration="1"`, `data-hold`, `data-width="1280"`, `data-height="720"`
- Register a paused GSAP timeline at `window.__timelines["thumbnail"]`
- Use **pure SVG** for all diagrams, icons, and illustrations — no external images required

Render and copy:

```bash
cd projects/<project-id>/renders/thumbnail-hf
npx hyperframes snapshot --at 0 --output snapshot_0.png
cp snapshot_0.png/frame-00-at-0s.png ../thumbnail.png
```

**HyperFrames thumbnail design rules (apply to every video):**

| Element | Specification |
|---|---|
| Background | `#F5F5F1` (off-white / light grey) — never plain white |
| Grid | 48px pattern · `rgba(17,24,39,0.045)` lines · `0.65px` stroke · tiny dot intersections at each node |
| Module rules | 192px overlay · `rgba(17,24,39,0.07)` · `0.8px` stroke |
| Corner marks | Registration L-brackets in `#94A3B8` · inset ~36px from each corner |
| Vignette | Soft radial gradient overlay — adds depth without darkening the frame |
| Panel split | Left visual / right text, divided by a thin vertical rule with gradient fade-in/out |
| Headline | Inter 900 · 60–72px · tight letter-spacing · ≤ 5 words · high contrast against `#F5F5F1` |
| Eyebrow | JetBrains Mono · ~11px · `0.28em` letter-spacing · accent colour |
| Stat chips | 4–6 chips · `font-mono` value + `font-sans` label · thin border · semi-transparent fill |
| Brand | `REFACTORIAN` in JetBrains Mono · bottom-right · `#64748B` |
| Left diagram | Topic-appropriate SVG — sensor rings, data flows, circuit diagrams, etc. — built from SVG primitives |

---

### Method 2 — Image Generation (fallback)

If HyperFrames is unavailable, use the best available image generation tool
(`flux_image`, `imagen`, `gpt_image` — check `registry.get_by_capability("image_generation")`).

Build the prompt from:
- The script's hook / title / key claim
- The scene_plan's most visually compelling hero moment
- The video's established palette and style

Always request explicitly in the prompt: bold text overlay, high contrast, 16:9 aspect ratio, thumbnail composition, 1280×720.

---

### Method 3 — FFmpeg Still Frame (last resort)

If no image generation tool is available:

```bash
ffmpeg -ss <best_timestamp> -i projects/<project-id>/renders/final.mp4 \
  -frames:v 1 -vf scale=1280:720 \
  projects/<project-id>/renders/thumbnail.png
```

Pick `<best_timestamp>` from the scene_plan's hero scene — the moment with the strongest visual. Never use the first frame (usually a black or title card).

---

### Shared Task Rules

- Both tasks are mandatory. Never skip either because the compose stage passed.
- Both outputs go in `renders/` — not the project root, not `assets/`.
- If Method 1 fails for the thumbnail, fall back to Method 2, then Method 3 — never leave `thumbnail.png` missing.
- Log both as the final entries in the compose checkpoint metadata (`metadata.post_production`).
