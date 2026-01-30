import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { Plus, Trash2, X } from 'lucide-react'
import { relationshipsApi, Relationship } from '../api/relationships'
import { entitiesApi } from '../api/entities'

export default function Relationships() {
  const [showModal, setShowModal] = useState(false)
  const [formData, setFormData] = useState<Relationship>({
    subject_id: '',
    predicate: '',
    object_id: '',
    properties: {},
  })

  const queryClient = useQueryClient()

  const { data: relationships, isLoading, error } = useQuery({
    queryKey: ['relationships'],
    queryFn: () => relationshipsApi.list(),
  })

  const { data: entities } = useQuery({
    queryKey: ['entities'],
    queryFn: () => entitiesApi.list(),
  })

  const createMutation = useMutation({
    mutationFn: relationshipsApi.create,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['relationships'] })
      queryClient.invalidateQueries({ queryKey: ['graph-stats'] })
      setShowModal(false)
      resetForm()
    },
  })

  const deleteMutation = useMutation({
    mutationFn: relationshipsApi.delete,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['relationships'] })
      queryClient.invalidateQueries({ queryKey: ['graph-stats'] })
    },
  })

  const resetForm = () => {
    setFormData({
      subject_id: '',
      predicate: '',
      object_id: '',
      properties: {},
    })
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    createMutation.mutate(formData)
  }

  const handleDelete = (relationshipId: string) => {
    if (confirm('Are you sure you want to delete this relationship?')) {
      deleteMutation.mutate(relationshipId)
    }
  }

  const getEntityLabel = (entityId: string) => {
    const entity = entities?.find((e: any) => e.entity_id === entityId)
    return entity?.label || entityId
  }

  if (isLoading) {
    return <div className="loading">Loading relationships...</div>
  }

  if (error) {
    return <div className="error">Error loading relationships: {(error as Error).message}</div>
  }

  return (
    <div>
      <div className="page-header">
        <h1>Relationships</h1>
        <p>Manage relationships between entities</p>
      </div>

      <div className="card">
        <div className="card-header">
          <h2 className="card-title">All Relationships</h2>
          <button
            className="btn btn-primary"
            onClick={() => {
              resetForm()
              setShowModal(true)
            }}
          >
            <Plus size={16} />
            Add Relationship
          </button>
        </div>

        {relationships && relationships.length > 0 ? (
          <table className="table">
            <thead>
              <tr>
                <th>Subject</th>
                <th>Predicate</th>
                <th>Object</th>
                <th>Created</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {relationships.map((rel: Relationship) => (
                <tr key={rel.relationship_id}>
                  <td>{getEntityLabel(rel.subject_id)}</td>
                  <td>
                    <span className="badge badge-info">{rel.predicate}</span>
                  </td>
                  <td>{getEntityLabel(rel.object_id)}</td>
                  <td>{rel.created_at ? new Date(rel.created_at).toLocaleDateString() : '-'}</td>
                  <td>
                    <button
                      className="btn btn-danger"
                      onClick={() => rel.relationship_id && handleDelete(rel.relationship_id)}
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
            <h3 className="empty-state-title">No relationships yet</h3>
            <p>Create your first relationship to connect entities</p>
          </div>
        )}
      </div>

      {showModal && (
        <div className="modal-overlay" onClick={() => setShowModal(false)}>
          <div className="modal" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h2 className="modal-title">Create Relationship</h2>
              <button onClick={() => setShowModal(false)} style={{ border: 'none', background: 'none', cursor: 'pointer' }}>
                <X size={24} />
              </button>
            </div>

            <form onSubmit={handleSubmit}>
              <div className="form-group">
                <label className="form-label">Subject Entity</label>
                <select
                  className="form-select"
                  value={formData.subject_id}
                  onChange={(e) => setFormData({ ...formData, subject_id: e.target.value })}
                  required
                >
                  <option value="">Select entity</option>
                  {entities?.map((entity: any) => (
                    <option key={entity.entity_id} value={entity.entity_id}>
                      {entity.label} ({entity.entity_type})
                    </option>
                  ))}
                </select>
              </div>

              <div className="form-group">
                <label className="form-label">Predicate</label>
                <select
                  className="form-select"
                  value={formData.predicate}
                  onChange={(e) => setFormData({ ...formData, predicate: e.target.value })}
                  required
                >
                  <option value="">Select predicate</option>
                  <option value="OWNS">OWNS</option>
                  <option value="PURCHASED">PURCHASED</option>
                  <option value="RELATED_TO">RELATED_TO</option>
                  <option value="DEPENDS_ON">DEPENDS_ON</option>
                  <option value="CONTAINS">CONTAINS</option>
                  <option value="CUSTOM">CUSTOM</option>
                </select>
              </div>

              <div className="form-group">
                <label className="form-label">Object Entity</label>
                <select
                  className="form-select"
                  value={formData.object_id}
                  onChange={(e) => setFormData({ ...formData, object_id: e.target.value })}
                  required
                >
                  <option value="">Select entity</option>
                  {entities?.map((entity: any) => (
                    <option key={entity.entity_id} value={entity.entity_id}>
                      {entity.label} ({entity.entity_type})
                    </option>
                  ))}
                </select>
              </div>

              <div className="form-group">
                <label className="form-label">Properties (JSON)</label>
                <textarea
                  className="form-textarea"
                  value={JSON.stringify(formData.properties, null, 2)}
                  onChange={(e) => {
                    try {
                      setFormData({ ...formData, properties: JSON.parse(e.target.value) })
                    } catch {
                      // Invalid JSON, ignore
                    }
                  }}
                />
              </div>

              <div className="modal-footer">
                <button type="button" className="btn btn-secondary" onClick={() => setShowModal(false)}>
                  Cancel
                </button>
                <button type="submit" className="btn btn-primary">
                  Create
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  )
}
