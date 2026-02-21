"""Output formatter for CLI responses."""

import json
from src.models.task import Task


class TaskFormatter:
    """Format tasks and messages for CLI output.
    
    Supports both human-readable text format and JSON format.
    """
    
    @staticmethod
    def format_task(task: Task, show_description: bool = True) -> str:
        """Format a single task for display.
        
        Args:
            task: Task to format
            show_description: Whether to show description if available
            
        Returns:
            Formatted task string
        """
        status = "[x]" if task.completed else "[ ]"
        line = f"[{task.id}] {status} {task.title}"
        
        if show_description and task.description:
            line += f"\n    Description: {task.description}"
        
        return line
    
    @staticmethod
    def format_task_list(tasks: list[Task], format: str = "text") -> str:
        """Format a list of tasks.
        
        Args:
            tasks: List of tasks to format
            format: Output format ('text' or 'json')
            
        Returns:
            Formatted task list string
        """
        if not tasks:
            if format == "text":
                return "No tasks yet. Add one with: add <title>"
            return "[]"
        
        if format == "json":
            return json.dumps([
                {
                    "id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "completed": task.completed
                }
                for task in tasks
            ], indent=2)
        
        # Text format
        lines = [TaskFormatter.format_task(task) for task in tasks]
        return "\n\n".join(lines)
    
    @staticmethod
    def format_success(message: str) -> str:
        """Format a success message.
        
        Args:
            message: Success message text
            
        Returns:
            Formatted success message
        """
        return f"✓ {message}"
    
    @staticmethod
    def format_task_created(task: Task) -> str:
        """Format task creation success message.
        
        Args:
            task: The created task
            
        Returns:
            Formatted success message
        """
        return f"✓ Task created: [{task.id}] \"{task.title}\""
    
    @staticmethod
    def format_task_updated(task: Task) -> str:
        """Format task update success message.
        
        Args:
            task: The updated task
            
        Returns:
            Formatted success message
        """
        return f"✓ Task [{task.id}] updated"
    
    @staticmethod
    def format_task_deleted(task_id: int) -> str:
        """Format task deletion success message.
        
        Args:
            task_id: ID of deleted task
            
        Returns:
            Formatted success message
        """
        return f"✓ Task [{task_id}] deleted"
    
    @staticmethod
    def format_task_completed(task: Task) -> str:
        """Format task completion toggle message.
        
        Args:
            task: The toggled task
            
        Returns:
            Formatted success message
        """
        status = "completed" if task.completed else "incomplete"
        return f"✓ Task [{task.id}] marked as {status}"
    
    @staticmethod
    def format_error(message: str) -> str:
        """Format an error message.
        
        Args:
            message: Error message text
            
        Returns:
            Formatted error message
        """
        return f"Error: {message}"
    
    @staticmethod
    def format_help() -> str:
        """Format help message with available commands.
        
        Returns:
            Formatted help message
        """
        return """Todo App - Phase 1

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
  delete 1"""
