# Text-to-Speech (TTS) Service

Audio narration service for Storyteller - converting stories into natural speech for hands-free listening during walks.

## Responsibilities

- Convert story text to natural-sounding speech audio
- Support multiple voices and languages (Italian, English, etc.)
- Audio file caching to reduce API costs and improve performance
- Streaming support for long-form content
- Voice customization (speed, pitch, volume)
- Hands-free narration delivery during walks
- Integration with user preferences for personalized audio experience

## Tech Stack

### Primary TTS Provider Options

1. **Google Cloud Text-to-Speech** (Recommended)
   - High-quality Italian voice support
   - WaveNet and Neural2 voices
   - SSML support for natural pauses
   - Competitive pricing with free tier

2. **ElevenLabs**
   - State-of-the-art natural voices
   - Emotion and tone control
   - Great multilingual support
   - Higher cost, premium quality

3. **Azure Speech Services**
   - Neural voices
   - Custom voice training
   - Real-time streaming
   - Microsoft ecosystem integration

4. **AWS Polly**
   - Neural voices
   - SSML support
   - AWS ecosystem benefits
   - Good Italian support

### Supporting Technologies

- **Audio Format**: MP3 (mobile-friendly, good compression)
- **Async Processing**: `aiohttp`, `asyncio`
- **Audio Manipulation**: `pydub` (optional, for post-processing)
- **Caching**: Local filesystem or S3/Cloud Storage
- **Streaming**: Chunked audio delivery for large texts

## Features

### Core Functionality

- **Text to Audio Conversion**
  - Convert story text to MP3 audio files
  - Support for multiple languages
  - Automatic language detection
  - SSML formatting for natural speech

- **Voice Selection**
  - Multiple voice profiles (male/female, age ranges)
  - Language-specific voices (Italian, English, Spanish, etc.)
  - Voice characteristics preview
  - User-selectable preferred voices

- **Speech Customization**
  - Speech rate control (0.5x - 2.0x speed)
  - Pitch adjustment
  - Volume normalization
  - Speaking style (conversational, news, storytelling)

- **Audio Caching**
  - Cache generated audio files by story ID
  - Automatic cache expiration based on story updates
  - Storage optimization (compression, cleanup)
  - CDN integration for fast delivery

- **Streaming Support**
  - Real-time audio streaming for long stories
  - Chunk-based delivery
  - Progressive playback
  - Buffer management

### Advanced Features

- **SSML Support**
  - Emphasis tags for important words
  - Pause control for natural rhythm
  - Prosody adjustment (pitch, rate, volume)
  - Break tags for sentence boundaries

- **Multi-Language Support**
  - Italian (it-IT) - Primary
  - English (en-US, en-GB)
  - Spanish (es-ES)
  - French (fr-FR)
  - German (de-DE)

- **Quality Options**
  - High quality (for favorites/repeated listening)
  - Standard quality (for on-the-go)
  - Low quality (for data saving)

## Integration Points

### Input
- **Story content** from LLM component
- **User preferences** from Database (preferred voice, speed, language)
- **Story metadata** (length, type, importance)

### Output
- **Audio file URL** or stream endpoint
- **Audio metadata** (duration, file size, format)
- **Generation metrics** (time, cost, cache hit/miss)

### Backend API Endpoints
```
GET  /stories/{story_id}/audio    # Get audio for a story
POST /stories/{story_id}/audio    # Generate audio for a story
GET  /tts/voices                   # List available voices
POST /tts/preview                  # Preview voice with sample text
GET  /tts/preferences              # Get user TTS preferences
PUT  /tts/preferences              # Update user TTS preferences
```

### Database Integration
Story model additions:
- `audio_url`: Link to generated audio file
- `audio_generated_at`: Timestamp of audio generation
- `audio_duration`: Duration in seconds
- `voice_used`: Voice ID/name used

UserPreference additions:
- `audio_enabled`: Enable/disable audio narration
- `preferred_voice`: Default voice selection
- `speech_rate`: Playback speed (0.5-2.0)

## Development

### Setup

```bash
# Install dependencies
pip install google-cloud-texttospeech aiohttp pydub

# Set environment variables
export TTS_PROVIDER=google
export GOOGLE_TTS_API_KEY=your_api_key_here
export TTS_CACHE_DIR=./audio_cache
export TTS_CACHE_ENABLED=true
```

### Configuration

Create `.env` file:
```env
# TTS Provider Configuration
TTS_PROVIDER=google  # google, elevenlabs, azure, aws
GOOGLE_TTS_API_KEY=your_api_key
TTS_CACHE_ENABLED=true
TTS_CACHE_DIR=./audio_cache
TTS_CACHE_EXPIRY_DAYS=30

# Voice Defaults
DEFAULT_VOICE_IT=it-IT-Neural2-A  # Italian female
DEFAULT_VOICE_EN=en-US-Neural2-F  # English female
DEFAULT_SPEECH_RATE=1.0
DEFAULT_AUDIO_FORMAT=mp3
```

### Usage Example

```python
from tts import TTSService, Voice, AudioConfig

# Initialize service
tts = TTSService(provider="google", api_key="your_key")

# Generate audio
audio_url = await tts.generate_audio(
    text="Benvenuto a Porta Venezia, uno dei portali storici di Milano.",
    language="it-IT",
    voice="it-IT-Neural2-A",
    speed=1.0
)

# List available voices
voices = await tts.list_voices(language="it-IT")
for voice in voices:
    print(f"{voice.name}: {voice.gender}, {voice.description}")

# Check cache
cached = await tts.get_cached_audio(story_id=123)
if cached:
    print(f"Audio already generated: {cached}")

# Stream audio for long text
async for chunk in tts.stream_audio(
    text=long_story_text,
    voice="it-IT-Neural2-C"
):
    # Send chunk to client
    yield chunk
```

### Testing

```bash
# Run TTS service tests
python test_tts.py

# Generate test audio
python text_to_speech.py --text "Ciao Milano!" --voice it-IT-Neural2-A --output test.mp3

# Test voice listing
python text_to_speech.py --list-voices --language it-IT
```

## API Reference

### TTSService Class

```python
class TTSService:
    def __init__(self, provider: str, api_key: str, cache_dir: str = None)
    
    async def generate_audio(
        self,
        text: str,
        language: str = "it-IT",
        voice: str = None,
        speed: float = 1.0,
        pitch: float = 0.0,
        output_format: str = "mp3"
    ) -> str  # Returns audio URL
    
    async def list_voices(
        self,
        language: str = None
    ) -> List[Voice]
    
    async def get_cached_audio(
        self,
        story_id: int
    ) -> Optional[str]  # Returns cached audio URL if exists
    
    async def cache_audio(
        self,
        story_id: int,
        audio_data: bytes
    ) -> str  # Returns cached audio URL
    
    async def stream_audio(
        self,
        text: str,
        voice: str,
        chunk_size: int = 4096
    ) -> AsyncIterator[bytes]
    
    def get_audio_duration(
        self,
        text: str,
        speed: float = 1.0
    ) -> float  # Estimate duration in seconds
```

### Voice Class

```python
@dataclass
class Voice:
    name: str                    # Voice ID (e.g., "it-IT-Neural2-A")
    language: str               # Language code (e.g., "it-IT")
    gender: str                 # "MALE", "FEMALE", "NEUTRAL"
    description: str            # Human-readable description
    sample_rate: int = 24000    # Audio sample rate
    quality: str = "standard"   # "standard", "premium", "wavenet"
```

## Cost Optimization

### Caching Strategy
- Cache all generated audio files
- Set expiration based on story update frequency
- Use content-based hashing for cache keys
- Implement LRU eviction for storage limits

### Batch Processing
- Generate audio for popular POIs in advance
- Batch process stories during off-peak hours
- Pre-generate for frequently visited locations

### Quality Tiers
- Standard quality for initial generation
- High quality on-demand for favorites
- Lower quality for previews

## Performance Considerations

- **Generation Time**: 2-5 seconds for typical story (200 words)
- **File Size**: ~100KB per minute of audio (MP3, 64kbps)
- **Cache Hit Rate**: Target 80%+ for repeated locations
- **Streaming Latency**: <500ms for first chunk

## Troubleshooting

### Common Issues

1. **"API key invalid"**
   - Check TTS_PROVIDER environment variable
   - Verify API key is correct and has TTS permissions

2. **"Language not supported"**
   - List available voices with `list_voices()`
   - Check language code format (e.g., "it-IT" not "it")

3. **"Cache directory not writable"**
   - Check TTS_CACHE_DIR permissions
   - Ensure directory exists and has write access

4. **"Audio quality poor"**
   - Try WaveNet or Neural2 voices (higher quality)
   - Adjust speech rate (slower = clearer)
   - Check SSML formatting for proper pauses

## Future Enhancements

- [ ] Custom voice training for branded experience
- [ ] Emotion detection and appropriate voice modulation
- [ ] Background music/ambient sounds for immersion
- [ ] Voice cloning for personalized narration
- [ ] Multilingual mixing (code-switching support)
- [ ] Real-time voice synthesis with WebSocket
- [ ] Voice effects (echo, reverb for specific locations)
- [ ] Accessibility features (dyslexia-friendly pacing)

## Resources

- [Google Cloud TTS Documentation](https://cloud.google.com/text-to-speech/docs)
- [ElevenLabs API Docs](https://docs.elevenlabs.io/)
- [Azure Speech Service](https://learn.microsoft.com/azure/cognitive-services/speech-service/)
- [AWS Polly Developer Guide](https://docs.aws.amazon.com/polly/)
- [SSML Reference](https://www.w3.org/TR/speech-synthesis11/)
