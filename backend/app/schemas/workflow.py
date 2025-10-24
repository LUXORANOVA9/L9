"""
LUXORANOVA Workflow Schemas
"""

from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field, validator
from app.models.workflow import WorkflowStatus, WorkflowTriggerType


# ============================================================================
# Workflow CRUD Schemas
# ============================================================================

class WorkflowBase(BaseModel):
    """Base workflow schema with common fields."""
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=5000)
    definition: Dict[str, Any] = Field(..., description="Workflow DAG definition")
    trigger_type: WorkflowTriggerType = WorkflowTriggerType.MANUAL
    trigger_config: Dict[str, Any] = Field(default_factory=dict)
    config: Dict[str, Any] = Field(default_factory=dict)
    tags: List[str] = Field(default_factory=list)
    is_active: bool = True


class WorkflowCreate(WorkflowBase):
    """Schema for creating a new workflow."""
    n8n_workflow_id: Optional[str] = None
    
    @validator('definition')
    def validate_definition(cls, v):
        """Validate workflow definition structure."""
        if 'nodes' not in v:
            raise ValueError('Workflow definition must contain "nodes"')
        if 'edges' not in v:
            raise ValueError('Workflow definition must contain "edges"')
        if not isinstance(v['nodes'], list):
            raise ValueError('"nodes" must be a list')
        if not isinstance(v['edges'], list):
            raise ValueError('"edges" must be a list')
        return v


class WorkflowUpdate(BaseModel):
    """Schema for updating workflow information."""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=5000)
    definition: Optional[Dict[str, Any]] = None
    trigger_type: Optional[WorkflowTriggerType] = None
    trigger_config: Optional[Dict[str, Any]] = None
    config: Optional[Dict[str, Any]] = None
    tags: Optional[List[str]] = None
    is_active: Optional[bool] = None


class WorkflowResponse(WorkflowBase):
    """Schema for workflow response."""
    id: str
    user_id: str
    tenant_id: Optional[str] = None
    status: WorkflowStatus
    n8n_workflow_id: Optional[str] = None
    version: int
    execution_count: int
    last_executed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class WorkflowListResponse(BaseModel):
    """Schema for paginated workflow list response."""
    workflows: List[WorkflowResponse]
    total: int
    page: int
    page_size: int
    total_pages: int


# ============================================================================
# Workflow Execution Schemas
# ============================================================================

class WorkflowExecuteRequest(BaseModel):
    """Schema for workflow execution request."""
    input_data: Dict[str, Any] = Field(default_factory=dict)
    override_config: Optional[Dict[str, Any]] = Field(default_factory=dict)
    async_execution: bool = True
    wait_for_completion: bool = False


class WorkflowExecuteResponse(BaseModel):
    """Schema for workflow execution response."""
    workflow_id: str
    execution_id: str
    status: str
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    started_at: datetime
    completed_at: Optional[datetime] = None
    execution_time_ms: Optional[int] = None
    nodes_executed: int
    nodes_failed: int


class WorkflowExecutionStatus(BaseModel):
    """Schema for workflow execution status."""
    execution_id: str
    workflow_id: str
    status: str
    progress: int
    current_node: Optional[str] = None
    nodes_completed: int
    nodes_total: int
    started_at: datetime
    updated_at: datetime


# ============================================================================
# Workflow Node Schemas
# ============================================================================

class WorkflowNodeBase(BaseModel):
    """Base workflow node schema."""
    id: str = Field(..., min_length=1, max_length=100)
    type: str = Field(..., min_length=1, max_length=100)
    name: str = Field(..., min_length=1, max_length=255)
    config: Dict[str, Any] = Field(default_factory=dict)
    position: Dict[str, float] = Field(default_factory=dict)


class WorkflowEdgeBase(BaseModel):
    """Base workflow edge schema."""
    id: str = Field(..., min_length=1, max_length=100)
    source: str = Field(..., min_length=1, max_length=100)
    target: str = Field(..., min_length=1, max_length=100)
    condition: Optional[str] = None


class WorkflowDefinition(BaseModel):
    """Schema for complete workflow definition."""
    nodes: List[WorkflowNodeBase]
    edges: List[WorkflowEdgeBase]
    variables: Dict[str, Any] = Field(default_factory=dict)
    
    @validator('nodes')
    def validate_nodes(cls, v):
        """Validate nodes have unique IDs."""
        node_ids = [node.id for node in v]
        if len(node_ids) != len(set(node_ids)):
            raise ValueError('Node IDs must be unique')
        return v
    
    @validator('edges')
    def validate_edges(cls, v, values):
        """Validate edges reference existing nodes."""
        if 'nodes' in values:
            node_ids = {node.id for node in values['nodes']}
            for edge in v:
                if edge.source not in node_ids:
                    raise ValueError(f'Edge source "{edge.source}" not found in nodes')
                if edge.target not in node_ids:
                    raise ValueError(f'Edge target "{edge.target}" not found in nodes')
        return v


# ============================================================================
# Workflow Trigger Schemas
# ============================================================================

class WorkflowTriggerUpdate(BaseModel):
    """Schema for updating workflow trigger."""
    trigger_type: WorkflowTriggerType
    trigger_config: Dict[str, Any] = Field(default_factory=dict)


class WorkflowScheduleTrigger(BaseModel):
    """Schema for schedule trigger configuration."""
    cron_expression: str = Field(..., min_length=1, max_length=100)
    timezone: str = Field("UTC", min_length=1, max_length=50)
    enabled: bool = True


class WorkflowWebhookTrigger(BaseModel):
    """Schema for webhook trigger configuration."""
    webhook_url: str
    secret: Optional[str] = None
    enabled: bool = True


class WorkflowEventTrigger(BaseModel):
    """Schema for event trigger configuration."""
    event_type: str = Field(..., min_length=1, max_length=100)
    filters: Dict[str, Any] = Field(default_factory=dict)
    enabled: bool = True


# ============================================================================
# Workflow Version Schemas
# ============================================================================

class WorkflowVersionResponse(BaseModel):
    """Schema for workflow version response."""
    id: str
    workflow_id: str
    version: int
    definition: Dict[str, Any]
    created_by: str
    created_at: datetime
    is_current: bool
    
    class Config:
        from_attributes = True


class WorkflowVersionListResponse(BaseModel):
    """Schema for workflow version list response."""
    versions: List[WorkflowVersionResponse]
    total: int


class WorkflowVersionRestore(BaseModel):
    """Schema for restoring workflow version."""
    version: int


# ============================================================================
# Workflow Template Schemas
# ============================================================================

class WorkflowTemplateCreate(BaseModel):
    """Schema for creating workflow template."""
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    category: str = Field(..., min_length=1, max_length=100)
    template_data: WorkflowCreate
    is_public: bool = False
    tags: List[str] = Field(default_factory=list)


class WorkflowTemplateResponse(BaseModel):
    """Schema for workflow template response."""
    id: str
    name: str
    description: Optional[str] = None
    category: str
    template_data: WorkflowCreate
    is_public: bool
    user_id: str
    usage_count: int
    rating: float
    tags: List[str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class WorkflowFromTemplateRequest(BaseModel):
    """Schema for creating workflow from template."""
    template_id: str
    name: str = Field(..., min_length=1, max_length=255)
    overrides: Optional[Dict[str, Any]] = Field(default_factory=dict)


# ============================================================================
# Workflow Metrics Schemas
# ============================================================================

class WorkflowMetricsResponse(BaseModel):
    """Schema for workflow metrics response."""
    workflow_id: str
    total_executions: int
    successful_executions: int
    failed_executions: int
    success_rate: float
    average_execution_time_ms: float
    total_execution_time_ms: int
    last_7_days: Dict[str, int]
    last_30_days: Dict[str, int]


class WorkflowPerformanceResponse(BaseModel):
    """Schema for workflow performance response."""
    workflow_id: str
    period: str
    executions: int
    success_rate: float
    avg_execution_time_ms: float
    p50_execution_time_ms: float
    p95_execution_time_ms: float
    p99_execution_time_ms: float
    nodes_avg: float
    last_execution_at: Optional[datetime] = None


# ============================================================================
# Workflow N8N Integration Schemas
# ============================================================================

class WorkflowN8NSync(BaseModel):
    """Schema for syncing workflow with N8N."""
    n8n_workflow_id: str
    sync_direction: str = Field(..., pattern="^(to_n8n|from_n8n|bidirectional)$")


class WorkflowN8NImport(BaseModel):
    """Schema for importing workflow from N8N."""
    n8n_workflow_id: str
    name: Optional[str] = None
    import_triggers: bool = True


class WorkflowN8NExport(BaseModel):
    """Schema for exporting workflow to N8N."""
    workflow_id: str
    export_name: Optional[str] = None
    activate: bool = False


# ============================================================================
# Workflow Validation Schemas
# ============================================================================

class WorkflowValidateRequest(BaseModel):
    """Schema for validating workflow definition."""
    definition: Dict[str, Any]


class WorkflowValidateResponse(BaseModel):
    """Schema for workflow validation response."""
    is_valid: bool
    errors: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)
    suggestions: List[str] = Field(default_factory=list)


# ============================================================================
# Workflow Clone Schema
# ============================================================================

class WorkflowCloneRequest(BaseModel):
    """Schema for cloning a workflow."""
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    include_triggers: bool = True
    include_config: bool = True


# ============================================================================
# Workflow Export/Import Schemas
# ============================================================================

class WorkflowExportRequest(BaseModel):
    """Schema for exporting workflow."""
    format: str = Field(..., pattern="^(json|yaml|n8n)$")
    include_executions: bool = False
    include_versions: bool = False


class WorkflowExportResponse(BaseModel):
    """Schema for workflow export response."""
    export_id: str
    format: str
    file_url: str
    file_size_bytes: int
    created_at: datetime
    expires_at: datetime


class WorkflowImportRequest(BaseModel):
    """Schema for importing workflow."""
    format: str = Field(..., pattern="^(json|yaml|n8n)$")
    data: Dict[str, Any]
    name: Optional[str] = None
    activate: bool = False


# ============================================================================
# Workflow Batch Operations
# ============================================================================

class WorkflowBatchExecuteRequest(BaseModel):
    """Schema for batch workflow execution."""
    workflow_ids: List[str] = Field(..., min_items=1, max_items=10)
    input_data: Dict[str, Any] = Field(default_factory=dict)
    parallel: bool = True


class WorkflowBatchExecuteResponse(BaseModel):
    """Schema for batch workflow execution response."""
    batch_id: str
    results: List[WorkflowExecuteResponse]
    total: int
    successful: int
    failed: int
    in_progress: int
