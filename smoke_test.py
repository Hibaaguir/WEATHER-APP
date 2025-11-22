#!/usr/bin/env python3
import requests
import time
import sys

def smoke_test():
    max_retries = 5
    retry_delay = 3
    
    for i in range(max_retries):
        try:
            print(f"Tentative {i+1}/{max_retries}...")
            
            # Test health endpoint
            health_response = requests.get('http://weather-app:5000/health', timeout=10)
            if health_response.status_code == 200:
                health_data = health_response.json()
                if health_data.get('status') == 'healthy':
                    print("✅ Health check PASSED")
                else:
                    print("❌ Health check FAILED - Status not healthy")
                    return False
            else:
                print(f"❌ Health check FAILED - Status code: {health_response.status_code}")
                return False
            
            # Test API endpoint
            api_response = requests.get('http://weather-app:5000/api/weather/Paris', timeout=10)
            if api_response.status_code == 200:
                api_data = api_response.json()
                if all(key in api_data for key in ['city', 'temperature', 'condition']):
                    print("✅ API test PASSED")
                else:
                    print("❌ API test FAILED - Missing required fields")
                    return False
            else:
                print(f"❌ API test FAILED - Status code: {api_response.status_code}")
                return False
            
            # Test main page
            main_response = requests.get('http://weather-app:5000/', timeout=10)
            if main_response.status_code == 200:
                print("✅ Main page test PASSED")
            else:
                print(f"❌ Main page test FAILED - Status code: {main_response.status_code}")
                return False
            
            print("🎉 Tous les tests smoke PASSED!")
            return True
            
        except requests.exceptions.ConnectionError:
            print(f"🌐 Service non disponible, nouvel essai dans {retry_delay} secondes...")
            time.sleep(retry_delay)
        except requests.exceptions.Timeout:
            print(f"⏰ Timeout, nouvel essai dans {retry_delay} secondes...")
            time.sleep(retry_delay)
        except Exception as e:
            print(f"❌ Erreur inattendue: {e}")
            return False
    
    print("❌ Échec après tous les essais")
    return False

if __name__ == '__main__':
    success = smoke_test()
    sys.exit(0 if success else 1)