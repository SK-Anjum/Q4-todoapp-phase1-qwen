"""Main entry point for the Todo CLI application."""

import sys
from src.services.task_store import TaskStore
from src.cli.commands import CommandHandler
from src.cli.parser import CommandParser
from src.lib.exceptions import InvalidCommandError


def main_loop():
    """Run interactive CLI session."""
    store = TaskStore()
    handler = CommandHandler(store)
    loop_running = True
    
    print("Todo App - Phase 1. Type 'help' for commands, 'exit' to quit.")
    
    while loop_running:
        try:
            # Accept user input
            try:
                user_input = input("> ").strip()
            except EOFError:
                # Handle Ctrl+D (end of input)
                print("\nGoodbye!")
                break
            
            # Handle empty input
            if not user_input:
                continue
            
            # Parse command
            try:
                command, args = CommandParser.parse(user_input)
            except InvalidCommandError as e:
                print(f"Error: {e.message}", file=sys.stderr)
                continue
            
            # Handle exit command
            if command == "exit":
                output, _ = handler.handle(command, args)
                print(output)
                loop_running = False
                continue
            
            # Execute command
            output, exit_code = handler.handle(command, args)
            if exit_code != 0:
                print(output, file=sys.stderr)
            else:
                print(output)
                
        except KeyboardInterrupt:
            # Handle Ctrl+C gracefully
            print("\nUse 'exit' to quit", file=sys.stderr)
        except Exception as e:
            # Catch-all to prevent crash
            print(f"Error: {e}", file=sys.stderr)


def main():
    """Main entry point."""
    main_loop()
    return 0


if __name__ == "__main__":
    sys.exit(main())
