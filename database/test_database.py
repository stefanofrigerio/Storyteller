#!/usr/bin/env python3
"""
Simple test script to validate database setup.

Usage:
    python test_database.py
"""
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from database import (
    SessionLocal, test_connection,
    User, UserPreference, Location, POI, Story
)
from database.utils import (
    get_user_by_email,
    get_nearby_pois,
    get_user_stories,
    get_statistics
)


def test_connection_check():
    """Test database connectivity."""
    print("\n[TEST 1] Testing database connection...")
    result = test_connection()
    assert result, "Database connection failed"
    print("✓ Database connection successful")


def test_models():
    """Test that all models are accessible."""
    print("\n[TEST 2] Testing model imports...")
    models = [User, UserPreference, Location, POI, Story]
    for model in models:
        assert model is not None, f"{model.__name__} not imported"
        print(f"✓ {model.__name__} model imported")


def test_query_users():
    """Test querying users."""
    print("\n[TEST 3] Testing user queries...")
    db = SessionLocal()
    try:
        users = db.query(User).all()
        print(f"✓ Found {len(users)} users in database")

        if users:
            first_user = users[0]
            print(f"  Sample user: {first_user.email} ({first_user.name})")

            # Test utility function
            user = get_user_by_email(db, first_user.email)
            assert user is not None, "get_user_by_email failed"
            print(f"✓ Utility function get_user_by_email works")
    finally:
        db.close()


def test_query_locations():
    """Test querying locations."""
    print("\n[TEST 4] Testing location queries...")
    db = SessionLocal()
    try:
        locations = db.query(Location).all()
        print(f"✓ Found {len(locations)} locations in database")

        if locations:
            first_loc = locations[0]
            print(f"  Sample location: ({first_loc.latitude}, {first_loc.longitude})")
    finally:
        db.close()


def test_query_pois():
    """Test querying POIs."""
    print("\n[TEST 5] Testing POI queries...")
    db = SessionLocal()
    try:
        pois = db.query(POI).all()
        print(f"✓ Found {len(pois)} POIs in database")

        if pois:
            first_poi = pois[0]
            print(f"  Sample POI: {first_poi.name} ({first_poi.poi_type})")

            # Test nearby POI search
            nearby = get_nearby_pois(db, first_poi.latitude, first_poi.longitude, 1.0)
            print(f"✓ Found {len(nearby)} POIs within 1km radius")
    finally:
        db.close()


def test_query_stories():
    """Test querying stories."""
    print("\n[TEST 6] Testing story queries...")
    db = SessionLocal()
    try:
        stories = db.query(Story).all()
        print(f"✓ Found {len(stories)} stories in database")

        if stories:
            first_story = stories[0]
            print(f"  Sample story: {first_story.title or 'Untitled'}")
            print(f"  Type: {first_story.content_type.value}")
            print(f"  Favorite: {first_story.is_favorite}")

            # Test utility function
            user_stories = get_user_stories(db, first_story.user_id, limit=10)
            print(f"✓ User has {len(user_stories)} stories")
    finally:
        db.close()


def test_relationships():
    """Test model relationships."""
    print("\n[TEST 7] Testing model relationships...")
    db = SessionLocal()
    try:
        user = db.query(User).first()
        if user:
            print(f"✓ User: {user.email}")
            print(f"  - Locations: {len(user.locations)}")
            print(f"  - Stories: {len(user.stories)}")
            print(f"  - Has preferences: {user.preferences is not None}")

        story = db.query(Story).first()
        if story:
            print(f"✓ Story relationships:")
            print(f"  - Has user: {story.user is not None}")
            print(f"  - Has location: {story.location is not None}")
            print(f"  - Has POI: {story.poi is not None}")
    finally:
        db.close()


def test_statistics():
    """Test statistics utility function."""
    print("\n[TEST 8] Testing statistics...")
    db = SessionLocal()
    try:
        user = db.query(User).first()
        if user:
            stats = get_statistics(db, user.id)
            print(f"✓ Statistics for {user.email}:")
            print(f"  - Total locations: {stats['total_locations']}")
            print(f"  - Total stories: {stats['total_stories']}")
            print(f"  - Favorite stories: {stats['favorite_stories']}")
            print(f"  - Read stories: {stats['read_stories']}")
            print(f"  - Unread stories: {stats['unread_stories']}")
    finally:
        db.close()


def run_all_tests():
    """Run all tests."""
    print("=" * 60)
    print("Storyteller Database Tests")
    print("=" * 60)

    try:
        test_connection_check()
        test_models()
        test_query_users()
        test_query_locations()
        test_query_pois()
        test_query_stories()
        test_relationships()
        test_statistics()

        print("\n" + "=" * 60)
        print("All tests passed! ✓")
        print("=" * 60)
        print("\nDatabase is ready to use.")
        print("Next steps:")
        print("  - Build backend API with FastAPI")
        print("  - Integrate LLM for story generation")
        print("  - Add geolocation services")

        return True

    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        return False
    except Exception as e:
        print(f"\n✗ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
