# Geolocation Service

Location intelligence and POI discovery.

## Responsibilities

- Reverse geocoding (coordinates to places)
- POI discovery from multiple sources
- Proximity detection
- Area context determination
- Map data integration
- Location caching

## Tech Stack

- OpenStreetMap Nominatim API
- Google Places API (optional)
- GeoPy for calculations
- Redis for caching

## Features

### Reverse Geocoding
Convert GPS coordinates to:
- Street address
- City, region, country
- Nearby landmarks
- Area type (residential, commercial, historical)

### POI Discovery
Find nearby:
- Historical sites
- Museums and cultural centers
- Restaurants and cafes
- Parks and nature
- Points of interest

### Context Detection
Determine area characteristics:
- Historical significance
- Cultural context
- Tourist vs local areas
- Density and activity level

## Data Sources

1. **OpenStreetMap**: Free, open-source map data
2. **Google Places**: Rich POI database (requires API key)
3. **Local database**: Cached and manually curated POIs

## Development

```bash
cd geolocation
python poi_finder.py
```

## API Usage

```python
from geolocation import GeoService

geo = GeoService()
nearby = geo.find_nearby_pois(lat=45.464, lon=9.188, radius=500)
context = geo.get_area_context(lat=45.464, lon=9.188)
```
