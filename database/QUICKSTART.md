# Database Quick Start Guide

Get the Storyteller database up and running in 5 minutes.

## Prerequisites

- PostgreSQL 14+ installed and running
- Python 3.9+ with pip or Poetry

## Step 1: Install PostgreSQL

### macOS (Homebrew)
```bash
brew install postgresql@14
brew services start postgresql@14
```

### Ubuntu/Debian
```bash
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
```

### Windows
Download and install from [PostgreSQL Downloads](https://www.postgresql.org/download/windows/)

## Step 2: Create Database

```bash
# Connect to PostgreSQL
psql -U postgres

# In psql shell, create database
CREATE DATABASE storyteller;
CREATE USER storyteller_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE storyteller TO storyteller_user;
\q
```

## Step 3: Install Python Dependencies

```bash
# Navigate to database directory
cd /path/to/Storyteller/database

# Install dependencies
pip install -r requirements.txt

# Or with Poetry (from project root)
cd ..
poetry install
```

## Step 4: Configure Environment

Create `.env` file in project root:

```bash
# From project root
cat > .env << EOF
DATABASE_URL=postgresql://storyteller_user:your_password@localhost:5432/storyteller
EOF
```

Or export as environment variable:

```bash
export DATABASE_URL="postgresql://storyteller_user:your_password@localhost:5432/storyteller"
```

## Step 5: Initialize Database

```bash
cd database

# Test connection
python init_db.py --test-only

# Create tables and load sample data
python init_db.py --seed
```

You should see:
```
============================================================
Storyteller Database Initialization
============================================================

[1/4] Testing database connection...
SUCCESS: Database connection established.

[2/4] Skipping table drop (use --drop to drop existing tables).

[3/4] Creating database tables...
SUCCESS: All tables created.

Created tables: users, user_preferences, locations, pois, stories

[4/4] Loading seed data...
Creating test users...
  Created 3 users
Creating user preferences...
  Created preferences for 3 users
Creating sample locations...
  Created 7 locations
Creating sample POIs...
  Created 6 POIs
Creating sample stories...
  Created sample stories

Seed data summary:
  Users: 3
  Locations: 7
  POIs: 6
  Stories: 5
SUCCESS: Seed data loaded.

============================================================
Database initialization complete!
============================================================
```

## Step 6: Verify Installation

### Using Python

```python
from database import SessionLocal, User, Location, POI, Story

db = SessionLocal()

# Check users
users = db.query(User).all()
print(f"Users: {len(users)}")

# Check POIs
pois = db.query(POI).all()
print(f"POIs: {len(pois)}")

# Check stories
stories = db.query(Story).all()
print(f"Stories: {len(stories)}")

db.close()
```

### Using psql

```bash
psql -U storyteller_user -d storyteller

# In psql shell
\dt                          -- List all tables
SELECT COUNT(*) FROM users;  -- Should return 3
SELECT COUNT(*) FROM pois;   -- Should return 6
SELECT * FROM users LIMIT 1; -- View a user
\q
```

## Common Issues

### "Connection refused"

PostgreSQL isn't running:
```bash
# macOS
brew services start postgresql@14

# Ubuntu/Debian
sudo systemctl start postgresql
```

### "password authentication failed"

Check your DATABASE_URL credentials:
```bash
echo $DATABASE_URL
# Should match your PostgreSQL user and password
```

### "ImportError: No module named 'psycopg2'"

Install dependencies:
```bash
pip install -r requirements.txt
```

### "database does not exist"

Create the database:
```bash
createdb -U postgres storyteller
```

## Next Steps

1. **Explore the data**: Use psql or a GUI tool like pgAdmin to browse the tables
2. **Run queries**: Try the example queries in the main README
3. **Build the API**: Move to the backend component to create REST endpoints
4. **Test migrations**: Try creating a new migration with Alembic

## Test Users

The seed data creates these test users:

| Email | Password | Name | Interests |
|-------|----------|------|-----------|
| alice@example.com | password123 | Alice Johnson | History, Architecture |
| bob@example.com | password123 | Bob Smith | Food, Architecture |
| charlie@example.com | password123 | Charlie Brown | Art, Culture |

Note: Passwords are hashed with bcrypt in the database.

## Sample Data

The seed data includes:
- **3 users** with different profiles and preferences
- **7 locations** tracking a walk through Rome's historic center
- **6 POIs**: Colosseum, Trevi Fountain, Pantheon, Piazza Navona, Roscioli restaurant, Spanish Steps
- **5 stories** with various content types (historical, cultural, recommendation, architectural)

## Useful Commands

```bash
# Drop and recreate database
python init_db.py --drop --seed

# Test connection only
python init_db.py --test-only

# Create tables without seed data
python init_db.py

# Run migrations
alembic upgrade head

# Check migration status
alembic current
```

## Getting Help

- Check the main [README.md](README.md) for detailed documentation
- Review the models in [models.py](models.py)
- See example queries in [utils.py](utils.py)
- Refer to [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)

## Clean Up

To remove everything:

```bash
# Drop the database
dropdb -U postgres storyteller

# Or just drop tables (keeps database)
python init_db.py --drop
```

---

Ready to build something amazing! Check out the [main README](README.md) for more details.
