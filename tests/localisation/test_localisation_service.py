import unittest
import tempfile
import os
import json
from unittest.mock import patch, mock_open
from src.localisation.localisation_service import LocalisationService, get_localisation_service


class TestLocalisationService(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures with mock language data."""
        self.mock_languages = {
            'en': {
                'patient_not_found': 'patient not found',
                'new_patient_added': 'new patient added: {nhs_number}',
                'invalid_name': 'Invalid name. Must be at least 3 characters',
                'missing_required_field': 'Missing required field: {field}'
            },
            'fr': {
                'patient_not_found': 'patient non trouvé',
                'new_patient_added': 'nouveau patient ajouté : {nhs_number}',
                'invalid_name': 'Nom invalide. Doit comporter au moins 3 caractères',
                'missing_required_field': 'Champ obligatoire manquant : {field}'
            },
            'es': {
                'patient_not_found': 'paciente no encontrado',
                'new_patient_added': 'nuevo paciente agregado: {nhs_number}'
                # Note: missing some translations to test fallback behavior
            }
        }

    def test_init_creates_service_with_default_language(self):
        """Test that LocalisationService initializes with default language."""
        with patch('src.localisation.localisation_service.os.path.exists', return_value=False):
            service = LocalisationService()
            self.assertEqual(service.default_language, 'en')
            self.assertEqual(service.languages, {})

    def test_detect_language_with_no_header(self):
        """Test language detection when no Accept-Language header is provided."""
        with patch('src.localisation.localisation_service.os.path.exists', return_value=False):
            service = LocalisationService()
            detected = service.detect_language(None)
            self.assertEqual(detected, 'en')

    def test_detect_language_with_simple_header(self):
        """Test language detection with simple Accept-Language header."""
        with patch('src.localisation.localisation_service.os.path.exists', return_value=False):
            service = LocalisationService()
            service.languages = {'en': {}, 'fr': {}}
            
            # Test French preference
            detected = service.detect_language('fr')
            self.assertEqual(detected, 'fr')
            
            # Test English preference
            detected = service.detect_language('en')
            self.assertEqual(detected, 'en')

    def test_detect_language_with_quality_values(self):
        """Test language detection with quality values in Accept-Language header."""
        with patch('src.localisation.localisation_service.os.path.exists', return_value=False):
            service = LocalisationService()
            service.languages = {'en': {}, 'fr': {}, 'es': {}}
            
            # French has highest priority
            detected = service.detect_language('en;q=0.8,fr;q=0.9,es;q=0.7')
            self.assertEqual(detected, 'fr')
            
            # English has highest priority
            detected = service.detect_language('en;q=0.9,fr;q=0.8,es;q=0.7')
            self.assertEqual(detected, 'en')

    def test_detect_language_with_locale_codes(self):
        """Test language detection with locale codes (e.g., en-US)."""
        with patch('src.localisation.localisation_service.os.path.exists', return_value=False):
            service = LocalisationService()
            service.languages = {'en': {}, 'fr': {}}
            
            # Should extract 'en' from 'en-US'
            detected = service.detect_language('en-US,en;q=0.9')
            self.assertEqual(detected, 'en')
            
            # Should extract 'fr' from 'fr-FR'
            detected = service.detect_language('fr-FR,fr;q=0.9')
            self.assertEqual(detected, 'fr')

    def test_detect_language_fallback_to_default(self):
        """Test that language detection falls back to default when no match found."""
        with patch('src.localisation.localisation_service.os.path.exists', return_value=False):
            service = LocalisationService()
            service.languages = {'en': {}, 'fr': {}}
            
            # Request German, but it's not available
            detected = service.detect_language('de,es;q=0.8')
            self.assertEqual(detected, 'en')  # Should fallback to default

    def test_translate_with_existing_key(self):
        """Test translation of existing message key."""
        with patch('src.localisation.localisation_service.os.path.exists', return_value=False):
            service = LocalisationService()
            service.languages = self.mock_languages
            
            # Test English translation
            result = service.translate('patient_not_found', 'en')
            self.assertEqual(result, 'patient not found')
            
            # Test French translation
            result = service.translate('patient_not_found', 'fr')
            self.assertEqual(result, 'patient non trouvé')

    def test_translate_with_parameters(self):
        """Test translation with parameter substitution."""
        with patch('src.localisation.localisation_service.os.path.exists', return_value=False):
            service = LocalisationService()
            service.languages = self.mock_languages
            
            # Test English with parameters
            result = service.translate('new_patient_added', 'en', nhs_number='1234567890')
            self.assertEqual(result, 'new patient added: 1234567890')
            
            # Test French with parameters
            result = service.translate('new_patient_added', 'fr', nhs_number='1234567890')
            self.assertEqual(result, 'nouveau patient ajouté : 1234567890')

    def test_translate_missing_key_fallback_to_default(self):
        """Test translation fallback when key exists in default but not target language."""
        with patch('src.localisation.localisation_service.os.path.exists', return_value=False):
            service = LocalisationService()
            service.languages = self.mock_languages
            
            # 'missing_required_field' exists in English but not Spanish
            result = service.translate('missing_required_field', 'es', field='name')
            self.assertEqual(result, 'Missing required field: name')  # Should fallback to English

    def test_translate_missing_key_completely(self):
        """Test translation when key doesn't exist in any language."""
        with patch('src.localisation.localisation_service.os.path.exists', return_value=False):
            service = LocalisationService()
            service.languages = self.mock_languages
            
            result = service.translate('nonexistent_key', 'en')
            self.assertEqual(result, '[MISSING_KEY:nonexistent_key]')

    def test_translate_missing_language(self):
        """Test translation when requested language doesn't exist."""
        with patch('src.localisation.localisation_service.os.path.exists', return_value=False):
            service = LocalisationService()
            service.languages = self.mock_languages
            
            result = service.translate('patient_not_found', 'de')  # German not available
            self.assertEqual(result, 'patient not found')  # Should fallback to English

    def test_translate_parameter_format_error(self):
        """Test translation when parameter substitution fails."""
        with patch('src.localisation.localisation_service.os.path.exists', return_value=False):
            service = LocalisationService()
            service.languages = {
                'en': {
                    'test_message': 'Hello {missing_param}'
                }
            }
            
            # Missing parameter should cause format error
            result = service.translate('test_message', 'en', provided_param='value')
            self.assertIn('[FORMAT_ERROR:', result)
            self.assertIn('Hello {missing_param}', result)

    def test_translate_no_language_loaded(self):
        """Test translation when no languages are loaded."""
        with patch('src.localisation.localisation_service.os.path.exists', return_value=False):
            service = LocalisationService()
            # No languages loaded
            
            result = service.translate('any_key', 'en')
            self.assertEqual(result, '[MISSING_TRANSLATION:any_key]')

    def test_get_available_languages(self):
        """Test getting list of available languages."""
        with patch('src.localisation.localisation_service.os.path.exists', return_value=False):
            service = LocalisationService()
            service.languages = self.mock_languages
            
            available = service.get_available_languages()
            self.assertEqual(set(available), {'en', 'fr', 'es'})

    @patch('src.localisation.localisation_service.os.listdir')
    @patch('src.localisation.localisation_service.os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_load_languages_from_files(self, mock_file, mock_exists, mock_listdir):
        """Test loading language files from filesystem."""
        mock_exists.return_value = True
        mock_listdir.return_value = ['en.json', 'fr.json', 'invalid.txt']
        
        # Mock file contents
        def mock_read_side_effect(file_path, *args, **kwargs):
            if 'en.json' in file_path:
                mock_file.return_value.read.return_value = json.dumps({'key': 'English value'})
            elif 'fr.json' in file_path:
                mock_file.return_value.read.return_value = json.dumps({'key': 'French value'})
            return mock_file.return_value
        
        mock_file.side_effect = mock_read_side_effect
        
        service = LocalisationService()
        
        # Should have loaded en and fr, but not invalid.txt
        self.assertIn('en', service.languages)
        self.assertIn('fr', service.languages)
        self.assertEqual(service.languages['en']['key'], 'English value')
        self.assertEqual(service.languages['fr']['key'], 'French value')

    def test_global_service_instance(self):
        """Test that get_localisation_service returns a singleton instance."""
        with patch('src.localisation.localisation_service.os.path.exists', return_value=False):
            service1 = get_localisation_service()
            service2 = get_localisation_service()
            
            # Should be the same instance
            self.assertIs(service1, service2)


class TestLocalisationServiceEdgeCases(unittest.TestCase):
    """Test edge cases and error conditions for LocalisationService."""

    def test_invalid_json_file_handling(self):
        """Test handling of invalid JSON in language files."""
        with patch('src.localisation.localisation_service.os.path.exists', return_value=True), \
             patch('src.localisation.localisation_service.os.listdir', return_value=['invalid.json']), \
             patch('builtins.open', mock_open(read_data='invalid json content')):
            
            # Should not crash, should handle the error gracefully
            service = LocalisationService()
            self.assertEqual(service.languages, {})

    def test_malformed_accept_language_header(self):
        """Test handling of malformed Accept-Language headers."""
        with patch('src.localisation.localisation_service.os.path.exists', return_value=False):
            service = LocalisationService()
            service.languages = {'en': {}, 'fr': {}}
            
            # Test various malformed headers
            malformed_headers = [
                'en;q=invalid',  # Invalid quality value
                'en;q=',         # Empty quality value
                ';q=0.8',        # Missing language
                'en;;q=0.8',     # Double semicolon
                'en,fr;q=',      # Partial quality specification
            ]
            
            for header in malformed_headers:
                with self.subTest(header=header):
                    # Should not crash and should return a reasonable default
                    detected = service.detect_language(header)
                    self.assertIn(detected, ['en', 'fr'])  # Should pick one of the available languages


if __name__ == '__main__':
    unittest.main() 