# CLI Command Contracts: Phase 1 In-Memory Todo App

**Date**: 2026-02-21
**Branch**: `001-phase1-in-memory-todo`
**Purpose**: Define CLI command interfaces, arguments, outputs, and error handling

---

## Command Overview

| Command | Arguments | Description | Exit Code |
|---------|-----------|-------------|-----------|
| `add` | `<title> ["description"]` | Create a new task | 0 success, 1 error |
| `list` | `[--json]` | Display all tasks | 0 |
| `complete` | `<id>` | Toggle task completion | 0 success, 1 error |
| `update` | `<id> [title] [description]` | Modify task | 0 success, 1 error |
| `delete` | `<id>` | Remove a task | 0 success, 1 error |
| `help` | None | Show available commands | 0 |
| `exit` | None | Quit application | 0 |

---

## Command: add

**Purpose**: Create a new task with required title and optional description.

### Syntax

```bash
add <title> ["<description>"]
```

### Arguments

| Argument | Required | Type | Description |
|----------|----------|------|-------------|
| `title` | Yes | String | Task title (1-500 chars, non-empty) |
| `description` | No | String | Optional description (0-500 chars) |

### Success Output

**Human-readable**:
```
✓ Task created: [ID] "Title"
```

**Example**:
```
✓ Task created: [1] "Buy groceries"
```

### Error Cases

| Error | Trigger | Output | Exit Code |
|-------|---------|--------|-----------|
| Empty title | `add ""` or `add "   "` | `Error: Title is required and cannot be empty` | 1 |
| Missing title | `add` (no arguments) | `Usage: add <title> ["<description>"]` | 1 |

---

## Command: list

**Purpose**: Display all tasks in ascending ID order.

### Syntax

```bash
list [--json]
```

### Arguments

| Argument | Required | Type | Description |
|----------|----------|------|-------------|
| `--json` | No | Flag | Output in JSON format instead of human-readable |

### Success Output

**Human-readable** (with tasks):
```
[1] [ ] Buy groceries
    Description: Need milk and eggs

[2] [x] Finish report
    Description: Due tomorrow EOD

[3] [ ] Send email
```

**Human-readable** (empty list):
```
No tasks yet. Add one with: add <title>
```

**JSON format**:
```json
[
  {"id": 1, "title": "Buy groceries", "description": "Need milk and eggs", "completed": false},
  {"id": 2, "title": "Finish report", "description": "Due tomorrow EOD", "completed": true},
  {"id": 3, "title": "Send email", "description": null, "completed": false}
]
```

### Error Cases

None - command always succeeds (empty list is valid state).

---

## Command: complete

**Purpose**: Toggle task completion status (incomplete → complete, complete → incomplete).

### Syntax

```bash
complete <id>
```

### Arguments

| Argument | Required | Type | Description |
|----------|----------|------|-------------|
| `id` | Yes | Integer | Task unique identifier |

### Success Output

**Human-readable**:
```
✓ Task [ID] marked as completed
```
or
```
✓ Task [ID] marked as incomplete
```

**Example**:
```
✓ Task [1] marked as completed
```

### Error Cases

| Error | Trigger | Output | Exit Code |
|-------|---------|--------|-----------|
| Task not found | `complete 999` (non-existent ID) | `Error: Task not found` | 1 |
| Invalid ID format | `complete abc` | `Error: Task ID must be a positive integer` | 1 |
| Missing ID | `complete` (no arguments) | `Usage: complete <id>` | 1 |

---

## Command: update

**Purpose**: Update task title and/or description.

### Syntax

```bash
update <id> ["<new title>"] ["<new description>"]
```

### Arguments

| Argument | Required | Type | Description |
|----------|----------|------|-------------|
| `id` | Yes | Integer | Task unique identifier |
| `new title` | No | String | New title (if provided) |
| `new description` | No | String | New description (if provided) |

### Behavior

- If only `id` provided: No change (or info message)
- If `id` + `title` provided: Update title only
- If `id` + `title` + `description` provided: Update both
- If `id` + empty `title` + `description` provided: Error (empty title)

### Success Output

**Human-readable**:
```
✓ Task [ID] updated
```

**Example**:
```
✓ Task [1] updated
```

### Error Cases

| Error | Trigger | Output | Exit Code |
|-------|---------|--------|-----------|
| Task not found | `update 999 "New title"` | `Error: Task not found` | 1 |
| Empty title | `update 1 ""` | `Error: Title is required and cannot be empty` | 1 |
| Invalid ID format | `update abc "Title"` | `Error: Task ID must be a positive integer` | 1 |
| Missing ID | `update` (no arguments) | `Usage: update <id> ["<title>"] ["<description>"]` | 1 |

---

## Command: delete

**Purpose**: Remove a task from the store.

### Syntax

```bash
delete <id>
```

### Arguments

| Argument | Required | Type | Description |
|----------|----------|------|-------------|
| `id` | Yes | Integer | Task unique identifier |

### Success Output

**Human-readable**:
```
✓ Task [ID] deleted
```

**Example**:
```
✓ Task [2] deleted
```

### Error Cases

| Error | Trigger | Output | Exit Code |
|-------|---------|--------|-----------|
| Task not found | `delete 999` (non-existent ID) | `Error: Task not found` | 1 |
| Invalid ID format | `delete abc` | `Error: Task ID must be a positive integer` | 1 |
| Missing ID | `delete` (no arguments) | `Usage: delete <id>` | 1 |

---

## Command: help

**Purpose**: Display available commands and usage examples.

### Syntax

```bash
help
```

### Output

```
Todo App - Phase 1

Commands:
  add <title> ["<description>"]   - Create a new task
  list [--json]                   - Display all tasks
  complete <id>                   - Toggle task completion status
  update <id> ["<title>"] ["<description>"] - Update a task
  delete <id>                     - Remove a task
  help                            - Show this help message
  exit                            - Quit the application

Examples:
  add "Buy groceries" "Need milk and eggs"
  list
  list --json
  complete 1
  update 1 "New title"
  delete 1
```

---

## Command: exit

**Purpose**: Terminate the interactive CLI session.

### Syntax

```bash
exit
```

### Behavior

- Gracefully terminates the application
- Exit code: 0

### Output

```
Goodbye!
```

---

## Interactive Mode Behavior

### Prompt

```
> 
```

### Invalid Command Handling

**Input**: `invalidcmd`

**Output**:
```
Error: Invalid command. Type 'help' for available commands.
> 
```

### Keyboard Interrupt (Ctrl+C)

**Behavior**: Catch interrupt, display message, continue running

**Output**:
```
^C
Use 'exit' to quit
> 
```

### Empty Input

**Behavior**: Ignore, re-display prompt

**Output**:
```
> 
> 
```

---

## Exit Codes Summary

| Exit Code | Meaning | When |
|-----------|---------|------|
| 0 | Success | Command executed successfully, `exit` command |
| 1 | Error | Invalid arguments, task not found, empty title |

---

## Output Streams

| Stream | Content |
|--------|---------|
| stdout | Success messages, task lists, help text |
| stderr | Error messages |

**Example**:
```bash
# Success → stdout
$ add "Task"
✓ Task created: [1] "Task"

# Error → stderr
$ add ""
Error: Title is required and cannot be empty  # → stderr
```
