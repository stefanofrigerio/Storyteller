"""
Text-to-Speech service implementation.

Converts text stories into natural speech audio using cloud TTS providers.
"""
import os
import asyncio
import hashlib
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, AsyncIterator
from datetime import datetime, timedelta

try:
    from google.cloud import texttospeech
    GOOGLE_TTS_AVAILABLE = True
except ImportError:
    GOOGLE_TTS_AVAILABLE = False


@dataclass
class Voice:
    """Represents a TTS voice option."""
    name: str                    # Voice ID (e.g., "it-IT-Neural2-A")
    language: str               # Language code (e.g., "it-IT")
    gender: str                 # "MALE", "FEMALE", "NEUTRAL"
    description: str            # Human-readable description
    sample_rate: int = 24000    # Audio sample rate
    quality: str = "standard"   # "standard", "premium", "wavenet", "neural2"


@dataclass
class AudioConfig:
    """Configuration for audio generation."""
    language: str = "it-IT"
    voice: str = "it-IT-Neural2-A"
    speed: float = 1.0          # 0.5 - 2.0
    pitch: float = 0.0          # -20.0 to 20.0
    volume_gain_db: float = 0.0
    output_format: str = "mp3"  # mp3, wav, ogg


class TTSService:
    """
    Text-to-Speech service for generating audio from text.

    Supports multiple TTS providers with caching and streaming capabilities.
    """

    def __init__(
        self,
        provider: str = "google",
        api_key: Optional[str] = None,
        cache_dir: Optional[str] = None,
        cache_enabled: bool = True
    ):
        """
        Initialize TTS service.

        Args:
            provider: TTS provider ("google", "elevenlabs", "azure", "aws")
            api_key: API key for the provider
            cache_dir: Directory for audio cache
            cache_enabled: Enable/disable audio caching
        """
        self.provider = provider.lower()
        self.api_key = api_key or os.getenv(f"{provider.upper()}_TTS_API_KEY")
        self.cache_enabled = cache_enabled

        # Setup cache directory
        if cache_dir:
            self.cache_dir = Path(cache_dir)
        else:
            self.cache_dir = Path(os.getenv("TTS_CACHE_DIR", "./audio_cache"))

        if self.cache_enabled:
            self.cache_dir.mkdir(parents=True, exist_ok=True)

        # Initialize provider client
        self._init_provider()

    def _init_provider(self):
        """Initialize the TTS provider client."""
        if self.provider == "google":
            if not GOOGLE_TTS_AVAILABLE:
                raise ImportError(
                    "Google Cloud TTS not available. "
                    "Install with: pip install google-cloud-texttospeech"
                )
            self.client = texttospeech.TextToSpeechClient()
        elif self.provider == "elevenlabs":
            raise NotImplementedError("ElevenLabs provider not yet implemented")
        elif self.provider == "azure":
            raise NotImplementedError("Azure Speech provider not yet implemented")
        elif self.provider == "aws":
            raise NotImplementedError("AWS Polly provider not yet implemented")
        else:
            raise ValueError(f"Unsupported TTS provider: {self.provider}")

    async def generate_audio(
        self,
        text: str,
        language: str = "it-IT",
        voice: Optional[str] = None,
        speed: float = 1.0,
        pitch: float = 0.0,
        output_format: str = "mp3"
    ) -> str:
        """
        Generate audio from text.

        Args:
            text: Text to convert to speech
            language: Language code (e.g., "it-IT", "en-US")
            voice: Voice ID (if None, uses default for language)
            speed: Speech rate (0.5 - 2.0)
            pitch: Pitch adjustment (-20.0 to 20.0)
            output_format: Output format ("mp3", "wav", "ogg")

        Returns:
            URL or file path to generated audio
        """
        # Check cache first
        cache_key = self._get_cache_key(text, voice or language, speed, pitch)
        cached_path = await self.get_cached_audio(cache_key)
        if cached_path:
            return cached_path

        # Generate audio using provider
        if self.provider == "google":
            audio_data = await self._generate_google_tts(
                text, language, voice, speed, pitch
            )
        else:
            raise NotImplementedError(f"Provider {self.provider} not implemented")

        # Cache the audio
        if self.cache_enabled:
            audio_path = await self.cache_audio(cache_key, audio_data)
            return str(audio_path)

        # Return temporary path if caching disabled
        temp_path = self.cache_dir / f"temp_{cache_key}.{output_format}"
        with open(temp_path, "wb") as f:
            f.write(audio_data)
        return str(temp_path)

    async def _generate_google_tts(
        self,
        text: str,
        language: str,
        voice: Optional[str],
        speed: float,
        pitch: float
    ) -> bytes:
        """Generate audio using Google Cloud TTS."""
        # Set voice
        if voice:
            voice_params = texttospeech.VoiceSelectionParams(
                name=voice,
                language_code=language
            )
        else:
            voice_params = texttospeech.VoiceSelectionParams(
                language_code=language
            )

        # Configure audio
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3,
            speaking_rate=speed,
            pitch=pitch
        )

        # Generate
        synthesis_input = texttospeech.SynthesisInput(text=text)

        # Run in executor to avoid blocking
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            lambda: self.client.synthesize_speech(
                input=synthesis_input,
                voice=voice_params,
                audio_config=audio_config
            )
        )

        return response.audio_content

    async def list_voices(
        self,
        language: Optional[str] = None
    ) -> List[Voice]:
        """
        List available voices.

        Args:
            language: Filter by language code (e.g., "it-IT")

        Returns:
            List of available Voice objects
        """
        if self.provider == "google":
            return await self._list_google_voices(language)
        else:
            raise NotImplementedError(f"Provider {self.provider} not implemented")

    async def _list_google_voices(self, language: Optional[str]) -> List[Voice]:
        """List Google Cloud TTS voices."""
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            self.client.list_voices
        )

        voices = []
        for voice in response.voices:
            # Filter by language if specified
            if language and not any(lang.startswith(language) for lang in voice.language_codes):
                continue

            # Determine quality from name
            quality = "standard"
            if "Wavenet" in voice.name:
                quality = "wavenet"
            elif "Neural2" in voice.name:
                quality = "neural2"
            elif "Studio" in voice.name:
                quality = "premium"

            voices.append(Voice(
                name=voice.name,
                language=voice.language_codes[0],
                gender=voice.ssml_gender.name,
                description=f"{voice.name} ({voice.language_codes[0]})",
                quality=quality
            ))

        return voices

    async def get_cached_audio(self, cache_key: str) -> Optional[str]:
        """
        Get cached audio file if it exists.

        Args:
            cache_key: Cache key (hash)

        Returns:
            Path to cached audio file, or None if not cached
        """
        if not self.cache_enabled:
            return None

        cache_path = self.cache_dir / f"{cache_key}.mp3"
        if cache_path.exists():
            return str(cache_path)
        return None

    async def cache_audio(self, cache_key: str, audio_data: bytes) -> Path:
        """
        Cache audio data to disk.

        Args:
            cache_key: Cache key (hash)
            audio_data: Audio file bytes

        Returns:
            Path to cached file
        """
        cache_path = self.cache_dir / f"{cache_key}.mp3"

        # Write audio data
        with open(cache_path, "wb") as f:
            f.write(audio_data)

        return cache_path

    async def stream_audio(
        self,
        text: str,
        voice: str,
        chunk_size: int = 4096
    ) -> AsyncIterator[bytes]:
        """
        Stream audio in chunks (for large texts).

        Args:
            text: Text to convert
            voice: Voice ID
            chunk_size: Size of audio chunks

        Yields:
            Audio data chunks
        """
        # For now, generate full audio and chunk it
        # Future: implement true streaming with provider support
        audio_data = await self.generate_audio(text=text, voice=voice)

        # Read and yield chunks
        with open(audio_data, "rb") as f:
            while chunk := f.read(chunk_size):
                yield chunk

    def get_audio_duration(self, text: str, speed: float = 1.0) -> float:
        """
        Estimate audio duration in seconds.

        Args:
            text: Input text
            speed: Speech rate

        Returns:
            Estimated duration in seconds
        """
        # Average speaking rate: ~150 words per minute
        words = len(text.split())
        base_duration = (words / 150.0) * 60.0  # seconds

        # Adjust for speed
        adjusted_duration = base_duration / speed

        return adjusted_duration

    def _get_cache_key(
        self,
        text: str,
        voice: str,
        speed: float,
        pitch: float
    ) -> str:
        """Generate cache key from parameters."""
        key_string = f"{text}|{voice}|{speed}|{pitch}"
        return hashlib.md5(key_string.encode()).hexdigest()


# CLI interface for testing
if __name__ == "__main__":
    import sys

    async def main():
        if len(sys.argv) < 2:
            print("Usage: python text_to_speech.py <text> [--voice <voice_id>] [--list-voices]")
            sys.exit(1)

        tts = TTSService(provider="google")

        if "--list-voices" in sys.argv:
            language = sys.argv[sys.argv.index("--list-voices") + 1] if len(sys.argv) > sys.argv.index("--list-voices") + 1 else "it-IT"
            voices = await tts.list_voices(language=language)
            print(f"\nAvailable voices for {language}:")
            for v in voices:
                print(f"  {v.name:30} {v.gender:8} ({v.quality})")
        else:
            text = sys.argv[1]
            voice = sys.argv[sys.argv.index("--voice") + 1] if "--voice" in sys.argv else None

            print(f"Generating audio for: {text[:50]}...")
            audio_path = await tts.generate_audio(text=text, voice=voice)
            print(f"Audio saved to: {audio_path}")

            duration = tts.get_audio_duration(text)
            print(f"Estimated duration: {duration:.1f} seconds")

    asyncio.run(main())
