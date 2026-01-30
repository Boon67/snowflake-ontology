import apiClient from './client'

export interface WorkflowDefinition {
  workflow_id?: string
  name: string
  description?: string
  trigger_condition: string
  action_type: string
  action_config: Record<string, any>
  enabled: boolean
  created_at?: string
}

export interface WorkflowExecution {
  execution_id?: string
  workflow_id: string
  entity_id: string
  status: string
  input_data: Record<string, any>
  output_data?: Record<string, any>
  error_message?: string
  started_at?: string
  completed_at?: string
}

export const workflowsApi = {
  list: async (enabled?: boolean) => {
    const params = new URLSearchParams()
    if (enabled !== undefined) params.append('enabled', enabled.toString())
    
    const response = await apiClient.get(`/workflows?${params}`)
    return response.data
  },

  get: async (workflowId: string) => {
    const response = await apiClient.get(`/workflows/${workflowId}`)
    return response.data
  },

  create: async (workflow: WorkflowDefinition) => {
    const response = await apiClient.post('/workflows', workflow)
    return response.data
  },

  update: async (workflowId: string, workflow: WorkflowDefinition) => {
    const response = await apiClient.put(`/workflows/${workflowId}`, workflow)
    return response.data
  },

  delete: async (workflowId: string) => {
    await apiClient.delete(`/workflows/${workflowId}`)
  },

  execute: async (workflowId: string, entityId: string, inputData: Record<string, any> = {}) => {
    const response = await apiClient.post(`/workflows/${workflowId}/execute`, null, {
      params: { entity_id: entityId },
      data: inputData
    })
    return response.data
  },

  listExecutions: async (workflowId?: string, entityId?: string, limit = 100) => {
    const params = new URLSearchParams()
    if (workflowId) params.append('workflow_id', workflowId)
    if (entityId) params.append('entity_id', entityId)
    params.append('limit', limit.toString())
    
    const response = await apiClient.get(`/workflows/executions?${params}`)
    return response.data
  },
}
