# Data Model: Phase 1 In-Memory Todo App

**Date**: 2026-02-21
**Branch**: `001-phase1-in-memory-todo`
**Purpose**: Define data structures and validation rules

---

## Entity: Task

**Description**: A single todo item with required title, optional description, and completion status.

### Fields

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `id` | `int` | Yes (auto) | > 0, unique | Unique identifier assigned on creation |
| `title` | `str` | Yes | 1-500 chars, not whitespace-only | Task title/summary |
| `description` | `str` | No | 0-500 chars | Optional detailed description |
| `completed` | `bool` | Yes | Default: `False` | Completion status |

### Validation Rules

1. **ID Validation**:
   - MUST be a positive integer (> 0)
   - MUST be unique across all tasks
   - Auto-generated on creation (never user-provided)

2. **Title Validation**:
   - MUST NOT be empty
   - MUST NOT be whitespace-only
   - MUST NOT exceed 500 characters
   - MAY contain special characters, unicode, etc.

3. **Description Validation**:
   - MAY be empty string or `None`
   - MUST NOT exceed 500 characters
   - MAY contain special characters, unicode, etc.

4. **Completion Status**:
   - MUST be boolean (`True` or `False`)
   - Defaults to `False` on creation
   - Toggles on `complete` command

### State Transitions

```
┌─────────────┐
│   Created   │
│ completed=False │
└──────┬──────┘
       │
       │ complete command
       ▼
┌─────────────┐
│  Completed  │
│ completed=True  │
└──────┬──────┘
       │
       │ complete command (toggle)
       ▼
┌─────────────┐
│   Active    │
│ completed=False │
└─────────────┘
```

### Example Instances

**Minimal Task** (title only):
```python
Task(id=1, title="Buy groceries", description=None, completed=False)
```

**Full Task** (with description):
```python
Task(id=2, title="Finish report", description="Due tomorrow EOD", completed=False)
```

**Completed Task**:
```python
Task(id=3, title="Send email", description=None, completed=True)
```

---

## Entity: TaskStore (Repository)

**Description**: In-memory collection providing CRUD operations for tasks. Implements repository pattern for future persistence migration.

### Interface

```python
class TaskStore:
    """In-memory repository for tasks."""
    
    def __init__(self) -> None:
        """Initialize empty task store."""
    
    def add(self, title: str, description: str | None = None) -> Task:
        """
        Create and store a new task.
        
        Args:
            title: Task title (required, non-empty)
            description: Optional description
            
        Returns:
            Newly created task with assigned ID
            
        Raises:
            EmptyTitleError: If title is empty or whitespace
        """
    
    def get(self, id: int) -> Task | None:
        """
        Retrieve a task by ID.
        
        Args:
            id: Task unique identifier
            
        Returns:
            Task if found, None otherwise
        """
    
    def get_all(self) -> list[Task]:
        """
        Retrieve all tasks in ascending ID order.
        
        Returns:
            List of all tasks sorted by ID
        """
    
    def update(self, id: int, title: str | None = None, 
               description: str | None = None) -> Task | None:
        """
        Update task title and/or description.
        
        Args:
            id: Task unique identifier
            title: New title (if provided)
            description: New description (if provided)
            
        Returns:
            Updated task if found, None otherwise
            
        Raises:
            EmptyTitleError: If new title is empty
            TaskNotFoundError: If task ID doesn't exist
        """
    
    def delete(self, id: int) -> bool:
        """
        Delete a task by ID.
        
        Args:
            id: Task unique identifier
            
        Returns:
            True if deleted, False if not found
        """
    
    def toggle_complete(self, id: int) -> Task | None:
        """
        Toggle task completion status.
        
        Args:
            id: Task unique identifier
            
        Returns:
            Updated task if found, None otherwise
        """
```

### Implementation Notes

1. **Storage Backend**: Dictionary (`dict[int, Task]`) for O(1) lookup
2. **ID Generation**: Auto-increment counter starting at 1
3. **Ordering**: `get_all()` returns tasks sorted by ID (ascending)
4. **Thread Safety**: Not required for Phase 1 (single-user CLI)

---

## Exceptions

### Exception Hierarchy

```
TodoAppError (base)
├── TaskNotFoundError
├── EmptyTitleError
└── InvalidCommandError
```

### Exception Specifications

**TodoAppError**:
```python
class TodoAppError(Exception):
    """Base exception for all todo app errors."""
```

**TaskNotFoundError**:
```python
class TaskNotFoundError(TodoAppError):
    """Raised when a task ID does not exist."""
    message = "Task not found"
```

**EmptyTitleError**:
```python
class EmptyTitleError(TodoAppError):
    """Raised when task title is empty or whitespace-only."""
    message = "Title is required and cannot be empty"
```

**InvalidCommandError**:
```python
class InvalidCommandError(TodoAppError):
    """Raised when an unrecognized command is entered."""
    message = "Invalid command. Type 'help' for available commands."
```

---

## Data Flow Diagrams

### Add Task Flow

```
User Input → CLI Parser → Validate Title → TaskStore.add() → Task Created → Format Output → Display
                              ↓
                       EmptyTitleError → Error Message → Display
```

### List Tasks Flow

```
User Input → CLI Parser → TaskStore.get_all() → Sort by ID → Format Output → Display
```

### Complete Task Flow

```
User Input → CLI Parser → Get Task ID → TaskStore.toggle_complete() → Task Updated → Format Output → Display
                                    ↓
                            TaskNotFoundError → Error Message → Display
```

### Update Task Flow

```
User Input → CLI Parser → Get Task ID → Validate New Title → TaskStore.update() → Task Updated → Format Output → Display
                                    ↓                              ↓
                            TaskNotFoundError            EmptyTitleError → Error Message → Display
```

### Delete Task Flow

```
User Input → CLI Parser → Get Task ID → TaskStore.delete() → Task Deleted → Format Output → Display
                                    ↓
                            TaskNotFoundError → Error Message → Display
```

---

## Migration Path (Future Phases)

The repository pattern enables future persistence without changing business logic:

**Phase 2 (File Persistence)**:
```python
class FileTaskStore(TaskStore):
    """File-based task store (JSON backend)."""
    
    def __init__(self, filepath: str):
        self.filepath = filepath
        self._tasks = self._load_from_file()
```

**Phase 3 (Database Persistence)**:
```python
class DatabaseTaskStore(TaskStore):
    """Database-backed task store (SQLite/PostgreSQL)."""
    
    def __init__(self, connection_string: str):
        self.db = connect(connection_string)
```

**Key Point**: CLI layer and command handlers remain unchanged; only repository implementation changes.
