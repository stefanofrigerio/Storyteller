"""
Storyteller Database Package

This package provides database functionality including:
- SQLAlchemy ORM models
- Database connection management
- Utility functions for common operations
"""

from .database import (
    Base,
    engine,
    SessionLocal,
    get_db,
    init_db,
    drop_db,
    test_connection
)

from .models import (
    User,
    UserPreference,
    Location,
    POI,
    Story,
    ContentType,
    POISource
)

__all__ = [
    # Database connection
    "Base",
    "engine",
    "SessionLocal",
    "get_db",
    "init_db",
    "drop_db",
    "test_connection",
    # Models
    "User",
    "UserPreference",
    "Location",
    "POI",
    "Story",
    "ContentType",
    "POISource",
]

__version__ = "0.1.0"
