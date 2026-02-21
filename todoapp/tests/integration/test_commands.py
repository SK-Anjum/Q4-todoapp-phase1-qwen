"""Integration tests for CLI commands."""

import pytest
from src.services.task_store import TaskStore
from src.cli.commands import CommandHandler


class TestAddAndListIntegration:
    """Integration tests for add and list commands."""
    
    def test_add_then_list_shows_task(self):
        """Test that adding a task shows it in the list."""
        store = TaskStore()
        handler = CommandHandler(store)
        
        # Add a task
        output, exit_code = handler.handle("add", ["Buy groceries"])
        assert exit_code == 0
        assert "Task created" in output
        
        # List tasks
        output, exit_code = handler.handle("list", [])
        assert exit_code == 0
        assert "Buy groceries" in output
    
    def test_add_multiple_tasks_list_sorted(self):
        """Test adding multiple tasks and listing in order."""
        store = TaskStore()
        handler = CommandHandler(store)

        handler.handle("add", ["Third"])
        handler.handle("add", ["First"])
        handler.handle("add", ["Second"])

        output, exit_code = handler.handle("list", [])

        # Verify exit code is success
        assert exit_code == 0

        # Verify tasks are listed in ID order (by finding the ID patterns)
        # Task 1 (Third) should appear before Task 2 (First) before Task 3 (Second)
        lines = output.split('\n')
        task_lines = [l for l in lines if '[' in l and ']' in l and 'Description' not in l]

        assert len(task_lines) == 3
        assert '[1]' in task_lines[0] and 'Third' in task_lines[0]
        assert '[2]' in task_lines[1] and 'First' in task_lines[1]
        assert '[3]' in task_lines[2] and 'Second' in task_lines[2]


class TestCompleteIntegration:
    """Integration tests for complete command."""
    
    def test_complete_then_list_shows_status(self):
        """Test completing a task shows [x] in list."""
        store = TaskStore()
        handler = CommandHandler(store)
        
        store.add("Task to complete")
        output, exit_code = handler.handle("complete", ["1"])
        
        assert exit_code == 0
        assert "completed" in output
        
        output, _ = handler.handle("list", [])
        assert "[x]" in output


class TestDeleteIntegration:
    """Integration tests for delete command."""
    
    def test_delete_then_list_removes_task(self):
        """Test deleting a task removes it from list."""
        store = TaskStore()
        handler = CommandHandler(store)
        
        store.add("To delete")
        output, exit_code = handler.handle("delete", ["1"])
        
        assert exit_code == 0
        assert "deleted" in output
        
        output, _ = handler.handle("list", [])
        assert "To delete" not in output


class TestUpdateIntegration:
    """Integration tests for update command."""
    
    def test_update_then_list_shows_changes(self):
        """Test updating a task shows changes in list."""
        store = TaskStore()
        handler = CommandHandler(store)
        
        store.add("Old title")
        output, exit_code = handler.handle("update", ["1", "New title"])
        
        assert exit_code == 0
        assert "updated" in output
        
        output, _ = handler.handle("list", [])
        assert "New title" in output
        assert "Old title" not in output


class TestErrorHandlingIntegration:
    """Integration tests for error handling."""
    
    def test_add_empty_title_error(self):
        """Test add with empty title returns error."""
        store = TaskStore()
        handler = CommandHandler(store)
        
        output, exit_code = handler.handle("add", [""])
        
        assert exit_code == 1
        assert "Error:" in output
        assert "empty" in output.lower()
    
    def test_complete_nonexistent_task_error(self):
        """Test complete with invalid ID returns error."""
        store = TaskStore()
        handler = CommandHandler(store)
        
        output, exit_code = handler.handle("complete", ["999"])
        
        assert exit_code == 1
        assert "Error:" in output
        assert "not found" in output.lower()
    
    def test_delete_nonexistent_task_error(self):
        """Test delete with invalid ID returns error."""
        store = TaskStore()
        handler = CommandHandler(store)
        
        output, exit_code = handler.handle("delete", ["999"])
        
        assert exit_code == 1
        assert "Error:" in output
        assert "not found" in output.lower()
    
    def test_update_nonexistent_task_error(self):
        """Test update with invalid ID returns error."""
        store = TaskStore()
        handler = CommandHandler(store)
        
        output, exit_code = handler.handle("update", ["999", "New title"])
        
        assert exit_code == 1
        assert "Error:" in output
        assert "not found" in output.lower()


class TestWorkflowIntegration:
    """Full workflow integration tests."""
    
    def test_full_crud_workflow(self):
        """Test complete CRUD workflow."""
        store = TaskStore()
        handler = CommandHandler(store)
        
        # Create
        output, exit_code = handler.handle("add", ["Task 1"])
        assert exit_code == 0
        
        # Read
        output, exit_code = handler.handle("list", [])
        assert exit_code == 0
        assert "Task 1" in output
        
        # Update
        output, exit_code = handler.handle("update", ["1", "Updated Task"])
        assert exit_code == 0
        
        # Verify update
        output, _ = handler.handle("list", [])
        assert "Updated Task" in output
        
        # Complete
        output, exit_code = handler.handle("complete", ["1"])
        assert exit_code == 0
        
        # Verify complete
        output, _ = handler.handle("list", [])
        assert "[x]" in output
        
        # Delete
        output, exit_code = handler.handle("delete", ["1"])
        assert exit_code == 0
        
        # Verify delete
        output, _ = handler.handle("list", [])
        assert "Updated Task" not in output
