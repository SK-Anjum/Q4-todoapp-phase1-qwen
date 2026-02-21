"""Custom exceptions for the Todo application."""


class TodoAppError(Exception):
    """Base exception for all todo app errors."""
    message = "An error occurred"

    def __init__(self, message: str | None = None):
        self.message = message or self.message
        super().__init__(self.message)


class TaskNotFoundError(TodoAppError):
    """Raised when a task ID does not exist."""
    message = "Task not found"


class EmptyTitleError(TodoAppError):
    """Raised when task title is empty or whitespace-only."""
    message = "Title is required and cannot be empty"


class InvalidIdError(TodoAppError):
    """Raised when task ID is not a valid positive integer."""
    message = "Task ID must be a positive integer"


class InvalidCommandError(TodoAppError):
    """Raised when an unrecognized command is entered."""
    message = "Invalid command. Type 'help' for available commands."
