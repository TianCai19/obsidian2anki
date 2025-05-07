"""Main converter module for Obsidian to Anki conversion."""

import frontmatter
import markdown
from pathlib import Path
from typing import List, Dict, Any, Tuple
import re
from .card_types import create_card_handler
from .anki_connect import ensure_deck_exists, add_note

def extract_and_replace_math(content: str) -> Tuple[str, dict]:
    """Replace math blocks and inline math with unique placeholders and return mapping."""
    math_map = {}
    # Block math: $$...$$
    def block_repl(match):
        key = f"[[[MATH_BLOCK_{len(math_map)}]]]"
        math_map[key] = f"\\[{match.group(1).strip()}\\]"
        return key
    content = re.sub(r'(?<!\\)\$\$([\s\S]+?)(?<!\\)\$\$', block_repl, content)
    # Inline math: $...$
    def inline_repl(match):
        key = f"[[[MATH_INLINE_{len(math_map)}]]]"
        math_map[key] = f"\\({match.group(1).strip()}\\)"
        return key
    content = re.sub(r'(?<!\\)\$(?!\$)([^\$\n]+?)(?<!\\)\$', inline_repl, content)
    return content, math_map

def restore_math_placeholders(html: str, math_map: dict) -> str:
    """Restore math placeholders in HTML output."""
    for key, value in math_map.items():
        html = html.replace(key, value)
    return html

def convert_markdown_to_html(content: str) -> str:
    """Convert markdown to HTML for Anki, preserving math as raw TeX."""
    # Replace math with placeholders
    content, math_map = extract_and_replace_math(content)
    # Convert markdown to HTML
    html = markdown.markdown(content, extensions=['extra'])
    # Restore math placeholders as raw TeX
    html = restore_math_placeholders(html, math_map)
    return html

def process_obsidian_file(file_path: Path, card_type: str) -> List[Tuple[str, str]]:
    """Process a single Obsidian markdown file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    # Extract cards using appropriate handler
    handler = create_card_handler(card_type)
    cards = handler.extract_cards(content, file_path)
    # Convert each card's content to HTML
    converted_cards = []
    for front, back in cards:
        converted_front = convert_markdown_to_html(front)
        converted_back = convert_markdown_to_html(back)
        converted_cards.append((converted_front, converted_back))
    return converted_cards

def convert_directory(directory: Path, deck_name: str, card_type: str) -> int:
    """Convert all markdown files in a directory to Anki cards."""
    total_notes = 0
    for file_path in directory.glob('**/*.md'):
        try:
            notes = process_obsidian_file(file_path, card_type)
            for front, back in notes:
                result = add_note(deck_name, front, back, ["obsidian"])
                print(f"AnkiConnect response for {file_path}: {result}")
                if result.get('error'):
                    print(f"Error adding note from {file_path}: {result['error']}")
                else:
                    total_notes += 1
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
    return total_notes 