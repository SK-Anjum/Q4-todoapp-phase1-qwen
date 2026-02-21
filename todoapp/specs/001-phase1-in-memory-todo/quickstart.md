# Quickstart Guide: Phase 1 In-Memory Todo App

**Date**: 2026-02-21
**Branch**: `001-phase1-in-memory-todo`
**Purpose**: Developer onboarding and usage guide

---

## Prerequisites

- Python 3.10 or higher
- pip (Python package manager)
- Git

---

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd todoapp
   ```

2. **Create virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   # or
   venv\Scripts\activate  # Windows
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

---

## Running the Application

### Interactive Mode (Recommended)

```bash
python -m src.cli
```

You'll see the prompt:
```
> 
```

Enter commands at the prompt. Type `help` for available commands, `exit` to quit.

### Single Command Mode

```bash
python -m src.cli add "Buy groceries" "Need milk and eggs"
python -m src.cli list
python -m src.cli complete 1
```

---

## Basic Usage Examples

### Adding Tasks

```
> add "Buy groceries" "Need milk and eggs"
✓ Task created: [1] "Buy groceries"

> add "Finish report"
✓ Task created: [2] "Finish report"
```

### Viewing Tasks

```
> list
[1] [ ] Buy groceries
    Description: Need milk and eggs

[2] [ ] Finish report

> list --json
[{"id": 1, "title": "Buy groceries", "description": "Need milk and eggs", "completed": false}, ...]
```

### Completing Tasks

```
> complete 1
✓ Task [1] marked as completed

> list
[1] [x] Buy groceries
    Description: Need milk and eggs

[2] [ ] Finish report
```

### Updating Tasks

```
> update 2 "Finish quarterly report" "Due tomorrow EOD"
✓ Task [2] updated
```

### Deleting Tasks

```
> delete 1
✓ Task [1] deleted
```

### Getting Help

```
> help
Todo App - Phase 1

Commands:
  add <title> ["<description>"]   - Create a new task
  list [--json]                   - Display all tasks
  complete <id>                   - Toggle task completion status
  update <id> ["<title>"] ["<description>"] - Update a task
  delete <id>                     - Remove a task
  help                            - Show this help message
  exit                            - Quit the application
```

### Exiting

```
> exit
Goodbye!
```

---

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=term-missing

# Run specific test category
pytest tests/unit/
pytest tests/integration/
pytest tests/contract/
```

---

## Project Structure

```
todoapp/
├── src/
│   ├── models/
│   │   └── task.py          # Task data class
│   ├── services/
│   │   └── task_store.py    # In-memory repository
│   ├── cli/
│   │   ├── __init__.py      # CLI entry point
│   │   ├── commands.py      # Command handlers
│   │   └── formatter.py     # Output formatting
│   └── lib/
│       └── exceptions.py    # Custom exceptions
├── tests/
│   ├── contract/
│   ├── integration/
│   └── unit/
└── specs/
    └── 001-phase1-in-memory-todo/
        ├── spec.md          # Feature specification
        ├── plan.md          # Implementation plan
        ├── research.md      # Technical decisions
        ├── data-model.md    # Data structures
        └── contracts/       # CLI contracts
```

---

## Development Workflow

1. **Pick a task** from `specs/001-phase1-in-memory-todo/tasks.md`

2. **Write tests first** (Red-Green-Refactor):
   ```bash
   # Write failing test
   pytest tests/unit/test_task.py -v  # Should fail
   ```

3. **Implement minimum code** to pass tests:
   ```bash
   pytest tests/unit/test_task.py -v  # Should pass
   ```

4. **Refactor** while keeping tests passing

5. **Commit** with descriptive message

---

## Common Issues

### "Module not found" error

**Solution**: Ensure you're running from project root and virtual environment is activated.

```bash
cd /path/to/todoapp
source venv/bin/activate  # or venv\Scripts\activate
python -m src.cli
```

### Tests not running

**Solution**: Install test dependencies:

```bash
pip install -r requirements-dev.txt
```

### Permission denied on Linux/macOS

**Solution**: Make scripts executable:

```bash
chmod +x .specify/scripts/bash/*.sh
```

---

## Next Steps

1. Read the full specification: `specs/001-phase1-in-memory-todo/spec.md`
2. Review technical decisions: `specs/001-phase1-in-memory-todo/research.md`
3. Understand data models: `specs/001-phase1-in-memory-todo/data-model.md`
4. Check CLI contracts: `specs/001-phase1-in-memory-todo/contracts/cli-commands.md`

---

## Getting Help

- **Specification issues**: Review `spec.md` for requirements
- **Implementation questions**: Check `research.md` for technical decisions
- **Bug reports**: Create issue with reproduction steps
- **Feature requests**: Must align with approved specification
