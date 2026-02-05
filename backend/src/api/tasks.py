from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from sqlmodel import select
from ..models.task import Task, TaskUpdate, TaskComplete
from ..services.task_service import (
    get_tasks_by_user_id,
    create_task_for_user_id,
    get_task_by_id_and_user_id,
    update_task_by_id_and_user_id,
    delete_task_by_id_and_user_id,
    update_task_completion_status
)
from ..api.deps import get_current_user
from ..database.session import engine
from sqlmodel import Session

router = APIRouter()


@router.get("/tasks", response_model=List[Task])
async def get_tasks(
    user_id: str,
    current_user: str = Depends(get_current_user),
    status_query: Optional[str] = Query(None, alias="status"),
    priority: Optional[str] = Query(None),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    """
    Get all tasks for the specified user
    """
    # Verify that the user_id in the URL matches the authenticated user
    if user_id != current_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access forbidden: user_id mismatch"
        )
    
    # Get tasks for the user
    tasks = await get_tasks_by_user_id(user_id)
    
    # Apply filters if provided
    if status_query:
        tasks = [task for task in tasks if task.status.value == status_query]
    
    if priority:
        tasks = [task for task in tasks if task.priority.value == priority]
    
    # Apply pagination
    start_index = offset
    end_index = min(start_index + limit, len(tasks))
    paginated_tasks = tasks[start_index:end_index]
    
    return paginated_tasks


@router.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED)
async def create_task(
    user_id: str,
    task: Task,
    current_user: str = Depends(get_current_user)
):
    """
    Create a new task for the specified user
    """
    # Verify that the user_id in the URL matches the authenticated user
    if user_id != current_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access forbidden: user_id mismatch"
        )
    
    # Ensure the task is associated with the correct user
    task.user_id = user_id
    
    # Create the task
    created_task = await create_task_for_user_id(user_id, task)
    return created_task


@router.get("/tasks/{task_id}", response_model=Task)
async def get_task(
    user_id: str,
    task_id: str,
    current_user: str = Depends(get_current_user)
):
    """
    Get a specific task by ID for the specified user
    """
    # Verify that the user_id in the URL matches the authenticated user
    if user_id != current_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access forbidden: user_id mismatch"
        )
    
    # Get the task
    task = await get_task_by_id_and_user_id(task_id, user_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    return task


@router.put("/tasks/{task_id}", response_model=Task)
async def update_task(
    user_id: str,
    task_id: str,
    task_update: TaskUpdate,
    current_user: str = Depends(get_current_user)
):
    """
    Update a specific task by ID for the specified user
    """
    # Verify that the user_id in the URL matches the authenticated user
    if user_id != current_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access forbidden: user_id mismatch"
        )
    
    # Update the task
    updated_task = await update_task_by_id_and_user_id(task_id, user_id, task_update)
    if not updated_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    return updated_task


@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    user_id: str,
    task_id: str,
    current_user: str = Depends(get_current_user)
):
    """
    Delete a specific task by ID for the specified user
    """
    # Verify that the user_id in the URL matches the authenticated user
    if user_id != current_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access forbidden: user_id mismatch"
        )
    
    # Delete the task
    deleted = await delete_task_by_id_and_user_id(task_id, user_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    return


@router.patch("/tasks/{task_id}/complete", response_model=Task)
async def update_task_complete(
    user_id: str,
    task_id: str,
    task_complete: TaskComplete,
    current_user: str = Depends(get_current_user)
):
    """
    Mark a specific task as complete/incomplete for the specified user
    """
    # Verify that the user_id in the URL matches the authenticated user
    if user_id != current_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access forbidden: user_id mismatch"
        )
    
    # Update task completion status
    updated_task = await update_task_completion_status(task_id, user_id, task_complete)
    if not updated_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    return updated_task