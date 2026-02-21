"""Task data model for the Todo application."""

from dataclasses import dataclass, field
from src.lib.exceptions import EmptyTitleError


@dataclass
class Task:
    """A single todo item with ID, title, description, and completion status.
    
    Attributes:
        id: Unique identifier assigned on creation (auto-generated)
        title: Task title (required, 1-500 chars, non-empty)
        description: Optional detailed description (0-500 chars)
        completed: Completion status (False = pending, True = completed)
    """
    
    id: int
    title: str
    description: str | None = None
    completed: bool = field(default=False)
    
    def __post_init__(self):
        """Validate task data after initialization."""
        self._validate_title()
        self._validate_description()
        self._validate_id()
    
    def _validate_id(self) -> None:
        """Validate task ID is a positive integer."""
        if not isinstance(self.id, int) or self.id <= 0:
            raise ValueError("Task ID must be a positive integer")
    
    def _validate_title(self) -> None:
        """Validate title is non-empty and within length limits."""
        if not self.title or not self.title.strip():
            raise EmptyTitleError()
        if len(self.title) > 500:
            raise ValueError("Title must not exceed 500 characters")
    
    def _validate_description(self) -> None:
        """Validate description is within length limits if provided."""
        if self.description and len(self.description) > 500:
            raise ValueError("Description must not exceed 500 characters")
    
    def toggle(self) -> None:
        """Toggle the completion status."""
        self.completed = not self.completed
    
    def update(self, title: str | None = None, description: str | None = None) -> None:
        """Update task title and/or description.

        Args:
            title: New title (if provided, must be non-empty)
            description: New description (if provided)
        """
        if title is not None:
            if not title.strip():
                raise EmptyTitleError()
            if len(title) > 500:
                raise ValueError("Title must not exceed 500 characters")
            self.title = title

        if description is not None:
            if len(description) > 500:
                raise ValueError("Description must not exceed 500 characters")
            self.description = description
