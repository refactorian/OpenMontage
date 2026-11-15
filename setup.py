from setuptools import setup, find_packages

setup(
    name="openmontage",
    version="0.1.0",
    description="AI-Orchestrated Video Production Platform",
    packages=find_packages(),
    python_requires=">=3.10",
    install_requires=[
        "pyyaml>=6.0",
        "pydantic>=2.0",
        "jsonschema>=4.20",
        "python-dotenv>=1.0",
        "Pillow>=10.0",
        "requests>=2.31",
        "certifi>=2026.10.19",
        "google-genai>=1.0.0",
        "openai>=2.44.0",
        "faster-whisper>=1.0.0",
        "mediapipe>=0.10.0",
        "opencv-python-headless>=4.8.0",
        "kokoro-onnx>=0.4.0",
        "sherpa-onnx>=1.13.0",
        "soundfile>=0.12.1",
    ],
)
