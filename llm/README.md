# LLM Integration

Claude API integration for generating personalized content.

## Responsibilities

- Generate stories based on location and user profile
- Create historical narratives
- Produce fun facts and recommendations
- Context-aware content generation
- Cache management for generated content
- Prompt engineering and optimization

## Tech Stack

- Anthropic Claude SDK
- Prompt caching
- Async API calls

## Features

### Story Generation
- Historical stories about locations
- Personal interest-based narratives
- Cultural context stories
- Local legends and folklore

### Content Types
- **Historical**: Facts and stories about historical events
- **Cultural**: Information about local culture and traditions
- **Recreational**: Things to do, restaurants, activities
- **Educational**: Learning opportunities in the area

## Prompt Strategy

Content is generated using:
- User profile (interests, age, preferences)
- Current location coordinates
- Nearby POI information
- Historical context from database
- Previous interactions

## Development

```bash
cd llm
python story_generator.py
```
