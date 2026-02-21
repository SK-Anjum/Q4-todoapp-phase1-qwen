# Tasks: Phase 1 In-Memory Todo App

**Input**: Design documents from `/specs/001-phase1-in-memory-todo/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Test tasks are INCLUDED - Constitution Principle II requires Test-First Development (TDD).

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- Paths follow plan.md structure: `src/models/`, `src/services/`, `src/cli/`, `src/lib/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create project structure: src/models/, src/services/, src/cli/, src/lib/, tests/unit/, tests/integration/, tests/contract/
- [x] T002 Create src/__init__.py, src/models/__init__.py, src/services/__init__.py, src/cli/__init__.py, src/lib/__init__.py, tests/__init__.py
- [x] T003 [P] Create requirements.txt with Python 3.10+ compatibility (no external deps for Phase 1)
- [x] T004 [P] Create pytest.ini configuration for test discovery
- [x] T005 [P] Create .gitignore for Python projects

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T006 [P] Create custom exceptions in src/lib/exceptions.py: TodoAppError, TaskNotFoundError, EmptyTitleError, InvalidIdError, InvalidCommandError
- [x] T007 [P] Create Task data model in src/models/task.py with fields: id, title, description, completed
- [x] T008 [P] Create TaskStore in src/services/task_store.py with in-memory dictionary storage
- [x] T009 [P] Create output formatter in src/cli/formatter.py with text and JSON format support
- [x] T010 [P] Create input parser in src/cli/parser.py using shlex.split() for quote handling

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Add a New Task (Priority: P1) 🎯 MVP

**Goal**: Users can add tasks with required title and optional description

**Independent Test**: Can be fully tested by adding a task and verifying it appears in the task list

### Tests for User Story 1 ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T011 [P] [US1] Unit test Task model validation in tests/unit/test_task.py
- [ ] T012 [P] [US1] Unit test TaskStore.add() in tests/unit/test_task_store.py
- [ ] T013 [P] [US1] Contract test for 'add' command in tests/contract/test_cli_contract.py

### Implementation for User Story 1

- [ ] T014 [P] [US1] Add Task model validation: title required, non-empty, max 500 chars in src/models/task.py
- [ ] T015 [US1] Implement TaskStore.add(title, description) in src/services/task_store.py (depends on T014)
- [ ] T016 [US1] Implement 'add' command handler in src/cli/commands.py
- [ ] T017 [US1] Add success message formatting: "✓ Task created: [ID] 'Title'" in src/cli/formatter.py
- [ ] T018 [US1] Add error handling for EmptyTitleError in src/cli/commands.py

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - List All Tasks (Priority: P1)

**Goal**: Users can view all tasks in ascending ID order with completion status

**Independent Test**: Can be tested by adding tasks and verifying they appear correctly in the list output

### Tests for User Story 2 ⚠️

- [ ] T019 [P] [US2] Unit test TaskStore.get_all() sorting in tests/unit/test_task_store.py
- [ ] T020 [P] [US2] Contract test for 'list' command (text format) in tests/contract/test_cli_contract.py
- [ ] T021 [P] [US2] Contract test for 'list --json' command in tests/contract/test_cli_contract.py

### Implementation for User Story 2

- [ ] T022 [P] [US2] Implement TaskStore.get_all() with ID sorting in src/services/task_store.py
- [ ] T023 [US2] Implement text format task list display in src/cli/formatter.py
- [ ] T024 [US2] Implement JSON format task list output in src/cli/formatter.py
- [ ] T025 [US2] Implement 'list' command handler with --json flag support in src/cli/commands.py
- [ ] T026 [US2] Add empty list message: "No tasks yet. Add one with: add <title>" in src/cli/formatter.py

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Mark Task as Complete (Priority: P2)

**Goal**: Users can toggle task completion status using task ID

**Independent Test**: Can be tested by marking a task complete and verifying its status changes

### Tests for User Story 3 ⚠️

- [ ] T027 [P] [US3] Unit test TaskStore.toggle_complete() in tests/unit/test_task_store.py
- [ ] T028 [P] [US3] Contract test for 'complete' command in tests/contract/test_cli_contract.py

### Implementation for User Story 3

- [ ] T029 [P] [US3] Implement TaskStore.toggle_complete(id) in src/services/task_store.py
- [ ] T030 [US3] Implement 'complete' command handler with ID validation in src/cli/commands.py
- [ ] T031 [US3] Add TaskNotFoundError handling for non-existent IDs in src/cli/commands.py
- [ ] T032 [US3] Add success message: "✓ Task [ID] marked as completed/incomplete" in src/cli/formatter.py

**Checkpoint**: At this point, User Stories 1, 2, AND 3 should all work independently

---

## Phase 6: User Story 4 - Delete a Task (Priority: P2)

**Goal**: Users can remove tasks using task ID

**Independent Test**: Can be tested by deleting a task and verifying it no longer appears in the list

### Tests for User Story 4 ⚠️

- [ ] T033 [P] [US4] Unit test TaskStore.delete() in tests/unit/test_task_store.py
- [ ] T034 [P] [US4] Contract test for 'delete' command in tests/contract/test_cli_contract.py

### Implementation for User Story 4

- [ ] T035 [P] [US4] Implement TaskStore.delete(id) in src/services/task_store.py
- [ ] T036 [US4] Implement 'delete' command handler with ID validation in src/cli/commands.py
- [ ] T037 [US4] Add success message: "✓ Task [ID] deleted" in src/cli/formatter.py
- [ ] T038 [US4] Add TaskNotFoundError handling in src/cli/commands.py

**Checkpoint**: At this point, User Stories 1-4 should all work independently

---

## Phase 7: User Story 5 - Update Task (Priority: P2)

**Goal**: Users can update task title and/or description using task ID

**Independent Test**: Can be tested by updating a task and verifying its title/description changes

### Tests for User Story 5 ⚠️

- [ ] T039 [P] [US5] Unit test TaskStore.update() in tests/unit/test_task_store.py
- [ ] T040 [P] [US5] Contract test for 'update' command in tests/contract/test_cli_contract.py

### Implementation for User Story 5

- [ ] T041 [P] [US5] Implement TaskStore.update(id, title, description) in src/services/task_store.py
- [ ] T042 [US5] Implement 'update' command handler with optional arguments in src/cli/commands.py
- [ ] T043 [US5] Add success message: "✓ Task [ID] updated" in src/cli/formatter.py
- [ ] T044 [US5] Add EmptyTitleError and TaskNotFoundError handling in src/cli/commands.py

**Checkpoint**: At this point, User Stories 1-5 should all work independently

---

## Phase 8: User Story 6 - Interactive CLI Session (Priority: P3)

**Goal**: Users can run multiple commands in a single interactive session

**Independent Test**: Can be tested by running the app, entering multiple commands, and exiting

### Tests for User Story 6 ⚠️

- [ ] T045 [P] [US6] Integration test for CLI loop in tests/integration/test_commands.py
- [ ] T046 [P] [US6] Contract test for 'help' command in tests/contract/test_cli_contract.py
- [ ] T047 [P] [US6] Contract test for 'exit' command in tests/contract/test_cli_contract.py

### Implementation for User Story 6

- [ ] T048 [P] [US6] Implement main CLI loop in src/main.py with input() and error handling
- [ ] T049 [US6] Implement command dispatcher to route commands to handlers in src/cli/commands.py
- [ ] T050 [US6] Implement 'help' command with usage examples in src/cli/commands.py
- [ ] T051 [US6] Implement 'exit' command with graceful shutdown in src/cli/commands.py
- [ ] T052 [US6] Add KeyboardInterrupt and EOFError handling in src/main.py
- [ ] T053 [US6] Add application entry point: python -m src.cli in src/__main__.py

**Checkpoint**: All user stories should now be independently functional

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T054 [P] Create quickstart validation test in tests/integration/test_quickstart.py
- [ ] T055 [P] Run pytest --cov=src --cov-report=term-missing to verify 80%+ coverage
- [ ] T056 Code cleanup and refactoring (remove duplication, improve naming)
- [ ] T057 [P] Add integration tests for complete user workflows in tests/integration/test_commands.py
- [ ] T058 [P] Add unit tests for parser module in tests/unit/test_parser.py
- [ ] T059 [P] Add unit tests for formatter module in tests/unit/test_formatter.py
- [ ] T060 Verify all error messages go to stderr, success messages to stdout
- [ ] T061 [P] Update README.md with installation and usage instructions
- [ ] T062 [P] Verify quickstart.md examples work as documented

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-8)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Phase 9)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational (Phase 2) - Independent, may use US1 components
- **User Story 3 (P2)**: Can start after Foundational (Phase 2) - Independent
- **User Story 4 (P2)**: Can start after Foundational (Phase 2) - Independent
- **User Story 5 (P2)**: Can start after Foundational (Phase 2) - Independent
- **User Story 6 (P3)**: Can start after Foundational (Phase 2) - Integrates all previous stories

### Within Each User Story

- Tests MUST be written and FAIL before implementation (TDD)
- Models before services
- Services before command handlers
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- **Phase 1 (Setup)**: T003, T004, T005 can run in parallel
- **Phase 2 (Foundational)**: T006, T007, T008, T009, T010 can run in parallel (different files)
- **Phase 3-8 (User Stories)**: All test tasks within a story can run in parallel
- **Phase 3-8 (User Stories)**: All model tasks within a story can run in parallel
- **Across Stories**: Once Phase 2 complete, different developers can work on different stories

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together:
# (Run these in parallel, ensure they all FAIL before implementation)
Task: "Unit test Task model validation in tests/unit/test_task.py"
Task: "Unit test TaskStore.add() in tests/unit/test_task_store.py"
Task: "Contract test for 'add' command in tests/contract/test_cli_contract.py"

# Launch all models for User Story 1 together:
# (Different files, can be done in parallel)
Task: "Add Task model validation in src/models/task.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (add command only)
4. **STOP and VALIDATE**: Test 'add' and 'list' commands work
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 (add + list) → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 (complete) → Test independently → Deploy/Demo
4. Add User Story 3 (delete) → Test independently → Deploy/Demo
5. Add User Story 4 (update) → Test independently → Deploy/Demo
6. Add User Story 5 (interactive CLI) → Test independently → Deploy/Demo
7. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (add, list)
   - Developer B: User Story 3 (complete)
   - Developer C: User Story 4 (delete)
3. Then continue:
   - Developer A: User Story 5 (update)
   - Developer B: User Story 6 (interactive CLI)
4. Stories complete and integrate independently

---

## Task Summary

| Phase | User Story | Priority | Task Count | Independent Test |
|-------|-----------|----------|------------|------------------|
| 1 | Setup | - | 5 | N/A |
| 2 | Foundational | - | 5 | N/A |
| 3 | Add a New Task | P1 | 8 | Add task, verify in list |
| 4 | List All Tasks | P1 | 8 | List shows all tasks correctly |
| 5 | Mark Task Complete | P2 | 7 | Toggle completion status |
| 6 | Delete a Task | P2 | 7 | Delete removes task from list |
| 7 | Update Task | P2 | 7 | Update changes title/description |
| 8 | Interactive CLI | P3 | 9 | Multiple commands in session |
| 9 | Polish | - | 9 | Cross-cutting concerns |

**Total Tasks**: 65

**MVP Scope** (minimum viable product): Phases 1-4 (23 tasks)
- Add tasks with title/description
- List all tasks with completion status

---

## Notes

- [P] tasks = different files, no dependencies on incomplete tasks
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing (TDD requirement)
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Constitution Principle II: Test-First is NON-NEGOTIABLE
