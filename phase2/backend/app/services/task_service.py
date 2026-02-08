from typing import List, Optional
from sqlmodel import Session, select
from shared.models.task import Task, TaskCreate, TaskUpdate, TaskRead
from shared.models.user import User


def create_task(db: Session, task: TaskCreate, user_id: int) -> TaskRead:
    task_data = task.model_dump()
    # Convert tags list to JSON string if tags are provided as a list
    if 'tags' in task_data and task_data['tags'] is not None:
        import json
        if isinstance(task_data['tags'], list):
            task_data['tags'] = json.dumps(task_data['tags'])
    elif 'tags' not in task_data or task_data['tags'] is None:
        task_data['tags'] = '[]'  # Default to empty JSON array

    db_task = Task(**task_data, user_id=user_id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    # Return only the fields that are in TaskRead schema to avoid relationship issues
    return TaskRead.from_orm(db_task) if hasattr(TaskRead, 'from_orm') else TaskRead(
        id=db_task.id,
        title=db_task.title,
        description=db_task.description,
        completed=db_task.completed,
        user_id=db_task.user_id,
        created_at=db_task.created_at
    )


def get_task_by_id(db: Session, task_id: int, user_id: int) -> Optional[TaskRead]:
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    db_task = db.exec(statement).first()
    if db_task:
        # Return only the fields that are in TaskRead schema to avoid relationship issues
        return TaskRead.from_orm(db_task) if hasattr(TaskRead, 'from_orm') else TaskRead(
            id=db_task.id,
            title=db_task.title,
            description=db_task.description,
            completed=db_task.completed,
            user_id=db_task.user_id,
            created_at=db_task.created_at
        )
    return None


def get_tasks(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[TaskRead]:
    statement = select(Task).where(Task.user_id == user_id).offset(skip).limit(limit)
    db_tasks = db.exec(statement).all()
    # Convert to TaskRead models to avoid relationship issues
    return [
        TaskRead.from_orm(task) if hasattr(TaskRead, 'from_orm') else TaskRead(
            id=task.id,
            title=task.title,
            description=task.description,
            completed=task.completed,
            user_id=task.user_id,
            created_at=task.created_at
        ) for task in db_tasks
    ]


def update_task(db: Session, task_id: int, task_update: TaskUpdate, user_id: int) -> Optional[TaskRead]:
    # Get the original task record from the database
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    db_task = db.exec(statement).first()

    if db_task:
        update_data = task_update.model_dump(exclude_unset=True)

        # Convert tags list to JSON string if tags are provided as a list
        if 'tags' in update_data and update_data['tags'] is not None:
            import json
            if isinstance(update_data['tags'], list):
                update_data['tags'] = json.dumps(update_data['tags'])

        for field, value in update_data.items():
            setattr(db_task, field, value)

        db.add(db_task)
        db.commit()
        db.refresh(db_task)

        # Return only the fields that are in TaskRead schema to avoid relationship issues
        return TaskRead.from_orm(db_task) if hasattr(TaskRead, 'from_orm') else TaskRead(
            id=db_task.id,
            title=db_task.title,
            description=db_task.description,
            completed=db_task.completed,
            user_id=db_task.user_id,
            created_at=db_task.created_at
        )
    return None


def delete_task(db: Session, task_id: int, user_id: int) -> bool:
    # Get the actual Task object, not the TaskRead model
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    db_task = db.exec(statement).first()
    if db_task:
        db.delete(db_task)
        db.commit()
        return True
    return False


def complete_task(db: Session, task_id: int, user_id: int) -> Optional[TaskRead]:
    # Get the original task record from the database
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    db_task = db.exec(statement).first()

    if db_task:
        db_task.completed = True
        db.add(db_task)
        db.commit()
        db.refresh(db_task)

        # Return only the fields that are in TaskRead schema to avoid relationship issues
        return TaskRead.from_orm(db_task) if hasattr(TaskRead, 'from_orm') else TaskRead(
            id=db_task.id,
            title=db_task.title,
            description=db_task.description,
            completed=db_task.completed,
            user_id=db_task.user_id,
            created_at=db_task.created_at
        )
    return None


def get_tasks_by_status(db: Session, user_id: int, completed: bool) -> List[TaskRead]:
    statement = select(Task).where(Task.user_id == user_id, Task.completed == completed)
    db_tasks = db.exec(statement).all()
    # Convert to TaskRead models to avoid relationship issues
    return [
        TaskRead.from_orm(task) if hasattr(TaskRead, 'from_orm') else TaskRead(
            id=task.id,
            title=task.title,
            description=task.description,
            completed=task.completed,
            user_id=task.user_id,
            created_at=task.created_at
        ) for task in db_tasks
    ]