#!/usr/bin/env python3
"""Convert Obsidian markdown notes to Anki cards."""

import argparse
from pathlib import Path
from src.converter import convert_directory, convert_markdown_to_html
from src.anki_connect import check_anki_running, ensure_deck_exists, add_note
from src.card_types import create_card_handler

def main():
    """Main entry point."""
    print("[DEBUG] Starting obsidian2anki main()")
    parser = argparse.ArgumentParser(description='Convert Obsidian notes to Anki cards.')
    parser.add_argument('input', help='Input file or directory')
    parser.add_argument('--type', choices=['qa', 'whole'], default='qa',
                      help='Card type: qa (Question-Answer) or whole (Whole Note)')
    parser.add_argument('--deck', default='Obsidian Notes',
                      help='Target deck name in Anki')
    
    args = parser.parse_args()
    input_path = Path(args.input)
    
    # Check if Anki is running
    if not check_anki_running():
        print("Please start Anki and make sure AnkiConnect is installed.")
        return
    
    # Ensure deck exists
    try:
        ensure_deck_exists(args.deck)
    except Exception as e:
        print(f"Error ensuring deck exists: {e}")
        return
    
    # Process single file or directory
    try:
        if input_path.is_file():
            print(f"\n[DEBUG] Processing file: {input_path}")
            with open(input_path, 'r', encoding='utf-8') as f:
                content = f.read()
            print(f"[DEBUG] File content loaded, length: {len(content)}")
            
            # Extract cards using appropriate handler
            handler = create_card_handler(args.type)
            cards = handler.extract_cards(content, input_path)
            
            # Add each card to Anki
            added_notes = 0
            for front, back in cards:
                # Always convert to HTML before sending to Anki
                html_front = convert_markdown_to_html(front)
                html_back = convert_markdown_to_html(back)

                print(f"\nAdding card {added_notes + 1}/{len(cards)}:")
                print(f"Front preview (raw): {front[:100]}...")
                print(f"Back preview (raw): {back[:100]}...")
                print("--- HTML Front ---")
                print(html_front)
                print("--- HTML Back ---")
                print(html_back)
                print("------------------")
                
                result = add_note(args.deck, html_front, html_back, ["obsidian"])
                print(f"AnkiConnect response: {result}")
                if result.get('error'):
                    print(f"Error adding note: {result['error']}")
                else:
                    added_notes += 1
                    print(f"Successfully added note with ID: {result['result']}")
            
            print(f"\nSuccessfully processed {added_notes} cards")
        
        elif input_path.is_dir():
            added_notes = convert_directory(input_path, args.deck, args.type)
            print(f"\nSuccessfully processed {added_notes} cards from directory")
        
        else:
            print(f"Error: {input_path} does not exist")
            return
        
    except Exception as e:
        print(f"Error processing {input_path}: {e}")
        raise

if __name__ == '__main__':
    main() 