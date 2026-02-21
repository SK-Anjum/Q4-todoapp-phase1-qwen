"""Unit tests for Task model."""

import pytest
from src.models.task import Task
from src.lib.exceptions import EmptyTitleError


class TestTaskCreation:
    """Test task creation and validation."""
    
    def test_create_task_with_title_only(self):
        """Test creating a task with just a title."""
        task = Task(id=1, title="Buy groceries")
        assert task.id == 1
        assert task.title == "Buy groceries"
        assert task.description is None
        assert task.completed is False
    
    def test_create_task_with_description(self):
        """Test creating a task with title and description."""
        task = Task(id=1, title="Buy groceries", description="Need milk and eggs")
        assert task.title == "Buy groceries"
        assert task.description == "Need milk and eggs"
        assert not task.completed
    
    def test_create_completed_task(self):
        """Test creating a task that's already completed."""
        task = Task(id=1, title="Done task", completed=True)
        assert task.completed is True


class TestTaskValidation:
    """Test task validation rules."""
    
    def test_empty_title_raises_error(self):
        """Test that empty title raises EmptyTitleError."""
        with pytest.raises(EmptyTitleError):
            Task(id=1, title="")
    
    def test_whitespace_only_title_raises_error(self):
        """Test that whitespace-only title raises EmptyTitleError."""
        with pytest.raises(EmptyTitleError):
            Task(id=1, title="   ")
    
    def test_title_max_length(self):
        """Test that title over 500 chars raises ValueError."""
        with pytest.raises(ValueError):
            Task(id=1, title="a" * 501)
    
    def test_description_max_length(self):
        """Test that description over 500 chars raises ValueError."""
        with pytest.raises(ValueError):
            Task(id=1, title="Valid", description="b" * 501)
    
    def test_invalid_id_raises_error(self):
        """Test that non-positive ID raises ValueError."""
        with pytest.raises(ValueError):
            Task(id=0, title="Test")
        
        with pytest.raises(ValueError):
            Task(id=-1, title="Test")


class TestTaskToggle:
    """Test task completion toggle."""
    
    def test_toggle_from_incomplete_to_complete(self):
        """Test toggling an incomplete task."""
        task = Task(id=1, title="Test", completed=False)
        task.toggle()
        assert task.completed is True
    
    def test_toggle_from_complete_to_incomplete(self):
        """Test toggling a completed task."""
        task = Task(id=1, title="Test", completed=True)
        task.toggle()
        assert task.completed is False
    
    def test_double_toggle_returns_original(self):
        """Test that toggling twice returns to original state."""
        task = Task(id=1, title="Test", completed=False)
        task.toggle()
        task.toggle()
        assert task.completed is False


class TestTaskUpdate:
    """Test task update functionality."""
    
    def test_update_title_only(self):
        """Test updating only the title."""
        task = Task(id=1, title="Old title", description="Desc")
        task.update(title="New title")
        assert task.title == "New title"
        assert task.description == "Desc"
    
    def test_update_description_only(self):
        """Test updating only the description."""
        task = Task(id=1, title="Title", description="Old desc")
        task.update(description="New desc")
        assert task.title == "Title"
        assert task.description == "New desc"
    
    def test_update_both_fields(self):
        """Test updating both title and description."""
        task = Task(id=1, title="Old title", description="Old desc")
        task.update(title="New title", description="New desc")
        assert task.title == "New title"
        assert task.description == "New desc"
    
    def test_update_empty_title_raises_error(self):
        """Test that updating to empty title raises EmptyTitleError."""
        task = Task(id=1, title="Title")
        with pytest.raises(EmptyTitleError):
            task.update(title="")
    
    def test_update_no_changes(self):
        """Test update with no arguments makes no changes."""
        task = Task(id=1, title="Title", description="Desc")
        task.update()
        assert task.title == "Title"
        assert task.description == "Desc"
