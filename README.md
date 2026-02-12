# Drive Network Analyzer

Analyzes interpersonal networks to identify strongest partner-company relationships.

## Installation

```bash
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
pytest -v
pytest --cov=src
```

