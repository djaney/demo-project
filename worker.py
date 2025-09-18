import requests
import os
import time

API_URL = os.environ.get('API_URL')

while API_URL:
    try:
        requests.post(f"{API_URL}/verify")
        print("Verified")
    except KeyboardInterrupt:
        print("Bye...")
        break
    time.sleep(1)
