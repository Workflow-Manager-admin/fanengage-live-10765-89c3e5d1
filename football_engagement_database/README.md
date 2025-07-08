# football_engagement_database

PostgreSQL database container for Football Engagement App.

## Usage

- Docker image based on `postgres:15-alpine`.
- Default credentials in `.env` (override as needed).
- Schema auto-initialized via `initdb/01_schema.sql`.

## Development

Run via Docker Compose from this directory:

    docker-compose up -d

Database exposed on port 5432. Schema and tables are set up on first launch.

## Schema Overview

- `users`: App users
- `matches`: YouTube football matches
- `questions`: Yes/no questions surfaced during matches
- `responses`: User answers to questions
- `analysis`: GPT-4o-mini generated analyses for audience answers

Change credentials as needed in `.env`.
