import { useQuery } from '@tanstack/react-query'
import { Database, Network, Workflow, TrendingUp } from 'lucide-react'
import { graphApi } from '../api/graph'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'

export default function Dashboard() {
  const { data: stats, isLoading, error } = useQuery({
    queryKey: ['graph-stats'],
    queryFn: graphApi.stats,
  })

  if (isLoading) {
    return <div className="loading">Loading dashboard...</div>
  }

  if (error) {
    return <div className="error">Error loading dashboard: {(error as Error).message}</div>
  }

  const entityChartData = Object.entries(stats?.entities_by_type || {}).map(([type, count]) => ({
    name: type,
    count: count,
  }))

  const relationshipChartData = Object.entries(stats?.relationships_by_predicate || {}).map(([predicate, count]) => ({
    name: predicate,
    count: count,
  }))

  return (
    <div>
      <div className="page-header">
        <h1>Dashboard</h1>
        <p>Overview of your ontology and workflow engine</p>
      </div>

      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-header">
            <span className="stat-label">Total Entities</span>
            <Database size={24} color="#0066ff" />
          </div>
          <div className="stat-value">{stats?.total_entities || 0}</div>
        </div>

        <div className="stat-card">
          <div className="stat-header">
            <span className="stat-label">Total Relationships</span>
            <Network size={24} color="#10b981" />
          </div>
          <div className="stat-value">{stats?.total_relationships || 0}</div>
        </div>

        <div className="stat-card">
          <div className="stat-header">
            <span className="stat-label">Entity Types</span>
            <TrendingUp size={24} color="#f59e0b" />
          </div>
          <div className="stat-value">{Object.keys(stats?.entities_by_type || {}).length}</div>
        </div>

        <div className="stat-card">
          <div className="stat-header">
            <span className="stat-label">Relationship Types</span>
            <Workflow size={24} color="#ef4444" />
          </div>
          <div className="stat-value">{Object.keys(stats?.relationships_by_predicate || {}).length}</div>
        </div>
      </div>

      <div className="card">
        <div className="card-header">
          <h2 className="card-title">Entities by Type</h2>
        </div>
        {entityChartData.length > 0 ? (
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={entityChartData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="count" fill="#0066ff" />
            </BarChart>
          </ResponsiveContainer>
        ) : (
          <div className="empty-state">
            <p>No entities yet</p>
          </div>
        )}
      </div>

      <div className="card">
        <div className="card-header">
          <h2 className="card-title">Relationships by Type</h2>
        </div>
        {relationshipChartData.length > 0 ? (
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={relationshipChartData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="count" fill="#10b981" />
            </BarChart>
          </ResponsiveContainer>
        ) : (
          <div className="empty-state">
            <p>No relationships yet</p>
          </div>
        )}
      </div>
    </div>
  )
}
