"""
LUXORANOVA Agent Schemas
"""

from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field, validator
from app.models.agent import AgentType, AgentStatus


# ============================================================================
# Agent CRUD Schemas
# ============================================================================

class AgentBase(BaseModel):
    """Base agent schema with common fields."""
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    type: AgentType
    model: str = Field(..., min_length=1, max_length=100)
    system_prompt: Optional[str] = Field(None, max_length=10000)
    temperature: float = Field(0.7, ge=0.0, le=2.0)
    max_tokens: int = Field(4096, ge=1, le=128000)
    capabilities: List[str] = Field(default_factory=list)
    tools: List[str] = Field(default_factory=list)
    is_active: bool = True


class AgentCreate(AgentBase):
    """Schema for creating a new agent."""
    parent_agent_id: Optional[str] = None
    config: Optional[Dict[str, Any]] = Field(default_factory=dict)
    
    @validator('capabilities')
    def validate_capabilities(cls, v):
        """Validate agent capabilities."""
        valid_capabilities = [
            'text_generation',
            'code_generation',
            'data_analysis',
            'web_search',
            'file_operations',
            'api_calls',
            'computer_use',
            'image_generation',
            'image_analysis',
        ]
        for cap in v:
            if cap not in valid_capabilities:
                raise ValueError(f'Invalid capability: {cap}')
        return v


class AgentUpdate(BaseModel):
    """Schema for updating agent information."""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    model: Optional[str] = Field(None, min_length=1, max_length=100)
    system_prompt: Optional[str] = Field(None, max_length=10000)
    temperature: Optional[float] = Field(None, ge=0.0, le=2.0)
    max_tokens: Optional[int] = Field(None, ge=1, le=128000)
    capabilities: Optional[List[str]] = None
    tools: Optional[List[str]] = None
    is_active: Optional[bool] = None
    config: Optional[Dict[str, Any]] = None


class AgentResponse(AgentBase):
    """Schema for agent response."""
    id: str
    user_id: str
    tenant_id: Optional[str] = None
    parent_agent_id: Optional[str] = None
    status: AgentStatus
    config: Dict[str, Any]
    metrics: Dict[str, Any]
    created_at: datetime
    updated_at: datetime
    last_executed_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class AgentListResponse(BaseModel):
    """Schema for paginated agent list response."""
    agents: List[AgentResponse]
    total: int
    page: int
    page_size: int
    total_pages: int


# ============================================================================
# Agent Execution Schemas
# ============================================================================

class AgentExecuteRequest(BaseModel):
    """Schema for agent execution request."""
    input: str = Field(..., min_length=1, max_length=50000)
    context: Optional[Dict[str, Any]] = Field(default_factory=dict)
    stream: bool = False
    max_iterations: int = Field(10, ge=1, le=100)
    timeout: int = Field(300, ge=1, le=3600)


class AgentExecuteResponse(BaseModel):
    """Schema for agent execution response."""
    agent_id: str
    execution_id: str
    output: str
    status: str
    steps: List[Dict[str, Any]]
    metrics: Dict[str, Any]
    started_at: datetime
    completed_at: datetime
    duration_ms: int


class AgentStreamChunk(BaseModel):
    """Schema for agent streaming response chunk."""
    execution_id: str
    chunk_type: str  # 'text', 'tool_call', 'status', 'error'
    content: str
    metadata: Optional[Dict[str, Any]] = None


# ============================================================================
# Hierarchical Agent Schemas
# ============================================================================

class SupervisorAgentCreate(AgentBase):
    """Schema for creating a supervisor agent."""
    type: AgentType = AgentType.SUPERVISOR
    worker_agent_ids: List[str] = Field(default_factory=list)
    orchestration_strategy: str = Field(
        "sequential",
        pattern="^(sequential|parallel|dynamic)$"
    )
    max_workers: int = Field(5, ge=1, le=10)


class WorkerAgentCreate(AgentBase):
    """Schema for creating a worker agent."""
    type: AgentType = AgentType.WORKER
    supervisor_agent_id: str
    specialization: str = Field(..., min_length=1, max_length=255)


class AgentHierarchyResponse(BaseModel):
    """Schema for agent hierarchy response."""
    agent: AgentResponse
    children: List['AgentHierarchyResponse'] = []
    depth: int
    
    class Config:
        from_attributes = True


# ============================================================================
# Agent Metrics Schemas
# ============================================================================

class AgentMetricsResponse(BaseModel):
    """Schema for agent metrics response."""
    agent_id: str
    total_executions: int
    successful_executions: int
    failed_executions: int
    success_rate: float
    average_duration_ms: float
    total_tokens_used: int
    total_cost: float
    last_7_days: Dict[str, int]
    last_30_days: Dict[str, int]


class AgentPerformanceResponse(BaseModel):
    """Schema for agent performance response."""
    agent_id: str
    period: str
    executions: int
    success_rate: float
    avg_duration_ms: float
    p50_duration_ms: float
    p95_duration_ms: float
    p99_duration_ms: float
    tokens_used: int
    cost: float


# ============================================================================
# Agent Configuration Schemas
# ============================================================================

class AgentConfigUpdate(BaseModel):
    """Schema for updating agent configuration."""
    memory_enabled: Optional[bool] = None
    memory_window_size: Optional[int] = Field(None, ge=1, le=100)
    retry_enabled: Optional[bool] = None
    retry_attempts: Optional[int] = Field(None, ge=1, le=10)
    retry_delay_seconds: Optional[int] = Field(None, ge=1, le=60)
    timeout_seconds: Optional[int] = Field(None, ge=1, le=3600)
    rate_limit_per_minute: Optional[int] = Field(None, ge=1, le=1000)
    custom_config: Optional[Dict[str, Any]] = None


# ============================================================================
# Agent Tool Schemas
# ============================================================================

class AgentToolAdd(BaseModel):
    """Schema for adding tool to agent."""
    tool_name: str = Field(..., min_length=1, max_length=100)
    tool_config: Optional[Dict[str, Any]] = Field(default_factory=dict)


class AgentToolRemove(BaseModel):
    """Schema for removing tool from agent."""
    tool_name: str = Field(..., min_length=1, max_length=100)


class AgentToolResponse(BaseModel):
    """Schema for agent tool response."""
    name: str
    description: str
    parameters: Dict[str, Any]
    config: Dict[str, Any]


# ============================================================================
# Agent Capability Schemas
# ============================================================================

class AgentCapabilityAdd(BaseModel):
    """Schema for adding capability to agent."""
    capability: str = Field(..., min_length=1, max_length=100)


class AgentCapabilityRemove(BaseModel):
    """Schema for removing capability from agent."""
    capability: str = Field(..., min_length=1, max_length=100)


# ============================================================================
# Agent Clone Schema
# ============================================================================

class AgentCloneRequest(BaseModel):
    """Schema for cloning an agent."""
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    include_config: bool = True
    include_tools: bool = True
    include_capabilities: bool = True


# ============================================================================
# Agent Batch Operations
# ============================================================================

class AgentBatchExecuteRequest(BaseModel):
    """Schema for batch agent execution."""
    agent_ids: List[str] = Field(..., min_items=1, max_items=10)
    input: str = Field(..., min_length=1, max_length=50000)
    context: Optional[Dict[str, Any]] = Field(default_factory=dict)
    parallel: bool = True


class AgentBatchExecuteResponse(BaseModel):
    """Schema for batch agent execution response."""
    batch_id: str
    results: List[AgentExecuteResponse]
    total: int
    successful: int
    failed: int
    duration_ms: int


# Enable forward references
AgentHierarchyResponse.model_rebuild()
