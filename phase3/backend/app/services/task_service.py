from typing import List, Optional
from sqlmodel import Session, select
from datetime import datetime, timedelta
from ..models.task import Task, TaskCreate, TaskUpdate, TaskRead
import json


class TaskService:
    def create_task(self, db: Session, task_data: TaskCreate, user_id: int) -> TaskRead:
        """Create a new task with advanced features"""
        db_task = Task(
            title=task_data.title,
            description=task_data.description,
            completed=task_data.completed,
            priority=task_data.priority,
            tags=task_data.tags if task_data.tags else [],
            due_date=task_data.due_date,
            recurring=task_data.recurring,
            recurrence_pattern=task_data.recurrence_pattern,
            parent_task_id=task_data.parent_task_id,
            user_id=user_id
        )
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        return TaskRead.from_orm(db_task) if hasattr(TaskRead, 'from_orm') else TaskRead(
            id=db_task.id,
            title=db_task.title,
            description=db_task.description,
            completed=db_task.completed,
            priority=db_task.priority,
            tags=db_task.tags,
            due_date=db_task.due_date,
            recurring=db_task.recurring,
            recurrence_pattern=db_task.recurrence_pattern,
            parent_task_id=db_task.parent_task_id,
            user_id=db_task.user_id,
            created_at=db_task.created_at,
            updated_at=db_task.updated_at,
            reminder_sent=db_task.reminder_sent
        )

    def get_task(self, db: Session, task_id: int, user_id: int) -> Optional[TaskRead]:
        """Get a specific task for a user"""
        statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        db_task = db.exec(statement).first()
        if db_task:
            return TaskRead.from_orm(db_task) if hasattr(TaskRead, 'from_orm') else TaskRead(
                id=db_task.id,
                title=db_task.title,
                description=db_task.description,
                completed=db_task.completed,
                priority=db_task.priority,
                tags=db_task.tags,
                due_date=db_task.due_date,
                recurring=db_task.recurring,
                recurrence_pattern=db_task.recurrence_pattern,
                parent_task_id=db_task.parent_task_id,
                user_id=db_task.user_id,
                created_at=db_task.created_at,
                updated_at=db_task.updated_at,
                reminder_sent=db_task.reminder_sent
            )
        return None

    def get_tasks(
        self,
        db: Session,
        user_id: int,
        completed: Optional[bool] = None,
        priority: Optional[str] = None,
        tags: Optional[List[str]] = None,
        due_date_from: Optional[datetime] = None,
        due_date_to: Optional[datetime] = None,
        search_query: Optional[str] = None,
        sort_by: str = "created_at",
        sort_order: str = "asc"
    ) -> List[TaskRead]:
        """Get all tasks for a user with filters and sorting"""
        statement = select(Task).where(Task.user_id == user_id)

        # Apply filters
        if completed is not None:
            statement = statement.where(Task.completed == completed)

        if priority is not None:
            statement = statement.where(Task.priority == priority)

        if tags:
            # Filter tasks that contain any of the specified tags
            # Since tags are stored as JSON, we need to handle differently
            # For now, we'll filter in memory
            pass  # We'll handle tags filtering in memory below

        if due_date_from:
            statement = statement.where(Task.due_date >= due_date_from)

        if due_date_to:
            statement = statement.where(Task.due_date <= due_date_to)

        if search_query:
            statement = statement.where(
                Task.title.contains(search_query) |
                Task.description.contains(search_query)
            )

        # Apply sorting
        if sort_by == "due_date":
            if sort_order == "desc":
                statement = statement.order_by(Task.due_date.desc())
            else:
                statement = statement.order_by(Task.due_date.asc())
        elif sort_by == "priority":
            if sort_order == "desc":
                statement = statement.order_by(Task.priority.desc())
            else:
                statement = statement.order_by(Task.priority.asc())
        elif sort_by == "created_at":
            if sort_order == "desc":
                statement = statement.order_by(Task.created_at.desc())
            else:
                statement = statement.order_by(Task.created_at.asc())

        tasks = db.exec(statement).all()

        # Apply tags filtering in memory since SQLModel has limitations with JSON
        if tags:
            filtered_tasks = []
            for task in tasks:
                if hasattr(task, 'tags') and task.tags:
                    if any(tag in task.tags for tag in tags):
                        filtered_tasks.append(task)
            tasks = filtered_tasks

        # Convert to TaskRead objects
        return [
            TaskRead.from_orm(task) if hasattr(TaskRead, 'from_orm') else TaskRead(
                id=task.id,
                title=task.title,
                description=task.description,
                completed=task.completed,
                priority=task.priority,
                tags=task.tags,
                due_date=task.due_date,
                recurring=task.recurring,
                recurrence_pattern=task.recurrence_pattern,
                parent_task_id=task.parent_task_id,
                user_id=task.user_id,
                created_at=task.created_at,
                updated_at=task.updated_at,
                reminder_sent=task.reminder_sent
            )
            for task in tasks
        ]

    def update_task(self, db: Session, task_id: int, task_update: TaskUpdate, user_id: int) -> Optional[TaskRead]:
        """Update a specific task for a user"""
        statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        db_task = db.exec(statement).first()

        if not db_task:
            return None

        # Update fields if they are provided
        update_data = task_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_task, field, value)

        db_task.updated_at = datetime.utcnow()

        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        return TaskRead.from_orm(db_task) if hasattr(TaskRead, 'from_orm') else TaskRead(
            id=db_task.id,
            title=db_task.title,
            description=db_task.description,
            completed=db_task.completed,
            priority=db_task.priority,
            tags=db_task.tags,
            due_date=db_task.due_date,
            recurring=db_task.recurring,
            recurrence_pattern=db_task.recurrence_pattern,
            parent_task_id=db_task.parent_task_id,
            user_id=db_task.user_id,
            created_at=db_task.created_at,
            updated_at=db_task.updated_at,
            reminder_sent=db_task.reminder_sent
        )

    def delete_task(self, db: Session, task_id: int, user_id: int) -> bool:
        """Delete a specific task for a user"""
        statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        db_task = db.exec(statement).first()

        if not db_task:
            return False

        db.delete(db_task)
        db.commit()
        return True

    def mark_complete(self, db: Session, task_id: int, user_id: int) -> Optional[TaskRead]:
        """Mark a task as complete"""
        statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        db_task = db.exec(statement).first()

        if not db_task:
            return None

        db_task.completed = True
        db_task.updated_at = datetime.utcnow()

        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        return TaskRead.from_orm(db_task) if hasattr(TaskRead, 'from_orm') else TaskRead(
            id=db_task.id,
            title=db_task.title,
            description=db_task.description,
            completed=db_task.completed,
            priority=db_task.priority,
            tags=db_task.tags,
            due_date=db_task.due_date,
            recurring=db_task.recurring,
            recurrence_pattern=db_task.recurrence_pattern,
            parent_task_id=db_task.parent_task_id,
            user_id=db_task.user_id,
            created_at=db_task.created_at,
            updated_at=db_task.updated_at,
            reminder_sent=db_task.reminder_sent
        )

    def get_due_soon_tasks(self, db: Session, user_id: int, days_ahead: int = 3) -> List[TaskRead]:
        """Get tasks that are due soon"""
        due_date_limit = datetime.utcnow() + timedelta(days=days_ahead)
        statement = select(Task).where(
            Task.user_id == user_id,
            Task.completed == False,
            Task.due_date.is_not(None),
            Task.due_date <= due_date_limit
        ).order_by(Task.due_date.asc())

        tasks = db.exec(statement).all()
        return [
            TaskRead.from_orm(task) if hasattr(TaskRead, 'from_orm') else TaskRead(
                id=task.id,
                title=task.title,
                description=task.description,
                completed=task.completed,
                priority=task.priority,
                tags=task.tags,
                due_date=task.due_date,
                recurring=task.recurring,
                recurrence_pattern=task.recurrence_pattern,
                parent_task_id=task.parent_task_id,
                user_id=task.user_id,
                created_at=task.created_at,
                updated_at=task.updated_at,
                reminder_sent=task.reminder_sent
            )
            for task in tasks
        ]

    def get_recurring_tasks(self, db: Session, user_id: int) -> List[TaskRead]:
        """Get all recurring tasks for a user"""
        statement = select(Task).where(
            Task.user_id == user_id,
            Task.recurring == True
        )

        tasks = db.exec(statement).all()
        return [
            TaskRead.from_orm(task) if hasattr(TaskRead, 'from_orm') else TaskRead(
                id=task.id,
                title=task.title,
                description=task.description,
                completed=task.completed,
                priority=task.priority,
                tags=task.tags,
                due_date=task.due_date,
                recurring=task.recurring,
                recurrence_pattern=task.recurrence_pattern,
                parent_task_id=task.parent_task_id,
                user_id=task.user_id,
                created_at=task.created_at,
                updated_at=task.updated_at,
                reminder_sent=task.reminder_sent
            )
            for task in tasks
        ]

    def create_recurring_instance(self, db: Session, original_task_id: int, user_id: int) -> Optional[TaskRead]:
        """Create a new instance of a recurring task"""
        original_task = self.get_task(db, original_task_id, user_id)
        if not original_task or not original_task.recurring:
            return None

        # Calculate next occurrence based on recurrence pattern
        next_due_date = self._calculate_next_occurrence(original_task.due_date, original_task.recurrence_pattern)

        # Create new task instance
        new_task_data = TaskCreate(
            title=original_task.title,
            description=original_task.description,
            completed=False,
            priority=original_task.priority,
            tags=original_task.tags,
            due_date=next_due_date,
            recurring=original_task.recurring,
            recurrence_pattern=original_task.recurrence_pattern,
            parent_task_id=original_task.id
        )

        return self.create_task(db, new_task_data, user_id)

    def _calculate_next_occurrence(self, current_date: datetime, pattern: str) -> datetime:
        """Calculate the next occurrence based on the recurrence pattern"""
        if pattern == "daily":
            return current_date + timedelta(days=1)
        elif pattern == "weekly":
            return current_date + timedelta(weeks=1)
        elif pattern == "monthly":
            # Simple month addition - in production, consider month-end edge cases
            if current_date.month == 12:
                return current_date.replace(year=current_date.year + 1, month=1)
            else:
                return current_date.replace(month=current_date.month + 1)
        elif pattern == "yearly":
            return current_date.replace(year=current_date.year + 1)
        else:
            # Default to daily if pattern is unknown
            return current_date + timedelta(days=1)