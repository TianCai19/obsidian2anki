"""Card type handlers for different Obsidian note formats."""

from abc import ABC, abstractmethod
import frontmatter
from pathlib import Path
from typing import List, Tuple, Dict, Any
import re

class CardHandler(ABC):
    """Abstract base class for card handlers."""
    
    @abstractmethod
    def extract_cards(self, content: str, file_path: Path) -> List[Tuple[str, str]]:
        """Extract cards from content."""
        pass

class QACardHandler(CardHandler):
    """Handler for Question-Answer format cards."""
    
    def extract_cards(self, content: str, file_path: Path) -> List[Tuple[str, str]]:
        """Extract question-answer pairs from content."""
        cards = []
        sections = re.split(r'\n##\s+', content)
        
        for section in sections[1:]:  # Skip the first section (title)
            lines = section.strip().split('\n', 1)
            if len(lines) == 2:
                question, answer = lines
                cards.append((question.strip(), answer.strip()))
        
        return cards

class WholeNoteCardHandler(CardHandler):
    """Handler for whole note as single card format."""
    
    def extract_cards(self, content: str, file_path: Path) -> List[Tuple[str, str]]:
        """Convert the whole note into a single card."""
        # Parse frontmatter and content
        post = frontmatter.loads(content)
        body = post.content.strip()
        
        # Split content into title and body
        sections = body.split('\n', 1)
        
        if len(sections) < 2:
            # If no clear title, use filename
            title = file_path.stem.replace('_', ' ').title()
            body = body
        else:
            # Extract title from first line (remove # if present)
            title = sections[0].lstrip('#').strip()
            body = sections[1].strip()
            
            # If title is empty, use filename
            if not title:
                title = file_path.stem.replace('_', ' ').title()
        
        print(f"Creating card with title: {title}")
        print(f"Content preview: {body[:100]}...")
        
        return [(title, body)]

def create_card_handler(card_type: str) -> CardHandler:
    """Create a card handler based on type."""
    handlers = {
        'qa': QACardHandler(),
        'whole': WholeNoteCardHandler()
    }
    
    if card_type not in handlers:
        raise ValueError(f"Unknown card type: {card_type}. Available types: {list(handlers.keys())}")
    
    return handlers[card_type] 