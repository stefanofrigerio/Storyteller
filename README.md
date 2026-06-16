# Storyteller

An intelligent mobile companion that brings your walks to life with personalized stories, historical facts, and local recommendations.

## Overview

Storyteller tracks your location as you walk and uses AI to generate engaging, context-aware content based on:
- Your current location and surroundings
- Your personal interests and profile
- Historical and cultural context of the area
- Nearby points of interest

## Features

- **Location-aware storytelling**: Get personalized stories about places as you walk by them
- **Historical insights**: Learn fascinating facts about the history of your surroundings
- **Smart recommendations**: Discover things to do based on your preferences and location
- **Profile-based content**: Stories and suggestions tailored to your interests
- **Offline support**: Cache stories for areas you frequently visit

## Architecture

The project is split into 4 main components:

```
storyteller/
├── backend/          # REST API (FastAPI)
├── llm/              # Claude API integration
├── database/         # PostgreSQL schema & migrations
└── geolocation/      # Location & POI services
```

### Components

1. **Backend API**: User management, authentication, and core API endpoints
2. **LLM Integration**: AI-powered story generation using Claude
3. **Database**: Data persistence for users, locations, and content
4. **Geolocation**: Maps integration and POI discovery

## Getting Started

### Prerequisites

- Python 3.9+
- Poetry
- PostgreSQL
- Claude API key

### Installation

```bash
# Clone the repository
git clone https://github.com/stefanofrigerio/Storyteller.git
cd Storyteller

# Install dependencies
poetry install

# Activate virtual environment
poetry shell
```

### Configuration

Create a `.env` file with:

```env
DATABASE_URL=postgresql://user:password@localhost/storyteller
CLAUDE_API_KEY=your_claude_api_key
GOOGLE_MAPS_API_KEY=your_google_maps_key  # Optional
```

### Running

```bash
# Set up database
cd database && python init_db.py

# Run the backend
cd ../backend && uvicorn main:app --reload --port 8000
```

## Development Status

🚧 **Early Development** - All components are actively being built.

## Tech Stack

- **Backend**: Python, FastAPI, Pydantic
- **AI**: Claude 4 API
- **Database**: PostgreSQL, SQLAlchemy
- **Geolocation**: OpenStreetMap, Google Places API
- **Deployment**: Docker, Docker Compose

## Contributing

This is a personal project in early stages. Contributions welcome once core functionality is established.

## License

MIT

## Author

Stefano Frigerio
