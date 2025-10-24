"""
LUXORANOVA Task Schemas
"""

from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field, validator
from app.models.task import TaskStatus, TaskPriority


# ============================================================================
# Task CRUD Schemas
# ============================================================================

class TaskBase(BaseModel):
    """Base task schema with common fields."""
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=5000)
    priority: TaskPriority = TaskPriority.MEDIUM
    agent_id: Optional[str] = None
    workflow_id: Optional[str] = None
    input_data: Dict[str, Any] = Field(default_factory=dict)
    config: Dict[str, Any] = Field(default_factory=dict)
    tags: List[str] = Field(default_factory=list)


class TaskCreate(TaskBase):
    """Schema for creating a new task."""
    parent_task_id: Optional[str] = None
    dependencies: List[str] = Field(default_factory=list)
    scheduled_at: Optional[datetime] = None
    timeout_seconds: int = Field(300, ge=1, le=3600)
    retry_on_failure: bool = True
    max_retries: int = Field(3, ge=0, le=10)


class TaskUpdate(BaseModel):
    """Schema for updating task information."""
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=5000)
    priority: Optional[TaskPriority] = None
    status: Optional[TaskStatus] = None
    agent_id: Optional[str] = None
    input_data: Optional[Dict[str, Any]] = None
    config: Optional[Dict[str, Any]] = None
    tags: Optional[List[str]] = None
    scheduled_at: Optional[datetime] = None


class TaskResponse(TaskBase):
    """Schema for task response."""
    id: str
    user_id: str
    tenant_id: Optional[str] = None
    parent_task_id: Optional[str] = None
    status: TaskStatus
    progress: int
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    dependencies: List[str]
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    scheduled_at: Optional[datetime] = None
    retry_count: int
    execution_time_ms: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class TaskListResponse(BaseModel):
    """Schema for paginated task list response."""
    tasks: List[TaskResponse]
    total: int
    page: int
    page_size: int
    total_pages: int


# ============================================================================
# Task Execution Schemas
# ============================================================================

class TaskExecuteRequest(BaseModel):
    """Schema for task execution request."""
    input_data: Optional[Dict[str, Any]] = Field(default_factory=dict)
    override_config: Optional[Dict[str, Any]] = Field(default_factory=dict)
    async_execution: bool = True


class TaskExecuteResponse(BaseModel):
    """Schema for task execution response."""
    task_id: str
    execution_id: str
    status: TaskStatus
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    started_at: datetime
    completed_at: Optional[datetime] = None
    execution_time_ms: Optional[int] = None


class TaskProgressUpdate(BaseModel):
    """Schema for task progress update."""
    progress: int = Field(..., ge=0, le=100)
    message: Optional[str] = Field(None, max_length=500)
    metadata: Optional[Dict[str, Any]] = None


# ============================================================================
# Task Hierarchy Schemas
# ============================================================================

class TaskHierarchyResponse(BaseModel):
    """Schema for task hierarchy response."""
    task: TaskResponse
    children: List['TaskHierarchyResponse'] = []
    depth: int
    
    class Config:
        from_attributes = True


class TaskDependencyGraph(BaseModel):
    """Schema for task dependency graph."""
    task_id: str
    dependencies: List[str]
    dependents: List[str]
    can_execute: bool
    blocking_tasks: List[str]


# ============================================================================
# Task Scheduling Schemas
# ============================================================================

class TaskScheduleRequest(BaseModel):
    """Schema for scheduling a task."""
    scheduled_at: datetime
    recurrence: Optional[str] = Field(
        None,
        pattern="^(hourly|daily|weekly|monthly|custom)$"
    )
    recurrence_config: Optional[Dict[str, Any]] = None


class TaskScheduleResponse(BaseModel):
    """Schema for task schedule response."""
    task_id: str
    scheduled_at: datetime
    recurrence: Optional[str] = None
    next_run_at: Optional[datetime] = None
    is_active: bool


# ============================================================================
# Task Batch Operations
# ============================================================================

class TaskBatchCreate(BaseModel):
    """Schema for batch task creation."""
    tasks: List[TaskCreate] = Field(..., min_items=1, max_items=100)
    execute_immediately: bool = False


class TaskBatchCreateResponse(BaseModel):
    """Schema for batch task creation response."""
    batch_id: str
    tasks: List[TaskResponse]
    total: int
    successful: int
    failed: int


class TaskBatchExecuteRequest(BaseModel):
    """Schema for batch task execution."""
    task_ids: List[str] = Field(..., min_items=1, max_items=50)
    parallel: bool = True
    max_concurrent: int = Field(5, ge=1, le=20)


class TaskBatchExecuteResponse(BaseModel):
    """Schema for batch task execution response."""
    batch_id: str
    results: List[TaskExecuteResponse]
    total: int
    successful: int
    failed: int
    in_progress: int


# ============================================================================
# Task Retry Schemas
# ============================================================================

class TaskRetryRequest(BaseModel):
    """Schema for retrying a failed task."""
    reset_retry_count: bool = False
    override_config: Optional[Dict[str, Any]] = None


class TaskRetryResponse(BaseModel):
    """Schema for task retry response."""
    task_id: str
    retry_count: int
    status: TaskStatus
    scheduled_at: datetime


# ============================================================================
# Task Cancel Schema
# ============================================================================

class TaskCancelRequest(BaseModel):
    """Schema for canceling a task."""
    reason: Optional[str] = Field(None, max_length=500)
    cancel_children: bool = True


class TaskCancelResponse(BaseModel):
    """Schema for task cancel response."""
    task_id: str
    status: TaskStatus
    canceled_at: datetime
    children_canceled: int


# ============================================================================
# Task Metrics Schemas
# ============================================================================

class TaskMetricsResponse(BaseModel):
    """Schema for task metrics response."""
    total_tasks: int
    pending_tasks: int
    running_tasks: int
    completed_tasks: int
    failed_tasks: int
    canceled_tasks: int
    success_rate: float
    average_execution_time_ms: float
    total_execution_time_ms: int


class TaskPerformanceResponse(BaseModel):
    """Schema for task performance response."""
    task_id: str
    executions: int
    success_rate: float
    avg_execution_time_ms: float
    p50_execution_time_ms: float
    p95_execution_time_ms: float
    p99_execution_time_ms: float
    last_execution_at: Optional[datetime] = None


# ============================================================================
# Task Filter Schemas
# ============================================================================

class TaskFilterRequest(BaseModel):
    """Schema for filtering tasks."""
    status: Optional[List[TaskStatus]] = None
    priority: Optional[List[TaskPriority]] = None
    agent_id: Optional[str] = None
    workflow_id: Optional[str] = None
    tags: Optional[List[str]] = None
    created_after: Optional[datetime] = None
    created_before: Optional[datetime] = None
    scheduled_after: Optional[datetime] = None
    scheduled_before: Optional[datetime] = None


# ============================================================================
# Task Export Schema
# ============================================================================

class TaskExportRequest(BaseModel):
    """Schema for exporting tasks."""
    format: str = Field(..., pattern="^(json|csv|excel)$")
    filters: Optional[TaskFilterRequest] = None
    include_results: bool = True
    include_metadata: bool = True


class TaskExportResponse(BaseModel):
    """Schema for task export response."""
    export_id: str
    format: str
    file_url: str
    file_size_bytes: int
    task_count: int
    created_at: datetime
    expires_at: datetime


# ============================================================================
# Task Template Schemas
# ============================================================================

class TaskTemplateCreate(BaseModel):
    """Schema for creating a task template."""
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    template_data: TaskCreate
    is_public: bool = False


class TaskTemplateResponse(BaseModel):
    """Schema for task template response."""
    id: str
    name: str
    description: Optional[str] = None
    template_data: TaskCreate
    is_public: bool
    user_id: str
    usage_count: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class TaskFromTemplateRequest(BaseModel):
    """Schema for creating task from template."""
    template_id: str
    overrides: Optional[Dict[str, Any]] = Field(default_factory=dict)
    execute_immediately: bool = False


# Enable forward references
TaskHierarchyResponse.model_rebuild()
