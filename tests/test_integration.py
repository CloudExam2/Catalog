import os
import requests

# Use the environment variable passed from the YAML
BASE_URL = os.getenv("BASE_URL") 
# Fallback for local testing only
if not BASE_URL:
    BASE_URL = "http://54.81.167.105" 

ENDPOINT = f"{BASE_URL}/catalog"

def test_catalog_persistence():
    payloads = [
        {"name": "Industrial Copper(II) Sulfate", "description": "High purity for chemical synthesis", "price": 45.50},
        {"name": "Potassium Permanganate", "description": "Oxidizing agent for laboratory use", "price": 32.00},
        {"name": "ITESO Lab Flask", "description": "250ml Borosilicate glass", "price": 15.00}
    ]

    # Batch POST items
    for item in payloads:
        response = requests.post(f"{ENDPOINT}/", json=item)
        assert response.status_code == 201 or response.status_code == 200, f"Failed to POST {item['name']}"

    # Verify via GET
    get_response = requests.get(f"{ENDPOINT}/")
    assert get_response.status_code == 200
    
    data = get_response.json()
    assert len(data) >= len(payloads)
    
    # Validation: Ensure created names exist in the returned list
    retrieved_names = [record['name'] for record in data]
    for item in payloads:
        assert item['name'] in retrieved_names, f"{item['name']} not found in GET response"