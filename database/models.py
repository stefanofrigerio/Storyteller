"""
SQLAlchemy database models for Storyteller application.
"""
from datetime import datetime
from typing import List, Optional
from sqlalchemy import (
    Column, Integer, String, Float, DateTime, Boolean, Text,
    ForeignKey, Index, JSON, Enum as SQLEnum, UniqueConstraint
)
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.sql import func
import enum

from .database import Base


class ContentType(enum.Enum):
    """Enum for story content types."""
    HISTORICAL = "historical"
    CULTURAL = "cultural"
    FUNNY = "funny"
    RECOMMENDATION = "recommendation"
    NARRATIVE = "narrative"
    ARCHITECTURAL = "architectural"


class POISource(enum.Enum):
    """Enum for POI data sources."""
    OSM = "osm"
    GOOGLE = "google"
    MANUAL = "manual"
    GENERATED = "generated"


class User(Base):
    """
    User account model.

    Stores user authentication information and profile data.
    """
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)

    # Profile information
    name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    age: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    bio: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    language: Mapped[str] = mapped_column(String(10), default="en", nullable=False)

    # Account status
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    last_login: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    # Relationships
    locations: Mapped[List["Location"]] = relationship("Location", back_populates="user", cascade="all, delete-orphan")
    stories: Mapped[List["Story"]] = relationship("Story", back_populates="user", cascade="all, delete-orphan")
    preferences: Mapped[Optional["UserPreference"]] = relationship("UserPreference", back_populates="user", uselist=False, cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<User(id={self.id}, email='{self.email}', name='{self.name}')>"


class UserPreference(Base):
    """
    User preferences and interests.

    Stores personalization settings for content generation.
    """
    __tablename__ = "user_preferences"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), unique=True, nullable=False)

    # Interest tags (stored as JSON array)
    interest_tags: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    # Example: ["history", "architecture", "food", "art", "music"]

    # Preferred content types (stored as JSON array)
    preferred_content_types: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    # Example: ["historical", "cultural", "recommendation"]

    # Content settings
    story_length: Mapped[str] = mapped_column(String(20), default="medium", nullable=False)
    # short, medium, long

    verbosity_level: Mapped[int] = mapped_column(Integer, default=5, nullable=False)
    # 1-10 scale

    # Notification preferences
    notifications_enabled: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    distance_threshold: Mapped[float] = mapped_column(Float, default=50.0, nullable=False)
    # meters before triggering new content

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="preferences")

    def __repr__(self) -> str:
        return f"<UserPreference(id={self.id}, user_id={self.user_id})>"


class Location(Base):
    """
    User location tracking model.

    Stores GPS coordinates and metadata for user's walking paths.
    """
    __tablename__ = "locations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)

    # Geographic coordinates
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)
    altitude: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    # Location metadata
    accuracy: Mapped[Optional[float]] = mapped_column(Float, nullable=True)  # meters
    speed: Mapped[Optional[float]] = mapped_column(Float, nullable=True)  # m/s
    heading: Mapped[Optional[float]] = mapped_column(Float, nullable=True)  # degrees

    # Reverse geocoding data (cached)
    address: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    city: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    country: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    # Timestamp
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="locations")
    stories: Mapped[List["Story"]] = relationship("Story", back_populates="location", cascade="all, delete-orphan")

    # Indexes for geospatial queries
    __table_args__ = (
        Index("idx_location_coords", "latitude", "longitude"),
        Index("idx_location_user_time", "user_id", "timestamp"),
    )

    def __repr__(self) -> str:
        return f"<Location(id={self.id}, lat={self.latitude}, lon={self.longitude}, user_id={self.user_id})>"


class POI(Base):
    """
    Point of Interest model.

    Stores places, landmarks, and notable locations.
    """
    __tablename__ = "pois"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    # Basic information
    name: Mapped[str] = mapped_column(String(500), nullable=False)
    poi_type: Mapped[str] = mapped_column(String(100), nullable=False)
    # restaurant, museum, monument, park, historical_site, etc.

    # Geographic coordinates
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)

    # Content
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    historical_context: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    fun_facts: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Source information
    source: Mapped[str] = mapped_column(SQLEnum(POISource), default=POISource.MANUAL, nullable=False)
    external_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    # ID from external API (OSM node id, Google Place ID, etc.)

    # Additional metadata (JSON for flexibility)
    metadata: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    # opening_hours, website, phone, rating, etc.

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    stories: Mapped[List["Story"]] = relationship("Story", back_populates="poi")

    # Indexes for geospatial queries
    __table_args__ = (
        Index("idx_poi_coords", "latitude", "longitude"),
        Index("idx_poi_type", "poi_type"),
        UniqueConstraint("source", "external_id", name="uq_poi_source_external_id"),
    )

    def __repr__(self) -> str:
        return f"<POI(id={self.id}, name='{self.name}', type='{self.poi_type}')>"


class Story(Base):
    """
    Generated story/content model.

    Stores AI-generated content for locations and POIs.
    """
    __tablename__ = "stories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    location_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("locations.id"), nullable=True)
    poi_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("pois.id"), nullable=True)

    # Content
    title: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    content_type: Mapped[str] = mapped_column(SQLEnum(ContentType), nullable=False)

    # Generation metadata
    prompt_used: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    model_version: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    # e.g., "claude-4-opus-20240229"

    tokens_used: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    generation_time: Mapped[Optional[float]] = mapped_column(Float, nullable=True)  # seconds

    # User interaction
    is_favorite: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_read: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    read_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    user_rating: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    # 1-5 stars

    # Cache settings
    is_cached: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    cache_expires_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    # Timestamps
    generated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="stories")
    location: Mapped[Optional["Location"]] = relationship("Location", back_populates="stories")
    poi: Mapped[Optional["POI"]] = relationship("POI", back_populates="stories")

    # Indexes for queries
    __table_args__ = (
        Index("idx_story_user_generated", "user_id", "generated_at"),
        Index("idx_story_type", "content_type"),
        Index("idx_story_favorite", "user_id", "is_favorite"),
    )

    def __repr__(self) -> str:
        return f"<Story(id={self.id}, type={self.content_type}, user_id={self.user_id})>"
