from pathlib import Path
import subprocess
import tempfile
import whisper

SUPPORTED_FORMATS = {".wav", ".mp3", ".m4a", ".flac"}
model = whisper.load_model("base")


def validate_audio(file_path: str) -> Path:
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError("Audio file not found.")

    if path.suffix.lower() not in SUPPORTED_FORMATS:
        raise ValueError(f"Unsupported format: {path.suffix}")

    return path


def normalize_audio(file_path: str, output_path: str) -> str:
    subprocess.run(
        [
            "ffmpeg", "-y",
            "-i", file_path,
            "-ar", "16000",
            "-ac", "1",
            output_path,
        ],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return output_path


def transcribe_audio(file_path: str):
    path = validate_audio(file_path)

    with tempfile.TemporaryDirectory() as temp_dir:
        normalized = str(Path(temp_dir) / "normalized.wav")
        normalize_audio(str(path), normalized)

        result = model.transcribe(normalized)

        return {
            "text": result["text"].strip(),
            "segments": [
                {
                    "start": segment["start"],
                    "end": segment["end"],
                    "text": segment["text"].strip(),
                }
                for segment in result["segments"]
            ],
        }


if __name__ == "__main__":
    import sys
    import json

    if len(sys.argv) != 2:
        print("Usage: python transcribe.py <audio_file>")
        raise SystemExit(1)

    print(json.dumps(transcribe_audio(sys.argv[1]), indent=2))
