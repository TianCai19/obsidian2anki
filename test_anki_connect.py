import requests
import json

def test_anki_connect():
    url = "http://localhost:8765"
    
    # Test 1: Version check
    print("\nTest 1: Checking Anki version")
    payload = {
        "action": "version",
        "version": 6
    }
    response = requests.post(url, json=payload)
    print(f"Version response: {response.json()}")
    
    # Test 2: List decks
    print("\nTest 2: Listing decks")
    payload = {
        "action": "deckNames",
        "version": 6
    }
    response = requests.post(url, json=payload)
    print(f"Decks: {response.json()}")
    
    # Test 3: Create test deck
    print("\nTest 3: Creating test deck")
    deck_name = "Test Deck Python"
    payload = {
        "action": "createDeck",
        "version": 6,
        "params": {
            "deck": deck_name
        }
    }
    response = requests.post(url, json=payload)
    print(f"Create deck response: {response.json()}")
    
    # Test 4: Add a simple note
    print("\nTest 4: Adding test note")
    payload = {
        "action": "addNote",
        "version": 6,
        "params": {
            "note": {
                "deckName": deck_name,
                "modelName": "Basic",
                "fields": {
                    "Front": "Test Question",
                    "Back": "Test Answer"
                },
                "options": {
                    "allowDuplicate": True
                },
                "tags": ["test"]
            }
        }
    }
    response = requests.post(url, json=payload)
    print(f"Add note response: {response.json()}")

if __name__ == "__main__":
    try:
        test_anki_connect()
        print("\nAll tests completed!")
    except Exception as e:
        print(f"\nError during testing: {e}")
        print("Please make sure:")
        print("1. Anki is running")
        print("2. AnkiConnect add-on is installed (Tools -> Add-ons)")
        print("3. You've restarted Anki after installing AnkiConnect") 