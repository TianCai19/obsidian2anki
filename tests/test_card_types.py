"""Tests for card type handlers."""

import unittest
from pathlib import Path
from src.card_types import QACardHandler, WholeNoteCardHandler, create_card_handler

class TestCardHandlers(unittest.TestCase):
    def setUp(self):
        """Set up test environment."""
        self.qa_handler = QACardHandler()
        self.whole_handler = WholeNoteCardHandler()
        
        # Load test files
        self.qa_content = Path('notes/test_note.md').read_text(encoding='utf-8')
        self.whole_content = Path('tests/test_whole_note.md').read_text(encoding='utf-8')
        
        # Create test file paths
        self.test_file_path = Path('test-note.md')
        self.test_file_path_with_underscores = Path('test_note_with_underscores.md')
        self.test_file_path_with_spaces = Path('test note with spaces.md')

    def test_qa_handler(self):
        """Test question-answer card handler."""
        cards = self.qa_handler.extract_cards(self.qa_content)
        
        self.assertEqual(len(cards), 3)
        self.assertEqual(cards[0][0], "What is the capital of France?")
        self.assertTrue(cards[0][1].startswith("Paris is the capital"))
        
    def test_whole_note_handler(self):
        """Test whole note card handler."""
        cards = self.whole_handler.extract_cards(self.whole_content)
        
        self.assertEqual(len(cards), 1)
        self.assertEqual(cards[0][0], "Understanding Python Decorators")
        self.assertTrue("Decorators in Python" in cards[0][1])
        self.assertTrue("Common Use Cases" in cards[0][1])

    def test_whole_note_handler_filename_fallback(self):
        """Test whole note handler with filename fallback."""
        # Test with hyphenated filename
        content = "This is a test note without a heading."
        cards = self.whole_handler.extract_cards(content, self.test_file_path)
        
        self.assertEqual(len(cards), 1)
        self.assertEqual(cards[0][0], "Test Note")
        self.assertEqual(cards[0][1], content)

        # Test with underscores
        cards = self.whole_handler.extract_cards(content, self.test_file_path_with_underscores)
        self.assertEqual(cards[0][0], "Test Note With Underscores")

        # Test with spaces
        cards = self.whole_handler.extract_cards(content, self.test_file_path_with_spaces)
        self.assertEqual(cards[0][0], "Test Note With Spaces")

    def test_whole_note_handler_empty_content(self):
        """Test whole note handler with empty content."""
        # Test with filename fallback
        cards = self.whole_handler.extract_cards("", self.test_file_path)
        self.assertEqual(len(cards), 1)
        self.assertEqual(cards[0][0], "Test Note")
        self.assertEqual(cards[0][1], "")

        # Test without filename
        cards = self.whole_handler.extract_cards("")
        self.assertEqual(len(cards), 0)

    def test_create_card_handler(self):
        """Test card handler factory function."""
        qa_handler = create_card_handler('qa')
        whole_handler = create_card_handler('whole')
        default_handler = create_card_handler('invalid')
        
        self.assertIsInstance(qa_handler, QACardHandler)
        self.assertIsInstance(whole_handler, WholeNoteCardHandler)
        self.assertIsInstance(default_handler, QACardHandler)  # Default to QA handler

    def test_empty_content(self):
        """Test handlers with empty content."""
        empty_content = ""
        
        qa_cards = self.qa_handler.extract_cards(empty_content)
        whole_cards = self.whole_handler.extract_cards(empty_content)
        
        self.assertEqual(len(qa_cards), 0)
        self.assertEqual(len(whole_cards), 0)

    def test_no_header_content(self):
        """Test handlers with content without headers."""
        no_header = "This is just some text\nwithout any headers."
        
        qa_cards = self.qa_handler.extract_cards(no_header)
        whole_cards = self.whole_handler.extract_cards(no_header)
        
        self.assertEqual(len(qa_cards), 0)
        self.assertEqual(len(whole_cards), 0)

if __name__ == '__main__':
    unittest.main() 