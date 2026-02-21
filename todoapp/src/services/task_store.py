"""In-memory repository for task storage."""

from src.models.task import Task
from src.lib.exceptions import TaskNotFoundError


class TaskStore:
    """In-memory repository for tasks with CRUD operations.
    
    Uses dictionary-based storage for O(1) lookup by ID.
    Implements repository pattern for future persistence migration.
    """
    
    def __init__(self):
        """Initialize empty task store with ID counter starting at 1."""
        self._tasks: dict[int, Task] = {}
        self._next_id: int = 1
    
    def add(self, title: str, description: str | None = None) -> Task:
        """Create and store a new task.
        
        Args:
            title: Task title (required, non-empty)
            description: Optional description
            
        Returns:
            Newly created task with assigned ID
            
        Raises:
            EmptyTitleError: If title is empty or whitespace
        """
        task = Task(id=self._next_id, title=title, description=description)
        self._tasks[task.id] = task
        self._next_id += 1
        return task
    
    def get(self, id: int) -> Task | None:
        """Retrieve a task by ID.
        
        Args:
            id: Task unique identifier
            
        Returns:
            Task if found, None otherwise
        """
        return self._tasks.get(id)
    
    def get_all(self) -> list[Task]:
        """Retrieve all tasks in ascending ID order.
        
        Returns:
            List of all tasks sorted by ID
        """
        return sorted(self._tasks.values(), key=lambda t: t.id)
    
    def update(self, id: int, title: str | None = None, 
               description: str | None = None) -> Task | None:
        """Update task title and/or description.
        
        Args:
            id: Task unique identifier
            title: New title (if provided, must be non-empty)
            description: New description (if provided)
            
        Returns:
            Updated task if found, None otherwise
            
        Raises:
            TaskNotFoundError: If task ID doesn't exist
            EmptyTitleError: If new title is empty
        """
        task = self.get(id)
        if task is None:
            raise TaskNotFoundError()
        task.update(title=title, description=description)
        return task
    
    def delete(self, id: int) -> bool:
        """Delete a task by ID.
        
        Args:
            id: Task unique identifier
            
        Returns:
            True if deleted, False if not found
        """
        if id in self._tasks:
            del self._tasks[id]
            return True
        return False
    
    def toggle_complete(self, id: int) -> Task | None:
        """Toggle task completion status.
        
        Args:
            id: Task unique identifier
            
        Returns:
            Updated task if found, None otherwise
        """
        task = self.get(id)
        if task is None:
            return None
        task.toggle()
        return task
    
    def count(self) -> int:
        """Return the total number of tasks."""
        return len(self._tasks)
