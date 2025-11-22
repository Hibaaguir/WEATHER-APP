import unittest
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from app.main import app

class TestWeatherApp(unittest.TestCase):
    
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
    
    def test_index_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Weather App', response.data)
    
    def test_health_endpoint(self):
        response = self.app.get('/health')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'healthy', response.data)
    
    def test_weather_api(self):
        response = self.app.get('/api/weather/Paris')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'temperature', response.data)
    
    def test_weather_api_invalid_city(self):
        response = self.app.get('/api/weather/InvalidCity')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()