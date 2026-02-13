# Drive Network Analyzer

A command-line tool that analyzes interpersonal networks to identify the strongest partner-company relationships based on contact frequency.

## Quick Start

```bash
# Setup
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run with example
python network_analyzer.py examples/basic.txt

# Run tests
pytest -v
```

## Usage

The analyzer accepts input via file or stdin:

```bash
# From file
python network_analyzer.py input.txt

# From stdin (pipe)
cat input.txt | python network_analyzer.py

# From stdin (redirect)
python network_analyzer.py < input.txt
```

### Input Format

Commands are processed line-by-line:
```
Partner <Name>                          # Declare a partner
Company <Name>                          # Declare a company
Employee <Name> <CompanyName>           # Declare an employee at a company
Contact <EmployeeName> <PartnerName> <Type>  # Record a contact (email/call/coffee)
```

### Output Format

Results are sorted alphabetically by company, showing the partner with the strongest relationship:
```
Acme: Alice (3)
Globex: Bob (1)
NoContacts: No current relationship
```

## Design Approach

### Architecture

I structured the code into three focused modules:

- **`entities.py`** - Domain objects (Partner, Company, Employee, Contact, Network). These handle data storage and basic validation.
- **`analyzer.py`** - Relationship analysis logic. Takes a network and calculates which partner has the strongest relationship with each company.
- **`cli.py`** - Command-line interface. Parses commands, reads input, and orchestrates the workflow.

This separation makes the code easier to test and understand. Each module has a single clear responsibility.

### Algorithm

The relationship strength calculation works like this:

1. Loop through all contacts
2. For each contact, figure out which company the employee works at
3. Build a nested dict: `{company_name: {partner_name: contact_count}}`
4. For each company, find the partner with the maximum count
5. If there's a tie, pick the first partner alphabetically
6. Sort companies alphabetically and format the output

## Development Notes

### What Felt Challenging

**Finding the right design approach:** I initially considered a more complex architecture with multiple abstraction layers. After planning it out, I realized this was over-engineered for the problem. The challenge was simplifying down to just 3 focused modules while still maintaining good separation of concerns.

**Balancing simplicity vs over-engineering:** The spec guarantees well-formed input, but I kept wanting to add extra validation and error handling. It was challenging maintaining a balance of covering all requirements while keeping the code simple and readable.

**Designing the counting algorithm:** Figuring out how to efficiently track contact counts across the partner-company relationship. I needed to map from employees to their companies while counting contacts per partner, and settled on a nested dictionary approach.

### Development Process

I approached this methodically to ensure quality:

**Planning:**
- Started by creating a detailed implementation plan with Claude
- Created GitHub issues for each phase to stay organized
- Documented all design decisions in a development log as I went

**Phased Implementation:**
Rather than building everything at once, I broke the work into phases with separate PRs:
1. Project structure and setup
2. Domain entities and tests (Partner, Company, Employee, Contact, Network)
3. Relationship analyzer and tests
4. CLI interface and integration tests
5. Documentation and polish

**Quality Gates:**
- Each phase was implemented on a feature branch
- Created GitHub PRs for each phase and used GitHub Copilot to review the code
- Copilot caught potential issues (like silently ignoring invalid commands) - I made informed decisions about whether to add the suggested validation
- All tests had to pass before merging each PR
- Tested from fresh clone to ensure setup instructions work

This workflow helped me stay organized and catch issues early.

### LLM Usage

**Claude**
- Brainstorming the architecture
- Writing comprehensive tests (Claude generated most of the test cases, which I then reviewed)
- Debugging issues (helped me spot a missing variable assignment)
- Created example input files
- Once I wrote out the content of the readme, claude formatted it in .md format

**GitHub Copilot**
- Used for PR reviews on each phase of development