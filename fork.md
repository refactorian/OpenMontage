# Working on a personal fork of OpenMontage

This checkout is a fork: upstream is `calesthio/OpenMontage`, and all personal
work (offline Bangla/English TTS, word-level bilingual captions, local config)
lives in a single branch named `personal`.

```
origin    https://github.com/refactorian/OpenMontage.git   # your fork (push here)
upstream  https://github.com/calesthio/OpenMontage.git     # the project (read-only)
```

| Branch | Role | Tracking |
| --- | --- | --- |
| `main` | Clean mirror of upstream | `upstream/main` |
| `personal` | Your commits, always on top of `upstream/main` | `origin/personal` |

Never commit to `main`. It exists so `git rebase upstream/main` and
`git diff main personal` mean something, and so you can see exactly what is
yours.

## One-time setup (already done, for reference)

```bash
git remote rename origin upstream
git remote add origin https://github.com/refactorian/OpenMontage.git
git config pull.rebase true
git fetch upstream --prune
git switch -c personal
git push -u origin personal
```

## Daily loop

```bash
git fetch upstream --prune          # see what landed upstream
git log --oneline HEAD..upstream/main   # optional: what is new

git switch personal
git rebase upstream/main            # replay your commits on the latest upstream
git push --force-with-lease origin personal
```

`--force-with-lease` is required because rebasing rewrites your commit hashes;
it refuses to overwrite anything you have not seen, unlike `--force`.

To update `main` too (so `main` keeps mirroring upstream):

```bash
git switch main
git merge --ff-only upstream/main
git push origin main
```

Only fast-forwards are allowed there, so a slip cannot overwrite upstream's
history inside your fork.

## Conflict resolution

Rebase conflicts mean upstream touched the same lines as your personal commits.

```bash
git status                     # which files
# edit the files, keep both behaviours where possible
git add <resolved files>
git rebase --continue
```

- `git rebase --abort` returns to exactly where you started; nothing is lost.
- `git rebase --skip` drops the one commit being applied — only when upstream
  already implemented that change.
- Enable `git config rerere.enabled true` so git remembers conflict resolutions
  and applies them automatically on the next rebase.

Rule of thumb: keep personal commits small and focused (this branch has three:
TTS, captions, tests). A rebase over a 20-file squashed commit is a manual
merge; three small ones resolve in seconds.

## Backups

Even with a fork, a local snapshot is cheap insurance against a bad rebase or a
mistaken `reset --hard`.

```bash
# Single-file snapshot of every branch, tag and commit:
git bundle create ~/openmontage-personal-$(date +%F).bundle --all

# Verify the bundle before trusting it:
git bundle verify ~/openmontage-personal-$(date +%F).bundle

# Restore: clone the bundle, then re-point remotes
git clone ~/openmontage-personal-2026-11-08.bundle restored-openmontage
cd restored-openmontage && git remote set-url origin https://github.com/refactorian/OpenMontage.git
git remote add upstream https://github.com/calesthio/OpenMontage.git
```

`--all` includes `origin/personal`, so a bundle restores the pushed branch even
on a machine that has never seen the fork. Run it before a risky rebase, on a
schedule, or after a milestone.

Patch exports are a lighter alternative for a handful of commits:

```bash
git format-patch upstream/main..personal -o ~/openmontage-patches
# reapply elsewhere:
git am ~/openmontage-patches/*.patch
```

## What stays out of git

These are already ignored and must never be committed:

| Path | Why |
| --- | --- |
| `.env` | API keys and local voice/model choices |
| `models/` | ~500 MB sherpa-onnx weights, regenerable |
| `outputs/`, `output/`, `pipeline/` | Generated media |
| `.venv/` | Project virtualenv |
| `~/.cache/huggingface/` | Whisper weights (outside the repo) |

A fresh clone needs only:

```bash
uv venv --python 3.11 .venv
uv pip install --python .venv/bin/python -r requirements.txt
.venv/bin/python scripts/setup_audio_models.py      # sherpa-onnx models
cp .env.example .env                                # then fill in keys
```

Whisper weights download to the HuggingFace cache on first transcription, or
run with `WHISPER_LOCAL_FILES_ONLY=1` after one online run to stay offline.

## Re-verifying after an upstream pull

A rebase can silently change assumptions (renamed env vars, changed tool
schemas). After every non-trivial rebase:

```bash
.venv/bin/python tests/test_sherpa_whisper_bilingual.py
.venv/bin/python -m pytest -q tests/contracts tests/tools
```

The contract tests are the early warning: they assert the provider catalog and
tool schemas that new upstream code may have extended.

## Contributing a change upstream

Because `personal` is a rebased series of focused commits, any of them can be
proposed as a pull request without carrying your whole branch:

```bash
git switch -c sherpa-tts upstream/main
git cherry-pick <commit>            # or: git checkout -p, if only part belongs upstream
git push -u origin sherpa-tts
```

Open the PR from `refactorian/OpenMontage:sherpa-tts` into
`calesthio/OpenMontage:main`, then keep using `personal` locally. If the PR
merges, the next rebase drops that commit automatically.

## Troubleshooting

| Symptom | Cause and fix |
| --- | --- |
| `! [rejected] ... (stale info)` on `--force-with-lease` | Someone pushed to your fork; `git fetch origin`, then retry. |
| `! [rejected] ... (fetch first)` on `main` | You committed on `main`; move it: `git switch personal && git cherry-pick main && git switch main && git reset --hard upstream/main`. |
| `fatal: refusing to merge unrelated histories` | Cloned from a bundle without the upstream commits; fetch `upstream` first. |
| Rebase replays dozens of commits | Your branch was merged upstream squashed; `git rebase --skip` the now-duplicate ones or reset `personal` onto `upstream/main` and re-apply only what is missing. |
| Local changes block `git switch` | `git stash -u`, switch, then `git stash pop`; or `git config rebase.autoStash true`. |
| Upstream force-pushed its own history | Rare but possible on a busy project; `git fetch upstream` and rebase onto the new `upstream/main`. Your commits are unaffected. |
