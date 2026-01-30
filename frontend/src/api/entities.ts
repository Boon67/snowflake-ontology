import apiClient from './client'

export interface Entity {
  entity_id?: string
  entity_type: string
  label: string
  properties: Record<string, any>
  tags: string[]
  created_at?: string
  updated_at?: string
}

export const entitiesApi = {
  list: async (entityType?: string, limit = 100, offset = 0) => {
    const params = new URLSearchParams()
    if (entityType) params.append('entity_type', entityType)
    params.append('limit', limit.toString())
    params.append('offset', offset.toString())
    
    const response = await apiClient.get(`/entities?${params}`)
    return response.data
  },

  get: async (entityId: string) => {
    const response = await apiClient.get(`/entities/${entityId}`)
    return response.data
  },

  create: async (entity: Entity) => {
    const response = await apiClient.post('/entities', entity)
    return response.data
  },

  update: async (entityId: string, entity: Entity) => {
    const response = await apiClient.put(`/entities/${entityId}`, entity)
    return response.data
  },

  delete: async (entityId: string) => {
    await apiClient.delete(`/entities/${entityId}`)
  },
}
