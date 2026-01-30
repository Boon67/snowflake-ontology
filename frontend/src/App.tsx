import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom'
import { Database, Workflow, BarChart3, Network, LogOut } from 'lucide-react'
import Dashboard from './pages/Dashboard'
import Entities from './pages/Entities'
import Relationships from './pages/Relationships'
import Workflows from './pages/Workflows'
import GraphView from './pages/GraphView'
import './App.css'

function App() {
  return (
    <Router>
      <div className="app">
        <nav className="sidebar">
          <div className="sidebar-header">
            <Database size={32} />
            <h1>Ontology Engine</h1>
          </div>
          <ul className="nav-links">
            <li>
              <Link to="/">
                <BarChart3 size={20} />
                <span>Dashboard</span>
              </Link>
            </li>
            <li>
              <Link to="/entities">
                <Database size={20} />
                <span>Entities</span>
              </Link>
            </li>
            <li>
              <Link to="/relationships">
                <Network size={20} />
                <span>Relationships</span>
              </Link>
            </li>
            <li>
              <Link to="/graph">
                <Network size={20} />
                <span>Graph View</span>
              </Link>
            </li>
            <li>
              <Link to="/workflows">
                <Workflow size={20} />
                <span>Workflows</span>
              </Link>
            </li>
          </ul>
          <div className="sidebar-footer">
            <a href="/sfc-endpoint/logout" className="logout-button">
              <LogOut size={20} />
              <span>Logout</span>
            </a>
          </div>
        </nav>
        <main className="main-content">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/entities" element={<Entities />} />
            <Route path="/relationships" element={<Relationships />} />
            <Route path="/graph" element={<GraphView />} />
            <Route path="/workflows" element={<Workflows />} />
          </Routes>
        </main>
      </div>
    </Router>
  )
}

export default App
