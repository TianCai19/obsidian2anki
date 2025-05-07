"""Card type handlers for different Obsidian note formats."""

from abc import ABC, abstractmethod
import frontmatter
from pathlib import Path
from typing import List, Tuple, Dict, Any

class CardHandler(ABC):
    """Abstract base class for card handlers."""
    
    @abstractmethod
    def extract_cards(self, content: str, file_path: Path = None) -> List[Tuple[str, str]]:
        """Extract cards from content."""
        pass

class QACardHandler(CardHandler):
    """Handler for Question-Answer format cards."""
    
    def extract_cards(self, content: str, file_path: Path = None) -> List[Tuple[str, str]]:
        """Extract question-answer pairs from content using # headers."""
        import re
        sections = re.split(r'(?m)^#\s+', content)
        cards = []
        
        for section in sections[1:]:  # Skip the first empty section
            lines = section.strip().split('\n', 1)
            if len(lines) == 2:
                question, answer = lines
                cards.append((question.strip(), answer.strip()))
        
        return cards

class WholeNoteCardHandler(CardHandler):
    """Handler for whole note as single card format."""
    
    def extract_cards(self, content: str, file_path: Path = None) -> List[Tuple[str, str]]:
        """Extract title as front and content as back."""
        import re
        
        # Find the first heading
        match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        
        if match:
            # Use the heading as the front
            title = match.group(1).strip()
            # Get everything after the first heading
            content_parts = content.split('\n', 1)
            if len(content_parts) < 2:
                return [(title, "")]
            return [(title, content_parts[1].strip())]
        else:
            # No heading found, use filename as front
            if file_path:
                # Remove .md extension and convert to title case
                title = file_path.stem.replace('-', ' ').replace('_', ' ').title()
                return [(title, content.strip())]
            return []

def create_card_handler(card_type: str) -> CardHandler:
    """Factory function to create appropriate card handler."""
    handlers = {
        'qa': QACardHandler(),
        'whole': WholeNoteCardHandler()
    }
    return handlers.get(card_type, QACardHandler()) 