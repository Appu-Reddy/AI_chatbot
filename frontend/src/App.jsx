import React from 'react';
import { BrowserRouter as Router, Routes, Route, NavLink } from 'react-router-dom';
import { LayoutDashboard, FileText, ClipboardList, HelpCircle, MessageSquare } from 'lucide-react';
import Dashboard from './pages/Dashboard';
import Reports from './pages/Reports';
import Forms from './pages/Forms';
import Feedback from './pages/Feedback';
import Help from './pages/Help';
import Chatbot from './components/Chatbot';

function App() {
  return (
    <Router>
      <div className="app-container">
        {/* Sidebar Navigation */}
        <aside className="sidebar">
          <div className="sidebar-title">
            <LayoutDashboard size={24} color="var(--accent-color)" />
            In-App Product
          </div>
          
          <nav>
            <NavLink id="dashboard-tab" to="/" className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}>
              <LayoutDashboard size={18} />
              Dashboard
            </NavLink>
            <NavLink id="reports-tab" to="/reports" className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}>
              <FileText size={18} />
              Reports
            </NavLink>
            <NavLink id="forms-tab" to="/forms" className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}>
              <ClipboardList size={18} />
              Forms
            </NavLink>
          </nav>
          
          <div style={{ marginTop: 'auto', paddingTop: '1rem', borderTop: '1px solid var(--border-color)' }}>
            <NavLink id="help-tab" to="/help" className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}>
              <HelpCircle size={18} />
              Help Center
            </NavLink>
            <NavLink id="feedback-tab" to="/feedback" className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}>
              <MessageSquare size={18} />
              Give Feedback
            </NavLink>
          </div>
        </aside>

        {/* Main Content Area */}
        <main className="main-content">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/reports" element={<Reports />} />
            <Route path="/forms" element={<Forms />} />
            <Route path="/feedback" element={<Feedback />} />
            <Route path="/help" element={<Help />} />
          </Routes>
          
          {/* Integrated Chatbot Component */}
          <Chatbot />
        </main>
      </div>
    </Router>
  );
}

export default App;
