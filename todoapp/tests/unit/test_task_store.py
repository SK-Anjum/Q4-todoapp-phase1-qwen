"""Unit tests for TaskStore repository."""

import pytest
from src.services.task_store import TaskStore
from src.models.task import Task
from src.lib.exceptions import EmptyTitleError, TaskNotFoundError


class TestTaskStoreAdd:
    """Test TaskStore.add() method."""
    
    def test_add_task_returns_task_with_id(self):
        """Test adding a task returns task with auto-generated ID."""
        store = TaskStore()
        task = store.add("Test task")
        assert task.id == 1
        assert task.title == "Test task"
        assert not task.completed
    
    def test_add_task_with_description(self):
        """Test adding a task with description."""
        store = TaskStore()
        task = store.add("Test", "Description")
        assert task.description == "Description"
    
    def test_add_multiple_tasks_increments_id(self):
        """Test that adding multiple tasks increments ID."""
        store = TaskStore()
        task1 = store.add("First")
        task2 = store.add("Second")
        task3 = store.add("Third")
        assert task1.id == 1
        assert task2.id == 2
        assert task3.id == 3
    
    def test_add_empty_title_raises_error(self):
        """Test that adding with empty title raises EmptyTitleError."""
        store = TaskStore()
        with pytest.raises(EmptyTitleError):
            store.add("")
    
    def test_add_whitespace_title_raises_error(self):
        """Test that adding with whitespace-only title raises error."""
        store = TaskStore()
        with pytest.raises(EmptyTitleError):
            store.add("   ")


class TestTaskStoreGet:
    """Test TaskStore.get() method."""
    
    def test_get_existing_task(self):
        """Test getting an existing task."""
        store = TaskStore()
        added = store.add("Test")
        retrieved = store.get(added.id)
        assert retrieved is not None
        assert retrieved.id == added.id
        assert retrieved.title == "Test"
    
    def test_get_nonexistent_task(self):
        """Test getting a task that doesn't exist."""
        store = TaskStore()
        task = store.get(999)
        assert task is None


class TestTaskStoreGetAll:
    """Test TaskStore.get_all() method."""
    
    def test_get_all_empty_store(self):
        """Test getting all tasks from empty store."""
        store = TaskStore()
        tasks = store.get_all()
        assert tasks == []
    
    def test_get_all_returns_sorted_by_id(self):
        """Test that get_all returns tasks sorted by ID."""
        store = TaskStore()
        store.add("Third")
        store.add("First")
        store.add("Second")
        tasks = store.get_all()
        assert len(tasks) == 3
        assert tasks[0].id == 1
        assert tasks[1].id == 2
        assert tasks[2].id == 3
    
    def test_get_all_after_delete(self):
        """Test get_all after deleting a task."""
        store = TaskStore()
        store.add("First")
        store.add("Second")
        store.delete(1)
        tasks = store.get_all()
        assert len(tasks) == 1
        assert tasks[0].id == 2


class TestTaskStoreUpdate:
    """Test TaskStore.update() method."""
    
    def test_update_existing_task(self):
        """Test updating an existing task."""
        store = TaskStore()
        store.add("Original")
        updated = store.update(1, title="Updated")
        assert updated is not None
        assert updated.title == "Updated"
    
    def test_update_nonexistent_task_raises_error(self):
        """Test that updating nonexistent task raises TaskNotFoundError."""
        store = TaskStore()
        with pytest.raises(TaskNotFoundError):
            store.update(999, title="Updated")
    
    def test_update_with_empty_title_raises_error(self):
        """Test that updating to empty title raises EmptyTitleError."""
        store = TaskStore()
        store.add("Title")
        with pytest.raises(EmptyTitleError):
            store.update(1, title="")


class TestTaskStoreDelete:
    """Test TaskStore.delete() method."""
    
    def test_delete_existing_task(self):
        """Test deleting an existing task."""
        store = TaskStore()
        store.add("To delete")
        result = store.delete(1)
        assert result is True
        assert store.get(1) is None
    
    def test_delete_nonexistent_task(self):
        """Test deleting a task that doesn't exist."""
        store = TaskStore()
        result = store.delete(999)
        assert result is False


class TestTaskStoreToggleComplete:
    """Test TaskStore.toggle_complete() method."""
    
    def test_toggle_incomplete_task(self):
        """Test toggling an incomplete task."""
        store = TaskStore()
        store.add("Task")
        task = store.toggle_complete(1)
        assert task is not None
        assert task.completed is True
    
    def test_toggle_completed_task(self):
        """Test toggling a completed task back."""
        store = TaskStore()
        store.add("Task")
        store.toggle_complete(1)
        task = store.toggle_complete(1)
        assert task is not None
        assert task.completed is False
    
    def test_toggle_nonexistent_task(self):
        """Test toggling a task that doesn't exist."""
        store = TaskStore()
        task = store.toggle_complete(999)
        assert task is None


class TestTaskStoreCount:
    """Test TaskStore.count() method."""
    
    def test_count_empty_store(self):
        """Test count of empty store."""
        store = TaskStore()
        assert store.count() == 0
    
    def test_count_after_adds(self):
        """Test count after adding tasks."""
        store = TaskStore()
        store.add("One")
        store.add("Two")
        assert store.count() == 2
    
    def test_count_after_delete(self):
        """Test count after deleting."""
        store = TaskStore()
        store.add("One")
        store.add("Two")
        store.delete(1)
        assert store.count() == 1
