# Implementation Plan: Phase 1 In-Memory Todo App

**Branch**: `001-phase1-in-memory-todo` | **Date**: 2026-02-21 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/001-phase1-in-memory-todo/spec.md`

## Summary

Build a CLI-based todo application with in-memory storage supporting five core operations (add, list, complete, delete, update) plus an interactive session mode. The app uses Python with UVPy framework for CLI handling, follows test-first development, and implements a repository pattern for future persistence migration.

## Technical Context

**Language/Version**: Python 3.10+
**Primary Dependencies**: UVPy framework (CLI handling)
**Storage**: In-memory dictionary/list (Phase 1 - no persistence)
**Testing**: pytest
**Target Platform**: Cross-platform (Linux, macOS, Windows)
**Project Type**: Single project (CLI application)
**Performance Goals**: 
  - Add task: < 2 seconds
  - List tasks: < 1 second for up to 1000 tasks
  - 100% command success rate with proper exit codes
**Constraints**: 
  - No external database dependencies (Phase 1)
  - Text-based I/O only
  - Memory-only storage
**Scale/Scope**: 
  - Single CLI application
  - 5 core commands + exit
  - Support up to 1000 tasks in memory

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Spec-Driven Development | ✅ PASS | Spec complete at `specs/001-phase1-in-memory-todo/spec.md` |
| II. Test-First Development | ✅ PASS | Plan includes test structure; tests will precede implementation |
| III. In-Memory Storage | ✅ PASS | Repository pattern will abstract data access for future migration |
| IV. CLI Interface | ✅ PASS | All functionality via CLI commands with text I/O |
| V. Simplicity (YAGNI) | ✅ PASS | Only specified features (add, list, complete, delete, update) |

**Gate Result**: ✅ PASS - All principles satisfied. Proceed to Phase 0.

## Project Structure

### Documentation (this feature)

```text
specs/001-phase1-in-memory-todo/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
└── tasks.md             # Phase 2 output
```

### Source Code (repository root)

```text
src/
├── models/
│   └── task.py          # Task data class
├── services/
│   └── task_store.py    # In-memory repository
├── cli/
│   ├── __init__.py      # CLI entry point
│   ├── commands.py      # Command handlers
│   └── formatter.py     # Output formatting
└── lib/
    └── exceptions.py    # Custom exceptions

tests/
├── contract/
│   └── test_cli_contract.py  # CLI interface tests
├── integration/
│   └── test_commands.py      # Command integration tests
└── unit/
    ├── test_task.py          # Task model tests
    ├── test_task_store.py    # Repository tests
    └── test_commands.py      # Command handler tests
```

**Structure Decision**: Single project structure with clear separation between models, services, and CLI layers. Repository pattern implemented in `services/task_store.py` to satisfy Constitution Principle III (In-Memory Storage with future migration path).

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

No violations detected. All principles satisfied with standard complexity.

## Phase 0: Research & Decisions

*Status: ✅ COMPLETE*

### Research Completed

All technical decisions documented in `research.md`:

1. **CLI Framework**: Python `argparse` (built-in, no external deps)
2. **Repository Pattern**: Dictionary-based `TaskStore` with O(1) lookup
3. **ID Generation**: Auto-increment integers starting at 1
4. **Interactive Loop**: `input()` with command parsing
5. **Output Formatting**: Separate formatter module (text + JSON)
6. **Error Handling**: Custom exception hierarchy
7. **Testing Strategy**: Three-tier approach (unit, integration, contract)

**Output**: [`research.md`](research.md) - All NEEDS CLARIFICATION items resolved

## Phase 1: Design & Contracts

*Status: ✅ COMPLETE*

### Design Artifacts Created

1. **data-model.md**: Task entity with validation rules, TaskStore repository interface
2. **contracts/cli-commands.md**: All 7 commands fully specified with examples
3. **quickstart.md**: Developer onboarding guide
4. **Agent context update**: ✅ Completed via `.specify/scripts/bash/update-agent-context.sh qwen`

### Design Gates

- [x] Data model aligns with spec entities
- [x] Contracts cover all functional requirements (FR-001 through FR-017)
- [x] Quickstart enables developer onboarding
- [x] Constitution Check re-validated post-design (all principles still satisfied)

**Output**:
- [`data-model.md`](data-model.md)
- [`contracts/cli-commands.md`](contracts/cli-commands.md)
- [`quickstart.md`](quickstart.md)

## Phase 2: Task Breakdown

*Status: READY - Handoff to `/sp.tasks`*

All design artifacts complete. Ready for task breakdown creation.

---

## Detailed Implementation Plan

### 1️⃣ Project Structure Plan

**Recommended Python Project Structure:**

```
todoapp/
├── src/
│   ├── __init__.py              # Package marker
│   ├── main.py                  # Entry point (CLI loop)
│   ├── models/
│   │   ├── __init__.py
│   │   └── task.py              # Task data class (single responsibility: data structure)
│   ├── services/
│   │   ├── __init__.py
│   │   └── task_store.py        # Business logic layer (single responsibility: data management)
│   ├── cli/
│   │   ├── __init__.py
│   │   ├── parser.py            # Input parsing (single responsibility: parse user input)
│   │   ├── commands.py          # Command handlers (single responsibility: execute commands)
│   │   └── formatter.py         # Output formatting (single responsibility: format output)
│   └── exceptions.py            # Custom exceptions (single responsibility: error types)
├── tests/
│   ├── __init__.py
│   ├── unit/
│   │   ├── test_task.py
│   │   ├── test_task_store.py
│   │   ├── test_parser.py
│   │   └── test_formatter.py
│   ├── integration/
│   │   └── test_commands.py
│   └── contract/
│       └── test_cli_contract.py
└── requirements.txt
```

**Component Responsibilities:**

| Component | Single Responsibility |
|-----------|----------------------|
| `main.py` | Application entry point, main loop orchestration |
| `task.py` | Task data structure with validation |
| `task_store.py` | In-memory CRUD operations for tasks |
| `parser.py` | Parse raw input into command + arguments |
| `commands.py` | Map commands to business logic, handle errors |
| `formatter.py` | Convert tasks/results to human-readable or JSON output |
| `exceptions.py` | Define application-specific error types |

---

### 2️⃣ Data Flow Plan

**Task Lifecycle:**

```
User Input → Parser → Command Handler → TaskStore → Task → Formatter → Output
```

**Task Creation Flow:**
```
1. User: add "Buy groceries" "Need milk"
2. Parser: extracts command="add", title="Buy groceries", description="Need milk"
3. Command Handler: validates title non-empty
4. TaskStore:
   - Generates next_id (starts at 1, increments)
   - Creates Task(id=next_id, title=title, description=description, completed=False)
   - Stores in _tasks dictionary: _tasks[1] = task
   - Increments _next_id counter
5. Formatter: formats success message
6. Output: "✓ Task created: [1] 'Buy groceries'"
```

**Task Storage Mechanism:**
- **Backend**: `dict[int, Task]` for O(1) lookup by ID
- **ID Generation**: Counter `_next_id` starts at 1, increments after each creation
- **Ordering**: `get_all()` returns `sorted(self._tasks.values(), key=lambda t: t.id)`

**Task State Change Propagation:**
```
1. User: complete 1
2. Parser: extracts command="complete", id=1
3. Command Handler: validates ID is positive integer
4. TaskStore.toggle_complete(1):
   - Retrieves task from _tasks[1]
   - Flips task.completed: False → True
   - Returns updated task
5. Formatter: formats confirmation
6. Output: "✓ Task [1] marked as completed"
```

**Data Integrity:**
- IDs are never reused (prevents confusion)
- Tasks are immutable except through TaskStore methods
- All state changes go through TaskStore (single source of truth)

---

### 3️⃣ Command Handling Plan

**Input Parsing Approach:**
- Use `shlex.split()` for proper quote handling
- First token = command name
- Remaining tokens = arguments

**Per-Command Breakdown:**

#### `add <title> ["<description>"]`

| Step | Action |
|------|--------|
| **Input Parsing** | Extract title (required), description (optional, may be quoted) |
| **Validation** | Title must be non-empty, non-whitespace, ≤500 chars |
| **Execution** | Call `TaskStore.add(title, description)` |
| **Output** | Success: `✓ Task created: [ID] "Title"` |
| **Error** | Empty title → `Error: Title is required and cannot be empty` (exit 1) |

#### `list [--json]`

| Step | Action |
|------|--------|
| **Input Parsing** | Check for `--json` flag |
| **Validation** | No validation required |
| **Execution** | Call `TaskStore.get_all()`, sort by ID |
| **Output** | Human-readable table OR JSON array |
| **Error** | None (empty list shows friendly message) |

#### `update <id> ["<title>"] ["<description>"]`

| Step | Action |
|------|--------|
| **Input Parsing** | Extract id (required), new title, new description |
| **Validation** | ID must exist, new title (if provided) must be non-empty |
| **Execution** | Call `TaskStore.update(id, title=new_title, description=new_description)` |
| **Output** | Success: `✓ Task [ID] updated` |
| **Error** | Task not found → `Error: Task not found` (exit 1) |

#### `delete <id>`

| Step | Action |
|------|--------|
| **Input Parsing** | Extract id (required) |
| **Validation** | ID must be positive integer |
| **Execution** | Call `TaskStore.delete(id)` |
| **Output** | Success: `✓ Task [ID] deleted` |
| **Error** | Task not found → `Error: Task not found` (exit 1) |

#### `complete <id>`

| Step | Action |
|------|--------|
| **Input Parsing** | Extract id (required) |
| **Validation** | ID must be positive integer |
| **Execution** | Call `TaskStore.toggle_complete(id)` |
| **Output** | Success: `✓ Task [ID] marked as completed/incomplete` |
| **Error** | Task not found → `Error: Task not found` (exit 1) |

#### `exit`

| Step | Action |
|------|--------|
| **Input Parsing** | No arguments |
| **Validation** | None |
| **Execution** | Set loop_running = False |
| **Output** | `Goodbye!` |
| **Error** | None |

---

### 4️⃣ Control Loop Plan

**Main CLI Loop Structure:**

```python
def main_loop():
    """Run interactive CLI session."""
    task_store = TaskStore()
    loop_running = True

    print("Todo App - Phase 1. Type 'help' for commands, 'exit' to quit.")

    while loop_running:
        try:
            # 1. Accept user input
            user_input = input("> ").strip()

            # 2. Handle empty input
            if not user_input:
                continue

            # 3. Parse command
            command, args = parse_input(user_input)

            # 4. Handle exit command
            if command == "exit":
                print("Goodbye!")
                loop_running = False
                continue

            # 5. Execute command
            execute_command(command, args, task_store)

        except KeyboardInterrupt:
            # Handle Ctrl+C gracefully
            print("\nUse 'exit' to quit")
        except EOFError:
            # Handle Ctrl+D (end of input)
            print("\nGoodbye!")
            break
        except Exception as e:
            # Catch-all to prevent crash
            print(f"Error: {e}", file=sys.stderr)
```

**Invalid Command Handling:**
- Unknown command → `Error: Invalid command. Type 'help' for available commands.`
- Loop continues (does not crash)
- Error goes to stderr

**Clean Exit:**
- `exit` command sets `loop_running = False`
- `KeyboardInterrupt` (Ctrl+C) caught and handled
- `EOFError` (Ctrl+D) caught and handled
- Exit code 0 on normal exit, 1 on error

---

### 5️⃣ Error Handling Strategy

**Error Categories & Responses:**

| Error Type | Trigger | User Message | Exit Code |
|------------|---------|--------------|-----------|
| Missing Arguments | `add` without title | `Usage: add <title> ["<description>"]` | 1 |
| Empty Title | `add ""` or `add "   "` | `Error: Title is required and cannot be empty` | 1 |
| Invalid Task ID | `complete abc` | `Error: Task ID must be a positive integer` | 1 |
| Task Not Found | `delete 999` | `Error: Task not found` | 1 |
| Unknown Command | `foobar` | `Error: Invalid command. Type 'help' for available commands.` | 1 (continues loop) |
| Empty Task List | `list` with no tasks | `No tasks yet. Add one with: add <title>` | 0 |

**User-Friendly Messaging Rules:**
1. **Start with "Error:"** for all error messages
2. **Be specific** about what went wrong
3. **Provide guidance** when possible (e.g., usage examples)
4. **Never expose stack traces** to users
5. **Log errors to stderr**, success messages to stdout

**Exception Hierarchy:**
```python
class TodoAppError(Exception):
    """Base exception - provides consistent error formatting."""

class TaskNotFoundError(TodoAppError):
    message = "Task not found"

class EmptyTitleError(TodoAppError):
    message = "Title is required and cannot be empty"

class InvalidIdError(TodoAppError):
    message = "Task ID must be a positive integer"

class InvalidCommandError(TodoAppError):
    message = "Invalid command. Type 'help' for available commands."
```

---

### 6️⃣ Execution Order

**Logical Implementation Sequence:**

| Phase | Task | Dependencies | Estimated Effort |
|-------|------|--------------|------------------|
| **1** | Define `Task` data model with validation | None | 1 hour |
| **2** | Implement `TaskStore` (in-memory repository) | Task model | 2 hours |
| **3** | Create custom exceptions | None | 30 min |
| **4** | Implement input parser | Exceptions | 1 hour |
| **5** | Implement output formatter | Task model | 1 hour |
| **6** | Implement `add` command handler | TaskStore, Parser, Formatter | 1 hour |
| **7** | Implement `list` command handler | TaskStore, Formatter | 1 hour |
| **8** | Implement `complete` command handler | TaskStore, Formatter | 1 hour |
| **9** | Implement `delete` command handler | TaskStore, Formatter | 1 hour |
| **10** | Implement `update` command handler | TaskStore, Formatter | 1 hour |
| **11** | Implement `help` command | None | 30 min |
| **12** | Implement main CLI loop | All commands | 2 hours |
| **13** | Add validation and error handling | All components | 2 hours |
| **14** | Write unit tests | Each component | 4 hours |
| **15** | Write integration tests | All commands | 2 hours |
| **16** | Write contract tests | CLI interface | 2 hours |

**Total Estimated Effort**: ~22 hours

**Implementation Waves:**
- **Wave 1** (Tasks 1-5): Core data structures and utilities
- **Wave 2** (Tasks 6-11): Command implementations
- **Wave 3** (Tasks 12-13): Application integration
- **Wave 4** (Tasks 14-16): Testing (concurrent with Waves 1-3, test-first)

---

### 7️⃣ Non-Goals (Explicit Exclusions)

**Phase 1 MUST NOT implement:**

| Excluded Feature | Rationale |
|------------------|-----------|
| **File/Database Persistence** | Violates Constitution Principle III (In-Memory Storage for Phase 1) |
| **Authentication/User System** | Out of scope - single-user CLI app |
| **GUI or Web UI** | Violates Constitution Principle IV (CLI Interface only) |
| **Task Priority** | Beyond approved spec (FR-001 to FR-017) |
| **Due Dates/Deadlines** | Beyond approved spec |
| **Reminders/Notifications** | Beyond approved spec |
| **Task Categories/Tags** | Beyond approved spec |
| **Search/Filter** | Beyond approved spec (simple list only) |
| **Task Dependencies** | Beyond approved spec |
| **Recurring Tasks** | Beyond approved spec |
| **Export/Import** | Beyond approved spec |
| **Multi-user Support** | Beyond approved spec |
| **Cloud Sync** | Beyond approved spec |
| **Third-party Integrations** | Violates Constitution Principle V (Simplicity/YAGNI) |

**Constraint Summary:**
- ✅ Python standard library only (no third-party deps for Phase 1)
- ✅ In-memory storage only (no files, no database)
- ✅ CLI interface only (no GUI, no web)
- ✅ Only specified commands (add, list, update, delete, complete, exit, help)
- ✅ Deterministic, testable behavior

---

### 8️⃣ Output Requirements

**This Plan Delivers:**

1. ✅ Structured, numbered implementation plan
2. ✅ Clear responsibilities per component (single responsibility principle)
3. ✅ No code implementation (design only)
4. ✅ No feature expansion beyond approved spec (FR-001 to FR-017)
5. ✅ Explicit exclusions documented (Non-Goals section)
6. ✅ Logical execution order with effort estimates
7. ✅ Error handling strategy with user-friendly messages
8. ✅ Data flow diagrams for all operations
9. ✅ Control loop specification for CLI interaction
10. ✅ Test strategy (unit, integration, contract)
