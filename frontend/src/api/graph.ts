import apiClient from './client'

export interface GraphQuery {
  start_entity_id: string
  relationship_types?: string[]
  max_depth?: number
  direction?: 'outgoing' | 'incoming' | 'both'
}

export const graphApi = {
  query: async (query: GraphQuery) => {
    const response = await apiClient.post('/graph/query', query)
    return response.data
  },

  stats: async () => {
    const response = await apiClient.get('/graph/stats')
    return response.data
  },
}
