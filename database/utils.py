"""
Database utility functions for common operations.
"""
from typing import Optional, List, Tuple
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func

from .models import User, Location, POI, Story, UserPreference, ContentType


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """
    Get user by email address.

    Args:
        db: Database session
        email: User email address

    Returns:
        User object or None if not found
    """
    return db.query(User).filter(User.email == email).first()


def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    """
    Get user by ID.

    Args:
        db: Database session
        user_id: User ID

    Returns:
        User object or None if not found
    """
    return db.query(User).filter(User.id == user_id).first()


def create_user(
    db: Session,
    email: str,
    password_hash: str,
    name: Optional[str] = None,
    age: Optional[int] = None
) -> User:
    """
    Create a new user.

    Args:
        db: Database session
        email: User email
        password_hash: Hashed password
        name: User name (optional)
        age: User age (optional)

    Returns:
        Created User object
    """
    user = User(
        email=email,
        password_hash=password_hash,
        name=name,
        age=age
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_nearby_pois(
    db: Session,
    latitude: float,
    longitude: float,
    radius_km: float = 0.5
) -> List[POI]:
    """
    Find POIs within a radius of given coordinates.

    Note: This uses a simple bounding box calculation.
    For production, use PostGIS with ST_DWithin for accurate distance.

    Args:
        db: Database session
        latitude: Center latitude
        longitude: Center longitude
        radius_km: Search radius in kilometers (default: 0.5)

    Returns:
        List of POI objects
    """
    # Approximate degrees per kilometer (rough estimation)
    # 1 degree latitude ≈ 111 km
    # 1 degree longitude ≈ 111 km * cos(latitude)
    import math

    lat_delta = radius_km / 111.0
    lon_delta = radius_km / (111.0 * math.cos(math.radians(latitude)))

    return db.query(POI).filter(
        and_(
            POI.latitude.between(latitude - lat_delta, latitude + lat_delta),
            POI.longitude.between(longitude - lon_delta, longitude + lon_delta)
        )
    ).all()


def get_user_recent_locations(
    db: Session,
    user_id: int,
    limit: int = 50
) -> List[Location]:
    """
    Get user's most recent locations.

    Args:
        db: Database session
        user_id: User ID
        limit: Maximum number of locations to return

    Returns:
        List of Location objects
    """
    return db.query(Location).filter(
        Location.user_id == user_id
    ).order_by(Location.timestamp.desc()).limit(limit).all()


def get_user_location_history(
    db: Session,
    user_id: int,
    start_time: datetime,
    end_time: datetime
) -> List[Location]:
    """
    Get user's location history within a time range.

    Args:
        db: Database session
        user_id: User ID
        start_time: Start of time range
        end_time: End of time range

    Returns:
        List of Location objects
    """
    return db.query(Location).filter(
        and_(
            Location.user_id == user_id,
            Location.timestamp >= start_time,
            Location.timestamp <= end_time
        )
    ).order_by(Location.timestamp.asc()).all()


def create_story(
    db: Session,
    user_id: int,
    content: str,
    content_type: ContentType,
    location_id: Optional[int] = None,
    poi_id: Optional[int] = None,
    title: Optional[str] = None,
    **kwargs
) -> Story:
    """
    Create a new story.

    Args:
        db: Database session
        user_id: User ID
        content: Story content
        content_type: Type of content
        location_id: Associated location ID (optional)
        poi_id: Associated POI ID (optional)
        title: Story title (optional)
        **kwargs: Additional story fields

    Returns:
        Created Story object
    """
    story = Story(
        user_id=user_id,
        location_id=location_id,
        poi_id=poi_id,
        title=title,
        content=content,
        content_type=content_type,
        **kwargs
    )
    db.add(story)
    db.commit()
    db.refresh(story)
    return story


def get_user_stories(
    db: Session,
    user_id: int,
    content_type: Optional[ContentType] = None,
    favorites_only: bool = False,
    limit: int = 50
) -> List[Story]:
    """
    Get user's stories with optional filtering.

    Args:
        db: Database session
        user_id: User ID
        content_type: Filter by content type (optional)
        favorites_only: Only return favorites
        limit: Maximum number of stories

    Returns:
        List of Story objects
    """
    query = db.query(Story).filter(Story.user_id == user_id)

    if content_type:
        query = query.filter(Story.content_type == content_type)

    if favorites_only:
        query = query.filter(Story.is_favorite == True)

    return query.order_by(Story.generated_at.desc()).limit(limit).all()


def mark_story_as_favorite(db: Session, story_id: int, is_favorite: bool = True) -> Optional[Story]:
    """
    Mark a story as favorite or unfavorite.

    Args:
        db: Database session
        story_id: Story ID
        is_favorite: True to favorite, False to unfavorite

    Returns:
        Updated Story object or None if not found
    """
    story = db.query(Story).filter(Story.id == story_id).first()
    if story:
        story.is_favorite = is_favorite
        db.commit()
        db.refresh(story)
    return story


def mark_story_as_read(db: Session, story_id: int) -> Optional[Story]:
    """
    Mark a story as read.

    Args:
        db: Database session
        story_id: Story ID

    Returns:
        Updated Story object or None if not found
    """
    story = db.query(Story).filter(Story.id == story_id).first()
    if story:
        story.is_read = True
        story.read_at = datetime.utcnow()
        db.commit()
        db.refresh(story)
    return story


def rate_story(db: Session, story_id: int, rating: int) -> Optional[Story]:
    """
    Rate a story (1-5 stars).

    Args:
        db: Database session
        story_id: Story ID
        rating: Rating value (1-5)

    Returns:
        Updated Story object or None if not found

    Raises:
        ValueError: If rating is not between 1 and 5
    """
    if not 1 <= rating <= 5:
        raise ValueError("Rating must be between 1 and 5")

    story = db.query(Story).filter(Story.id == story_id).first()
    if story:
        story.user_rating = rating
        db.commit()
        db.refresh(story)
    return story


def get_user_preferences(db: Session, user_id: int) -> Optional[UserPreference]:
    """
    Get user preferences.

    Args:
        db: Database session
        user_id: User ID

    Returns:
        UserPreference object or None if not found
    """
    return db.query(UserPreference).filter(UserPreference.user_id == user_id).first()


def update_user_preferences(
    db: Session,
    user_id: int,
    **kwargs
) -> UserPreference:
    """
    Update or create user preferences.

    Args:
        db: Database session
        user_id: User ID
        **kwargs: Preference fields to update

    Returns:
        Updated or created UserPreference object
    """
    prefs = get_user_preferences(db, user_id)

    if prefs:
        # Update existing preferences
        for key, value in kwargs.items():
            if hasattr(prefs, key):
                setattr(prefs, key, value)
    else:
        # Create new preferences
        prefs = UserPreference(user_id=user_id, **kwargs)
        db.add(prefs)

    db.commit()
    db.refresh(prefs)
    return prefs


def get_cached_story(
    db: Session,
    user_id: int,
    poi_id: int,
    content_type: ContentType
) -> Optional[Story]:
    """
    Get a cached story for a POI if it exists and hasn't expired.

    Args:
        db: Database session
        user_id: User ID
        poi_id: POI ID
        content_type: Content type

    Returns:
        Story object or None if no valid cache exists
    """
    now = datetime.utcnow()

    return db.query(Story).filter(
        and_(
            Story.user_id == user_id,
            Story.poi_id == poi_id,
            Story.content_type == content_type,
            Story.is_cached == True,
            or_(
                Story.cache_expires_at.is_(None),
                Story.cache_expires_at > now
            )
        )
    ).first()


def get_poi_by_external_id(db: Session, source: str, external_id: str) -> Optional[POI]:
    """
    Get POI by external source ID.

    Args:
        db: Database session
        source: Source name (OSM, GOOGLE, etc.)
        external_id: External identifier

    Returns:
        POI object or None if not found
    """
    return db.query(POI).filter(
        and_(
            POI.source == source,
            POI.external_id == external_id
        )
    ).first()


def get_statistics(db: Session, user_id: int) -> dict:
    """
    Get user statistics.

    Args:
        db: Database session
        user_id: User ID

    Returns:
        Dictionary with user statistics
    """
    total_locations = db.query(func.count(Location.id)).filter(
        Location.user_id == user_id
    ).scalar()

    total_stories = db.query(func.count(Story.id)).filter(
        Story.user_id == user_id
    ).scalar()

    favorite_stories = db.query(func.count(Story.id)).filter(
        and_(
            Story.user_id == user_id,
            Story.is_favorite == True
        )
    ).scalar()

    read_stories = db.query(func.count(Story.id)).filter(
        and_(
            Story.user_id == user_id,
            Story.is_read == True
        )
    ).scalar()

    return {
        "total_locations": total_locations,
        "total_stories": total_stories,
        "favorite_stories": favorite_stories,
        "read_stories": read_stories,
        "unread_stories": total_stories - read_stories
    }
