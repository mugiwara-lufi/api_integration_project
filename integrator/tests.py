from django.test import TestCase
from django.urls import reverse
from rest_framework import status

class UnifiedApiTests(TestCase):
    def setUp(self):
        # Requirement V: Using the versioned URL name
        self.url = reverse('weather-v1')

    def test_get_weather_summary_success(self):
        """Test Case: Successful API call with a valid country"""
        # We use a real country to ensure the external APIs return data
        response = self.client.get(f"{self.url}?country=Philippines")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Requirement III: Check if transformed fields exist
        self.assertIn('country_name', response.data)
        self.assertIn('current_temp_celsius', response.data)
        self.assertIn('is_warm', response.data)
        self.assertEqual(response.data['country_name'], 'Philippines')

    def test_missing_parameter_error(self):
        """Requirement IV: Handle 400 Bad Request (Missing Parameter)"""
        response = self.client.get(self.url) # No ?country=
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], "Missing 'country' parameter")

    def test_invalid_country_error(self):
        """Requirement IV: Handle 404 Not Found (Invalid Country)"""
        response = self.client.get(f"{self.url}?country=InvalidCountryName123")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)