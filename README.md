# Drive Network Analyzer

Analyzes interpersonal networks to identify strongest partner-company relationships.

## Installation

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

```bash
# From file
python network_analyzer.py input.txt

# From stdin
python network_analyzer.py < input.txt
cat input.txt | python network_analyzer.py
```

## Running Tests

```bash
# Run all tests
pytest -v

# Run with coverage report
pytest --cov=src

# Run specific test file
pytest tests/test_entities.py -v
```

