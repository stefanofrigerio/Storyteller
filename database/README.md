# Database

PostgreSQL schema and data management for the Storyteller application.

## Overview

This module provides the complete database layer including:
- SQLAlchemy ORM models
- Database connection management
- Alembic migrations
- Seed data for development/testing
- Initialization scripts

## Tech Stack

- **PostgreSQL 14+**: Primary database
- **SQLAlchemy 2.0+**: ORM with modern typed API
- **Alembic**: Database migration management
- **Python 3.9+**: Runtime environment

## Installation

### Prerequisites

1. PostgreSQL server running (14+ recommended)
2. Python 3.9+ with required packages

### Install Dependencies

```bash
# From project root
poetry install

# Or with pip
pip install sqlalchemy psycopg2-binary alembic python-dotenv
```

### Environment Configuration

Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/storyteller
```

Or export as environment variable:

```bash
export DATABASE_URL="postgresql://username:password@localhost:5432/storyteller"
```

## Database Schema

### Users Table

Stores user accounts and profile information.

**Fields:**
- `id` (Integer, PK): Unique user identifier
- `email` (String, Unique): User email address
- `password_hash` (String): Hashed password
- `name` (String, Optional): User's display name
- `age` (Integer, Optional): User's age
- `bio` (Text, Optional): User biography
- `language` (String): Preferred language (default: "en")
- `is_active` (Boolean): Account active status
- `is_verified` (Boolean): Email verification status
- `created_at` (DateTime): Account creation timestamp
- `updated_at` (DateTime): Last update timestamp
- `last_login` (DateTime, Optional): Last login timestamp

**Relationships:**
- One-to-Many with Locations
- One-to-Many with Stories
- One-to-One with UserPreference

### UserPreference Table

Stores user preferences for content personalization.

**Fields:**
- `id` (Integer, PK): Unique preference identifier
- `user_id` (Integer, FK): Reference to Users
- `interest_tags` (JSON): Array of interest tags (e.g., ["history", "art"])
- `preferred_content_types` (JSON): Preferred story types
- `story_length` (String): Preferred story length (short/medium/long)
- `verbosity_level` (Integer): Content detail level (1-10)
- `notifications_enabled` (Boolean): Push notification setting
- `distance_threshold` (Float): Distance in meters to trigger new content
- `created_at` (DateTime): Creation timestamp
- `updated_at` (DateTime): Last update timestamp

### Location Table

Tracks user location history during walks.

**Fields:**
- `id` (Integer, PK): Unique location identifier
- `user_id` (Integer, FK): Reference to Users
- `latitude` (Float): GPS latitude coordinate
- `longitude` (Float): GPS longitude coordinate
- `altitude` (Float, Optional): Altitude in meters
- `accuracy` (Float, Optional): GPS accuracy in meters
- `speed` (Float, Optional): Movement speed in m/s
- `heading` (Float, Optional): Direction in degrees
- `address` (String, Optional): Cached reverse geocoded address
- `city` (String, Optional): City name
- `country` (String, Optional): Country name
- `timestamp` (DateTime): Location capture time

**Indexes:**
- `idx_location_coords`: (latitude, longitude) for spatial queries
- `idx_location_user_time`: (user_id, timestamp) for user history

### POI (Points of Interest) Table

Stores notable locations, landmarks, and places.

**Fields:**
- `id` (Integer, PK): Unique POI identifier
- `name` (String): POI name
- `poi_type` (String): Type (restaurant, museum, monument, etc.)
- `latitude` (Float): GPS latitude
- `longitude` (Float): GPS longitude
- `description` (Text, Optional): POI description
- `historical_context` (Text, Optional): Historical information
- `fun_facts` (Text, Optional): Interesting facts
- `source` (Enum): Data source (OSM/GOOGLE/MANUAL/GENERATED)
- `external_id` (String, Optional): External API identifier
- `metadata` (JSON, Optional): Additional flexible data
- `created_at` (DateTime): Creation timestamp
- `updated_at` (DateTime): Last update timestamp

**Indexes:**
- `idx_poi_coords`: (latitude, longitude) for spatial queries
- `idx_poi_type`: (poi_type) for filtering by type
- Unique constraint on (source, external_id)

### Story Table

Stores AI-generated content for locations.

**Fields:**
- `id` (Integer, PK): Unique story identifier
- `user_id` (Integer, FK): Reference to Users
- `location_id` (Integer, FK, Optional): Associated location
- `poi_id` (Integer, FK, Optional): Associated POI
- `title` (String, Optional): Story title
- `content` (Text): Story content
- `content_type` (Enum): Type (HISTORICAL/CULTURAL/FUNNY/RECOMMENDATION/NARRATIVE/ARCHITECTURAL)
- `prompt_used` (Text, Optional): AI prompt used
- `model_version` (String, Optional): AI model identifier
- `tokens_used` (Integer, Optional): Token count
- `generation_time` (Float, Optional): Generation time in seconds
- `is_favorite` (Boolean): User favorite flag
- `is_read` (Boolean): Read status
- `read_at` (DateTime, Optional): Read timestamp
- `user_rating` (Integer, Optional): User rating (1-5)
- `is_cached` (Boolean): Cache status
- `cache_expires_at` (DateTime, Optional): Cache expiration
- `generated_at` (DateTime): Generation timestamp
- `updated_at` (DateTime): Last update timestamp

**Indexes:**
- `idx_story_user_generated`: (user_id, generated_at) for user history
- `idx_story_type`: (content_type) for filtering
- `idx_story_favorite`: (user_id, is_favorite) for favorites

## Usage

### Initialize Database

Create all tables and optionally load seed data:

```bash
cd database

# Create tables only
python init_db.py

# Create tables and load seed data
python init_db.py --seed

# Drop existing tables, recreate, and seed
python init_db.py --drop --seed

# Test connection only
python init_db.py --test-only
```

### Use in Application Code

```python
from database.database import SessionLocal, get_db
from database.models import User, Location, Story

# Direct session usage
db = SessionLocal()
try:
    user = db.query(User).filter(User.email == "alice@example.com").first()
    print(f"Found user: {user.name}")
finally:
    db.close()

# With FastAPI dependency injection
from fastapi import Depends
from sqlalchemy.orm import Session

@app.get("/users/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    return db.query(User).filter(User.id == user_id).first()
```

### Query Examples

```python
from sqlalchemy import and_, or_
from database.models import Location, POI, Story, ContentType

# Find nearby POIs (simple example, use PostGIS for production)
nearby_pois = db.query(POI).filter(
    and_(
        POI.latitude.between(41.89, 41.91),
        POI.longitude.between(12.48, 12.50)
    )
).all()

# Get user's favorite stories
favorites = db.query(Story).filter(
    and_(
        Story.user_id == user_id,
        Story.is_favorite == True
    )
).order_by(Story.generated_at.desc()).all()

# Get stories by type
historical_stories = db.query(Story).filter(
    Story.content_type == ContentType.HISTORICAL
).all()

# Get user's recent locations
recent_locations = db.query(Location).filter(
    Location.user_id == user_id
).order_by(Location.timestamp.desc()).limit(10).all()
```

## Migrations with Alembic

### Initial Setup (Already Done)

The Alembic environment is pre-configured. The initial migration is in `alembic/versions/001_initial_schema.py`.

### Apply Migrations

```bash
cd database

# Upgrade to latest version
alembic upgrade head

# Upgrade to specific version
alembic upgrade 001

# Downgrade one version
alembic downgrade -1

# Show current version
alembic current

# Show migration history
alembic history
```

### Create New Migrations

```bash
cd database

# Auto-generate migration from model changes
alembic revision --autogenerate -m "Add new column to users table"

# Create empty migration for manual changes
alembic revision -m "Add custom index"
```

### Migration Best Practices

1. **Review auto-generated migrations** - Always check the generated code
2. **Test migrations** - Test both upgrade and downgrade
3. **Use transactions** - Migrations run in transactions by default
4. **Data migrations** - Separate schema and data migrations
5. **Backup first** - Always backup production data before migrations

## Seed Data

The `seed_data.py` module provides sample data for development:

- 3 test users with different profiles
- User preferences for each user
- 7 locations tracking a walk through Rome
- 6 POIs (Colosseum, Trevi Fountain, Pantheon, etc.)
- 5 sample AI-generated stories

Load seed data:

```bash
python seed_data.py
```

Or use the init script:

```bash
python init_db.py --seed
```

## Database Utilities

### Test Connection

```python
from database.database import test_connection

if test_connection():
    print("Database is accessible")
else:
    print("Cannot connect to database")
```

### Drop All Tables (Dangerous!)

```python
from database.database import drop_db

# WARNING: This deletes all data
drop_db()
```

## Geospatial Queries

For production use with geospatial queries, consider adding PostGIS extension:

```sql
-- In PostgreSQL
CREATE EXTENSION postgis;
```

Then use GeoAlchemy2 for advanced spatial queries:

```python
from geoalchemy2 import Geometry
from sqlalchemy import func

# Find POIs within radius
nearby = db.query(POI).filter(
    func.ST_DWithin(
        func.ST_MakePoint(POI.longitude, POI.latitude),
        func.ST_MakePoint(user_lon, user_lat),
        radius_in_meters
    )
).all()
```

## Performance Optimization

### Indexes

The schema includes indexes on:
- User email (unique)
- Location coordinates (lat, lon)
- Location user + timestamp
- POI coordinates (lat, lon)
- POI type
- Story user + generated_at
- Story content_type
- Story user + is_favorite

### Query Optimization Tips

1. **Use indexes** - The schema has indexes for common queries
2. **Eager loading** - Use `joinedload()` for relationships
3. **Pagination** - Use `limit()` and `offset()` for large result sets
4. **Connection pooling** - Configured in `database.py`
5. **Query profiling** - Enable SQL logging for debugging

### Connection Pooling

Connection pool settings in `database.py`:
- Pool size: 5 connections
- Max overflow: 10 additional connections
- Pre-ping: Verify connection health before use

## Troubleshooting

### Connection Issues

```bash
# Test connection
python init_db.py --test-only

# Check PostgreSQL is running
psql -U postgres -l

# Verify DATABASE_URL
echo $DATABASE_URL
```

### Migration Issues

```bash
# Check current state
alembic current

# Show pending migrations
alembic history

# Reset to specific version
alembic downgrade <revision>
alembic upgrade <revision>
```

### Common Errors

**"relation does not exist"**
- Run `python init_db.py` or `alembic upgrade head`

**"password authentication failed"**
- Check DATABASE_URL credentials

**"database does not exist"**
- Create database: `createdb storyteller`

## File Structure

```
database/
├── __init__.py              # Package initialization
├── README.md                # This file
├── database.py              # Database connection & session management
├── models.py                # SQLAlchemy ORM models
├── init_db.py               # Database initialization script
├── seed_data.py             # Sample test data
├── alembic.ini              # Alembic configuration
└── alembic/
    ├── env.py               # Alembic environment
    ├── script.py.mako       # Migration template
    └── versions/
        └── 001_initial_schema.py  # Initial migration
```

## Development

### Adding New Models

1. Add model class to `models.py`
2. Import in `database.py` (ensure registration)
3. Generate migration: `alembic revision --autogenerate -m "Add model"`
4. Review and edit migration file
5. Apply migration: `alembic upgrade head`

### Updating Existing Models

1. Modify model in `models.py`
2. Generate migration: `alembic revision --autogenerate -m "Update model"`
3. Review migration (auto-generate may miss complex changes)
4. Apply migration: `alembic upgrade head`

## Production Considerations

### Security

- Use strong DATABASE_URL credentials
- Never commit `.env` files
- Use SSL connections for remote databases
- Implement proper password hashing (bcrypt)
- Sanitize user inputs

### Backup

```bash
# Backup database
pg_dump -U postgres storyteller > backup.sql

# Restore database
psql -U postgres storyteller < backup.sql
```

### Monitoring

- Enable SQL query logging for debugging
- Monitor connection pool usage
- Track slow queries
- Set up database monitoring (e.g., pgAdmin)

## Next Steps

1. Set up Alembic migrations: `alembic init alembic` (already done)
2. Create initial migration: `alembic revision --autogenerate -m "Initial"` (already done)
3. Initialize database: `python init_db.py --seed`
4. Build backend API using these models
5. Implement authentication endpoints
6. Add geolocation integration

## Contributing

When modifying the database schema:
1. Update models in `models.py`
2. Create migration with descriptive message
3. Update this README if adding new tables/relationships
4. Test migrations (upgrade and downgrade)
5. Update seed data if necessary

## License

MIT
