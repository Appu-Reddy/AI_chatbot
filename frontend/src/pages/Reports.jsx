import React, { useState } from 'react';
import { Plus, X } from 'lucide-react';

function Reports() {
  const [isCreatingReport, setIsCreatingReport] = useState(false);
  const [reports, setReports] = useState([
    { id: 1, name: 'Q3 Financial Overview', date: 'Oct 12, 2023', status: 'Completed' },
    { id: 2, name: 'User Engagement Metrics', date: 'Oct 15, 2023', status: 'Completed' }
  ]);
  const [newReportName, setNewReportName] = useState('');

  const handleCreateReport = (e) => {
    e.preventDefault();
    if (!newReportName.trim()) return;
    
    const newReport = {
      id: reports.length + 1,
      name: newReportName,
      date: new Date().toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' }),
      status: 'Pending'
    };
    
    setReports([newReport, ...reports]);
    setNewReportName('');
    setIsCreatingReport(false);
  };

  return (
    <div className="page-container">
      <div className="page-header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div>
          <h1 className="page-title">Reports</h1>
          <p className="page-subtitle">View and generate your activity reports here.</p>
        </div>
        {!isCreatingReport && (
          <button id="create-report-btn" className="btn btn-primary" onClick={() => setIsCreatingReport(true)}>
            <Plus size={18} />
            Create Report
          </button>
        )}
      </div>

      {isCreatingReport && (
        <div className="card" style={{ borderLeft: '4px solid var(--accent-color)' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
            <h3 style={{ color: 'var(--text-primary)', margin: 0 }}>Configure New Report</h3>
            <button 
              onClick={() => setIsCreatingReport(false)}
              style={{ background: 'none', border: 'none', cursor: 'pointer', color: 'var(--text-secondary)' }}
            >
              <X size={20} />
            </button>
          </div>
          <form onSubmit={handleCreateReport} style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
            <input 
              type="text" 
              placeholder="Report Name..." 
              value={newReportName}
              onChange={(e) => setNewReportName(e.target.value)}
              style={{ 
                flex: 1,
                padding: '0.75rem', 
                borderRadius: '6px', 
                border: '1px solid var(--border-color)',
                background: 'var(--bg-surface)',
                color: 'var(--text-primary)'
              }} 
              autoFocus
            />
            <button type="submit" className="btn btn-primary">
              Generate
            </button>
          </form>
        </div>
      )}
      
      <div className="card">
        <h3 style={{ color: 'var(--text-primary)', marginBottom: '1rem' }}>Recent Reports</h3>
        <table style={{ width: '100%', textAlign: 'left', borderCollapse: 'collapse' }}>
          <thead>
            <tr style={{ borderBottom: '1px solid var(--border-color)', color: 'var(--text-secondary)' }}>
              <th style={{ padding: '0.75rem 0' }}>Report Name</th>
              <th style={{ padding: '0.75rem 0' }}>Date</th>
              <th style={{ padding: '0.75rem 0' }}>Status</th>
            </tr>
          </thead>
          <tbody>
            {reports.map((report) => (
              <tr key={report.id} style={{ borderBottom: '1px solid var(--border-color)' }}>
                <td style={{ padding: '1rem 0', color: 'var(--text-primary)' }}>{report.name}</td>
                <td style={{ padding: '1rem 0', color: 'var(--text-secondary)' }}>{report.date}</td>
                <td style={{ padding: '1rem 0' }}>
                  <span style={{ 
                    color: report.status === 'Completed' ? '#059669' : '#d97706',
                    backgroundColor: report.status === 'Completed' ? '#d1fae5' : '#fef3c7',
                    padding: '0.25rem 0.5rem',
                    borderRadius: '4px',
                    fontSize: '0.85rem',
                    fontWeight: 500
                  }}>
                    {report.status}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default Reports;
