"""Contract tests for CLI interface."""

import pytest
from src.cli.parser import CommandParser, InvalidCommandError, InvalidIdError
from src.cli.formatter import TaskFormatter
from src.services.task_store import TaskStore
from src.lib.exceptions import EmptyTitleError, TaskNotFoundError


class TestAddCommand:
    """Test 'add' command contract."""
    
    def test_add_command_parsed_correctly(self):
        """Test that add command is parsed correctly."""
        cmd, args = CommandParser.parse('add "Buy groceries"')
        assert cmd == "add"
        assert args == ["Buy groceries"]
    
    def test_add_command_with_description(self):
        """Test add command with description."""
        cmd, args = CommandParser.parse('add "Title" "Description"')
        assert cmd == "add"
        assert args == ["Title", "Description"]
    
    def test_add_execution_creates_task(self):
        """Test that executing add creates a task."""
        store = TaskStore()
        task = store.add("Buy groceries", "Need milk")
        assert task.id == 1
        assert task.title == "Buy groceries"
    
    def test_add_empty_title_error(self):
        """Test add with empty title raises error."""
        store = TaskStore()
        with pytest.raises(EmptyTitleError):
            store.add("")
    
    def test_add_success_message_format(self):
        """Test add success message format."""
        store = TaskStore()
        task = store.add("Test")
        message = TaskFormatter.format_task_created(task)
        assert message == '✓ Task created: [1] "Test"'


class TestListCommand:
    """Test 'list' command contract."""
    
    def test_list_command_parsed_correctly(self):
        """Test that list command is parsed correctly."""
        cmd, args = CommandParser.parse('list')
        assert cmd == "list"
        assert args == []
    
    def test_list_command_with_json_flag(self):
        """Test list command with --json flag."""
        cmd, args = CommandParser.parse('list --json')
        assert cmd == "list"
        assert args == ["--json"]
    
    def test_list_empty_store_message(self):
        """Test list with no tasks shows friendly message."""
        store = TaskStore()
        tasks = store.get_all()
        output = TaskFormatter.format_task_list(tasks)
        assert output == "No tasks yet. Add one with: add <title>"
    
    def test_list_with_tasks_shows_all(self):
        """Test list shows all tasks."""
        store = TaskStore()
        store.add("First")
        store.add("Second")
        tasks = store.get_all()
        output = TaskFormatter.format_task_list(tasks)
        assert "[1]" in output
        assert "[2]" in output
        assert "First" in output
        assert "Second" in output
    
    def test_list_json_format(self):
        """Test list JSON output format."""
        store = TaskStore()
        store.add("Test")
        tasks = store.get_all()
        output = TaskFormatter.format_task_list(tasks, format="json")
        assert '"id": 1' in output
        assert '"title": "Test"' in output
        assert '"completed": false' in output


class TestCompleteCommand:
    """Test 'complete' command contract."""
    
    def test_complete_command_parsed_correctly(self):
        """Test that complete command is parsed correctly."""
        cmd, args = CommandParser.parse('complete 1')
        assert cmd == "complete"
        assert args == ["1"]
    
    def test_complete_id_must_be_integer(self):
        """Test that complete requires integer ID."""
        with pytest.raises(InvalidIdError):
            CommandParser.parse_id("abc")
    
    def test_complete_toggles_status(self):
        """Test complete toggles task status."""
        store = TaskStore()
        store.add("Task")
        task = store.toggle_complete(1)
        assert task is not None
        assert task.completed is True
    
    def test_complete_nonexistent_task(self):
        """Test complete on nonexistent task."""
        store = TaskStore()
        task = store.toggle_complete(999)
        assert task is None
    
    def test_complete_success_message(self):
        """Test complete success message format."""
        store = TaskStore()
        store.add("Task")
        task = store.toggle_complete(1)
        message = TaskFormatter.format_task_completed(task)
        assert message == "✓ Task [1] marked as completed"


class TestDeleteCommand:
    """Test 'delete' command contract."""
    
    def test_delete_command_parsed_correctly(self):
        """Test that delete command is parsed correctly."""
        cmd, args = CommandParser.parse('delete 1')
        assert cmd == "delete"
        assert args == ["1"]
    
    def test_delete_removes_task(self):
        """Test delete removes task from store."""
        store = TaskStore()
        store.add("To delete")
        result = store.delete(1)
        assert result is True
        assert store.get(1) is None
    
    def test_delete_nonexistent_task(self):
        """Test delete on nonexistent task."""
        store = TaskStore()
        result = store.delete(999)
        assert result is False
    
    def test_delete_success_message(self):
        """Test delete success message format."""
        message = TaskFormatter.format_task_deleted(1)
        assert message == "✓ Task [1] deleted"


class TestUpdateCommand:
    """Test 'update' command contract."""
    
    def test_update_command_parsed_correctly(self):
        """Test that update command is parsed correctly."""
        cmd, args = CommandParser.parse('update 1 "New title"')
        assert cmd == "update"
        assert args == ["1", "New title"]
    
    def test_update_changes_title(self):
        """Test update changes task title."""
        store = TaskStore()
        store.add("Old title")
        updated = store.update(1, title="New title")
        assert updated is not None
        assert updated.title == "New title"
    
    def test_update_nonexistent_task(self):
        """Test update on nonexistent task."""
        store = TaskStore()
        with pytest.raises(TaskNotFoundError):
            store.update(999, title="New")
    
    def test_update_success_message(self):
        """Test update success message format."""
        store = TaskStore()
        store.add("Title")
        task = store.update(1, title="Updated")
        message = TaskFormatter.format_task_updated(task)
        assert message == "✓ Task [1] updated"


class TestHelpCommand:
    """Test 'help' command contract."""
    
    def test_help_command_parsed_correctly(self):
        """Test that help command is parsed correctly."""
        cmd, args = CommandParser.parse('help')
        assert cmd == "help"
        assert args == []
    
    def test_help_message_format(self):
        """Test help message contains all commands."""
        help_text = TaskFormatter.format_help()
        assert "add" in help_text
        assert "list" in help_text
        assert "complete" in help_text
        assert "delete" in help_text
        assert "update" in help_text
        assert "exit" in help_text


class TestExitCommand:
    """Test 'exit' command contract."""
    
    def test_exit_command_parsed_correctly(self):
        """Test that exit command is parsed correctly."""
        cmd, args = CommandParser.parse('exit')
        assert cmd == "exit"
        assert args == []


class TestInvalidCommands:
    """Test invalid command handling."""
    
    def test_unknown_command_raises_error(self):
        """Test unknown command raises InvalidCommandError."""
        with pytest.raises(InvalidCommandError):
            CommandParser.parse('foobar')
    
    def test_empty_input_raises_error(self):
        """Test empty input raises InvalidCommandError."""
        with pytest.raises(InvalidCommandError):
            CommandParser.parse('')
    
    def test_whitespace_only_raises_error(self):
        """Test whitespace-only input raises InvalidCommandError."""
        with pytest.raises(InvalidCommandError):
            CommandParser.parse('   ')
