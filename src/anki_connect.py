"""AnkiConnect interaction module."""

import requests
from typing import Dict, Any

ANKI_CONNECT_URL = "http://localhost:8765"

def invoke(action: str, **params) -> Dict[str, Any]:
    """Invoke AnkiConnect API."""
    request_data = {
        'action': action,
        'version': 6,
        'params': params
    }
    response = requests.post(ANKI_CONNECT_URL, json=request_data)
    return response.json()

def ensure_deck_exists(deck_name: str) -> str:
    """Ensure the deck exists in Anki."""
    decks = invoke('deckNames')
    if deck_name not in decks['result']:
        invoke('createDeck', deck=deck_name)
    return deck_name

def add_note(deck_name: str, front: str, back: str, tags: list = None) -> Dict[str, Any]:
    """Add a note to Anki."""
    if tags is None:
        tags = []
        
    note = {
        'deckName': deck_name,
        'modelName': 'Basic',
        'fields': {
            'Front': front,
            'Back': back
        },
        'options': {
            'allowDuplicate': False
        },
        'tags': tags
    }
    
    return invoke('addNote', note=note) 