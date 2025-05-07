# Obsidian to Anki Converter

A Python tool that converts Obsidian markdown notes to Anki flashcards using AnkiConnect. This tool allows you to easily create Anki cards from your Obsidian notes, either as question-answer pairs or as whole notes.

## Features

- Convert Obsidian markdown notes to Anki cards
- Support for both question-answer format and whole note format
- Direct integration with Anki using AnkiConnect
- Preserves markdown formatting in cards
- Supports tags from frontmatter
- Can process single files or entire directories

## Prerequisites

1. Python 3.6 or higher
2. Anki installed on your computer
3. AnkiConnect add-on installed in Anki
   - Install AnkiConnect from AnkiWeb (code: 2055492159)
   - Restart Anki after installation

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/obsidian2anki.git
   cd obsidian2anki
   ```

2. Create and activate a virtual environment (recommended):
   ```bash
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Basic Usage

1. Ensure Anki is running
2. Run the converter with your Obsidian notes:

```bash
# Convert a single note
python obsidian2anki.py "path/to/your/note.md" --deck "Your Deck Name"

# Convert all notes in a directory
python obsidian2anki.py "path/to/your/obsidian/vault" --deck "Your Deck Name"
```

### Command Line Options

- `path`: Path to an Obsidian note file or directory containing notes
- `--type`: Type of cards to create (default: whole)
  - `whole`: Creates one card per note with title as front and content as back
  - `qa`: Creates cards from question-answer pairs in the note
- `--deck`: Name of the Anki deck to create/use (default: "Obsidian Notes")

### Note Formats

#### Whole Note Format
The entire note becomes a single card:
- Front: The first heading in the note (or filename if no heading exists)
- Back: All content after the first heading (or entire content if no heading)

Example with heading:
```markdown
# Understanding Python Decorators

Decorators in Python are a way to modify functions...
```

Example without heading (file named `python-decorators.md`):
```markdown
Decorators in Python are a way to modify functions...
```
This will create a card with:
- Front: "Python Decorators"
- Back: The entire content

#### Question-Answer Format
Create multiple cards from question-answer pairs:
```markdown
# What is the capital of France?
Paris is the capital of France...

# What is the largest planet?
Jupiter is the largest planet...
```

## Troubleshooting

1. **AnkiConnect Connection Error**
   - Ensure Anki is running
   - Verify AnkiConnect is installed and enabled
   - Check AnkiConnect version (should be 6 or higher)

2. **No Cards Created**
   - Check if your markdown files are properly formatted
   - Verify the path to your notes is correct
   - Ensure you have write permissions in your Anki profile

3. **Formatting Issues**
   - Basic markdown formatting is supported
   - Code blocks are preserved
   - Images are not currently supported

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 