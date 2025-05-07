"""Tests for card type handlers."""

import unittest
from pathlib import Path
from src.card_types import QACardHandler, WholeNoteCardHandler, create_card_handler
import tempfile
import shutil
from src.converter import convert_directory

class TestCardHandlers(unittest.TestCase):
    def setUp(self):
        """Set up test environment."""
        self.qa_handler = QACardHandler()
        self.whole_handler = WholeNoteCardHandler()
        
        # Load test files
        self.qa_content = """
# Test Note
## Question 1
What is 2+2?
4
## Question 2
What is the capital of France?
Paris
"""
        self.whole_content = """
# Test Note
This is the body of the note.
"""
        
        # Create test file paths
        self.test_file_path = Path('test-note.md')
        self.test_file_path_with_underscores = Path('test_note_with_underscores.md')
        self.test_file_path_with_spaces = Path('test note with spaces.md')

    def test_qa_handler(self):
        """Test question-answer card handler."""
        cards = self.qa_handler.extract_cards(self.qa_content, self.test_file_path)
        
        self.assertEqual(len(cards), 2)
        self.assertEqual(cards[0][0], "Question 1")
        self.assertEqual(cards[0][1], "What is 2+2?\n4")
        
    def test_whole_note_handler(self):
        """Test whole note card handler."""
        cards = self.whole_handler.extract_cards(self.whole_content, self.test_file_path)
        
        self.assertEqual(len(cards), 1)
        self.assertEqual(cards[0][0], "Test Note")
        self.assertIn("This is the body", cards[0][1])

    def test_whole_note_handler_filename_fallback(self):
        """Test whole note handler with filename fallback."""
        # Test with hyphenated filename
        content = "This is a test note without a heading."
        cards = self.whole_handler.extract_cards(content, self.test_file_path)
        
        self.assertEqual(len(cards), 1)
        self.assertEqual(cards[0][0], "Test-Note")
        self.assertIn("This is a test note", cards[0][1])

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
        self.assertEqual(cards[0][0], "Test-Note")
        self.assertEqual(cards[0][1], "")

        # Test without filename (should return empty list)
        with self.assertRaises(TypeError):
            self.whole_handler.extract_cards("")

    def test_create_card_handler(self):
        """Test card handler factory function."""
        qa_handler = create_card_handler('qa')
        whole_handler = create_card_handler('whole')
        with self.assertRaises(ValueError):
            create_card_handler('invalid')
        
        self.assertIsInstance(qa_handler, QACardHandler)
        self.assertIsInstance(whole_handler, WholeNoteCardHandler)

    def test_empty_content(self):
        """Test handlers with empty content."""
        empty_content = ""
        
        qa_cards = self.qa_handler.extract_cards(empty_content, self.test_file_path)
        whole_cards = self.whole_handler.extract_cards(empty_content, self.test_file_path)
        
        self.assertEqual(len(qa_cards), 0)
        self.assertEqual(len(whole_cards), 1)

    def test_no_header_content(self):
        """Test handlers with content without headers."""
        no_header = "Just some text without headers."
        
        qa_cards = self.qa_handler.extract_cards(no_header, self.test_file_path)
        whole_cards = self.whole_handler.extract_cards(no_header, self.test_file_path)
        
        self.assertEqual(len(qa_cards), 0)
        self.assertEqual(len(whole_cards), 1)

    def test_convert_directory_whole_folder(self):
        """Test processing a whole folder of markdown files."""
        # Create a temporary directory
        with tempfile.TemporaryDirectory() as tmpdirname:
            tmpdir = Path(tmpdirname)
            # Create multiple markdown files
            file_contents = [
                "# Note 1\nContent 1.",
                "# Note 2\nContent 2.",
                "# Note 3\nContent 3."
            ]
            for i, content in enumerate(file_contents, 1):
                (tmpdir / f"note{i}.md").write_text(content, encoding="utf-8")
            # Run convert_directory
            num_cards = convert_directory(tmpdir, "Test Deck", "whole")
            self.assertEqual(num_cards, len(file_contents))

if __name__ == '__main__':
    unittest.main() 