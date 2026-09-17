from pathlib import Path
import shutil
import tempfile
from fastapi import FastAPI, UploadFile, File, HTTPException
from transcribe import transcribe_audio, SUPPORTED_FORMATS

app = FastAPI(title="Transcription API")


@app.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    suffix = Path(file.filename or "").suffix.lower()

    if suffix not in SUPPORTED_FORMATS:
        raise HTTPException(status_code=400, detail="Unsupported audio format.")

    with tempfile.TemporaryDirectory() as temp_dir:
        input_path = Path(temp_dir) / f"input{suffix}"

        with open(input_path, "wb") as output:
            shutil.copyfileobj(file.file, output)

        return transcribe_audio(str(input_path))
