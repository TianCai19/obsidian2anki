import unittest
import os
import json
import time
import requests
from pathlib import Path
from obsidian2anki import (
    invoke,
    convert_markdown_to_html,
    extract_cards,
    process_obsidian_file,
    ensure_deck_exists
)

class TestObsidian2Anki(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up test environment."""
        # Check if Anki is running with AnkiConnect
        try:
            invoke('version')
        except requests.exceptions.ConnectionError:
            raise Exception(
                "Anki is not running or AnkiConnect is not installed. "
                "Please start Anki and ensure AnkiConnect is installed."
            )
        
        # Create test deck
        cls.test_deck = f"Test Obsidian Notes {int(time.time())}"
        ensure_deck_exists(cls.test_deck)

    def test_convert_markdown_to_html(self):
        """Test markdown to HTML conversion."""
        markdown_text = "# Test\n**Bold** and *italic*"
        html = convert_markdown_to_html(markdown_text)
        self.assertIn("<h1>Test</h1>", html)
        self.assertIn("<strong>Bold</strong>", html)
        self.assertIn("<em>italic</em>", html)

    def test_extract_cards(self):
        """Test card extraction from markdown content."""
        content = """# Question 1
Answer 1

# Question 2
Answer 2"""
        cards = extract_cards(content)
        self.assertEqual(len(cards), 2)
        self.assertEqual(cards[0][0], "Question 1")
        self.assertEqual(cards[0][1], "Answer 1")
        self.assertEqual(cards[1][0], "Question 2")
        self.assertEqual(cards[1][1], "Answer 2")

    def test_process_obsidian_file(self):
        """Test processing of an Obsidian file."""
        # Create a temporary test file
        test_file = Path("notes/test_note.md")
        self.assertTrue(test_file.exists(), "Test file not found")
        
        notes = process_obsidian_file(test_file)
        self.assertGreater(len(notes), 0)
        
        # Verify note structure
        note = notes[0]
        self.assertEqual(note['deckName'], 'Obsidian Notes')
        self.assertEqual(note['modelName'], 'Basic')
        self.assertIn('Front', note['fields'])
        self.assertIn('Back', note['fields'])

    def test_add_cards_to_anki(self):
        """Test adding cards to Anki."""
        # Process test file
        test_file = Path("notes/test_note.md")
        notes = process_obsidian_file(test_file)
        
        # Add notes to test deck with timestamp to avoid duplicates
        timestamp = int(time.time())
        added_notes = 0
        for i, note in enumerate(notes):
            note['deckName'] = self.test_deck
            note['fields']['Front'] = f"{note['fields']['Front']} (Test {timestamp}-{i})"
            result = invoke('addNote', note=note)
            
            # Check if note was added successfully
            if result.get('error') is not None:
                self.fail(f"Failed to add note: {result['error']}")
            elif isinstance(result.get('result'), (int, str)):
                added_notes += 1
            else:
                self.fail(f"Unexpected response format: {result}")
        
        self.assertGreater(added_notes, 0, "No notes were added to Anki")
        print(f"Successfully added {added_notes} notes to deck '{self.test_deck}'")

    @classmethod
    def tearDownClass(cls):
        """Clean up test environment."""
        # Delete test deck
        try:
            invoke('deleteDeck', deck=cls.test_deck, cardsToo=True)
        except:
            pass

if __name__ == '__main__':
    unittest.main() 