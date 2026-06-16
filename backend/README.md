# Backend API

REST API service for Storyteller mobile app.

## Responsibilities

- User authentication and session management
- User profile CRUD operations
- Location tracking endpoints
- Story/suggestion retrieval
- User preferences management
- API rate limiting and security

## Tech Stack

- FastAPI
- Pydantic for validation
- JWT for authentication
- SQLAlchemy ORM

## Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - User login
- `POST /auth/logout` - User logout
- `GET /auth/me` - Get current user

### Profile
- `GET /profile` - Get user profile
- `PUT /profile` - Update user profile
- `GET /profile/preferences` - Get user preferences
- `PUT /profile/preferences` - Update preferences

### Location
- `POST /location/track` - Track user location
- `GET /location/history` - Get location history
- `GET /location/nearby` - Get nearby POIs

### Stories
- `GET /stories` - Get stories for current location
- `GET /stories/{id}` - Get specific story
- `POST /stories/favorite` - Save favorite story

## Development

```bash
cd backend
uvicorn main:app --reload --port 8000
```
