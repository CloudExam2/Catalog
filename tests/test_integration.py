import os
import requests

# Use the environment variable passed from the YAML
BASE_URL = os.getenv("BASE_URL") 
if not BASE_URL:
    BASE_URL = "http://54.81.167.105" 

# If your app is at root, remove '/catalog'. 
# If it HAS a prefix, ensure this matches your main.py
ENDPOINT = f"{BASE_URL.rstrip('/')}/catalog" 

def test_catalog_persistence():
    payloads = [
        {"name": "Industrial Copper(II) Sulfate", "description": "High purity for chemical synthesis", "price": 45.50},
        {"name": "Potassium Permanganate", "description": "Oxidizing agent for laboratory use", "price": 32.00},
        {"name": "ITESO Lab Flask", "description": "250ml Borosilicate glass", "price": 15.00}
    ]

    # Batch POST items
    for item in payloads:
        # Removed the trailing slash here
        response = requests.post(ENDPOINT, json=item)
        assert response.status_code in [200, 201], f"Failed to POST {item['name']}. Got {response.status_code}"

    # Verify via GET
    get_response = requests.get(ENDPOINT)
    assert get_response.status_code == 200
    
    data = get_response.json()
    assert len(data) >= len(payloads)
    
    retrieved_names = [record['name'] for record in data]
    for item in payloads:
        assert item['name'] in retrieved_names, f"{item['name']} not found in GET response"