"""Tests for the converter module."""

import unittest
from pathlib import Path
from src.converter import convert_markdown_to_html, convert_math_delimiters

class TestConverter(unittest.TestCase):
    def test_math_conversion(self):
        """Test conversion of math equations."""
        # Test inline math
        text = "The formula is $E = mc^2$"
        converted = convert_math_delimiters(text)
        self.assertIn(r'\(E = mc^2\)', converted)
        
        # Test block math
        text = "The equation is:\n$$\na^2 + b^2 = c^2\n$$"
        converted = convert_math_delimiters(text)
        self.assertIn(r'\[a^2 + b^2 = c^2\]', converted)
        
        # Test HTML conversion with math
        html = convert_markdown_to_html(text)
        self.assertIn('MathJax', html)
        self.assertIn(r'\[a^2 + b^2 = c^2\]', html)
        
        # Test complex math with multiple lines
        text = "The equations are:\n$$\n\\begin{align}\ny &= mx + b \\\\\ny &= ax^2 + bx + c\n\\end{align}\n$$"
        converted = convert_math_delimiters(text)
        self.assertIn(r'\[\begin{align}', converted)
        self.assertIn(r'\\end{align}\]', converted)

if __name__ == '__main__':
    unittest.main() 