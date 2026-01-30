from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum


class EntityType(str, Enum):
    """Types of entities in the ontology"""
    CUSTOMER = "CUSTOMER"
    ACCOUNT = "ACCOUNT"
    PRODUCT = "PRODUCT"
    ORDER = "ORDER"
    CUSTOM = "CUSTOM"


class EntityStatus(str, Enum):
    """Status of entities"""
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    AT_RISK = "AT_RISK"
    ARCHIVED = "ARCHIVED"


class WorkflowStatus(str, Enum):
    """Status of workflow executions"""
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class ActionType(str, Enum):
    """Types of workflow actions"""
    NOTIFICATION = "NOTIFICATION"
    EMAIL = "EMAIL"
    SLACK = "SLACK"
    WEBHOOK = "WEBHOOK"
    SNOWFLAKE_TASK = "SNOWFLAKE_TASK"
    STORED_PROCEDURE = "STORED_PROCEDURE"
    SQL_QUERY = "SQL_QUERY"
    CREATE_ENTITY = "CREATE_ENTITY"
    UPDATE_ENTITY = "UPDATE_ENTITY"
    CREATE_RELATIONSHIP = "CREATE_RELATIONSHIP"
    DELETE_RELATIONSHIP = "DELETE_RELATIONSHIP"
    TAG_ENTITY = "TAG_ENTITY"
    STATE_TRANSITION = "STATE_TRANSITION"
    AGGREGATE = "AGGREGATE"
    PROPAGATE = "PROPAGATE"
    VALIDATE = "VALIDATE"
    ENRICH = "ENRICH"
    ARCHIVE = "ARCHIVE"
    ALERT = "ALERT"
    AUDIT_LOG = "AUDIT_LOG"
    COMPOSITE = "COMPOSITE"


class Severity(str, Enum):
    """Severity levels for notifications and alerts"""
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class ValidationRuleType(str, Enum):
    """Types of validation rules"""
    EMAIL = "email"
    REGEX = "regex"
    IN_LIST = "in_list"
    RANGE = "range"
    REQUIRED = "required"


class HTTPMethod(str, Enum):
    """HTTP methods for webhooks"""
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"


class Entity(BaseModel):
    """Represents an entity in the ontology"""
    entity_id: Optional[str] = None
    entity_type: str
    label: str
    properties: Dict[str, Any] = Field(default_factory=dict)
    tags: List[str] = Field(default_factory=list)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class EntityResponse(Entity):
    """Response model for entity with ID"""
    entity_id: str
    created_at: datetime
    updated_at: datetime


class Relationship(BaseModel):
    """Represents a relationship between entities (Subject -> Predicate -> Object)"""
    relationship_id: Optional[str] = None
    subject_id: str
    predicate: str
    object_id: str
    properties: Dict[str, Any] = Field(default_factory=dict)
    created_at: Optional[datetime] = None


class RelationshipResponse(Relationship):
    """Response model for relationship with ID"""
    relationship_id: str
    created_at: datetime


class EntityState(BaseModel):
    """Represents the current state of an entity"""
    entity_id: str
    current_state: str
    previous_state: Optional[str] = None
    state_data: Dict[str, Any] = Field(default_factory=dict)
    updated_at: Optional[datetime] = None


class WorkflowDefinition(BaseModel):
    """Defines a workflow that can be triggered"""
    workflow_id: Optional[str] = None
    name: str
    description: Optional[str] = None
    trigger_condition: str  # SQL condition or state change
    action_type: str  # SQL, PYTHON, NOTIFICATION
    action_config: Dict[str, Any] = Field(default_factory=dict)
    enabled: bool = True
    created_at: Optional[datetime] = None


class WorkflowExecution(BaseModel):
    """Represents an execution of a workflow"""
    execution_id: Optional[str] = None
    workflow_id: str
    entity_id: str
    status: WorkflowStatus = WorkflowStatus.PENDING
    input_data: Dict[str, Any] = Field(default_factory=dict)
    output_data: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None


class GraphQuery(BaseModel):
    """Query model for graph traversal"""
    start_entity_id: str
    relationship_types: Optional[List[str]] = None
    max_depth: int = Field(default=3, ge=1, le=10)
    direction: str = Field(default="both")  # outgoing, incoming, both


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    database: str
    timestamp: datetime


# ==================== ACTION CONFIGURATION MODELS ====================

class NotificationConfig(BaseModel):
    """Configuration for NOTIFICATION action"""
    message: str
    severity: Severity = Severity.MEDIUM
    recipients: List[str] = Field(default_factory=list)
    channels: List[str] = Field(default_factory=lambda: ["email"])
    include_fields: Optional[List[str]] = None


class EmailConfig(BaseModel):
    """Configuration for EMAIL action"""
    to: List[str]
    cc: Optional[List[str]] = None
    bcc: Optional[List[str]] = None
    subject: str
    template: Optional[str] = None
    body: Optional[str] = None
    attachments: Optional[List[str]] = None
    reply_to: Optional[str] = None


class SlackConfig(BaseModel):
    """Configuration for SLACK action"""
    channel: str
    message: str
    username: Optional[str] = "Ontology Bot"
    icon_emoji: Optional[str] = ":robot_face:"
    include_link: bool = False
    thread_ts: Optional[str] = None


class WebhookConfig(BaseModel):
    """Configuration for WEBHOOK action"""
    url: str
    method: HTTPMethod = HTTPMethod.POST
    headers: Dict[str, str] = Field(default_factory=dict)
    body: Optional[Dict[str, Any]] = None
    retry_count: int = Field(default=3, ge=0, le=10)
    timeout_seconds: int = Field(default=30, ge=1, le=300)
    verify_ssl: bool = True


class SnowflakeTaskConfig(BaseModel):
    """Configuration for SNOWFLAKE_TASK action"""
    task_name: str
    schedule: str  # CRON expression
    warehouse: str
    sql: str
    timeout_minutes: int = Field(default=30, ge=1, le=1440)
    suspend_after_failures: int = Field(default=3, ge=1, le=10)


class StoredProcedureConfig(BaseModel):
    """Configuration for STORED_PROCEDURE action"""
    procedure_name: str
    parameters: List[Any] = Field(default_factory=list)
    database: Optional[str] = None
    schema_name: Optional[str] = Field(default=None, alias="schema")
    timeout_seconds: int = Field(default=300, ge=1, le=3600)
    
    class Config:
        populate_by_name = True


class SQLQueryConfig(BaseModel):
    """Configuration for SQL_QUERY action"""
    query: str
    timeout_seconds: int = Field(default=60, ge=1, le=600)
    return_results: bool = False


class CreateEntityConfig(BaseModel):
    """Configuration for CREATE_ENTITY action"""
    entity_type: str
    label: str
    properties: Dict[str, Any] = Field(default_factory=dict)
    tags: List[str] = Field(default_factory=list)
    create_relationship: Optional[Dict[str, Any]] = None


class UpdateEntityConfig(BaseModel):
    """Configuration for UPDATE_ENTITY action"""
    target_query: Optional[str] = None  # SQL query to find entities to update
    target_entity_id: Optional[str] = None  # Specific entity to update
    updates: Dict[str, Any]  # Properties to update


class CreateRelationshipConfig(BaseModel):
    """Configuration for CREATE_RELATIONSHIP action"""
    predicate: str
    object_query: Optional[str] = None  # SQL query to find object entity
    object_id: Optional[str] = None  # Specific object entity
    properties: Dict[str, Any] = Field(default_factory=dict)


class DeleteRelationshipConfig(BaseModel):
    """Configuration for DELETE_RELATIONSHIP action"""
    relationship_query: Optional[str] = None  # SQL query to find relationships
    relationship_id: Optional[str] = None  # Specific relationship
    predicate: Optional[str] = None  # Delete by predicate


class TagEntityConfig(BaseModel):
    """Configuration for TAG_ENTITY action"""
    add_tags: List[str] = Field(default_factory=list)
    remove_tags: List[str] = Field(default_factory=list)
    notify: bool = False


class StateTransitionConfig(BaseModel):
    """Configuration for STATE_TRANSITION action"""
    new_state: str
    state_data: Dict[str, Any] = Field(default_factory=dict)
    trigger_workflows: List[str] = Field(default_factory=list)
    validate_transition: bool = True


class CalculationRule(BaseModel):
    """Single calculation rule for AGGREGATE action"""
    field: str
    formula: str
    description: Optional[str] = None


class AggregateConfig(BaseModel):
    """Configuration for AGGREGATE action"""
    calculations: List[CalculationRule]
    update_entity: bool = True
    store_history: bool = False


class PropagateConfig(BaseModel):
    """Configuration for PROPAGATE action"""
    relationship_path: str  # e.g., "PRODUCT -[INCLUDED_IN]-> QUOTE"
    update_fields: Dict[str, Any]
    max_depth: int = Field(default=2, ge=1, le=5)
    async_execution: bool = True


class ValidationRule(BaseModel):
    """Single validation rule"""
    field: str
    type: ValidationRuleType
    pattern: Optional[str] = None  # For regex
    values: Optional[List[Any]] = None  # For in_list
    min: Optional[float] = None  # For range
    max: Optional[float] = None  # For range
    required: bool = False
    error_message: str


class ValidateConfig(BaseModel):
    """Configuration for VALIDATE action"""
    rules: List[ValidationRule]
    on_failure: str = "TAG_INVALID"  # TAG_INVALID, REJECT, NOTIFY, ROLLBACK
    notify_on_failure: bool = False


class EnrichConfig(BaseModel):
    """Configuration for ENRICH action"""
    data_source: str  # API name or service identifier
    lookup_field: str  # Field to use for lookup
    enrich_fields: List[str]  # Fields to enrich
    cache_duration_days: int = Field(default=30, ge=0, le=365)
    update_existing: bool = False
    api_config: Optional[Dict[str, Any]] = None


class ArchiveConfig(BaseModel):
    """Configuration for ARCHIVE action"""
    archive_location: str  # Schema.Table for archived data
    delete_relationships: bool = False
    create_audit_log: bool = True
    notify: List[str] = Field(default_factory=list)


class AlertActionConfig(BaseModel):
    """Single action within an alert"""
    type: str
    target: Optional[str] = None
    config: Optional[Dict[str, Any]] = None


class AlertConfig(BaseModel):
    """Configuration for ALERT action"""
    alert_type: str
    severity: Severity
    title: str
    description: str
    assignees: List[str] = Field(default_factory=list)
    escalate_after_minutes: Optional[int] = None
    actions: List[AlertActionConfig] = Field(default_factory=list)


class AuditLogConfig(BaseModel):
    """Configuration for AUDIT_LOG action"""
    log_table: str
    fields: List[str]
    retention_days: int = Field(default=2555, ge=1, le=7300)  # 7 years max
    encrypt: bool = False
    include_metadata: bool = True


class CompositeStep(BaseModel):
    """Single step in a composite workflow"""
    step: int
    action: ActionType
    config: Dict[str, Any]
    depends_on: Optional[List[int]] = None  # Step numbers this depends on


class CompositeConfig(BaseModel):
    """Configuration for COMPOSITE action (multi-step workflow)"""
    steps: List[CompositeStep]
    on_failure: str = "ROLLBACK"  # ROLLBACK, CONTINUE, STOP
    notify_on_completion: bool = False
    parallel_execution: bool = False


# ==================== WORKFLOW MODELS ====================

class WorkflowDefinitionCreate(BaseModel):
    """Model for creating a workflow definition"""
    name: str
    description: Optional[str] = None
    trigger_condition: str
    action_type: ActionType
    action_config: Dict[str, Any]
    enabled: bool = True


class WorkflowDefinitionUpdate(BaseModel):
    """Model for updating a workflow definition"""
    name: Optional[str] = None
    description: Optional[str] = None
    trigger_condition: Optional[str] = None
    action_type: Optional[ActionType] = None
    action_config: Optional[Dict[str, Any]] = None
    enabled: Optional[bool] = None


class WorkflowDefinitionResponse(BaseModel):
    """Response model for workflow definition"""
    workflow_id: str
    name: str
    description: Optional[str]
    trigger_condition: str
    action_type: str
    action_config: Dict[str, Any]
    enabled: bool
    created_at: datetime


class WorkflowExecutionResponse(BaseModel):
    """Response model for workflow execution"""
    execution_id: str
    workflow_id: str
    entity_id: str
    status: WorkflowStatus
    input_data: Dict[str, Any]
    output_data: Optional[Dict[str, Any]]
    error_message: Optional[str]
    started_at: datetime
    completed_at: Optional[datetime]


class WorkflowTriggerRequest(BaseModel):
    """Request to manually trigger a workflow"""
    workflow_id: str
    entity_id: str
    input_data: Optional[Dict[str, Any]] = None


class WorkflowStats(BaseModel):
    """Statistics for workflow executions"""
    workflow_id: str
    workflow_name: str
    action_type: str
    total_executions: int
    completed: int
    failed: int
    pending: int
    avg_duration_seconds: Optional[float]
    last_execution: Optional[datetime]


# ==================== GRAPH MODELS ====================

class GraphNode(BaseModel):
    """Node in a graph visualization"""
    id: str
    label: str
    type: str
    properties: Dict[str, Any] = Field(default_factory=dict)
    tags: List[str] = Field(default_factory=list)


class GraphEdge(BaseModel):
    """Edge in a graph visualization"""
    id: str
    source: str
    target: str
    predicate: str
    properties: Dict[str, Any] = Field(default_factory=dict)


class GraphResponse(BaseModel):
    """Response for graph queries"""
    nodes: List[GraphNode]
    edges: List[GraphEdge]
    total_nodes: int
    total_edges: int


class GraphStats(BaseModel):
    """Statistics about the graph"""
    total_entities: int
    total_relationships: int
    entity_types: Dict[str, int]
    relationship_types: Dict[str, int]
    avg_connections_per_entity: float


# ==================== ENTITY MODELS ====================

class EntityCreate(BaseModel):
    """Model for creating an entity"""
    entity_type: str
    label: str
    properties: Dict[str, Any] = Field(default_factory=dict)
    tags: List[str] = Field(default_factory=list)


class EntityUpdate(BaseModel):
    """Model for updating an entity"""
    label: Optional[str] = None
    properties: Optional[Dict[str, Any]] = None
    tags: Optional[List[str]] = None


class EntityWithRelationships(EntityResponse):
    """Entity with its relationships"""
    outgoing_relationships: List[RelationshipResponse] = Field(default_factory=list)
    incoming_relationships: List[RelationshipResponse] = Field(default_factory=list)


# ==================== RELATIONSHIP MODELS ====================

class RelationshipCreate(BaseModel):
    """Model for creating a relationship"""
    subject_id: str
    predicate: str
    object_id: str
    properties: Dict[str, Any] = Field(default_factory=dict)


class RelationshipUpdate(BaseModel):
    """Model for updating a relationship"""
    predicate: Optional[str] = None
    properties: Optional[Dict[str, Any]] = None


# ==================== STATE MODELS ====================

class StateTransitionRequest(BaseModel):
    """Request to transition entity state"""
    entity_id: str
    new_state: str
    state_data: Dict[str, Any] = Field(default_factory=dict)
    trigger_workflows: bool = True


class StateHistory(BaseModel):
    """Historical state of an entity"""
    entity_id: str
    state: str
    state_data: Dict[str, Any]
    timestamp: datetime


# ==================== SEARCH AND FILTER MODELS ====================

class EntityFilter(BaseModel):
    """Filter criteria for entity search"""
    entity_type: Optional[str] = None
    tags: Optional[List[str]] = None
    properties: Optional[Dict[str, Any]] = None
    current_state: Optional[str] = None
    created_after: Optional[datetime] = None
    created_before: Optional[datetime] = None


class RelationshipFilter(BaseModel):
    """Filter criteria for relationship search"""
    subject_id: Optional[str] = None
    object_id: Optional[str] = None
    predicate: Optional[str] = None
    created_after: Optional[datetime] = None
    created_before: Optional[datetime] = None


class PaginationParams(BaseModel):
    """Pagination parameters"""
    offset: int = Field(default=0, ge=0)
    limit: int = Field(default=100, ge=1, le=1000)


class PaginatedResponse(BaseModel):
    """Generic paginated response"""
    items: List[Any]
    total: int
    offset: int
    limit: int
    has_more: bool
