from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from unittest.mock import patch

class UnifiedApiTests(TestCase):
    def setUp(self):
        self.url = reverse('weather-v1')

    @patch('integrator.services.requests.get')
    def test_get_weather_summary_mocked_success(self, mock_get):
        """Test Case: Successful API call using MOCKED data (Requirement VII)"""
        
        # 1. Define what the "Fake" APIs should return
        mock_country_json = [{
            'name': {'common': 'Philippines'},
            'capital': ['Manila'],
            'population': 115559000,
            'latlng': [13.0, 122.0]
        }]
        
        mock_weather_json = {
            'current_weather': {
                'temperature': 30.5
            }
        }

        # 2. Tell the mock to return these values in order
        # First call is Country API, second is Weather API
        mock_get.side_effect = [
            type('Response', (object,), {'status_code': 200, 'json': lambda: mock_country_json}),
            type('Response', (object,), {'status_code': 200, 'json': lambda: mock_weather_json})
        ]

        # 3. Call your endpoint
        response = self.client.get(f"{self.url}?country=Philippines")
        
        # 4. Assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['country_name'], 'Philippines')
        self.assertEqual(response.data['current_temp_celsius'], 30.5)
        self.assertEqual(response.data['population_count'], "115,559,000")
        
        # Verify that we actually "mocked" it (requests.get was called twice)
        self.assertEqual(mock_get.call_count, 2)