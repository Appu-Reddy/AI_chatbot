import React from 'react';

function Dashboard() {
  return (
    <div className="page-container">
      <div className="page-header">
        <h1 className="page-title">Dashboard</h1>
        <p className="page-subtitle">Welcome back. Here is what's happening today.</p>
      </div>
      
      <div className="card" id="dashboard-overview">
        <h2 style={{ marginBottom: '1rem', color: 'var(--text-primary)' }}>Activity Overview</h2>
        <p style={{ color: 'var(--text-secondary)' }}>
          This is a dummy dashboard. Look out for the Chatbot functionality to guide you!
        </p>
        <div style={{ display: 'flex', gap: '1rem', marginTop: '1.5rem' }}>
          <div style={{ flex: 1, padding: '1rem', background: 'rgba(0,0,0,0.03)', borderRadius: '8px', border: '1px solid var(--border-color)' }}>
            <h3 style={{ fontSize: '2rem', color: 'var(--accent-color)' }}>12</h3>
            <span style={{ color: 'var(--text-secondary)' }}>Reports Created</span>
          </div>
          <div style={{ flex: 1, padding: '1rem', background: 'rgba(0,0,0,0.03)', borderRadius: '8px', border: '1px solid var(--border-color)' }}>
            <h3 style={{ fontSize: '2rem', color: 'var(--accent-color)' }}>8</h3>
            <span style={{ color: 'var(--text-secondary)' }}>Forms Submitted</span>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
