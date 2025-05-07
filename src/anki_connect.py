"""AnkiConnect interaction module."""

import requests
import json
from typing import Dict, Any, List
import time

ANKI_CONNECT_URL = "http://localhost:8765"

def invoke(action: str, **params) -> Dict[str, Any]:
    """Invoke AnkiConnect API."""
    request_data = {
        'action': action,
        'version': 6,
        'params': params
    }
    
    try:
        response = requests.post(ANKI_CONNECT_URL, json=request_data)
        response.raise_for_status()
        result = response.json()
        
        if 'error' in result and result['error'] is not None:
            print(f"AnkiConnect error: {result['error']}")
            raise Exception(result['error'])
            
        return result.get('result')
    except requests.exceptions.RequestException as e:
        print(f"Error communicating with AnkiConnect: {e}")
        raise

def check_anki_running() -> bool:
    """Check if Anki is running and accessible."""
    try:
        version = invoke("version")
        print(f"Connected to Anki with version: {version}")
        return True
    except Exception as e:
        print(f"Error connecting to Anki: {e}")
        print("Please make sure:")
        print("1. Anki is running")
        print("2. AnkiConnect add-on is installed")
        print("3. No firewall is blocking the connection")
        return False

def ensure_deck_exists(deck_name: str) -> str:
    """Ensure the specified deck exists in Anki."""
    try:
        decks = invoke("deckNames")
        if deck_name not in decks:
            print(f"Creating deck: {deck_name}")
            invoke("createDeck", deck=deck_name)
        return deck_name
    except Exception as e:
        print(f"Error ensuring deck exists: {e}")
        raise

def add_note(deck_name: str, front: str, back: str, tags: List[str] = None) -> Dict[str, Any]:
    """Add a note to Anki."""
    if not front or not back:
        raise ValueError("Front and back content cannot be empty")
    
    try:
        # Create the note
        note = {
            "deckName": deck_name,
            "modelName": "Basic",
            "fields": {
                "Front": front,
                "Back": back
            },
            "options": {
                "allowDuplicate": True
            },
            "tags": tags or []
        }
        
        # Add the note directly
        result = invoke("addNote", note=note)
        
        if result:
            print(f"Successfully added note with ID: {result}")
            return {"result": result, "error": None}
        else:
            print("Failed to add note")
            return {"result": None, "error": "Failed to add note"}
            
    except Exception as e:
        print(f"Error adding note: {e}")
        return {"result": None, "error": str(e)} 