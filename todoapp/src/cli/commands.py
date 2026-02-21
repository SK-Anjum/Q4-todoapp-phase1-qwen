"""Command handlers for CLI."""

import sys
from src.services.task_store import TaskStore
from src.cli.formatter import TaskFormatter
from src.cli.parser import CommandParser
from src.lib.exceptions import (
    TodoAppError,
    EmptyTitleError,
    TaskNotFoundError,
    InvalidIdError,
    InvalidCommandError,
)


class CommandHandler:
    """Handle CLI commands and coordinate between parser, store, and formatter."""
    
    def __init__(self, store: TaskStore):
        """Initialize handler with task store.
        
        Args:
            store: TaskStore instance for data operations
        """
        self.store = store
    
    def handle(self, command: str, args: list[str]) -> tuple[str, int]:
        """Handle a command and return output and exit code.
        
        Args:
            command: Command name
            args: List of command arguments
            
        Returns:
            Tuple of (output_message, exit_code)
        """
        handlers = {
            "add": self.handle_add,
            "list": self.handle_list,
            "complete": self.handle_complete,
            "update": self.handle_update,
            "delete": self.handle_delete,
            "help": self.handle_help,
            "exit": self.handle_exit,
        }
        
        handler = handlers.get(command)
        if handler is None:
            return TaskFormatter.format_error("Invalid command. Type 'help' for available commands."), 1
        
        try:
            return handler(args)
        except EmptyTitleError as e:
            return TaskFormatter.format_error(e.message), 1
        except TaskNotFoundError as e:
            return TaskFormatter.format_error(e.message), 1
        except InvalidIdError as e:
            return TaskFormatter.format_error(e.message), 1
        except TodoAppError as e:
            return TaskFormatter.format_error(e.message), 1
        except Exception as e:
            return TaskFormatter.format_error(str(e)), 1
    
    def handle_add(self, args: list[str]) -> tuple[str, int]:
        """Handle 'add' command.
        
        Args:
            args: List containing title and optional description
            
        Returns:
            Tuple of (output_message, exit_code)
        """
        if not args:
            return TaskFormatter.format_error("Usage: add <title> [\"<description>\"]"), 1
        
        title = args[0]
        description = args[1] if len(args) > 1 else None
        
        task = self.store.add(title, description)
        return TaskFormatter.format_task_created(task), 0
    
    def handle_list(self, args: list[str]) -> tuple[str, int]:
        """Handle 'list' command.
        
        Args:
            args: List potentially containing --json flag
            
        Returns:
            Tuple of (output_message, exit_code)
        """
        format_type = "json" if "--json" in args else "text"
        tasks = self.store.get_all()
        output = TaskFormatter.format_task_list(tasks, format=format_type)
        return output, 0
    
    def handle_complete(self, args: list[str]) -> tuple[str, int]:
        """Handle 'complete' command.
        
        Args:
            args: List containing task ID
            
        Returns:
            Tuple of (output_message, exit_code)
        """
        if not args:
            return TaskFormatter.format_error("Usage: complete <id>"), 1
        
        task_id = CommandParser.parse_id(args[0])
        task = self.store.toggle_complete(task_id)
        
        if task is None:
            raise TaskNotFoundError()
        
        return TaskFormatter.format_task_completed(task), 0
    
    def handle_update(self, args: list[str]) -> tuple[str, int]:
        """Handle 'update' command.
        
        Args:
            args: List containing task ID and optional new title/description
            
        Returns:
            Tuple of (output_message, exit_code)
        """
        if not args:
            return TaskFormatter.format_error("Usage: update <id> [\"<title>\"] [\"<description>\"]"), 1
        
        task_id = CommandParser.parse_id(args[0])
        
        # Extract optional title and description
        title = args[1] if len(args) > 1 else None
        description = args[2] if len(args) > 2 else None
        
        task = self.store.update(task_id, title=title, description=description)
        
        if task is None:
            raise TaskNotFoundError()
        
        return TaskFormatter.format_task_updated(task), 0
    
    def handle_delete(self, args: list[str]) -> tuple[str, int]:
        """Handle 'delete' command.
        
        Args:
            args: List containing task ID
            
        Returns:
            Tuple of (output_message, exit_code)
        """
        if not args:
            return TaskFormatter.format_error("Usage: delete <id>"), 1
        
        task_id = CommandParser.parse_id(args[0])
        result = self.store.delete(task_id)
        
        if not result:
            raise TaskNotFoundError()
        
        return TaskFormatter.format_task_deleted(task_id), 0
    
    def handle_help(self, args: list[str]) -> tuple[str, int]:
        """Handle 'help' command.
        
        Args:
            args: Unused
            
        Returns:
            Tuple of (output_message, exit_code)
        """
        return TaskFormatter.format_help(), 0
    
    def handle_exit(self, args: list[str]) -> tuple[str, int]:
        """Handle 'exit' command.
        
        Args:
            args: Unused
            
        Returns:
            Tuple of (output_message, exit_code)
        """
        return "Goodbye!", 0
