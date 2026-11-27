# MailMind AI

> An open-source, AI-powered email workspace that helps you manage, understand, search, and act on your emails intelligently.

## Features

- **AI Email Summarization** — Instant summaries of emails and long threads
- **Smart Categorization** — Automatic classification (Work, Personal, Academic, Finance, etc.)
- **Priority Detection** — AI identifies Critical, High, Medium, Low priority emails
- **Action Item Extraction** — Automatically surfaces tasks, deadlines, and follow-ups
- **Semantic Search** — Find emails by meaning, not just keywords
- **AI Conversational Assistant** — Ask questions about your emails in natural language (RAG-powered)
- **Reply Suggestions** — AI-generated reply drafts in your preferred tone
- **Daily Digest** — Summary of your email activity each morning

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Next.js 15, TypeScript, Tailwind CSS, shadcn/ui |
| Backend | FastAPI, Python 3.12, SQLAlchemy 2 |
| Database | PostgreSQL 16 + pgvector |
| Cache / Queue | Redis 7 + Celery |
| AI Providers | Gemini (primary), OpenRouter, Groq |
| Desktop | Tauri 2 *(planned)* |
| Containerization | Docker + Docker Compose |

## Quick Start

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) and Docker Compose
- Google Cloud project with Gmail API enabled (for Gmail integration)
- Gemini API key (or OpenRouter / Groq API key)

### Setup

```bash
git clone https://github.com/FawwazWiyoga/MAIL-MIND.git
cd MAIL-MIND

# Copy and configure environment variables
cp .env.example .env
# Edit .env with your API keys and secrets

# Start all services
docker compose up -d

# Run database migrations
docker compose exec api alembic upgrade head

# Open the app
# Web: http://localhost:3000
# API docs: http://localhost:8000/docs
```

## Project Structure

```
MAIL-MIND/
├── frontend/           # Next.js web application
│   ├── src/
│   │   ├── app/        # Next.js App Router pages
│   │   ├── components/ # React components
│   │   ├── hooks/      # Custom React hooks
│   │   ├── lib/        # Utilities and API client
│   │   ├── store/      # Zustand state stores
│   │   └── types/      # TypeScript type definitions
│   └── Dockerfile
├── backend/            # FastAPI Python backend
│   ├── app/
│   │   ├── api/        # API route handlers
│   │   ├── core/       # Config, security, database
│   │   ├── models/     # SQLAlchemy ORM models
│   │   ├── schemas/    # Pydantic request/response schemas
│   │   └── workers/    # Celery background tasks
│   ├── migrations/     # Alembic database migrations
│   ├── tests/          # Pytest test suite
│   └── Dockerfile
├── docker-compose.yml
├── .env.example
├── Makefile
└── prd.md              # Product Requirements Document
```

## Development

### Common Commands

```bash
make up         # Start all Docker services
make down       # Stop all services
make logs       # Tail logs
make migrate    # Run database migrations
make test-api   # Run backend tests
make shell-api  # Open shell in API container
make shell-db   # Open PostgreSQL shell
```

### Local Development (without Docker)

**Backend:**
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
uvicorn app.main:app --reload --port 8000
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/my-feature`)
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## License

MIT License — see [LICENSE](LICENSE) for details.

## Privacy Notice

MailMind AI processes your email content to provide AI features. When cloud AI providers are enabled, email content may be sent to those providers. You control this via Settings > AI Privacy.
