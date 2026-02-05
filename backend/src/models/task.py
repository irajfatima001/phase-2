from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum
import uuid


class TaskStatus(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"


class TaskPriority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.pending
    priority: TaskPriority = TaskPriority.medium
    user_id: str


class Task(TaskBase):
    id: str
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    completed_at: Optional[str] = None


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None


class TaskComplete(BaseModel):
    complete: bool