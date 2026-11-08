"""sherpa-onnx Kokoro v1.0 local text-to-speech provider tool.

Studio-quality, fully offline English narration using the full-precision
``kokoro-multi-lang-v1_0`` model. The tool exposes every English voice in the
model (US/UK male and female presets) and can also be addressed by numeric
speaker ID. Piper remains available as the lightweight offline fallback.

Model setup:
    python scripts/setup_sherpa_en.py

Environment variables:
    TTS_PROVIDER=sherpa_onnx     Prefer this provider in the TTS selector.
    SHERPA_EN_VOICE=am_santa     Default English voice preset.
    SHERPA_SPEED=1.0             Default speaking speed.
    SHERPA_MODEL_DIR=...         Optional override for the model directory.
"""

from __future__ import annotations

import os
import time
from pathlib import Path
from typing import Any

from tools.base_tool import (
    BaseTool,
    Determinism,
    ExecutionMode,
    ResourceProfile,
    RetryPolicy,
    ToolResult,
    ToolRuntime,
    ToolStability,
    ToolStatus,
    ToolTier,
)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_MODEL_DIR = PROJECT_ROOT / "models" / "sherpa_onnx" / "kokoro-multi-lang-v1_0"
MODEL_NAME = "kokoro-multi-lang-v1_0"
DEFAULT_VOICE = "am_santa"
DEFAULT_SPEED = 1.0

# (speaker_id, description) for every English voice in kokoro-multi-lang-v1_0.
# Speaker IDs 0-27 are English; 28-53 cover the other languages in the model.
VOICE_PRESETS: dict[str, tuple[int, str]] = {
    # US English female (af_*): 0-10
    "af_alloy": (0, "Balanced US female"),
    "af_aoede": (1, "Bright US female"),
    "af_bella": (2, "Warm US female"),
    "af_heart": (3, "Expressive US female"),
    "af_jessica": (4, "Conversational US female"),
    "af_kore": (5, "Clear US female"),
    "af_nicole": (6, "Soft US female"),
    "af_nova": (7, "Modern US female"),
    "af_river": (8, "Calm US female"),
    "af_sarah": (9, "Friendly US female"),
    "af_sky": (10, "Light US female"),
    # US English male (am_*): 11-19
    "am_adam": (11, "Deep US male"),
    "am_echo": (12, "Smooth US male"),
    "am_eric": (13, "Conversational US male"),
    "am_fenrir": (14, "Energetic / punchy US male"),
    "am_liam": (15, "Young US male"),
    "am_michael": (16, "Clear US narrator male"),
    "am_onyx": (17, "Rich / authoritative US male"),
    "am_puck": (18, "Upbeat / expressive US male"),
    "am_santa": (19, "Warm storyteller male"),
    # UK English female (bf_*): 20-23
    "bf_alice": (20, "Clear British female"),
    "bf_emma": (21, "Warm British female"),
    "bf_isabella": (22, "Refined British female"),
    "bf_lily": (23, "Light British female"),
    # UK English male (bm_*): 24-27
    "bm_daniel": (24, "Clear British male"),
    "bm_fable": (25, "Expressive British narrator male"),
    "bm_george": (26, "Classic British male"),
    "bm_lewis": (27, "Crisp British male"),
}

SID_TO_VOICE = {sid: name for name, (sid, _) in VOICE_PRESETS.items()}

REQUIRED_MODEL_FILES = (
    "model.onnx",
    "voices.bin",
    "tokens.txt",
)


class SherpaTTS(BaseTool):
    name = "sherpa_tts"
    version = "0.1.0"
    tier = ToolTier.VOICE
    capability = "tts"
    provider = "sherpa_onnx"
    stability = ToolStability.EXPERIMENTAL
    execution_mode = ExecutionMode.SYNC
    determinism = Determinism.DETERMINISTIC
    runtime = ToolRuntime.LOCAL

    dependencies = ["python:sherpa_onnx", "python:soundfile"]
    install_instructions = (
        "Install sherpa-onnx and download the Kokoro v1.0 model:\n"
        "  pip install sherpa-onnx soundfile\n"
        "  python scripts/setup_sherpa_en.py\n"
        "The model is extracted to "
        "models/sherpa_onnx/kokoro-multi-lang-v1_0/."
    )
    agent_skills = ["text-to-speech"]

    capabilities = [
        "text_to_speech",
        "offline_generation",
        "voice_selection",
    ]
    supports = {
        "voice_cloning": False,
        "multilingual": False,
        "offline": True,
        "native_audio": True,
        "named_voices": True,
        "speaker_ids": True,
        "speed_control": True,
    }
    best_for = [
        "studio-quality offline English narration",
        "privacy-sensitive local-only voiceovers",
        "multiple US and UK English male/female voice presets",
    ]
    not_good_for = [
        "voice clone matching",
        "non-English narration (this tool is configured for English)",
    ]
    fallback = "piper_tts"
    fallback_tools = ["piper_tts"]

    input_schema = {
        "type": "object",
        "required": ["text"],
        "properties": {
            "text": {"type": "string"},
            "voice": {
                "type": "string",
                "default": DEFAULT_VOICE,
                "description": (
                    "English voice preset, e.g. am_santa, am_michael, am_onyx, "
                    "af_heart. A numeric string is treated as a speaker ID."
                ),
                "enum": list(VOICE_PRESETS),
            },
            "voice_id": {
                "type": "string",
                "description": "Alias for voice (capability-level selectors pass this).",
            },
            "speaker_id": {
                "type": "integer",
                "minimum": 0,
                "maximum": 53,
                "description": "Numeric Kokoro speaker ID; overrides voice.",
            },
            "sid": {
                "type": "integer",
                "minimum": 0,
                "maximum": 53,
                "description": "Alias for speaker_id.",
            },
            "speed": {
                "type": "number",
                "default": DEFAULT_SPEED,
                "minimum": 0.1,
                "maximum": 4.0,
                "description": "Speaking speed. 1.0 is normal.",
            },
            "model_dir": {
                "type": "string",
                "description": "Optional override for the extracted Kokoro model directory.",
            },
            "output_path": {"type": "string"},
        },
    }

    resource_profile = ResourceProfile(
        cpu_cores=2, ram_mb=1024, vram_mb=0, disk_mb=400, network_required=False
    )
    retry_policy = RetryPolicy(max_retries=1, retryable_errors=[])
    idempotency_key_fields = [
        "text",
        "voice",
        "voice_id",
        "speaker_id",
        "sid",
        "speed",
        "model_dir",
    ]
    side_effects = ["writes audio file to output_path"]
    user_visible_verification = [
        "Listen to generated audio for intelligibility and voice identity"
    ]

    def __init__(self) -> None:
        self._tts_engine: Any = None
        self._tts_engine_dir: Path | None = None

    # ---- Model / dependency resolution -------------------------------------

    @staticmethod
    def _model_dir(inputs: dict[str, Any] | None = None) -> Path:
        override = (inputs or {}).get("model_dir") or os.environ.get(
            "SHERPA_MODEL_DIR", ""
        )
        return Path(override).expanduser() if override else DEFAULT_MODEL_DIR

    @staticmethod
    def _missing_model_files(model_dir: Path) -> list[str]:
        return [
            name
            for name in REQUIRED_MODEL_FILES
            if not (model_dir / name).is_file()
        ]

    def get_status(self) -> ToolStatus:
        if super().get_status() != ToolStatus.AVAILABLE:
            return ToolStatus.UNAVAILABLE
        if self._missing_model_files(self._model_dir()):
            return ToolStatus.UNAVAILABLE
        return ToolStatus.AVAILABLE

    def estimate_cost(self, inputs: dict[str, Any]) -> float:
        return 0.0

    def estimate_runtime(self, inputs: dict[str, Any]) -> float:
        return round(0.5 + len(inputs.get("text", "")) / 80.0, 2)

    # ---- Voice resolution --------------------------------------------------

    @staticmethod
    def _voice_from_sid(sid: int) -> str:
        return SID_TO_VOICE.get(sid, f"sid_{sid}")

    def _resolve_voice(self, inputs: dict[str, Any]) -> tuple[str, int]:
        """Return ``(voice_name, speaker_id)`` from explicit ID or preset name."""
        explicit_sid = inputs.get("speaker_id")
        if explicit_sid is None:
            explicit_sid = inputs.get("sid")
        voice = inputs.get("voice")
        if voice is None:
            voice = inputs.get("voice_id")

        if explicit_sid is None and isinstance(voice, int):
            explicit_sid = voice

        if explicit_sid is not None:
            try:
                sid = int(explicit_sid)
            except (TypeError, ValueError) as exc:
                raise ValueError(f"Invalid speaker_id: {explicit_sid!r}") from exc
            if sid < 0:
                raise ValueError("speaker_id must be zero or greater")
            return self._voice_from_sid(sid), sid

        name = str(
            voice or os.environ.get("SHERPA_EN_VOICE") or DEFAULT_VOICE
        ).strip()
        if name.isdigit():
            sid = int(name)
            return self._voice_from_sid(sid), sid

        key = name.lower()
        if key not in VOICE_PRESETS:
            valid = ", ".join(VOICE_PRESETS)
            raise ValueError(
                f"Unknown English voice {name!r}. Valid voices: {valid}"
            )
        return key, VOICE_PRESETS[key][0]

    @staticmethod
    def _resolve_speed(inputs: dict[str, Any]) -> float:
        raw = inputs.get("speed")
        if raw is None:
            raw = os.environ.get("SHERPA_SPEED", DEFAULT_SPEED)
        try:
            speed = float(raw)
        except (TypeError, ValueError) as exc:
            raise ValueError(f"Invalid speed: {raw!r}") from exc
        if speed <= 0:
            raise ValueError("speed must be greater than zero")
        return speed

    # ---- Engine ------------------------------------------------------------

    def _get_engine(self, model_dir: Path) -> Any:
        if self._tts_engine is not None and self._tts_engine_dir == model_dir:
            return self._tts_engine

        import sherpa_onnx

        model_config = sherpa_onnx.OfflineTtsKokoroModelConfig(
            model=str(model_dir / "model.onnx"),
            voices=str(model_dir / "voices.bin"),
            tokens=str(model_dir / "tokens.txt"),
            data_dir=str(model_dir / "espeak-ng-data"),
            dict_dir=str(model_dir / "dict"),
            # Comma-joined so both US and UK pronunciations are available.
            lexicon=",".join(
                [
                    str(model_dir / "lexicon-us-en.txt"),
                    str(model_dir / "lexicon-gb-en.txt"),
                ]
            ),
        )
        config = sherpa_onnx.OfflineTtsConfig(
            model=sherpa_onnx.OfflineTtsModelConfig(
                kokoro=model_config,
                num_threads=max(1, min(4, os.cpu_count() or 1)),
                provider="cpu",
            )
        )
        if not config.validate():
            raise RuntimeError(
                f"Invalid sherpa-onnx Kokoro configuration for {model_dir}"
            )

        self._tts_engine = sherpa_onnx.OfflineTts(config)
        self._tts_engine_dir = model_dir
        return self._tts_engine

    # ---- Execution ---------------------------------------------------------

    def execute(self, inputs: dict[str, Any]) -> ToolResult:
        if self.get_status() != ToolStatus.AVAILABLE:
            return ToolResult(
                success=False,
                error="sherpa-onnx TTS not available. " + self.install_instructions,
            )

        text = str(inputs.get("text") or "").strip()
        if not text:
            return ToolResult(success=False, error="text must be a non-empty string")

        start = time.time()
        try:
            result = self._generate(inputs, text)
        except Exception as exc:
            return ToolResult(
                success=False, error=f"sherpa-onnx TTS generation failed: {exc}"
            )

        result.duration_seconds = round(time.time() - start, 2)
        return result

    def _generate(self, inputs: dict[str, Any], text: str) -> ToolResult:
        import numpy as np
        import soundfile as sf

        model_dir = self._model_dir(inputs)
        missing = self._missing_model_files(model_dir)
        if missing:
            return ToolResult(
                success=False,
                error=(
                    f"Missing sherpa-onnx model files in {model_dir}: {missing}. "
                    + self.install_instructions
                ),
            )

        voice_name, sid = self._resolve_voice(inputs)
        speed = self._resolve_speed(inputs)

        output_path = Path(inputs.get("output_path", "tts_output.wav"))
        output_path.parent.mkdir(parents=True, exist_ok=True)

        engine = self._get_engine(model_dir)
        if sid >= engine.num_speakers:
            raise ValueError(
                f"speaker_id {sid} is out of range; "
                f"{engine.num_speakers} speakers are available"
            )

        audio = engine.generate(text, sid=sid, speed=speed)
        samples = np.asarray(audio.samples, dtype=np.float32)
        sample_rate = int(audio.sample_rate)
        if samples.size == 0:
            return ToolResult(
                success=False,
                error="sherpa-onnx returned empty audio for the supplied text",
            )

        sf.write(str(output_path), samples, sample_rate, subtype="PCM_16")
        if not output_path.exists() or output_path.stat().st_size == 0:
            return ToolResult(
                success=False,
                error=f"sherpa-onnx output file missing or empty: {output_path}",
            )

        duration = samples.size / sample_rate if sample_rate else 0.0
        return ToolResult(
            success=True,
            data={
                "provider": self.provider,
                "model": MODEL_NAME,
                "voice": voice_name,
                "speaker_id": sid,
                "speed": speed,
                "sample_rate": sample_rate,
                "duration_seconds": round(duration, 3),
                "text_length": len(text),
                "output": str(output_path),
                "format": "wav",
            },
            artifacts=[str(output_path)],
            model=MODEL_NAME,
        )
