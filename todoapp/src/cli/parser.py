"""Input parser for CLI commands."""

import shlex
from src.lib.exceptions import InvalidCommandError, InvalidIdError


class CommandParser:
    """Parse raw user input into commands and arguments."""
    
    VALID_COMMANDS = {"add", "list", "complete", "update", "delete", "help", "exit"}
    
    @staticmethod
    def parse(user_input: str) -> tuple[str, list[str]]:
        """Parse user input into command and arguments.
        
        Args:
            user_input: Raw user input string
            
        Returns:
            Tuple of (command, args_list)
            
        Raises:
            InvalidCommandError: If command is not recognized
        """
        if not user_input.strip():
            raise InvalidCommandError()
        
        # Use shlex for proper quote handling
        try:
            parts = shlex.split(user_input.strip())
        except ValueError:
            # Handle unclosed quotes
            raise InvalidCommandError()
        
        if not parts:
            raise InvalidCommandError()
        
        command = parts[0].lower()
        args = parts[1:]
        
        if command not in CommandParser.VALID_COMMANDS:
            raise InvalidCommandError()
        
        return command, args
    
    @staticmethod
    def parse_id(arg: str) -> int:
        """Parse and validate a task ID argument.
        
        Args:
            arg: String argument to parse
            
        Returns:
            Validated task ID as integer
            
        Raises:
            InvalidIdError: If ID is not a valid positive integer
        """
        try:
            task_id = int(arg)
            if task_id <= 0:
                raise InvalidIdError()
            return task_id
        except ValueError:
            raise InvalidIdError()
