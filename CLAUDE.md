# Storyteller

A mobile app that tracks you when you walk and suggests things to do in your surroundings, or tells you historical or funny facts based on your profile.

## Project Structure

This project is organized into 5 main components:

### 1. Backend API (`/backend`)
REST API service built with Python/FastAPI for:
- User management and authentication
- Profile and preferences management
- Location tracking endpoints
- Suggestion/story retrieval

### 2. LLM Integration (`/llm`)
Claude API integration for generating:
- Personalized stories based on location and user profile
- Historical facts about nearby places
- Fun facts and recommendations
- Context-aware narratives

### 3. Database (`/database`)
PostgreSQL database schema and migrations for:
- User accounts and profiles
- Location history
- User preferences and interests
- Generated stories cache
- POI (Points of Interest) data

### 4. Geolocation Service (`/geolocation`)
Location intelligence service for:
- Reverse geocoding (coordinates to places)
- POI discovery (OpenStreetMap/Google Places integration)
- Proximity detection
- Area context (historical, cultural, commercial zones)

### 5. Text-to-Speech Service (`/tts`)
Audio narration service for hands-free storytelling:
- Convert stories to natural speech
- Multiple voice options and languages (Italian, English, etc.)
- Voice customization (speed, pitch)
- Audio caching for performance
- Streaming support for long stories
- Hands-free narration during walks

## Tech Stack

- **Python 3.9+**
- **Poetry** for dependency management
- **FastAPI** for REST API
- **PostgreSQL** for database
- **Claude API** for LLM
- **Google Cloud TTS** (or ElevenLabs/Azure/AWS) for audio narration
- **Virtual environment** (.venv)

## Setup

```bash
# Install dependencies
poetry install

# Activate virtual environment
source .venv/bin/activate

# Set up database
cd database && python init_db.py

# Run backend API
cd backend && uvicorn main:app --reload
```

## Development

This project is in early development. Each component is being developed independently:
- Backend API: RESTful endpoints
- LLM Integration: Story generation with Claude
- Database: Schema design and migrations (✅ **completed with Milano seed data**)
- Geolocation: POI and location services
- TTS: Audio narration for hands-free experience (✅ **base implementation ready**)

## Git Workflow

**IMPORTANT**: After every major change or milestone, always push to GitHub:

```bash
git push origin master
```

This ensures all work is backed up and visible on the remote repository.
