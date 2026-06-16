# Database Schema Documentation

Visual representation of the Storyteller database schema.

## Entity Relationship Diagram

```
┌─────────────────────────────────────────┐
│              USERS                      │
├─────────────────────────────────────────┤
│ PK │ id               INTEGER           │
│    │ email            VARCHAR(255) [UQ] │
│    │ password_hash    VARCHAR(255)      │
│    │ name             VARCHAR(255)      │
│    │ age              INTEGER            │
│    │ bio              TEXT               │
│    │ language         VARCHAR(10)        │
│    │ is_active        BOOLEAN            │
│    │ is_verified      BOOLEAN            │
│    │ created_at       TIMESTAMP          │
│    │ updated_at       TIMESTAMP          │
│    │ last_login       TIMESTAMP          │
└─────────────────────────────────────────┘
         │
         │ 1:1
         ├──────────────────────────────────────┐
         │                                      │
         │                                      ▼
         │                        ┌─────────────────────────────────┐
         │                        │      USER_PREFERENCES           │
         │                        ├─────────────────────────────────┤
         │                        │ PK │ id                INTEGER │
         │                        │ FK │ user_id           INTEGER │
         │                        │    │ interest_tags     JSON    │
         │                        │    │ preferred_types   JSON    │
         │                        │    │ story_length      VARCHAR │
         │                        │    │ verbosity_level   INTEGER │
         │                        │    │ notifications     BOOLEAN │
         │                        │    │ distance_threshold FLOAT  │
         │                        │    │ created_at        TIMESTAMP│
         │                        │    │ updated_at        TIMESTAMP│
         │                        └─────────────────────────────────┘
         │
         │ 1:N
         ├──────────────────────────────────────┐
         │                                      │
         ▼                                      ▼
┌─────────────────────────────┐    ┌──────────────────────────────────┐
│        LOCATIONS            │    │            STORIES               │
├─────────────────────────────┤    ├──────────────────────────────────┤
│ PK │ id        INTEGER     │    │ PK │ id             INTEGER      │
│ FK │ user_id   INTEGER     │    │ FK │ user_id        INTEGER      │
│    │ latitude  FLOAT       │    │ FK │ location_id    INTEGER [N]  │
│    │ longitude FLOAT       │    │ FK │ poi_id         INTEGER [N]  │
│    │ altitude  FLOAT       │    │    │ title          VARCHAR(500) │
│    │ accuracy  FLOAT       │    │    │ content        TEXT         │
│    │ speed     FLOAT       │    │    │ content_type   ENUM         │
│    │ heading   FLOAT       │    │    │ prompt_used    TEXT         │
│    │ address   VARCHAR(500)│    │    │ model_version  VARCHAR(100) │
│    │ city      VARCHAR(255)│    │    │ tokens_used    INTEGER      │
│    │ country   VARCHAR(255)│    │    │ generation_time FLOAT       │
│    │ timestamp TIMESTAMP   │    │    │ is_favorite    BOOLEAN      │
└─────────────────────────────┘    │    │ is_read        BOOLEAN      │
         │                         │    │ read_at        TIMESTAMP    │
         │ 1:N                     │    │ user_rating    INTEGER      │
         │                         │    │ is_cached      BOOLEAN      │
         └────────────────────────>│    │ cache_expires  TIMESTAMP    │
                                   │    │ generated_at   TIMESTAMP    │
                                   │    │ updated_at     TIMESTAMP    │
                                   └──────────────────────────────────┘
                                            │
                                            │ N:1
                                            ▼
                                   ┌──────────────────────────────────┐
                                   │            POIS                  │
                                   ├──────────────────────────────────┤
                                   │ PK │ id               INTEGER   │
                                   │    │ name             VARCHAR   │
                                   │    │ poi_type         VARCHAR   │
                                   │    │ latitude         FLOAT     │
                                   │    │ longitude        FLOAT     │
                                   │    │ description      TEXT      │
                                   │    │ historical_ctx   TEXT      │
                                   │    │ fun_facts        TEXT      │
                                   │    │ source           ENUM      │
                                   │    │ external_id      VARCHAR   │
                                   │    │ metadata         JSON      │
                                   │    │ created_at       TIMESTAMP │
                                   │    │ updated_at       TIMESTAMP │
                                   └──────────────────────────────────┘
```

## Relationships

### User → UserPreference (1:1)
- Each user has one preference record
- Preferences are deleted when user is deleted (cascade)

### User → Location (1:N)
- Each user can have many location records
- Locations are deleted when user is deleted (cascade)

### User → Story (1:N)
- Each user can have many stories
- Stories are deleted when user is deleted (cascade)

### Location → Story (1:N)
- Each location can be associated with multiple stories
- Stories can exist without a location (location_id nullable)

### POI → Story (1:N)
- Each POI can be associated with multiple stories
- Stories can exist without a POI (poi_id nullable)

## Indexes

### Users Table
- `ix_users_id`: Primary key index
- `ix_users_email`: Unique index on email

### Locations Table
- `ix_locations_id`: Primary key index
- `ix_locations_timestamp`: Index on timestamp for time-based queries
- `idx_location_coords`: Composite index on (latitude, longitude) for geospatial queries
- `idx_location_user_time`: Composite index on (user_id, timestamp) for user history

### POIs Table
- `ix_pois_id`: Primary key index
- `idx_poi_coords`: Composite index on (latitude, longitude) for geospatial queries
- `idx_poi_type`: Index on poi_type for filtering
- `uq_poi_source_external_id`: Unique constraint on (source, external_id)

### Stories Table
- `ix_stories_id`: Primary key index
- `ix_stories_generated_at`: Index on generated_at for chronological queries
- `idx_story_user_generated`: Composite index on (user_id, generated_at) for user timeline
- `idx_story_type`: Index on content_type for filtering
- `idx_story_favorite`: Composite index on (user_id, is_favorite) for favorites

### UserPreferences Table
- `ix_user_preferences_id`: Primary key index
- Unique constraint on user_id

## Enums

### ContentType
Values for `stories.content_type`:
- `HISTORICAL`: Historical facts and context
- `CULTURAL`: Cultural information and traditions
- `FUNNY`: Humorous facts and stories
- `RECOMMENDATION`: Suggestions for places/activities
- `NARRATIVE`: Story-form content
- `ARCHITECTURAL`: Architecture and design information

### POISource
Values for `pois.source`:
- `OSM`: OpenStreetMap data
- `GOOGLE`: Google Places API data
- `MANUAL`: Manually entered data
- `GENERATED`: AI-generated POIs

## JSON Fields

### user_preferences.interest_tags
Array of interest strings:
```json
["history", "architecture", "food", "art", "music"]
```

### user_preferences.preferred_content_types
Array of preferred content types:
```json
["historical", "cultural", "recommendation"]
```

### pois.metadata
Flexible JSON object for additional POI data:
```json
{
  "opening_hours": "09:00-19:00",
  "website": "https://example.com",
  "phone": "+39 06 1234567",
  "rating": 4.6,
  "unesco_site": true,
  "year_built": 1762
}
```

## Constraints

### NOT NULL Constraints
- All primary keys
- All foreign keys
- User email and password_hash
- Location latitude, longitude, user_id, timestamp
- POI name, poi_type, latitude, longitude
- Story user_id, content, content_type

### UNIQUE Constraints
- User email
- UserPreference user_id
- POI (source, external_id) combination

### DEFAULT Values
- User language: "en"
- User is_active: true
- User is_verified: false
- UserPreference story_length: "medium"
- UserPreference verbosity_level: 5
- UserPreference notifications_enabled: true
- UserPreference distance_threshold: 50.0
- POI source: "MANUAL"
- Story is_favorite: false
- Story is_read: false
- Story is_cached: false

### TIMESTAMP Defaults
- created_at: Current timestamp (server default)
- updated_at: Current timestamp, auto-update on change
- generated_at: Current timestamp (for stories)

## Data Types

### Geospatial
- `latitude`: Float (-90 to 90)
- `longitude`: Float (-180 to 180)
- `altitude`: Float (meters)
- `accuracy`: Float (meters)

### Text Fields
- VARCHAR(10): Language codes
- VARCHAR(100): Model versions, POI types
- VARCHAR(255): Email, names, cities
- VARCHAR(500): Addresses, titles
- TEXT: Long-form content (bio, description, stories)

### Numeric
- INTEGER: IDs, ages, ratings (1-5), token counts
- FLOAT: Coordinates, distances, generation time
- BOOLEAN: Flags (is_active, is_favorite, etc.)

### Temporal
- TIMESTAMP WITH TIMEZONE: All datetime fields

## Storage Estimates

Approximate storage per record:

- **User**: ~500 bytes
- **UserPreference**: ~300 bytes
- **Location**: ~200 bytes
- **POI**: ~1-2 KB (depending on metadata)
- **Story**: ~2-5 KB (depending on content length)

For 1000 users with average usage:
- Users + Preferences: ~0.8 MB
- Locations (100/user): ~20 MB
- Stories (50/user): ~150 MB
- POIs: ~2 MB (shared data)

Total: ~173 MB for 1000 active users

## Query Performance

### Fast Queries (Using Indexes)
- Find user by email
- Get user's recent locations
- Get user's stories ordered by date
- Find user's favorite stories
- Filter stories by content type
- Geospatial POI lookups (with coordinate indexes)

### Potentially Slow Queries
- Full-text search in story content (without text search index)
- Complex geospatial calculations (without PostGIS)
- Aggregations across all users

### Optimization Recommendations
1. Add PostGIS extension for accurate geospatial queries
2. Add full-text search indexes for content search
3. Consider partitioning locations table by time (if very large)
4. Monitor and add indexes based on query patterns
5. Use connection pooling (already configured)

## Migrations

See `alembic/versions/` for migration history:
- `001_initial_schema.py`: Initial database schema

To create new migrations:
```bash
alembic revision --autogenerate -m "Description of change"
```

## Security Considerations

1. **Password Storage**: Always store hashed passwords (bcrypt recommended)
2. **API Keys**: Never store API keys in database (use environment variables)
3. **SQL Injection**: SQLAlchemy ORM provides protection, but validate all inputs
4. **Personal Data**: Users table contains PII - ensure GDPR compliance
5. **Access Control**: Implement row-level security if needed

## Backup Strategy

### Recommended Backup Schedule
- **Full backup**: Daily (off-peak hours)
- **Incremental**: Hourly (if high volume)
- **Point-in-time recovery**: Enable WAL archiving

### Backup Commands
```bash
# Full backup
pg_dump -U postgres storyteller > backup_$(date +%Y%m%d).sql

# Restore
psql -U postgres storyteller < backup_20240616.sql
```

## Monitoring

### Key Metrics to Monitor
1. Connection pool usage
2. Query execution times
3. Table sizes and growth rate
4. Index usage statistics
5. Cache hit ratios
6. Lock contention

### Useful Queries
```sql
-- Table sizes
SELECT 
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;

-- Index usage
SELECT
    schemaname,
    tablename,
    indexname,
    idx_scan,
    idx_tup_read,
    idx_tup_fetch
FROM pg_stat_user_indexes
ORDER BY idx_scan DESC;

-- Slow queries (if pg_stat_statements enabled)
SELECT
    query,
    calls,
    mean_exec_time,
    max_exec_time
FROM pg_stat_statements
ORDER BY mean_exec_time DESC
LIMIT 10;
```

---

For implementation details, see:
- [README.md](README.md): Complete documentation
- [QUICKSTART.md](QUICKSTART.md): Getting started guide
- [models.py](models.py): SQLAlchemy model definitions
- [database.py](database.py): Connection management
