import os
import json
import re
from typing import Dict, Optional, List
from constants import ROOT_PATH


class LocalisationService:
    """Service for handling message localisation with language detection."""

    def __init__(self):
        self.languages: Dict[str, Dict[str, str]] = {}
        self.default_language = 'en'
        self._load_languages()

    def _load_languages(self):
        """Load all language files from the localisation directory."""
        localisation_dir = os.path.join(ROOT_PATH, 'src', 'localisation', 'languages')
        
        if not os.path.exists(localisation_dir):
            try:
                os.makedirs(localisation_dir, exist_ok=True)
            except (OSError, PermissionError) as e:
                print(f"Warning: Could not create localisation directory {localisation_dir}: {e}")
            return

        for filename in os.listdir(localisation_dir):
            if filename.endswith('.json'):
                language_code = filename[:-5]  # Remove .json extension
                file_path = os.path.join(localisation_dir, filename)
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        self.languages[language_code] = json.load(f)
                except (json.JSONDecodeError, IOError) as e:
                    print(f"Error loading language file {filename}: {e}")

    def detect_language(self, accept_language_header: Optional[str] = None) -> str:
        """
        Detect preferred language from Accept-Language header.
        Falls back to default language if no match found.
        """
        if not accept_language_header:
            return self.default_language

        # Parse Accept-Language header (e.g., "en-US,en;q=0.9,fr;q=0.8")
        languages = []
        for lang_part in accept_language_header.split(','):
            lang_part = lang_part.strip()
            if ';q=' in lang_part:
                lang, quality = lang_part.split(';q=', 1)
                try:
                    quality = float(quality)
                except ValueError:
                    quality = 1.0
            else:
                lang = lang_part
                quality = 1.0
            
            # Extract primary language code (e.g., 'en' from 'en-US')
            primary_lang = lang.split('-')[0].lower()
            languages.append((primary_lang, quality))

        # Sort by quality score (highest first)
        languages.sort(key=lambda x: x[1], reverse=True)

        # Find first available language
        for lang_code, _ in languages:
            if lang_code in self.languages:
                return lang_code

        return self.default_language

    def translate(self, message_key: str, language: str = None, **kwargs) -> str:
        """
        Translate a message key to the specified language with parameter substitution.
        
        Args:
            message_key: The key to translate
            language: Target language code (auto-detected if None)
            **kwargs: Parameters for string interpolation
        
        Returns:
            Translated and formatted message
        """
        if language is None:
            language = self.default_language

        # Get the message template
        if language not in self.languages:
            language = self.default_language

        if language not in self.languages:
            # Fallback if even default language is not loaded
            return f"[MISSING_TRANSLATION:{message_key}]"

        message_template = self.languages[language].get(message_key)
        if message_template is None:
            # Try default language if key not found
            if language != self.default_language:
                return self.translate(message_key, self.default_language, **kwargs)
            return f"[MISSING_KEY:{message_key}]"

        # Perform parameter substitution
        try:
            return message_template.format(**kwargs)
        except (KeyError, ValueError) as e:
            # Fallback if parameter substitution fails
            return f"{message_template} [FORMAT_ERROR:{e}]"

    def get_available_languages(self) -> List[str]:
        """Return list of available language codes."""
        return list(self.languages.keys())


# Global instance
_localisation_service = None


def get_localisation_service() -> LocalisationService:
    """Get the global localisation service instance."""
    global _localisation_service
    if _localisation_service is None:
        _localisation_service = LocalisationService()
    return _localisation_service