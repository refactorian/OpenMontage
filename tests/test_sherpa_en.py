"""Verification test for the offline sherpa-onnx Kokoro English TTS tool.

Run:
    .venv/bin/python -m pytest tests/test_sherpa_en.py -v -s

Synthesizes the same sentence with five top English male voices, writes the
WAV files to ``outputs/test_voices/``, and validates sample rate, duration,
and file integrity.
"""

from __future__ import annotations

from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = PROJECT_ROOT / "outputs" / "test_voices"
MODEL_DIR = PROJECT_ROOT / "models" / "sherpa_onnx" / "kokoro-multi-lang-v1_0"

TEST_TEXT = (
    "Welcome to our coding channel. "
    "Today we are building an automated video pipeline."
)

# voice name -> expected Kokoro speaker ID
TEST_VOICES = {
    "am_michael": 16,
    "am_fenrir": 14,
    "am_onyx": 17,
    "am_adam": 11,
    "bm_george": 26,
}


def _require_runtime() -> None:
    pytest.importorskip("sherpa_onnx")
    pytest.importorskip("soundfile")
    if not (MODEL_DIR / "model.onnx").is_file():
        pytest.skip(
            "Kokoro v1.0 model not downloaded; run "
            "`python scripts/setup_sherpa_en.py` first."
        )


def test_five_english_male_voices() -> None:
    _require_runtime()

    import soundfile as sf

    from tools.audio.sherpa_tts import VOICE_PRESETS, SherpaTTS

    # Guard the documented mapping against accidental drift.
    for voice, expected_sid in TEST_VOICES.items():
        assert VOICE_PRESETS[voice][0] == expected_sid

    tool = SherpaTTS()
    assert tool.get_status().value == "available"

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    rows: list[tuple[str, int, Path, float]] = []
    for voice, expected_sid in TEST_VOICES.items():
        output_path = OUTPUT_DIR / f"{voice}.wav"
        result = tool.execute(
            {
                "text": TEST_TEXT,
                "voice": voice,
                "speed": 1.0,
                "output_path": str(output_path),
            }
        )

        assert result.success, f"{voice} failed: {result.error}"
        assert result.data["voice"] == voice
        assert result.data["speaker_id"] == expected_sid
        assert result.data["sample_rate"] == 24000
        assert result.artifacts == [str(output_path)]

        assert output_path.is_file(), f"missing output: {output_path}"
        assert output_path.stat().st_size > 0, f"empty output: {output_path}"

        info = sf.info(str(output_path))
        assert info.samplerate == 24000
        assert info.duration > 2.0, (
            f"{voice} duration {info.duration:.2f}s is not > 2.0s"
        )

        rows.append((voice, expected_sid, output_path, info.duration))

    # Clean summary table.
    print()
    print(f"{'Voice':<12} {'SID':>4}  {'Duration':>9}  File")
    print("-" * 78)
    for voice, sid, path, duration in rows:
        try:
            shown_path = path.relative_to(PROJECT_ROOT)
        except ValueError:
            shown_path = path
        print(f"{voice:<12} {sid:>4}  {duration:>8.2f}s  {shown_path}")
    print("-" * 78)
    print(f"{len(rows)} voices synthesized successfully.")
