import apiClient from './client'

export interface Relationship {
  relationship_id?: string
  subject_id: string
  predicate: string
  object_id: string
  properties: Record<string, any>
  created_at?: string
}

export const relationshipsApi = {
  list: async (entityId?: string, predicate?: string, limit = 100) => {
    const params = new URLSearchParams()
    if (entityId) params.append('entity_id', entityId)
    if (predicate) params.append('predicate', predicate)
    params.append('limit', limit.toString())
    
    const response = await apiClient.get(`/relationships?${params}`)
    return response.data
  },

  create: async (relationship: Relationship) => {
    const response = await apiClient.post('/relationships', relationship)
    return response.data
  },

  delete: async (relationshipId: string) => {
    await apiClient.delete(`/relationships/${relationshipId}`)
  },
}
