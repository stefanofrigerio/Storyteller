"""
Seed data for testing and development.

Creates sample users, locations, POIs, and stories.
"""
from datetime import datetime, timedelta
from typing import List
from sqlalchemy.orm import Session

from database.database import SessionLocal
from database.models import (
    User, UserPreference, Location, POI, Story,
    ContentType, POISource
)


def create_test_users(db: Session) -> List[User]:
    """Create test users with different profiles."""
    users = [
        User(
            email="alice@example.com",
            password_hash="$2b$12$KIXvvKZrqYnOmJ0xN5Jv0.Zzv0YnqYjcXkZv0YnqYjcXkZv0YnqYj",  # hashed "password123"
            name="Alice Johnson",
            age=28,
            bio="History enthusiast and urban explorer",
            language="en",
            is_active=True,
            is_verified=True,
            last_login=datetime.utcnow()
        ),
        User(
            email="bob@example.com",
            password_hash="$2b$12$KIXvvKZrqYnOmJ0xN5Jv0.Zzv0YnqYjcXkZv0YnqYjcXkZv0YnqYj",
            name="Bob Smith",
            age=35,
            bio="Architecture lover and foodie",
            language="en",
            is_active=True,
            is_verified=True,
            last_login=datetime.utcnow() - timedelta(days=2)
        ),
        User(
            email="charlie@example.com",
            password_hash="$2b$12$KIXvvKZrqYnOmJ0xN5Jv0.Zzv0YnqYjcXkZv0YnqYjcXkZv0YnqYj",
            name="Charlie Brown",
            age=42,
            bio="Art and culture aficionado",
            language="en",
            is_active=True,
            is_verified=False,
        )
    ]

    db.add_all(users)
    db.commit()

    for user in users:
        db.refresh(user)

    return users


def create_user_preferences(db: Session, users: List[User]) -> None:
    """Create preferences for test users."""
    preferences = [
        UserPreference(
            user_id=users[0].id,
            interest_tags=["history", "architecture", "museums", "ancient civilizations"],
            preferred_content_types=["historical", "cultural", "architectural"],
            story_length="long",
            verbosity_level=8,
            notifications_enabled=True,
            distance_threshold=30.0
        ),
        UserPreference(
            user_id=users[1].id,
            interest_tags=["food", "restaurants", "architecture", "design"],
            preferred_content_types=["recommendation", "architectural"],
            story_length="medium",
            verbosity_level=5,
            notifications_enabled=True,
            distance_threshold=50.0
        ),
        UserPreference(
            user_id=users[2].id,
            interest_tags=["art", "music", "culture", "galleries"],
            preferred_content_types=["cultural", "narrative", "funny"],
            story_length="short",
            verbosity_level=6,
            notifications_enabled=True,
            distance_threshold=40.0
        )
    ]

    db.add_all(preferences)
    db.commit()


def create_sample_locations(db: Session, users: List[User]) -> List[Location]:
    """Create sample location data (walking path in Milano - Porta Venezia area, Italy)."""
    # Sample coordinates around Milano's Porta Venezia district
    milano_locations = [
        # Porta Venezia gate
        (45.4773, 9.2070, "Porta Venezia", "Milano", "Italy"),
        # Giardini Pubblici
        (45.4761, 9.2033, "Giardini Pubblici Indro Montanelli", "Milano", "Italy"),
        # Villa Reale
        (45.4750, 9.2042, "Villa Reale", "Milano", "Italy"),
        # Corso Buenos Aires
        (45.4780, 9.2050, "Corso Buenos Aires", "Milano", "Italy"),
        # Piazza della Repubblica
        (45.4822, 9.2035, "Piazza della Repubblica", "Milano", "Italy"),
        # Central Station area
        (45.4855, 9.2040, "Milano Centrale", "Milano", "Italy"),
        # Corso Venezia
        (45.4760, 9.1980, "Corso Venezia", "Milano", "Italy"),
    ]

    locations = []
    base_time = datetime.utcnow() - timedelta(hours=2)

    for i, (lat, lon, address, city, country) in enumerate(milano_locations):
        # Create location for Alice (first user)
        location = Location(
            user_id=users[0].id,
            latitude=lat,
            longitude=lon,
            altitude=20.0 + i * 2,
            accuracy=5.0,
            speed=1.2,  # walking speed
            heading=45.0 + i * 10,
            address=address,
            city=city,
            country=country,
            timestamp=base_time + timedelta(minutes=i * 10)
        )
        locations.append(location)

    db.add_all(locations)
    db.commit()

    for location in locations:
        db.refresh(location)

    return locations


def create_sample_pois(db: Session) -> List[POI]:
    """Create sample Points of Interest in Milano - Porta Venezia area."""
    pois = [
        POI(
            name="Porta Venezia",
            poi_type="historical_site",
            latitude=45.4773,
            longitude=9.2070,
            description="Porta Venezia is one of the historic gates of the old Spanish walls of Milan.",
            historical_context="Built between 1827 and 1833 in Neoclassical style, it replaced the earlier Spanish gate. It marks the start of Corso Buenos Aires, one of Milan's longest shopping streets.",
            fun_facts="The gate features two symmetrical toll houses and was originally called Porta Orientale (Eastern Gate) before being renamed Porta Venezia.",
            source=POISource.MANUAL,
            external_id="porta_venezia_001",
            metadata={
                "style": "Neoclassical",
                "year_built": 1833,
                "architect": "Rodolfo Vantini",
                "unesco_site": False
            }
        ),
        POI(
            name="Giardini Pubblici Indro Montanelli",
            poi_type="park",
            latitude=45.4761,
            longitude=9.2033,
            description="Milan's first public park, also known as Giardini di Porta Venezia.",
            historical_context="Created in 1784, these historic public gardens are Milan's oldest park. They house the Natural History Museum and the Planetarium.",
            fun_facts="The park covers 172,000 square meters and features over 100 tree species, making it a green oasis in the city center!",
            source=POISource.OSM,
            external_id="osm_giardini_pubblici_123",
            metadata={
                "area_sqm": 172000,
                "features": ["Natural History Museum", "Planetarium", "children's playground"],
                "opening_hours": "06:30-21:00",
                "tree_species": 100
            }
        ),
        POI(
            name="Villa Reale",
            poi_type="museum",
            latitude=45.4750,
            longitude=9.2042,
            description="Neoclassical palace housing the Gallery of Modern Art (GAM).",
            historical_context="Built between 1790 and 1796 for Count Ludovico Barbiano di Belgioioso. Napoleon lived here as viceroy of the Kingdom of Italy (1802-1814).",
            fun_facts="The villa's English garden was the first of its kind in Milan, breaking from the traditional Italian garden style!",
            source=POISource.MANUAL,
            external_id="villa_reale_001",
            metadata={
                "opening_hours": "09:00-17:30",
                "style": "Neoclassical",
                "year_built": 1796,
                "architect": "Leopoldo Pollack",
                "collections": ["19th century Italian art", "Modern art"]
            }
        ),
        POI(
            name="Corso Buenos Aires",
            poi_type="shopping_street",
            latitude=45.4780,
            longitude=9.2050,
            description="One of Milan's longest and busiest shopping streets.",
            historical_context="Named in 1895 after Buenos Aires, Argentina, this 1.6 km street is one of Europe's longest commercial streets with over 350 shops.",
            fun_facts="On busy shopping days, Corso Buenos Aires sees up to 100,000 visitors! It's one of the most commercial streets in the world.",
            source=POISource.MANUAL,
            external_id="corso_buenos_aires_001",
            metadata={
                "length_km": 1.6,
                "number_of_shops": 350,
                "daily_visitors": 100000,
                "categories": ["fashion", "electronics", "restaurants", "cafes"]
            }
        ),
        POI(
            name="Piazza della Repubblica",
            poi_type="square",
            latitude=45.4822,
            longitude=9.2035,
            description="Major square near Milano Centrale train station.",
            historical_context="Created in the mid-19th century as part of Milan's urban expansion. The square was redesigned in 2013 with a modern architectural intervention.",
            fun_facts="The square features three iconic skyscrapers from the 1950s, known as the 'Torri' (Towers) of Piazza della Repubblica.",
            source=POISource.OSM,
            external_id="osm_piazza_repubblica_456",
            metadata={
                "features": ["fountain", "skyscrapers", "public transport hub"],
                "nearby": ["Milano Centrale", "Corso Buenos Aires"],
                "renovation_year": 2013
            }
        ),
        POI(
            name="Panzerotti Luini",
            poi_type="restaurant",
            latitude=45.4642,
            longitude=9.1895,
            description="Historic bakery famous for its panzerotti, a Milanese street food institution since 1949.",
            historical_context="Founded by Giuseppina Luini, this family-run business has been serving fried panzerotti for over 70 years.",
            fun_facts="Luini sells over 2,000 panzerotti daily! Their classic recipe with tomato and mozzarella is unchanged since 1949.",
            source=POISource.GOOGLE,
            external_id="google_place_luini_xyz",
            metadata={
                "cuisine": "Italian",
                "specialties": ["panzerotti with tomato and mozzarella", "panzerotti with vegetables"],
                "price_range": "$",
                "rating": 4.5,
                "opening_hours": "10:00-15:00, 16:00-20:00",
                "year_founded": 1949
            }
        )
    ]

    db.add_all(pois)
    db.commit()

    for poi in pois:
        db.refresh(poi)

    return pois


def create_sample_stories(db: Session, users: List[User], locations: List[Location], pois: List[POI]) -> None:
    """Create sample AI-generated stories."""
    stories = [
        Story(
            user_id=users[0].id,
            location_id=locations[0].id,
            poi_id=pois[0].id,
            title="Gateway to Milan's History",
            content="""As you pass through Porta Venezia, you're walking through one of Milan's historic city gates. Built between 1827 and 1833 in elegant Neoclassical style, this gate replaced the earlier Spanish fortifications. Originally called Porta Orientale, it marked the eastern entrance to the city. The two symmetrical toll houses flanking the gate once collected taxes on goods entering Milan. Today, it stands as a symbol of Milan's transformation from a walled medieval city to a modern metropolis.""",
            content_type=ContentType.HISTORICAL,
            prompt_used="Generate a historical story about Porta Venezia",
            model_version="claude-4-opus-20240229",
            tokens_used=220,
            generation_time=2.1,
            is_favorite=True,
            is_read=True,
            read_at=datetime.utcnow() - timedelta(hours=1),
            user_rating=5,
            is_cached=True,
            cache_expires_at=datetime.utcnow() + timedelta(days=30)
        ),
        Story(
            user_id=users[0].id,
            location_id=locations[1].id,
            poi_id=pois[1].id,
            title="Milan's Green Heart",
            content="""Welcome to Giardini Pubblici Indro Montanelli, Milan's oldest and most beloved park. Created in 1784, these gardens were revolutionary - Milan's first public green space open to all citizens, not just nobility. With over 100 species of trees, this 172,000 square meter oasis offers respite from the urban bustle. The park houses treasures like the Natural History Museum with its famous dinosaur skeletons, and the Planetarium, where Milanese have gazed at stars since 1930.""",
            content_type=ContentType.CULTURAL,
            prompt_used="Generate a cultural story about Giardini Pubblici",
            model_version="claude-4-opus-20240229",
            tokens_used=190,
            generation_time=1.9,
            is_favorite=False,
            is_read=True,
            read_at=datetime.utcnow() - timedelta(minutes=30),
            user_rating=4,
            is_cached=True,
            cache_expires_at=datetime.utcnow() + timedelta(days=30)
        ),
        Story(
            user_id=users[1].id,
            location_id=None,
            poi_id=pois[5].id,
            title="Must-Try: Luini Panzerotti",
            content="""Just steps away, you'll find Luini - a Milan institution since 1949. This tiny bakery serves what many consider the best panzerotti in the city: golden, crispy pockets of fried dough filled with oozing mozzarella and tomato. Founded by Giuseppina Luini, this family business still uses the original recipe. They make over 2,000 panzerotti daily, and the line of locals and tourists speaks volumes. Get there early - they often sell out! This is authentic Milanese street food at its finest.""",
            content_type=ContentType.RECOMMENDATION,
            prompt_used="Generate a restaurant recommendation for Luini",
            model_version="claude-4-opus-20240229",
            tokens_used=140,
            generation_time=1.4,
            is_favorite=True,
            is_read=False,
            user_rating=None,
            is_cached=False
        ),
        Story(
            user_id=users[0].id,
            location_id=locations[2].id,
            poi_id=pois[2].id,
            title="Napoleon's Milanese Palace",
            content="""Villa Reale stands before you - a Neoclassical masterpiece completed in 1796. Built for Count Ludovico Barbiano di Belgioioso, it soon became Napoleon's residence when he ruled as viceroy of the Kingdom of Italy from 1802 to 1814. The villa's English garden was revolutionary for Milan, introducing a more natural landscape style. Today, it houses the Gallery of Modern Art, where you can admire 19th-century Italian masterpieces. The villa's elegant proportions and harmonious design make it one of Milan's architectural gems.""",
            content_type=ContentType.ARCHITECTURAL,
            prompt_used="Generate an architectural story about Villa Reale",
            model_version="claude-4-opus-20240229",
            tokens_used=180,
            generation_time=1.8,
            is_favorite=False,
            is_read=True,
            read_at=datetime.utcnow(),
            user_rating=5,
            is_cached=True,
            cache_expires_at=datetime.utcnow() + timedelta(days=30)
        ),
        Story(
            user_id=users[2].id,
            location_id=locations[3].id,
            poi_id=pois[3].id,
            title="Shopping Marathon at Corso Buenos Aires",
            content="""You're standing on Corso Buenos Aires, one of the longest and busiest shopping streets in Europe! With 1.6 kilometers of shops - over 350 in total - this street sees up to 100,000 visitors on busy days. Named in 1895 after Argentina's capital (when Italian-Argentine relations were strong), it's a shopaholic's paradise. From international brands to local boutiques, from electronics to fashion, you'll find everything here. Pro tip: Visit on weekdays to avoid the weekend crowds!""",
            content_type=ContentType.FUNNY,
            prompt_used="Generate an interesting story about Corso Buenos Aires",
            model_version="claude-4-opus-20240229",
            tokens_used=150,
            generation_time=1.5,
            is_favorite=False,
            is_read=False,
            user_rating=None,
            is_cached=False
        )
    ]

    db.add_all(stories)
    db.commit()


def seed_database() -> None:
    """
    Main function to seed the database with test data.
    """
    db = SessionLocal()

    try:
        print("Creating test users...")
        users = create_test_users(db)
        print(f"  Created {len(users)} users")

        print("Creating user preferences...")
        create_user_preferences(db, users)
        print(f"  Created preferences for {len(users)} users")

        print("Creating sample locations...")
        locations = create_sample_locations(db, users)
        print(f"  Created {len(locations)} locations")

        print("Creating sample POIs...")
        pois = create_sample_pois(db)
        print(f"  Created {len(pois)} POIs")

        print("Creating sample stories...")
        create_sample_stories(db, users, locations, pois)
        print("  Created sample stories")

        print("\nSeed data summary:")
        print(f"  Users: {len(users)}")
        print(f"  Locations: {len(locations)}")
        print(f"  POIs: {len(pois)}")
        print(f"  Stories: 5")

    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
