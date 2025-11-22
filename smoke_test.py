#!/usr/bin/env python3
import requests
import sys
import time

def smoke_test():
    try:
        # Attendre que l'application démarre
        time.sleep(10)
        
        # Tester l'endpoint principal
        response = requests.get('http://localhost:5000/health', timeout=30)
        
        if response.status_code == 200:
            print("✅ Smoke test PASSED - Application is responding")
            return True
        else:
            print(f"❌ Smoke test FAILED - Status code: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Smoke test FAILED - Error: {str(e)}")
        return False

if __name__ == "__main__":
    success = smoke_test()
    sys.exit(0 if success else 1)