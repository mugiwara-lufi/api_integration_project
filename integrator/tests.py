from django.test import TestCase

class IntegrationTest(TestCase):
    def test_api_success(self):
        response = self.client.get('/api/v1/country-weather-summary/?country=Philippines')
        self.assertEqual(response.status_code, 200)
        self.assertIn('current_temp_celsius', response.json())