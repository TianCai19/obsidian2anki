"""Main converter module for Obsidian to Anki conversion."""

import frontmatter
import markdown
from pathlib import Path
from typing import List, Dict, Any
from .card_types import create_card_handler
from .anki_connect import ensure_deck_exists, add_note

def convert_markdown_to_html(text: str) -> str:
    """Convert markdown text to HTML."""
    return markdown.markdown(text, extensions=['extra'])

def process_obsidian_file(file_path: Path, card_type: str = 'qa') -> List[Dict[str, Any]]:
    """Process a single Obsidian markdown file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        post = frontmatter.load(f)
        content = post.content
        
        # Get tags from frontmatter
        tags = post.get('tags', [])
        if isinstance(tags, str):
            tags = [tag.strip() for tag in tags.split(',')]
        
        # Extract cards using appropriate handler
        handler = create_card_handler(card_type)
        cards = handler.extract_cards(content, file_path)
        
        # Create Anki notes
        anki_notes = []
        for front, back in cards:
            note = {
                'deckName': 'Obsidian Notes',
                'modelName': 'Basic',
                'fields': {
                    'Front': convert_markdown_to_html(front),
                    'Back': convert_markdown_to_html(back)
                },
                'options': {
                    'allowDuplicate': False
                },
                'tags': tags
            }
            anki_notes.append(note)
        
        return anki_notes

def convert_directory(directory: Path, deck_name: str, card_type: str = 'qa') -> int:
    """Convert all markdown files in directory to Anki cards."""
    # Ensure directory exists
    directory = Path(directory)
    if not directory.exists():
        raise FileNotFoundError(f"Directory not found: {directory}")
    
    # Ensure deck exists
    ensure_deck_exists(deck_name)
    
    # Process all markdown files
    added_notes = 0
    for file_path in directory.glob('**/*.md'):
        notes = process_obsidian_file(file_path, card_type)
        for note in notes:
            note['deckName'] = deck_name
            result = add_note(
                deck_name=deck_name,
                front=note['fields']['Front'],
                back=note['fields']['Back'],
                tags=note['tags']
            )
            if result.get('error') is None and result.get('result'):
                added_notes += 1
    
    return added_notes 