# Development Workflow

## How We Work Together

This project follows a structured development process. Follow these steps exactly.

---

## Project Context

**What it is:** CLI tool analyzing partner-company relationships
**Architecture:** 3 modules (entities.py, analyzer.py, cli.py)
**Tech:** Python 3.9+, no external dependencies except pytest

**Key files:**
- `src/entities.py` - Domain objects
- `src/analyzer.py` - Relationship algorithm
- `src/cli.py` - Command parsing
- `tests/` - Test suites

**Run tests:** `pytest -v`
**Run program:** `python network_analyzer.py examples/basic.txt`

---

## Critical Rules

**Git — NEVER run git commands:**
- NEVER run: git add, git commit, git push, git merge, git checkout, git branch
- Instead, pause and prompt the user to handle git operations, then wait for confirmation before continuing

**No Assumptions:**
- ALWAYS ask for input — don't assume what the user wants; present options instead
- If something is unclear, ask before proceeding — do not guess
- Communication > speed — correctness matters more than being fast

**Communication:**
- Think out loud and explain your reasoning
- Ask questions frequently — never code in silence

---

## Compaction Instructions

When compacting, always preserve: current branch name, files modified, what step of the implementation plan we're on, any failing tests or errors being debugged, and key decisions made during the session.

---

## The Development Process

### 1. Understand the Issue/Feature
- Read the requirement carefully
- Ask clarifying questions and research if needed (docs, similar implementations, best practices)
- IMPORTANT: Do not move forward until you fully understand WHAT needs to be built and WHY — ask more questions if anything is unclear

### 2. Planning & Design
- Before writing any code, STOP and plan
- Explain the approach out loud and ask: "Does this approach make sense?"
- Design the solution together before moving to implementation

### 3. Issue & Branch Setup
- Create a GitHub issue for the feature/change
- Prompt the user to create a branch and check it out
- Branch naming convention: `feature/123-short-description` or `fix/123-short-description`
- **Wait** for user to confirm the branch is created and checked out before proceeding

### 4. Implementation Strategy
- Make a step-by-step plan and explain each step BEFORE coding it
- Execute one step at a time
- After each step, explain what you did and wait for user review/approval before continuing

### 5. Testing & Verification
- After implementing a feature, write tests for it
- Tests should cover the new functionality
- Run tests and verify they pass — do not assume changes work without checking
- After making any change, always verify by running the relevant test or checking the output

### 6. Commit Breaks
- Pause periodically to let user make commits — especially before moving to new scope
- Say: "This is a good point to commit. Ready to continue?"

### 7. When Feature is Complete
- Run ALL tests: `pytest -v`
- Ensure the full test suite passes
- Prompt the user to run `/security-review` (built-in Claude command) and wait for results
- Do not proceed until everything passes

### 8. Pull Request Process
- Create PR with a structured description covering:
  - **What changed:** List what was added, modified, removed
  - **Why:** Brief explanation of the motivation/issue being solved
  - **How to test:** Steps to verify the changes work
- User will add Copilot as reviewer
- **WAIT** for Copilot to comment with review feedback
- Address review comments together and make fixes as needed

---

## Summary

**Understand → Plan → Issue → Branch (user creates) → Implement (step-by-step) → Test & Verify → Commit breaks → Full test suite → Security review (user runs) → PR → Copilot review → Address feedback**
