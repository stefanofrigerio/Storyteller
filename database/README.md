# Database

PostgreSQL schema and data management.

## Responsibilities

- Database schema design
- Migrations management
- Seed data for testing
- Data models
- Query optimization

## Tech Stack

- PostgreSQL 14+
- SQLAlchemy ORM
- Alembic for migrations

## Schema

### Users
- id, email, password_hash, created_at
- profile (name, age, bio)
- preferences (interests, content_types)

### Locations
- id, user_id, latitude, longitude, timestamp
- accuracy, altitude, speed

### Stories
- id, location_id, content, type, generated_at
- user_id, is_favorite

### POI (Points of Interest)
- id, name, type, latitude, longitude
- description, historical_context
- source (osm, google, manual)

### User Preferences
- id, user_id, interest_tags
- preferred_story_types, language

## Migrations

```bash
cd database
alembic revision --autogenerate -m "Description"
alembic upgrade head
```

## Development

```bash
cd database
python init_db.py
```
