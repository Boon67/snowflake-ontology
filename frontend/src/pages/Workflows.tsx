import { useState, useEffect } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { Plus, X, Edit, Trash2 } from 'lucide-react'
import { workflowsApi, WorkflowDefinition } from '../api/workflows'

// Entity types available in the system
const ENTITY_TYPES = [
  'CUSTOMER', 'ACCOUNT', 'PRODUCT', 'ORDER', 'INVOICE', 'PAYMENT',
  'EMPLOYEE', 'DEPARTMENT', 'PROJECT', 'TASK', 'DOCUMENT', 'CONTRACT',
  'VENDOR', 'PARTNER', 'LOCATION', 'ASSET', 'CAMPAIGN', 'LEAD'
]

// Common states and conditions
const STATES = [
  'ACTIVE', 'INACTIVE', 'PENDING', 'COMPLETED', 'CANCELLED',
  'AT_RISK', 'HEALTHY', 'ONBOARDING', 'CHURNED', 'SUSPENDED'
]

const ACTIONS = ['CREATE', 'UPDATE', 'DELETE', 'STATE_CHANGE']

// All available action types
const ACTION_TYPES = [
  { value: 'NOTIFICATION', label: 'Notification', description: 'Send notifications via multiple channels' },
  { value: 'EMAIL', label: 'Email', description: 'Send email notifications' },
  { value: 'SLACK', label: 'Slack', description: 'Send Slack messages' },
  { value: 'WEBHOOK', label: 'Webhook', description: 'Call external HTTP endpoints' },
  { value: 'SQL', label: 'SQL', description: 'Execute SQL queries' },
  { value: 'PYTHON', label: 'Python', description: 'Run Python code' },
  { value: 'STORED_PROCEDURE', label: 'Stored Procedure', description: 'Call Snowflake stored procedures' },
  { value: 'STREAM', label: 'Stream', description: 'Write to Snowflake streams' },
  { value: 'TASK', label: 'Task', description: 'Trigger Snowflake tasks' },
  { value: 'STATE_TRANSITION', label: 'State Transition', description: 'Change entity states' },
  { value: 'TAG_MANAGEMENT', label: 'Tag Management', description: 'Add/remove entity tags' },
  { value: 'RELATIONSHIP_CREATE', label: 'Create Relationship', description: 'Create entity relationships' },
  { value: 'ENTITY_CREATE', label: 'Create Entity', description: 'Create new entities' },
  { value: 'ENTITY_UPDATE', label: 'Update Entity', description: 'Update entity properties' },
  { value: 'ENTITY_DELETE', label: 'Delete Entity', description: 'Delete entities' },
  { value: 'VALIDATE', label: 'Validate', description: 'Validate entity data' },
  { value: 'PROPAGATE', label: 'Propagate', description: 'Propagate changes through relationships' },
  { value: 'AGGREGATE', label: 'Aggregate', description: 'Calculate aggregate values' },
  { value: 'SCHEDULE', label: 'Schedule', description: 'Schedule future actions' },
  { value: 'CONDITIONAL', label: 'Conditional', description: 'Execute actions based on conditions' },
  { value: 'COMPOSITE', label: 'Composite', description: 'Execute multiple actions in sequence' }
]

const OPERATORS = [
  { value: '=', label: 'equals' },
  { value: '!=', label: 'not equals' },
  { value: '>', label: 'greater than' },
  { value: '<', label: 'less than' },
  { value: 'LIKE', label: 'contains' },
  { value: 'IN', label: 'in list' }
]

interface TriggerCondition {
  field: string
  operator: string
  value: string
}

interface TriggerConditionBuilderProps {
  conditions: TriggerCondition[]
  onChange: (conditions: TriggerCondition[]) => void
}

// Trigger Condition Builder Component
function TriggerConditionBuilder({ conditions, onChange }: TriggerConditionBuilderProps) {
  const addCondition = () => {
    onChange([...conditions, { field: 'entity_type', operator: '=', value: '' }])
  }

  const removeCondition = (index: number) => {
    onChange(conditions.filter((_, i) => i !== index))
  }

  const updateCondition = (index: number, updates: Partial<TriggerCondition>) => {
    const newConditions = [...conditions]
    newConditions[index] = { ...newConditions[index], ...updates }
    onChange(newConditions)
  }

  const buildConditionString = () => {
    if (conditions.length === 0) return '*'
    return conditions
      .map(c => {
        if (c.operator === 'IN') {
          return `${c.field} IN (${c.value})`
        }
        return `${c.field}${c.operator}${c.value}`
      })
      .join(' AND ')
  }

  return (
    <div>
      <div style={{ marginBottom: '12px' }}>
        {conditions.map((condition, index) => (
          <div key={index} style={{ 
            display: 'grid', 
            gridTemplateColumns: '1fr 1fr 1fr auto', 
            gap: '8px', 
            marginBottom: '8px',
            alignItems: 'end'
          }}>
            <div>
              {index === 0 && <label className="form-label" style={{ fontSize: '12px' }}>Field</label>}
              <select
                className="form-select"
                value={condition.field}
                onChange={(e) => updateCondition(index, { field: e.target.value })}
                style={{ fontSize: '13px' }}
              >
                <option value="entity_type">Entity Type</option>
                <option value="current_state">Current State</option>
                <option value="previous_state">Previous State</option>
                <option value="action">Action</option>
                <option value="tags">Tags</option>
                <option value="properties">Properties</option>
              </select>
            </div>

            <div>
              {index === 0 && <label className="form-label" style={{ fontSize: '12px' }}>Operator</label>}
              <select
                className="form-select"
                value={condition.operator}
                onChange={(e) => updateCondition(index, { operator: e.target.value })}
                style={{ fontSize: '13px' }}
              >
                {OPERATORS.map(op => (
                  <option key={op.value} value={op.value}>{op.label}</option>
                ))}
              </select>
            </div>

            <div>
              {index === 0 && <label className="form-label" style={{ fontSize: '12px' }}>Value</label>}
              {condition.field === 'entity_type' ? (
                <select
                  className="form-select"
                  value={condition.value}
                  onChange={(e) => updateCondition(index, { value: e.target.value })}
                  style={{ fontSize: '13px' }}
                >
                  <option value="">Select type...</option>
                  {ENTITY_TYPES.map(type => (
                    <option key={type} value={type}>{type}</option>
                  ))}
                </select>
              ) : condition.field === 'current_state' || condition.field === 'previous_state' ? (
                <select
                  className="form-select"
                  value={condition.value}
                  onChange={(e) => updateCondition(index, { value: e.target.value })}
                  style={{ fontSize: '13px' }}
                >
                  <option value="">Select state...</option>
                  {STATES.map(state => (
                    <option key={state} value={state}>{state}</option>
                  ))}
                </select>
              ) : condition.field === 'action' ? (
                <select
                  className="form-select"
                  value={condition.value}
                  onChange={(e) => updateCondition(index, { value: e.target.value })}
                  style={{ fontSize: '13px' }}
                >
                  <option value="">Select action...</option>
                  {ACTIONS.map(action => (
                    <option key={action} value={action}>{action}</option>
                  ))}
                </select>
              ) : (
                <input
                  type="text"
                  className="form-input"
                  value={condition.value}
                  onChange={(e) => updateCondition(index, { value: e.target.value })}
                  placeholder="Enter value..."
                  style={{ fontSize: '13px' }}
                />
              )}
            </div>

            <div>
              {index === 0 && <div style={{ height: '20px' }} />}
              <button
                type="button"
                onClick={() => removeCondition(index)}
                style={{
                  border: 'none',
                  background: 'var(--danger)',
                  color: 'white',
                  padding: '6px 12px',
                  borderRadius: '4px',
                  cursor: 'pointer',
                  fontSize: '13px'
                }}
              >
                <X size={14} />
              </button>
            </div>
          </div>
        ))}
      </div>

      <div style={{ display: 'flex', gap: '8px', alignItems: 'center', marginBottom: '12px' }}>
        <button
          type="button"
          onClick={addCondition}
          className="btn btn-secondary"
          style={{ fontSize: '13px', padding: '6px 12px' }}
        >
          <Plus size={14} style={{ marginRight: '4px' }} />
          Add Condition
        </button>
        {conditions.length === 0 && (
          <span style={{ fontSize: '12px', color: 'var(--text-secondary)' }}>
            No conditions = trigger on all events (*)
          </span>
        )}
      </div>

      <div style={{ 
        padding: '12px', 
        backgroundColor: 'var(--background)', 
        borderRadius: '6px',
        border: '1px solid var(--border)'
      }}>
        <div style={{ fontSize: '11px', color: 'var(--text-secondary)', marginBottom: '4px' }}>
          Generated Trigger Condition:
        </div>
        <code style={{ fontSize: '13px', color: 'var(--primary)' }}>
          {buildConditionString()}
        </code>
      </div>
    </div>
  )
}

export default function Workflows() {
  const [showModal, setShowModal] = useState(false)
  const [editingWorkflow, setEditingWorkflow] = useState<WorkflowDefinition | null>(null)
  const [formData, setFormData] = useState<WorkflowDefinition>({
    name: '',
    description: '',
    trigger_condition: '',
    action_type: 'NOTIFICATION',
    action_config: {},
    enabled: true,
  })
  const [triggerConditions, setTriggerConditions] = useState<TriggerCondition[]>([])

  // Update trigger_condition when conditions change
  useEffect(() => {
    if (triggerConditions.length === 0) {
      setFormData(prev => ({ ...prev, trigger_condition: '*' }))
    } else {
      const conditionString = triggerConditions
        .map(c => {
          if (c.operator === 'IN') {
            return `${c.field} IN (${c.value})`
          }
          return `${c.field}${c.operator}${c.value}`
        })
        .join(' AND ')
      setFormData(prev => ({ ...prev, trigger_condition: conditionString }))
    }
  }, [triggerConditions])

  const queryClient = useQueryClient()

  const { data: workflows, isLoading, error } = useQuery({
    queryKey: ['workflows'],
    queryFn: () => workflowsApi.list(),
  })

  const { data: executions } = useQuery({
    queryKey: ['workflow-executions'],
    queryFn: () => workflowsApi.listExecutions(),
  })

  const createMutation = useMutation({
    mutationFn: workflowsApi.create,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['workflows'] })
      setShowModal(false)
      resetForm()
    },
  })

  const updateMutation = useMutation({
    mutationFn: ({ id, data }: { id: string; data: WorkflowDefinition }) => 
      workflowsApi.update(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['workflows'] })
      setShowModal(false)
      resetForm()
    },
  })

  const deleteMutation = useMutation({
    mutationFn: workflowsApi.delete,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['workflows'] })
    },
  })

  const resetForm = () => {
    setFormData({
      name: '',
      description: '',
      trigger_condition: '',
      action_type: 'NOTIFICATION',
      action_config: {},
      enabled: true,
    })
    setTriggerConditions([])
    setEditingWorkflow(null)
  }

  const handleEdit = (workflow: WorkflowDefinition) => {
    setEditingWorkflow(workflow)
    setFormData({
      name: workflow.name,
      description: workflow.description || '',
      trigger_condition: workflow.trigger_condition,
      action_type: workflow.action_type,
      action_config: workflow.action_config,
      enabled: workflow.enabled,
    })
    
    // Parse trigger condition back to conditions array
    // This is a simplified parser - you may need to enhance it
    const conditionStr = workflow.trigger_condition
    if (conditionStr && conditionStr !== '*') {
      const parts = conditionStr.split(' AND ')
      const parsedConditions: TriggerCondition[] = parts.map(part => {
        const trimmed = part.trim()
        // Try to match pattern: field operator value
        const match = trimmed.match(/^(\w+)(=|!=|>|<|LIKE|IN)(.+)$/)
        if (match) {
          return {
            field: match[1],
            operator: match[2],
            value: match[3].trim()
          }
        }
        return { field: 'entity_type', operator: '=', value: '' }
      })
      setTriggerConditions(parsedConditions)
    } else {
      setTriggerConditions([])
    }
    
    setShowModal(true)
  }

  const handleDelete = (workflowId: string) => {
    if (confirm('Are you sure you want to delete this workflow?')) {
      deleteMutation.mutate(workflowId)
    }
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (editingWorkflow?.workflow_id) {
      updateMutation.mutate({ id: editingWorkflow.workflow_id, data: formData })
    } else {
      createMutation.mutate(formData)
    }
  }

  if (isLoading) {
    return <div className="loading">Loading workflows...</div>
  }

  if (error) {
    return <div className="error">Error loading workflows: {(error as Error).message}</div>
  }

  return (
    <div>
      <div className="page-header">
        <h1>Workflows</h1>
        <p>Manage workflow definitions and executions</p>
      </div>

      <div className="card">
        <div className="card-header">
          <h2 className="card-title">Workflow Definitions</h2>
          <button
            className="btn btn-primary"
            onClick={() => {
              resetForm()
              setShowModal(true)
            }}
          >
            <Plus size={16} />
            Add Workflow
          </button>
        </div>

        {workflows && workflows.length > 0 ? (
          <table className="table">
            <thead>
              <tr>
                <th>Name</th>
                <th>Trigger Condition</th>
                <th>Action Type</th>
                <th>Status</th>
                <th>Created</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {workflows.map((workflow: WorkflowDefinition) => (
                <tr key={workflow.workflow_id}>
                  <td>{workflow.name}</td>
                  <td>
                    <span className="badge badge-info">{workflow.trigger_condition}</span>
                  </td>
                  <td>{workflow.action_type}</td>
                  <td>
                    <span className={`badge ${workflow.enabled ? 'badge-success' : 'badge-danger'}`}>
                      {workflow.enabled ? 'Enabled' : 'Disabled'}
                    </span>
                  </td>
                  <td>{workflow.created_at ? new Date(workflow.created_at).toLocaleDateString() : '-'}</td>
                  <td>
                    <button
                      className="btn btn-secondary"
                      style={{ marginRight: '8px' }}
                      onClick={() => handleEdit(workflow)}
                    >
                      <Edit size={14} />
                    </button>
                    <button
                      className="btn btn-danger"
                      onClick={() => workflow.workflow_id && handleDelete(workflow.workflow_id)}
                    >
                      <Trash2 size={14} />
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <div className="empty-state">
            <div className="empty-state-icon">
              <Plus size={48} />
            </div>
            <h3 className="empty-state-title">No workflows yet</h3>
            <p>Create your first workflow to automate actions</p>
          </div>
        )}
      </div>

      <div className="card">
        <div className="card-header">
          <h2 className="card-title">Recent Executions</h2>
        </div>

        {executions && executions.length > 0 ? (
          <table className="table">
            <thead>
              <tr>
                <th>Workflow ID</th>
                <th>Entity ID</th>
                <th>Status</th>
                <th>Started</th>
                <th>Completed</th>
              </tr>
            </thead>
            <tbody>
              {executions.slice(0, 10).map((execution: any) => (
                <tr key={execution.execution_id}>
                  <td>{execution.workflow_id.substring(0, 8)}...</td>
                  <td>{execution.entity_id.substring(0, 8)}...</td>
                  <td>
                    <span
                      className={`badge ${
                        execution.status === 'COMPLETED'
                          ? 'badge-success'
                          : execution.status === 'FAILED'
                          ? 'badge-danger'
                          : 'badge-warning'
                      }`}
                    >
                      {execution.status}
                    </span>
                  </td>
                  <td>{execution.started_at ? new Date(execution.started_at).toLocaleString() : '-'}</td>
                  <td>{execution.completed_at ? new Date(execution.completed_at).toLocaleString() : '-'}</td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <div className="empty-state">
            <p>No executions yet</p>
          </div>
        )}
      </div>

      {showModal && (
        <div className="modal-overlay" onClick={() => setShowModal(false)}>
          <div className="modal" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h2 className="modal-title">{editingWorkflow ? 'Edit Workflow' : 'Create Workflow'}</h2>
              <button onClick={() => setShowModal(false)} style={{ border: 'none', background: 'none', cursor: 'pointer' }}>
                <X size={24} />
              </button>
            </div>

            <form onSubmit={handleSubmit}>
              <div className="form-group">
                <label className="form-label">Name</label>
                <input
                  type="text"
                  className="form-input"
                  value={formData.name}
                  onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                  required
                />
              </div>

              <div className="form-group">
                <label className="form-label">Description</label>
                <textarea
                  className="form-textarea"
                  value={formData.description}
                  onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                />
              </div>

              <div className="form-group">
                <label className="form-label">Trigger Condition</label>
                <TriggerConditionBuilder
                  conditions={triggerConditions}
                  onChange={setTriggerConditions}
                />
              </div>

              <div className="form-group">
                <label className="form-label">Action Type</label>
                <select
                  className="form-select"
                  value={formData.action_type}
                  onChange={(e) => setFormData({ ...formData, action_type: e.target.value })}
                  required
                >
                  {ACTION_TYPES.map(type => (
                    <option key={type.value} value={type.value} title={type.description}>
                      {type.label}
                    </option>
                  ))}
                </select>
                <div style={{ fontSize: '12px', color: 'var(--text-secondary)', marginTop: '4px' }}>
                  {ACTION_TYPES.find(t => t.value === formData.action_type)?.description}
                </div>
              </div>

              <div className="form-group">
                <label className="form-label">Action Config (JSON)</label>
                <textarea
                  className="form-textarea"
                  value={JSON.stringify(formData.action_config, null, 2)}
                  onChange={(e) => {
                    try {
                      setFormData({ ...formData, action_config: JSON.parse(e.target.value) })
                    } catch {
                      // Invalid JSON, ignore
                    }
                  }}
                />
              </div>

              <div className="form-group">
                <label style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                  <input
                    type="checkbox"
                    checked={formData.enabled}
                    onChange={(e) => setFormData({ ...formData, enabled: e.target.checked })}
                  />
                  <span className="form-label" style={{ margin: 0 }}>Enabled</span>
                </label>
              </div>

              <div className="modal-footer">
                <button type="button" className="btn btn-secondary" onClick={() => setShowModal(false)}>
                  Cancel
                </button>
                <button type="submit" className="btn btn-primary">
                  {editingWorkflow ? 'Update' : 'Create'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  )
}
