# Transcription Pipeline

A small Python transcription service that accepts common audio files, normalizes them with FFmpeg, transcribes speech using Whisper, and returns text with segment timestamps.

## Design Decisions

I kept the solution simple because the goal is to demonstrate the pipeline rather than train a speech model from scratch.

### Speech-to-text

I used OpenAI Whisper because it is open-source, supports multiple languages, and provides segment-level timestamps.

### Audio formats

The service accepts WAV, MP3, M4A, and FLAC files. FFmpeg converts incoming audio to 16 kHz mono WAV before transcription so the speech-to-text stage receives a consistent format.

### Long audio

For very long files, I would process the recording in smaller chunks and add each chunk's start offset to the returned timestamps. This keeps memory usage predictable and makes retries easier.

### Concurrent uploads

In production, uploads would be handled asynchronously. The API would save the uploaded file, create a transcription job, and place it on a queue such as Redis/Celery. Multiple worker processes could then handle jobs independently.

### Storage

Audio files would be stored in object storage such as Amazon S3 or Google Cloud Storage. Transcript text, timestamps, job status, and file references would be stored in a database such as PostgreSQL.

### Failure handling

Each job would have a status such as `queued`, `processing`, `completed`, or `failed`. Failed jobs would be retried automatically a limited number of times with exponential backoff. Permanent failures would keep the error message for debugging.

### API design

A production API could expose:

- `POST /transcriptions` — upload audio and create a job
- `GET /transcriptions/{job_id}` — check job status
- `GET /transcriptions/{job_id}/result` — retrieve transcript and timestamps

For this assessment, `app.py` includes a simple synchronous `POST /transcribe` endpoint.

## Project Structure

```text
transcription-pipeline/
├── app.py
├── transcribe.py
├── requirements.txt
└── README.md
```

## Setup

Install FFmpeg first, then install the Python dependencies:

```bash
pip install -r requirements.txt
```

## Run as a script

```bash
python transcribe.py sample.mp3
```

## Run the API

```bash
uvicorn app:app --reload
```

Then send an audio file to:

```text
POST /transcribe
```

## Example Output

```json
{
  "text": "Hello and welcome.",
  "segments": [
    {
      "start": 0.0,
      "end": 2.8,
      "text": "Hello and welcome."
    }
  ]
}
```

## Production Improvements

For a larger production system I would add authentication, request size limits, background workers, object storage, a database, monitoring, automatic retries, and cleanup rules for old audio files.
