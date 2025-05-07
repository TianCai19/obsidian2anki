#!/usr/bin/env python3
"""Convert Obsidian notes to Anki cards."""

import os
import sys
import argparse
from pathlib import Path
from src.converter import convert_directory, process_obsidian_file
from src.anki_connect import ensure_deck_exists

def main():
    parser = argparse.ArgumentParser(description='Convert Obsidian notes to Anki cards')
    parser.add_argument('path', help='Path to Obsidian note or directory containing notes')
    parser.add_argument('--type', choices=['qa', 'whole'], default='whole',
                      help='Type of cards to create (qa=question-answer pairs, whole=entire note)')
    parser.add_argument('--deck', default='Obsidian Notes',
                      help='Name of the Anki deck to create/use')
    
    args = parser.parse_args()
    path = Path(args.path)
    
    # Ensure Anki is running with AnkiConnect
    try:
        ensure_deck_exists(args.deck)
    except Exception as e:
        print("Error: Could not connect to Anki. Please ensure:")
        print("1. Anki is running")
        print("2. AnkiConnect add-on is installed")
        print("3. AnkiConnect is enabled")
        sys.exit(1)
    
    if path.is_file():
        # Process single file
        if not path.suffix == '.md':
            print(f"Error: {path} is not a markdown file")
            sys.exit(1)
            
        print(f"Processing file: {path}")
        notes = process_obsidian_file(path, args.type)
        print(f"Successfully processed {len(notes)} cards")
        
    elif path.is_dir():
        # Process directory
        print(f"Processing directory: {path}")
        added_notes = convert_directory(path, args.deck, args.type)
        print(f"Successfully added {added_notes} cards to deck '{args.deck}'")
        
    else:
        print(f"Error: Path {path} does not exist")
        sys.exit(1)

if __name__ == '__main__':
    main() 