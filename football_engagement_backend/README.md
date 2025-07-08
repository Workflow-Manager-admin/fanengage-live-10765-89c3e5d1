# football_engagement_backend

Backend for Football Engagement App: Extracts YouTube audio, transcribes with Whisper, generates questions/analysis via GPT-4o-mini, interfaces with PostgreSQL, and serves REST API for frontend.

## Features

- Ingest live or recorded YouTube football commentary audio
- Transcribe to text (OpenAI Whisper)
- Generate engaging yes/no questions (OpenAI GPT-4o-mini)
- Store matches, questions, responses in PostgreSQL
- Analyze and summarize aggregated responses
- REST APIs, OpenAPI docs at `/docs`

## Setup

```bash
cd football_engagement_backend
cp .env.example .env   # Update OPENAI_API_KEY!
docker build -t football_engagement_backend:latest .
docker run --env-file .env --network="host" -p 5000:5000 football_engagement_backend:latest
```

## Environment

- Requires running `football_engagement_database` PostgreSQL container
- Needs OpenAI API Key for GPT-4o-mini and Whisper (for question/analysis generation)

## API Endpoints

All endpoints prefixed `/api/`.

- `POST /api/ingest`  
  `{ "youtube_url": "<url>" }`
  - Ingests new match, extracts and transcribes audio, generates and stores questions.

- `GET /api/matches/<match_id>/questions`
  - Fetch yes/no questions for a match.

- `POST /api/questions/<question_id>/answer`  
  `{ "username": "...", "answer": true/false }`
  - Record answer to a question for a user.

- `GET /api/questions/<question_id>/analytics`
  - Get yes/no counts and GPT-powered analysis.

## Health Check

- `GET /`  
  Returns: `{ message: "Healthy" }`

## Adding Secrets

Set up `.env` with API keys and DB URL.

## Development

- To run locally: `FLASK_APP=run.py flask run`
- All major logic (audio extraction, transcription, question/analysis) is in `/app/utils` and `/app/routes`.

## License

MIT
