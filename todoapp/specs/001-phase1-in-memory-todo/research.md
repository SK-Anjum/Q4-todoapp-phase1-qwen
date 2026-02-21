# Research & Technical Decisions: Phase 1 In-Memory Todo App

**Date**: 2026-02-21
**Branch**: `001-phase1-in-memory-todo`
**Purpose**: Resolve all NEEDS CLARIFICATION items from Technical Context

---

## Decision 1: Python CLI Framework

**Decision**: Use Python's built-in `argparse` module for CLI argument parsing

**Rationale**: 
- No external dependencies required (aligns with Simplicity principle)
- Standard library, well-documented, stable
- Sufficient for simple CLI commands (add, list, complete, delete, update, exit)
- Cross-platform compatibility guaranteed

**Alternatives Considered**:
| Alternative | Pros | Cons | Why Rejected |
|-------------|------|------|--------------|
| `click` | Rich features, decorators | External dependency | Overkill for simple CLI; violates YAGNI |
| `typer` | Type hints, auto-completion | External dependency | Not needed for Phase 1 scope |
| `argparse` (chosen) | Built-in, no deps, stable | More verbose | Perfect fit for simple requirements |

**Note on UVPy**: UVPy is the project's Python framework convention. For Phase 1 CLI app, `argparse` satisfies the CLI Interface principle without requiring additional framework layers.

---

## Decision 2: Repository Pattern Implementation

**Decision**: Implement `TaskStore` class as an in-memory repository with dictionary-based storage

**Rationale**:
- Satisfies Constitution Principle III (In-Memory Storage with migration path)
- Dictionary provides O(1) lookup by ID
- Easy to replace with database backend in future phases
- Clean separation of concerns (data access vs business logic)

**Implementation Approach**:
```python
class TaskStore:
    def __init__(self):
        self._tasks: dict[int, Task] = {}
        self._next_id: int = 1
    
    def add(self, task: Task) -> Task
    def get(self, id: int) -> Task | None
    def get_all(self) -> list[Task]
    def update(self, id: int, **kwargs) -> Task | None
    def delete(self, id: int) -> bool
    def toggle_complete(self, id: int) -> Task | None
```

**Alternatives Considered**:
| Alternative | Pros | Cons | Why Rejected |
|-------------|------|------|--------------|
| List storage | Simple | O(n) lookup | Poor performance for large task counts |
| Dictionary (chosen) | O(1) lookup, simple | Slightly more complex | Best balance |
| SQLite | Persistent | Violates Phase 1 constraint | Not allowed in Phase 1 |

---

## Decision 3: Task ID Generation Strategy

**Decision**: Use auto-incrementing integer IDs starting from 1

**Rationale**:
- Simple and predictable
- Easy for users to reference tasks
- Sufficient for Phase 1 scope (up to 1000 tasks)
- Can be migrated to UUID in future phases if needed

**Alternatives Considered**:
| Alternative | Pros | Cons | Why Rejected |
|-------------|------|------|--------------|
| Auto-increment int (chosen) | Simple, user-friendly | Not globally unique | Perfect for single-user CLI app |
| UUID | Globally unique | Verbose for CLI usage | Overkill for Phase 1 |
| Timestamp-based | Sortable | Potential collisions | Unnecessary complexity |

---

## Decision 4: Interactive CLI Loop Implementation

**Decision**: Use `input()` loop with command parsing for interactive mode

**Rationale**:
- Simplest approach for interactive CLI
- Built-in Python functionality
- Easy to implement error handling
- Aligns with Simplicity principle

**Implementation Approach**:
```python
def main_loop():
    while True:
        try:
            user_input = input("> ").strip()
            if user_input == "exit":
                break
            command, args = parse_command(user_input)
            execute_command(command, args)
        except KeyboardInterrupt:
            print("\nUse 'exit' to quit")
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
```

**Alternatives Considered**:
| Alternative | Pros | Cons | Why Rejected |
|-------------|------|------|--------------|
| `input()` loop (chosen) | Simple, built-in | Blocking I/O | Perfect for single-user CLI |
| `readline` module | History, completion | More complex | Not needed for Phase 1 |
| `prompt_toolkit` | Rich features | External dependency | Violates YAGNI |

---

## Decision 5: Output Formatting Strategy

**Decision**: Implement separate formatter module with human-readable and JSON output modes

**Rationale**:
- Satisfies FR-017 (both output formats required)
- Clean separation of concerns
- Easy to extend with new formats
- Aligns with CLI Interface principle

**Implementation Approach**:
```python
class TaskFormatter:
    @staticmethod
    def format_task(task: Task, format: str = "text") -> str
    @staticmethod
    def format_task_list(tasks: list[Task], format: str = "text") -> str
    @staticmethod
    def format_error(message: str, format: str = "text") -> str
```

**Human-readable format**:
```
[1] [ ] Buy groceries
    Description: Need milk and eggs

[2] [x] Finish report
    Description: Due tomorrow
```

**JSON format**:
```json
[
  {"id": 1, "title": "Buy groceries", "description": "Need milk and eggs", "completed": false},
  {"id": 2, "title": "Finish report", "description": "Due tomorrow", "completed": true}
]
```

---

## Decision 6: Error Handling Strategy

**Decision**: Use custom exception classes with centralized error handling in CLI layer

**Rationale**:
- Clean separation of error types
- Consistent error messages
- Easy to test
- Prevents application crashes (SC-006)

**Exception Hierarchy**:
```python
class TodoAppError(Exception):
    """Base exception for todo app"""

class TaskNotFoundError(TodoAppError):
    """Raised when task ID doesn't exist"""

class EmptyTitleError(TodoAppError):
    """Raised when task title is empty"""

class InvalidCommandError(TodoAppError):
    """Raised when command is not recognized"""
```

---

## Decision 7: Testing Strategy

**Decision**: Three-tier testing approach (unit, integration, contract)

**Rationale**:
- Satisfies Constitution Principle II (Test-First Development)
- Clear test boundaries and purposes
- Enables 80%+ code coverage requirement

**Test Structure**:
| Test Type | Location | Purpose |
|-----------|----------|---------|
| Unit | `tests/unit/` | Test individual classes/functions in isolation |
| Integration | `tests/integration/` | Test command handlers with TaskStore |
| Contract | `tests/contract/` | Test CLI interface matches specification |

**Test-First Workflow**:
1. Write failing test (Red)
2. User approves test
3. Implement minimum code to pass (Green)
4. Refactor while keeping tests passing (Refactor)

---

## Summary of Technical Decisions

| Decision | Choice | Impact |
|----------|--------|--------|
| CLI Framework | `argparse` | No external deps, standard library |
| Repository Pattern | Dictionary-based `TaskStore` | Migration-ready, O(1) lookup |
| ID Generation | Auto-increment integers | Simple, user-friendly |
| Interactive Loop | `input()` with parsing | Built-in, simple |
| Output Formatting | Separate formatter module | Both text and JSON supported |
| Error Handling | Custom exceptions | Crash-free operation |
| Testing | Three-tier approach | 80%+ coverage achievable |

---

## Constitution Compliance Verification

All research decisions align with constitution principles:

- ✅ **Spec-Driven**: All decisions trace back to functional requirements
- ✅ **Test-First**: Testing strategy defined before implementation
- ✅ **In-Memory Storage**: Repository pattern enables future migration
- ✅ **CLI Interface**: All decisions support text-based I/O
- ✅ **Simplicity (YAGNI)**: No unnecessary dependencies or complexity

**Research Complete**: All NEEDS CLARIFICATION items resolved. Ready for Phase 1 design.
