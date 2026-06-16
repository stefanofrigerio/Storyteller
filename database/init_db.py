#!/usr/bin/env python3
"""
Database initialization script.

This script:
1. Tests database connectivity
2. Creates all tables
3. Optionally loads seed data

Usage:
    python init_db.py                    # Create tables only
    python init_db.py --seed             # Create tables and load seed data
    python init_db.py --drop --seed      # Drop existing, create fresh, and seed
"""
import argparse
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from database.database import init_db, drop_db, test_connection, engine
from database.models import Base


def main():
    parser = argparse.ArgumentParser(description="Initialize Storyteller database")
    parser.add_argument(
        "--drop",
        action="store_true",
        help="Drop all existing tables before creating (WARNING: deletes all data)"
    )
    parser.add_argument(
        "--seed",
        action="store_true",
        help="Load seed data after creating tables"
    )
    parser.add_argument(
        "--test-only",
        action="store_true",
        help="Only test database connection without making changes"
    )

    args = parser.parse_args()

    print("=" * 60)
    print("Storyteller Database Initialization")
    print("=" * 60)

    # Test database connection
    print("\n[1/4] Testing database connection...")
    if not test_connection():
        print("ERROR: Failed to connect to database.")
        print("Please check your DATABASE_URL environment variable.")
        sys.exit(1)
    print("SUCCESS: Database connection established.")

    if args.test_only:
        print("\nConnection test successful. Exiting.")
        sys.exit(0)

    # Drop tables if requested
    if args.drop:
        print("\n[2/4] Dropping existing tables...")
        confirm = input("WARNING: This will delete all data. Continue? (yes/no): ")
        if confirm.lower() != "yes":
            print("Aborted.")
            sys.exit(0)
        drop_db()
        print("SUCCESS: All tables dropped.")
    else:
        print("\n[2/4] Skipping table drop (use --drop to drop existing tables).")

    # Create tables
    print("\n[3/4] Creating database tables...")
    try:
        init_db()
        print("SUCCESS: All tables created.")

        # Show created tables
        from sqlalchemy import inspect
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        print(f"\nCreated tables: {', '.join(tables)}")

    except Exception as e:
        print(f"ERROR: Failed to create tables: {e}")
        sys.exit(1)

    # Load seed data if requested
    if args.seed:
        print("\n[4/4] Loading seed data...")
        try:
            from database.seed_data import seed_database
            seed_database()
            print("SUCCESS: Seed data loaded.")
        except ImportError:
            print("WARNING: seed_data.py not found. Skipping seed data.")
        except Exception as e:
            print(f"ERROR: Failed to load seed data: {e}")
            sys.exit(1)
    else:
        print("\n[4/4] Skipping seed data (use --seed to load test data).")

    print("\n" + "=" * 60)
    print("Database initialization complete!")
    print("=" * 60)
    print("\nNext steps:")
    print("  - Set up Alembic for migrations: alembic init alembic")
    print("  - Start the backend API: cd ../backend && uvicorn main:app --reload")


if __name__ == "__main__":
    main()
