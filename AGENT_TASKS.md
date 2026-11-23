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
**Output:** `projects/<project-id>/renders/thumbnail.png`. It is a PNG with the **same orientation as the video**: a vertical video gets a vertical thumbnail and a horizontal video gets a horizontal one (Step 1).

A great thumbnail has one clear focal point and 2–5 words of high-contrast text that stay legible at the size of a phone-feed tile. Its palette and energy match the video, and it has no clutter. Simple and bold wins every time.

---

### Step 1 — Detect the format (always first)

Read the format from the rendered file, not from the brief or the pipeline name. The size may have changed in production.

```bash
ffprobe -v error -select_streams v:0 -show_entries stream=width,height:stream_side_data=rotation \
  -of csv=p=0 projects/<project-id>/renders/final.mp4
```

This prints `width,height` and, if present, a rotation. If the rotation is 90 or -90, swap width and height. Then pick the format by width ÷ height:

| Video ratio (w/h) | Format | Typical use | Thumbnail canvas | Aspect |
|---|---|---|---|---|
| ≥ 1.2 | `horizontal` | YouTube long-form, LinkedIn, X | **1280×720** | 16:9 |
| 0.9 – 1.2 | `square` | feed posts | **1080×1080** | 1:1 |
| 0.7 – 0.9 | `portrait-4x5` | Instagram / LinkedIn feed | **1080×1350** | 4:5 |
| ≤ 0.7 | `vertical` | YouTube Shorts, Reels, TikTok | **1080×1920** | 9:16 |

Use the canvas from this table. **Never put a 16:9 thumbnail on a vertical video**, and never the other way round. A platform will either crop it unpredictably or letterbox it. Record the detected `format` in `metadata.post_production.thumbnail`.

---

### Step 2 — Layout per format

Every format shares the house style in Step 3. They differ in layout and safe zones. All coordinates below are on the delivered canvas.

#### Horizontal — 1280×720

- **Layout:** a split. The focal visual goes on the left (~55% of the width) and the text column on the right. A thin vertical rule fades in and out between them. Mirror the layout if the visual reads better on the right.
- **Safe box:** x 64–1216, y 48–672. Nothing essential goes outside it.
- **Keep clear:** the bottom-right 200×90 px. YouTube draws the duration badge there, so never put the brand or a chip in that corner.
- **Headline:** 72–96px, at most 3 lines.

#### Vertical — 1080×1920 (Shorts / Reels / TikTok)

- **Layout:** stacked and centred. Put the eyebrow at the top of the safe box and the headline (2–3 lines) below it. The focal visual is large and centred, and takes 40–55% of the height. One line of 2–3 chips can follow. Do **not** reuse the horizontal left/right split.
- **Safe box:** x 90–990, y 300–1500. The headline and the focal visual must sit inside it.
  - Profile grids crop the 9:16 frame to 3:4 (y 240–1680).
  - Feeds that show vertical video as 4:5 crop to y 285–1635.
  - The Shorts shelf draws the title and view count over the bottom ~20%.
  - The safe box keeps the essentials inside all three.
- **Keep clear:** y < 285 and y > 1500. Use them only for background, grid and the brand mark.
- **Headline:** 120–160px, at most 3 lines, at most 12 characters per line. Count the characters per line before building.
- **Minimum text size:** 34px.

#### Square — 1080×1080 / Portrait 4:5 — 1080×1350

- **Layout:** stacked like the vertical layout but shorter. Put the headline on top and the visual below it.
- **Safe box:** 90px in from each edge (for 4:5, y 105–1245; a 1:1 grid crop keeps y 135–1215).
- **Headline:** 100–130px.
- **Minimum text size:** 30px.

---

### Step 3 — House style (all formats)

| Element | Specification |
|---|---|
| Background | `#F5F5F1` (off-white / light grey) — never plain white |
| Grid | 48px pattern · `rgba(17,24,39,0.045)` lines · `0.65px` stroke · tiny dot intersections at each node. This is the only stroke allowed under 1px. |
| Module rules | 192px overlay · `rgba(17,24,39,0.07)` · `1px` stroke |
| Corner marks | Registration L-brackets in `#94A3B8`, 2px stroke, inset ~36px (horizontal) or ~48px (vertical / square) from each corner |
| Vignette | Soft radial gradient overlay. It adds depth without darkening the frame. |
| Headline | Inter 900 · size per format (Step 2) · letter-spacing −0.02em to −0.04em · line-height 0.95–1.05 · **≤ 5 words**. Ink `#15171A` (or the video's darkest ink). |
| Accent word | At most one accent word or idea per headline. Its text colour must pass **≥ 3:1** against the background. (WCAG contrast ratio). If the brand accent fails (e.g. orange `#FF6A13` on `#F5F5F1` is 2.62:1), keep the word in ink and put the accent on a solid highlight bar, an underline (≥ 8px) or a shape behind it. |
| Eyebrow | JetBrains Mono · **22–26px** on horizontal, **34–40px** on vertical / square · 0.2em letter-spacing · uppercase · colour ≥ 4.5:1 contrast |
| Stat chips | Horizontal: 3–4 chips. Vertical / square: 2–3 chips. Values in `font-mono` 26px+ (horizontal) or 36px+ (vertical); labels in `font-sans`. 1.5px border with a semi-transparent fill. The chips are optional and come out before the headline shrinks. |
| Brand | `REFACTORIAN` in JetBrains Mono, `#64748B`, 18–22px (horizontal) or 26–30px (vertical). Horizontal: bottom-left, inside the safe box. Vertical / square: bottom-centre, around 100px above the bottom edge. |
| Focal visual | A topic-appropriate SVG built from primitives, e.g. sensor rings, data flows or circuit diagrams. It is the largest element in the frame. Its strokes are ≥ 2px (horizontal) or ≥ 3px (vertical), so they survive downscaling. |

**Production-grade rules:**

1. **Truthful.** Show only what the video shows: its real diagram, numbers and claim. No invented stats, and no promise the video doesn't keep.
2. **Complement the title, don't repeat it.** The headline is the hook (2–5 words). The platform shows the title right next to it.
3. **One focal point.** Squint test: the visual and the headline are the first two things you see, and nothing competes with them.
4. **Legible small.** Check the headline in the small previews (Step 5) at the smallest size: 168×94 for horizontal, 120×213 for vertical. If it can't be read there, make it shorter or bigger.
5. **Contrast.** All text is ≥ 4.5:1, except accent words and headline-sized text, which need ≥ 3:1.
6. **Sharp.** Capture at 2× density and downscale with Lanczos (Method 1). Never upscale a smaller image to the canvas.
7. **Clean.** No placeholder text, no lorem ipsum, no tool or AI mentions, no watermark other than the brand mark, and no text clipped at an edge or a crop line.

---

### Step 4 — Build it

Try Method 1 first, then Method 2, then Method 3. All three produce the Step 1 canvas and follow Steps 2–3.

#### Method 1 — HyperFrames HTML (preferred)

Author a bespoke `thumbnail-hf/index.html` composition inside `renders/`:

```
projects/<project-id>/renders/thumbnail-hf/index.html
```

Composition spec:
- Root: `data-composition-id="thumbnail"`, `data-duration="1"`, `data-hold`, and `data-width` / `data-height` set to **the canvas from Step 1** (e.g. `1080` / `1920` for a vertical video).
- Register a paused GSAP timeline at `window.__timelines["thumbnail"]`.
- Use **pure SVG** for all diagrams, icons and illustrations. No external images are required.
- Fonts: Inter and JetBrains Mono are bundled. Any other family needs `@font-face` to `assets/fonts/`.

Render at 2× density and downscale to the delivered size. Replace `W,H` with the canvas, e.g. `0,0,1080,1920`:

```bash
cd projects/<project-id>/renders/thumbnail-hf
npx hyperframes check --json
npx hyperframes snapshot --at 0 --no-end --keep --zoom 0,0,W,H --zoom-scale 2 --output snap
ffmpeg -y -v error -i snap/at-0s.png -vf "scale=W:H:flags=lanczos,format=rgb24" ../thumbnail.png
```

Keep `snap/at-0s.png` as the 2× master. Then run Step 5.

---

#### Method 2 — Image Generation (fallback)

If HyperFrames is unavailable, use the best available image generation tool
(`flux_image`, `imagen`, `gpt_image` — check `registry.get_by_capability("image_generation")`).

Build the prompt from:
- the script's hook, title or key claim;
- the scene_plan's most visually compelling hero moment;
- the video's established palette and style.

Request the aspect ratio of the detected format explicitly. Use the tool's aspect parameter if it has one, and say it in the prompt as well:

| Format | Prompt says | Tool size / aspect |
|---|---|---|
| horizontal | "16:9 landscape thumbnail, subject on the left, empty space on the right for text" | 1280×720 or larger 16:9 |
| vertical | "9:16 vertical thumbnail, subject centred in the middle 60% of the frame, empty space at the top for text, nothing important near the top or bottom edges" | 1080×1920 or larger 9:16 |
| square / 4:5 | "1:1" or "4:5" with the subject centred | 1080×1080 / 1080×1350 |

Generate the image **without text**, because generated lettering is often misspelled. Then add the headline, eyebrow and brand as an overlay that follows Steps 2–3. Use a minimal HTML page rendered with any headless browser, or ffmpeg `drawtext` with an Inter / JetBrains Mono font file. If the image comes back at another size, scale and centre-crop it to the canvas (see Method 3). Never stretch it.

---

#### Method 3 — FFmpeg Still Frame (last resort)

If no image generation tool is available, take the strongest frame from the video. The frame already has the video's orientation, so scale it to the Step 1 canvas without distorting it:

```bash
ffmpeg -y -v error -ss <best_timestamp> -i projects/<project-id>/renders/final.mp4 -frames:v 1 \
  -vf "scale=W:H:force_original_aspect_ratio=increase:flags=lanczos,crop=W:H,format=rgb24" \
  projects/<project-id>/renders/thumbnail.png
```

`W:H` is the canvas from Step 1: `1280:720` for horizontal or `1080:1920` for vertical.

Pick `<best_timestamp>` from the scene_plan's hero scene, the moment with the strongest visual. Never use the first frame, which is usually a black or title card. If a font file is available, add the headline with `drawtext` and keep it inside the safe box. A frame with no text is acceptable only as a last resort; log it in `metadata.post_production.thumbnail.notes`.

---

### Step 5 — QA (mandatory, every method)

**Hard checks.** Fix and re-export until all of them pass:

```bash
cd projects/<project-id>/renders
ffprobe -v error -show_entries stream=width,height,pix_fmt -of csv=p=0 thumbnail.png
ls -l thumbnail.png
```

- `width,height` equals the Step 1 canvas.
- `pix_fmt` is `rgb24` (8-bit RGB with no alpha). If it is `rgba`, re-export with `-vf format=rgb24`.
- The file is under 2 MB.

**Look at it small.** Write previews to a temporary folder, not `renders/`, and open each one:

```bash
# horizontal: YouTube sidebar size
ffmpeg -y -v error -i thumbnail.png -vf scale=168:94 <tmp>/small.png
# vertical: shelf tile size, plus the 3:4 grid crop and the 4:5 feed crop
ffmpeg -y -v error -i thumbnail.png -vf scale=120:213 <tmp>/small.png
ffmpeg -y -v error -i thumbnail.png -vf crop=1080:1440:0:240 <tmp>/crop_3x4.png
ffmpeg -y -v error -i thumbnail.png -vf crop=1080:1350:0:285 <tmp>/crop_4x5.png
```

Confirm that the headline reads at the small size, that no crop cuts anything essential, and that nothing important sits in a keep-clear zone (Step 2).

If the PNG is over 2 MB (busy generated art), keep it as the master. Also write `thumbnail.jpg` with `ffmpeg -i thumbnail.png -q:v 2 thumbnail.jpg`, check that it is under 2 MB, and name it as the upload file in `publish.txt`.

Log the result in `metadata.post_production.thumbnail`: the method, format, canvas, file size, QA result and any notes.

In `publish.txt`, the THUMBNAIL section names the file with its real size and orientation, e.g. `thumbnail.png (1080x1920, vertical 9:16)`. For vertical videos, add a line saying that YouTube Shorts custom thumbnails are uploaded from YouTube Studio on desktop.

---

### Shared Task Rules

- Both tasks are mandatory. Never skip either because the compose stage passed.
- Both outputs go in `renders/` — not the project root, not `assets/`.
- If Method 1 fails for the thumbnail, fall back to Method 2, then Method 3. Never leave `thumbnail.png` missing, and never deliver one whose orientation differs from the video's.
- Log both as the final entries in the compose checkpoint metadata (`metadata.post_production`).
