import { useState, useMemo } from 'react'
import { useQuery } from '@tanstack/react-query'
import { Search } from 'lucide-react'
import ReactFlow, {
  Node,
  Edge,
  Controls,
  Background,
  useNodesState,
  useEdgesState,
  MarkerType,
  Position,
} from 'react-flow-renderer'
import { graphApi } from '../api/graph'
import { entitiesApi } from '../api/entities'

// Entity type colors
const entityColors: Record<string, string> = {
  CUSTOMER: '#3b82f6',
  ACCOUNT: '#10b981',
  PRODUCT: '#f59e0b',
  ORDER: '#8b5cf6',
  INVOICE: '#ef4444',
  EMPLOYEE: '#06b6d4',
  DEPARTMENT: '#84cc16',
  PROJECT: '#ec4899',
  DOCUMENT: '#6366f1',
  CAMPAIGN: '#f97316',
  LEAD: '#14b8a6',
  VENDOR: '#a855f7',
  LOCATION: '#22c55e',
  ASSET: '#eab308',
}

const getEntityColor = (entityType: string) => {
  return entityColors[entityType] || '#64748b'
}

// Calculate hierarchical layout based on depth
const calculateHierarchicalLayout = (nodes: any[], edges: any[]) => {
  const flowNodes: Node[] = []
  const depthMap = new Map<number, any[]>()
  
  // Group nodes by depth
  nodes.forEach((node) => {
    const depth = node.depth || 0
    if (!depthMap.has(depth)) {
      depthMap.set(depth, [])
    }
    depthMap.get(depth)!.push(node)
  })
  
  // Calculate positions
  const verticalSpacing = 150
  const horizontalSpacing = 250
  
  depthMap.forEach((nodesAtDepth, depth) => {
    const totalWidth = (nodesAtDepth.length - 1) * horizontalSpacing
    const startX = -totalWidth / 2
    
    nodesAtDepth.forEach((node, index) => {
      flowNodes.push({
        id: node.entity_id,
        type: 'default',
        data: {
          label: (
            <div style={{ textAlign: 'center' }}>
              <div style={{ fontWeight: 600, marginBottom: '4px' }}>{node.label}</div>
              <div style={{ fontSize: '11px', opacity: 0.7 }}>{node.entity_type}</div>
            </div>
          ),
        },
        position: {
          x: startX + index * horizontalSpacing,
          y: depth * verticalSpacing,
        },
        style: {
          background: getEntityColor(node.entity_type),
          color: 'white',
          border: '2px solid rgba(255, 255, 255, 0.3)',
          borderRadius: '8px',
          padding: '12px 16px',
          minWidth: '180px',
          fontSize: '13px',
        },
        sourcePosition: Position.Bottom,
        targetPosition: Position.Top,
      })
    })
  })
  
  // Create edges
  const flowEdges: Edge[] = edges.map((edge) => ({
    id: edge.relationship_id,
    source: edge.subject_id,
    target: edge.object_id,
    label: edge.predicate,
    type: 'smoothstep',
    animated: true,
    style: { stroke: '#94a3b8', strokeWidth: 2 },
    labelStyle: { fill: '#475569', fontWeight: 600, fontSize: '11px' },
    labelBgStyle: { fill: '#f8fafc', fillOpacity: 0.9 },
    markerEnd: {
      type: MarkerType.ArrowClosed,
      color: '#94a3b8',
    },
  }))
  
  return { nodes: flowNodes, edges: flowEdges }
}

export default function GraphView() {
  const [startEntityId, setStartEntityId] = useState('')
  const [maxDepth, setMaxDepth] = useState(2)
  const [direction, setDirection] = useState<'outgoing' | 'incoming' | 'both'>('both')
  const [nodes, setNodes, onNodesChange] = useNodesState([])
  const [edges, setEdges, onEdgesChange] = useEdgesState([])

  const { data: entities } = useQuery({
    queryKey: ['entities'],
    queryFn: () => entitiesApi.list(),
  })

  const { data: graphData, isLoading, refetch } = useQuery({
    queryKey: ['graph', startEntityId, maxDepth, direction],
    queryFn: () =>
      graphApi.query({
        start_entity_id: startEntityId,
        max_depth: maxDepth,
        direction: direction,
      }),
    enabled: !!startEntityId,
  })

  // Update flow nodes and edges when graph data changes
  useMemo(() => {
    if (graphData?.nodes && graphData?.edges) {
      const { nodes: flowNodes, edges: flowEdges } = calculateHierarchicalLayout(
        graphData.nodes,
        graphData.edges
      )
      setNodes(flowNodes)
      setEdges(flowEdges)
    }
  }, [graphData, setNodes, setEdges])

  const handleSearch = () => {
    if (startEntityId) {
      refetch()
    }
  }

  return (
    <div>
      <div className="page-header">
        <h1>Graph View</h1>
        <p>Visualize and explore entity relationships</p>
      </div>

      <div className="card">
        <div className="card-header">
          <h2 className="card-title">Graph Query</h2>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr auto', gap: '16px', marginBottom: '24px' }}>
          <div className="form-group" style={{ margin: 0 }}>
            <label className="form-label">Start Entity</label>
            <select
              className="form-select"
              value={startEntityId}
              onChange={(e) => setStartEntityId(e.target.value)}
            >
              <option value="">Select entity</option>
              {entities?.map((entity: any) => (
                <option key={entity.entity_id} value={entity.entity_id}>
                  {entity.label} ({entity.entity_type})
                </option>
              ))}
            </select>
          </div>

          <div className="form-group" style={{ margin: 0 }}>
            <label className="form-label">Max Depth</label>
            <input
              type="number"
              className="form-input"
              value={maxDepth}
              onChange={(e) => setMaxDepth(parseInt(e.target.value))}
              min="1"
              max="10"
            />
          </div>

          <div className="form-group" style={{ margin: 0 }}>
            <label className="form-label">Direction</label>
            <select
              className="form-select"
              value={direction}
              onChange={(e) => setDirection(e.target.value as any)}
            >
              <option value="both">Both</option>
              <option value="outgoing">Outgoing</option>
              <option value="incoming">Incoming</option>
            </select>
          </div>

          <div style={{ display: 'flex', alignItems: 'flex-end' }}>
            <button className="btn btn-primary" onClick={handleSearch} disabled={!startEntityId}>
              <Search size={16} />
              Query
            </button>
          </div>
        </div>

        {isLoading && <div className="loading">Loading graph...</div>}

        {graphData && nodes.length > 0 && (
          <div>
            <div style={{ marginBottom: '16px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <div>
                <h3 style={{ marginBottom: '8px' }}>DAG Visualization</h3>
                <p style={{ fontSize: '14px', color: 'var(--text-secondary)' }}>
                  Found <strong>{graphData.nodes?.length || 0}</strong> nodes and{' '}
                  <strong>{graphData.edges?.length || 0}</strong> edges
                </p>
              </div>
              <div style={{ display: 'flex', gap: '8px' }}>
                <span className="badge badge-info">Hierarchical Layout</span>
                <span className="badge badge-success">Depth-Based</span>
              </div>
            </div>

            {/* DAG Diagram */}
            <div style={{ 
              height: '600px', 
              border: '1px solid var(--border)', 
              borderRadius: '8px',
              backgroundColor: '#fafafa',
              marginBottom: '24px'
            }}>
              <ReactFlow
                nodes={nodes}
                edges={edges}
                onNodesChange={onNodesChange}
                onEdgesChange={onEdgesChange}
                fitView
                attributionPosition="bottom-left"
              >
                <Background color="#ddd" gap={16} />
                <Controls />
              </ReactFlow>
            </div>

            {/* Legend */}
            <div style={{ marginBottom: '24px', padding: '16px', backgroundColor: 'var(--background)', borderRadius: '8px' }}>
              <h4 style={{ marginBottom: '12px', fontSize: '14px', fontWeight: 600 }}>Entity Types</h4>
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: '12px' }}>
                {Object.entries(entityColors).map(([type, color]) => (
                  <div key={type} style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                    <div style={{ 
                      width: '16px', 
                      height: '16px', 
                      backgroundColor: color,
                      borderRadius: '4px',
                      border: '2px solid rgba(255, 255, 255, 0.3)'
                    }} />
                    <span style={{ fontSize: '12px' }}>{type}</span>
                  </div>
                ))}
              </div>
            </div>

            {/* Details Panel */}
            <details style={{ marginTop: '24px' }}>
              <summary style={{ 
                cursor: 'pointer', 
                fontWeight: 600, 
                padding: '12px',
                backgroundColor: 'var(--background)',
                borderRadius: '8px',
                marginBottom: '12px'
              }}>
                View Node & Edge Details
              </summary>
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '24px' }}>
                <div>
                  <h4 style={{ marginBottom: '12px' }}>Nodes</h4>
                  <div style={{ maxHeight: '400px', overflowY: 'auto' }}>
                    {graphData.nodes?.map((node: any) => (
                      <div
                        key={node.entity_id}
                        style={{
                          padding: '12px',
                          marginBottom: '8px',
                          backgroundColor: 'var(--background)',
                          borderRadius: '6px',
                          borderLeft: `4px solid ${getEntityColor(node.entity_type)}`,
                        }}
                      >
                        <div style={{ fontWeight: 600, marginBottom: '4px' }}>{node.label}</div>
                        <div style={{ fontSize: '12px', color: 'var(--text-secondary)' }}>
                          Type: {node.entity_type} | Depth: {node.depth}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                <div>
                  <h4 style={{ marginBottom: '12px' }}>Edges</h4>
                  <div style={{ maxHeight: '400px', overflowY: 'auto' }}>
                    {graphData.edges?.map((edge: any) => (
                      <div
                        key={edge.relationship_id}
                        style={{
                          padding: '12px',
                          marginBottom: '8px',
                          backgroundColor: 'var(--background)',
                          borderRadius: '6px',
                          borderLeft: `4px solid var(--success)`,
                        }}
                      >
                        <div style={{ fontWeight: 600, marginBottom: '4px' }}>
                          <span className="badge badge-info">{edge.predicate}</span>
                        </div>
                        <div style={{ fontSize: '12px', color: 'var(--text-secondary)' }}>
                          {edge.subject_id.substring(0, 8)}... → {edge.object_id.substring(0, 8)}...
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </details>
          </div>
        )}

        {!startEntityId && !graphData && (
          <div className="empty-state">
            <div className="empty-state-icon">
              <Search size={48} />
            </div>
            <h3 className="empty-state-title">Select an entity to start</h3>
            <p>Choose a starting entity and click Query to explore the graph</p>
          </div>
        )}
      </div>
    </div>
  )
}
