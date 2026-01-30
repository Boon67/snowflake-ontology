import { useState, useMemo } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { Plus, Trash2, Edit, X, ChevronDown, ChevronRight, Search } from 'lucide-react'
import { entitiesApi, Entity } from '../api/entities'

export default function Entities() {
  const [showModal, setShowModal] = useState(false)
  const [editingEntity, setEditingEntity] = useState<Entity | null>(null)
  const [searchQuery, setSearchQuery] = useState('')
  const [expandedTypes, setExpandedTypes] = useState<Set<string>>(new Set())
  const [formData, setFormData] = useState<Entity>({
    entity_type: '',
    label: '',
    properties: {},
    tags: [],
  })

  const queryClient = useQueryClient()

  const { data: entities, isLoading, error } = useQuery({
    queryKey: ['entities'],
    queryFn: () => entitiesApi.list(),
  })

  // Group entities by type and filter by search query
  const groupedEntities = useMemo(() => {
    if (!entities) return {}
    
    const filtered = entities.filter((entity: Entity) => {
      const query = searchQuery.toLowerCase()
      return (
        entity.label.toLowerCase().includes(query) ||
        entity.entity_type.toLowerCase().includes(query) ||
        entity.tags.some(tag => tag.toLowerCase().includes(query))
      )
    })

    const grouped: Record<string, Entity[]> = {}
    filtered.forEach((entity: Entity) => {
      if (!grouped[entity.entity_type]) {
        grouped[entity.entity_type] = []
      }
      grouped[entity.entity_type].push(entity)
    })

    // Sort entities within each type by label
    Object.keys(grouped).forEach(type => {
      grouped[type].sort((a, b) => a.label.localeCompare(b.label))
    })

    return grouped
  }, [entities, searchQuery])

  // Auto-expand types when searching
  useMemo(() => {
    if (searchQuery) {
      setExpandedTypes(new Set(Object.keys(groupedEntities)))
    }
  }, [searchQuery, groupedEntities])

  const toggleType = (type: string) => {
    const newExpanded = new Set(expandedTypes)
    if (newExpanded.has(type)) {
      newExpanded.delete(type)
    } else {
      newExpanded.add(type)
    }
    setExpandedTypes(newExpanded)
  }

  const expandAll = () => {
    setExpandedTypes(new Set(Object.keys(groupedEntities)))
  }

  const collapseAll = () => {
    setExpandedTypes(new Set())
  }

  const createMutation = useMutation({
    mutationFn: entitiesApi.create,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['entities'] })
      queryClient.invalidateQueries({ queryKey: ['graph-stats'] })
      setShowModal(false)
      resetForm()
    },
  })

  const updateMutation = useMutation({
    mutationFn: ({ id, data }: { id: string; data: Entity }) => entitiesApi.update(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['entities'] })
      setShowModal(false)
      resetForm()
    },
  })

  const deleteMutation = useMutation({
    mutationFn: entitiesApi.delete,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['entities'] })
      queryClient.invalidateQueries({ queryKey: ['graph-stats'] })
    },
  })

  const resetForm = () => {
    setFormData({
      entity_type: '',
      label: '',
      properties: {},
      tags: [],
    })
    setEditingEntity(null)
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (editingEntity?.entity_id) {
      updateMutation.mutate({ id: editingEntity.entity_id, data: formData })
    } else {
      createMutation.mutate(formData)
    }
  }

  const handleEdit = (entity: Entity) => {
    setEditingEntity(entity)
    setFormData({
      entity_type: entity.entity_type,
      label: entity.label,
      properties: entity.properties,
      tags: entity.tags,
    })
    setShowModal(true)
  }

  const handleDelete = (entityId: string) => {
    if (confirm('Are you sure you want to delete this entity?')) {
      deleteMutation.mutate(entityId)
    }
  }

  if (isLoading) {
    return <div className="loading">Loading entities...</div>
  }

  if (error) {
    return <div className="error">Error loading entities: {(error as Error).message}</div>
  }

  return (
    <div>
      <div className="page-header">
        <h1>Entities</h1>
        <p>Manage entities in your ontology</p>
      </div>

      <div className="card">
        <div className="card-header">
          <h2 className="card-title">All Entities</h2>
          <button
            className="btn btn-primary"
            onClick={() => {
              resetForm()
              setShowModal(true)
            }}
          >
            <Plus size={16} />
            Add Entity
          </button>
        </div>

        {/* Search Bar */}
        <div style={{ padding: '16px', borderBottom: '1px solid var(--border)' }}>
          <div style={{ position: 'relative' }}>
            <Search 
              size={18} 
              style={{ 
                position: 'absolute', 
                left: '12px', 
                top: '50%', 
                transform: 'translateY(-50%)',
                color: 'var(--text-secondary)'
              }} 
            />
            <input
              type="text"
              className="form-input"
              placeholder="Search entities by name, type, or tags..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              style={{ paddingLeft: '40px' }}
            />
          </div>
          {Object.keys(groupedEntities).length > 0 && (
            <div style={{ marginTop: '12px', display: 'flex', gap: '8px' }}>
              <button 
                className="btn btn-secondary" 
                onClick={expandAll}
                style={{ fontSize: '12px', padding: '4px 12px' }}
              >
                Expand All
              </button>
              <button 
                className="btn btn-secondary" 
                onClick={collapseAll}
                style={{ fontSize: '12px', padding: '4px 12px' }}
              >
                Collapse All
              </button>
              <span style={{ 
                marginLeft: 'auto', 
                fontSize: '13px', 
                color: 'var(--text-secondary)',
                display: 'flex',
                alignItems: 'center'
              }}>
                {Object.keys(groupedEntities).length} types, {entities?.length || 0} entities
              </span>
            </div>
          )}
        </div>

        {/* Tree View */}
        {Object.keys(groupedEntities).length > 0 ? (
          <div style={{ padding: '16px' }}>
            {Object.keys(groupedEntities).sort().map((type) => {
              const isExpanded = expandedTypes.has(type)
              const typeEntities = groupedEntities[type]
              
              return (
                <div key={type} style={{ marginBottom: '8px' }}>
                  {/* Type Header */}
                  <div
                    onClick={() => toggleType(type)}
                    style={{
                      display: 'flex',
                      alignItems: 'center',
                      padding: '12px',
                      backgroundColor: 'var(--background)',
                      borderRadius: '6px',
                      cursor: 'pointer',
                      userSelect: 'none',
                      border: '1px solid var(--border)',
                      transition: 'all 0.2s',
                    }}
                    onMouseEnter={(e) => {
                      e.currentTarget.style.backgroundColor = 'var(--hover)'
                    }}
                    onMouseLeave={(e) => {
                      e.currentTarget.style.backgroundColor = 'var(--background)'
                    }}
                  >
                    {isExpanded ? (
                      <ChevronDown size={18} style={{ marginRight: '8px', color: 'var(--text-secondary)' }} />
                    ) : (
                      <ChevronRight size={18} style={{ marginRight: '8px', color: 'var(--text-secondary)' }} />
                    )}
                    <span className="badge badge-info" style={{ marginRight: '12px' }}>
                      {type}
                    </span>
                    <span style={{ fontWeight: 600, fontSize: '14px' }}>
                      {typeEntities.length} {typeEntities.length === 1 ? 'entity' : 'entities'}
                    </span>
                  </div>

                  {/* Entity List */}
                  {isExpanded && (
                    <div style={{ marginLeft: '32px', marginTop: '8px' }}>
                      {typeEntities.map((entity: Entity) => (
                        <div
                          key={entity.entity_id}
                          style={{
                            display: 'flex',
                            alignItems: 'center',
                            padding: '12px',
                            marginBottom: '4px',
                            backgroundColor: 'white',
                            borderRadius: '6px',
                            border: '1px solid var(--border)',
                            transition: 'all 0.2s',
                          }}
                          onMouseEnter={(e) => {
                            e.currentTarget.style.boxShadow = '0 2px 4px rgba(0,0,0,0.1)'
                            e.currentTarget.style.borderColor = 'var(--primary)'
                          }}
                          onMouseLeave={(e) => {
                            e.currentTarget.style.boxShadow = 'none'
                            e.currentTarget.style.borderColor = 'var(--border)'
                          }}
                        >
                          <div style={{ flex: 1 }}>
                            <div style={{ fontWeight: 600, marginBottom: '4px', fontSize: '14px' }}>
                              {entity.label}
                            </div>
                            <div style={{ display: 'flex', gap: '4px', flexWrap: 'wrap' }}>
                              {entity.tags.map((tag) => (
                                <span key={tag} className="badge badge-success" style={{ fontSize: '11px' }}>
                                  {tag}
                                </span>
                              ))}
                            </div>
                            {entity.created_at && (
                              <div style={{ fontSize: '11px', color: 'var(--text-secondary)', marginTop: '4px' }}>
                                Created: {new Date(entity.created_at).toLocaleDateString()}
                              </div>
                            )}
                          </div>
                          <div style={{ display: 'flex', gap: '8px' }}>
                            <button
                              className="btn btn-secondary"
                              onClick={() => handleEdit(entity)}
                              style={{ padding: '6px 12px' }}
                            >
                              <Edit size={14} />
                            </button>
                            <button
                              className="btn btn-danger"
                              onClick={() => entity.entity_id && handleDelete(entity.entity_id)}
                              style={{ padding: '6px 12px' }}
                            >
                              <Trash2 size={14} />
                            </button>
                          </div>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              )
            })}
          </div>
        ) : searchQuery ? (
          <div className="empty-state">
            <div className="empty-state-icon">
              <Search size={48} />
            </div>
            <h3 className="empty-state-title">No matching entities</h3>
            <p>Try a different search term</p>
          </div>
        ) : (
          <div className="empty-state">
            <div className="empty-state-icon">
              <Plus size={48} />
            </div>
            <h3 className="empty-state-title">No entities yet</h3>
            <p>Create your first entity to get started</p>
          </div>
        )}
      </div>

      {showModal && (
        <div className="modal-overlay" onClick={() => setShowModal(false)}>
          <div className="modal" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h2 className="modal-title">{editingEntity ? 'Edit Entity' : 'Create Entity'}</h2>
              <button onClick={() => setShowModal(false)} style={{ border: 'none', background: 'none', cursor: 'pointer' }}>
                <X size={24} />
              </button>
            </div>

            <form onSubmit={handleSubmit}>
              <div className="form-group">
                <label className="form-label">Label</label>
                <input
                  type="text"
                  className="form-input"
                  value={formData.label}
                  onChange={(e) => setFormData({ ...formData, label: e.target.value })}
                  required
                />
              </div>

              <div className="form-group">
                <label className="form-label">Type</label>
                <select
                  className="form-select"
                  value={formData.entity_type}
                  onChange={(e) => setFormData({ ...formData, entity_type: e.target.value })}
                  required
                >
                  <option value="">Select type</option>
                  <option value="CUSTOMER">Customer</option>
                  <option value="ACCOUNT">Account</option>
                  <option value="PRODUCT">Product</option>
                  <option value="ORDER">Order</option>
                  <option value="CUSTOM">Custom</option>
                </select>
              </div>

              <div className="form-group">
                <label className="form-label">Tags (comma-separated)</label>
                <input
                  type="text"
                  className="form-input"
                  value={formData.tags.join(', ')}
                  onChange={(e) =>
                    setFormData({
                      ...formData,
                      tags: e.target.value.split(',').map((t) => t.trim()).filter(Boolean),
                    })
                  }
                />
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
                  {editingEntity ? 'Update' : 'Create'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  )
}
