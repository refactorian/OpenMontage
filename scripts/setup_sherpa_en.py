#!/usr/bin/env python3
"""Download the sherpa-onnx Kokoro multi-lang v1.0 TTS model.

The archive contains the English (US/UK) voices used by ``sherpa_tts``:
full-precision ``model.onnx``, ``voices.bin``, ``tokens.txt``, the espeak-ng
data directory, pronunciation dictionaries, and the US/UK English lexicons.

Usage:
    python scripts/setup_sherpa_en.py
    python scripts/setup_sherpa_en.py --force   # re-download and re-extract

The model is extracted to:
    models/sherpa_onnx/kokoro-multi-lang-v1_0/
"""

from __future__ import annotations

import argparse
import shutil
import sys
import tarfile
import time
import urllib.request
from pathlib import Path

MODEL_URL = (
    "https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/"
    "kokoro-multi-lang-v1_0.tar.bz2"
)
MODEL_NAME = "kokoro-multi-lang-v1_0"
ARCHIVE_NAME = f"{MODEL_NAME}.tar.bz2"

PROJECT_ROOT = Path(__file__).resolve().parent.parent
MODELS_ROOT = PROJECT_ROOT / "models" / "sherpa_onnx"
MODEL_DIR = MODELS_ROOT / MODEL_NAME
ARCHIVE_PATH = MODELS_ROOT / ARCHIVE_NAME

REQUIRED_FILES = (
    "model.onnx",
    "voices.bin",
    "tokens.txt",
    "lexicon-us-en.txt",
    "lexicon-gb-en.txt",
)


def _model_is_ready() -> bool:
    return MODEL_DIR.is_dir() and all(
        (MODEL_DIR / name).is_file() for name in REQUIRED_FILES
    )


def _download(url: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    partial = dest.with_suffix(dest.suffix + ".part")

    request = urllib.request.Request(url, headers={"User-Agent": "OpenMontage/1.0"})
    with urllib.request.urlopen(request, timeout=120) as response:
        total = int(response.headers.get("Content-Length") or 0)
        print(
            f"Downloading {url}\n  -> {dest}"
            + (f" ({total / 1_000_000:.1f} MB)" if total else "")
        )
        start = time.time()
        downloaded = 0
        with open(partial, "wb") as handle:
            while True:
                chunk = response.read(1024 * 1024)
                if not chunk:
                    break
                handle.write(chunk)
                downloaded += len(chunk)
                if total:
                    pct = downloaded * 100 / total
                    print(
                        f"\r  {pct:5.1f}%  {downloaded / 1_000_000:7.1f}"
                        f" / {total / 1_000_000:.1f} MB",
                        end="",
                        flush=True,
                    )
    elapsed = max(time.time() - start, 0.001)
    print(f"\r  Downloaded {downloaded / 1_000_000:.1f} MB in {elapsed:.1f}s")

    if total and partial.stat().st_size != total:
        partial.unlink(missing_ok=True)
        raise RuntimeError(
            f"Incomplete download: expected {total} bytes, "
            f"got {partial.stat().st_size}"
        )
    partial.replace(dest)


def _extract(archive: Path, destination: Path) -> None:
    print(f"Extracting {archive.name} ...")
    destination.mkdir(parents=True, exist_ok=True)
    with tarfile.open(archive, "r:bz2") as tar:
        members = tar.getmembers()
        # Guard against path traversal in a downloaded archive.
        for member in members:
            target = (destination / member.name).resolve()
            if not str(target).startswith(str(destination.resolve()) + "/") and target != destination.resolve():
                raise RuntimeError(f"Unsafe archive member: {member.name}")
        tar.extractall(destination, members=members)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--force",
        action="store_true",
        help="Re-download and re-extract even if the model already exists.",
    )
    args = parser.parse_args()

    MODELS_ROOT.mkdir(parents=True, exist_ok=True)

    if _model_is_ready() and not args.force:
        print(f"Model already present: {MODEL_DIR}")
        return 0

    if args.force and MODEL_DIR.exists():
        shutil.rmtree(MODEL_DIR)

    if not ARCHIVE_PATH.is_file():
        _download(MODEL_URL, ARCHIVE_PATH)

    _extract(ARCHIVE_PATH, MODELS_ROOT)

    if not _model_is_ready():
        missing = [name for name in REQUIRED_FILES if not (MODEL_DIR / name).is_file()]
        print(
            f"ERROR: extraction finished but required files are missing: {missing}\n"
            f"Looked inside {MODEL_DIR}",
            file=sys.stderr,
        )
        return 1

    print(f"Model ready: {MODEL_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
