# Luna AI Voice Companion Platform

Luna is a production-grade AI voice companion platform featuring real-time conversational AI with voice and text, long-term memory, emotion awareness, multilingual support, and Twilio-based phone call handling.

## Features

- **Text Chat:** Real-time markdown streaming chat interface.
- **Voice Chat:** Low-latency WebRTC browser voice pipeline with barge-in support.
- **Phone Calls:** Twilio integration for inbound/outbound phone calls with live AI conversation.
- **Long-term Memory:** pgvector-based semantic memory to remember user preferences, goals, and facts.
- **Emotion Awareness:** Adapts her tone based on sentiment analysis of the user's input.
- **Multilingual:** Fluent in English, Urdu, and Telugu.
- **Personalities:** Configurable companion profiles and traits.

## Architecture

- **Backend:** Django 4.2, Django REST Framework, Django Channels (WebSockets)
- **Frontend:** React 18, Vite, TypeScript, Tailwind CSS, Framer Motion, Zustand
- **Database:** PostgreSQL (with pgvector for embeddings)
- **Cache/Broker:** Redis
- **Workers:** Celery (for async tasks like memory summarization)
- **AI Providers:** OpenAI (GPT-4o) & Google Gemini (1.5 Pro) abstracted behind a common interface.
- **TTS:** ElevenLabs (Streaming) & Google Cloud TTS.
- **STT:** OpenAI Whisper & Google Cloud STT.

## Prerequisites

- Docker and Docker Compose
- Node.js (v20+) - for local frontend development
- Python (3.11+) - for local backend development
- API Keys for OpenAI/Gemini and ElevenLabs/Google Cloud.

## Getting Started (Docker)

1. **Clone the repository.**
2. **Environment variables:**
   Copy `.env.example` to `.env` and fill in your keys (OpenAI, ElevenLabs, etc.).
   ```bash
   cp .env.example .env
   ```
3. **Start the platform:**
   ```bash
   docker-compose up --build -d
   ```
4. **Database Setup & Seed Data:**
   Run migrations and seed the database with the default Luna personality and a test user.
   ```bash
   docker-compose exec backend python manage.py makemigrations users authentication chat memory voice calls personality notifications
   docker-compose exec backend python manage.py migrate
   docker-compose exec backend python manage.py seed
   ```
5. **Access the application:**
   - Frontend UI: `http://localhost:5173` (if running locally via `npm run dev`) or `http://localhost` (via nginx).
   - API Docs (Swagger): `http://localhost:8000/api/docs/`
   - Django Admin: `http://localhost:8000/admin/`

*Test user credentials (if seeded):*
- Email: `test@luna.ai`
- Password: `test123`

## Development - Local Setup

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Or venv\Scripts\activate on Windows
pip install -r requirements.txt
python manage.py runserver
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## Running Tests

### Backend Unit Tests
```bash
docker-compose exec backend pytest
```

### Frontend Unit Tests
```bash
cd frontend
npm run test
```

## License
MIT License
