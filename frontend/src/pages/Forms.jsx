import React, { useState } from 'react';

function Forms() {
  const [formData, setFormData] = useState({ title: '', description: '' });
  const [isSubmitted, setIsSubmitted] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!formData.title.trim() || !formData.description.trim()) {
      alert("Please fill out both title and description.");
      return;
    }
    
    setIsSubmitted(true);
    setFormData({ title: '', description: '' });
    
    setTimeout(() => {
      setIsSubmitted(false);
    }, 3000);
  };

  return (
    <div className="page-container">
      <div className="page-header">
        <h1 className="page-title">Forms</h1>
        <p className="page-subtitle">Submit essential data.</p>
      </div>
      
      <div className="card" style={{ maxWidth: '600px' }}>
        <h3 style={{ color: 'var(--text-primary)', marginBottom: '1.5rem' }}>New Entry</h3>
        
        {isSubmitted && (
          <div style={{ padding: '1rem', marginBottom: '1rem', backgroundColor: '#d1fae5', color: '#065f46', borderRadius: '6px', border: '1px solid #34d399' }}>
            Form submitted successfully!
          </div>
        )}

        <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
          <div>
            <label style={{ display: 'block', marginBottom: '0.5rem', color: 'var(--text-secondary)' }}>Title</label>
            <input 
              type="text" 
              placeholder="Enter title..." 
              value={formData.title}
              onChange={(e) => setFormData({...formData, title: e.target.value})}
              style={{ 
                width: '100%', 
                padding: '0.75rem', 
                borderRadius: '6px', 
                border: '1px solid var(--border-color)',
                background: 'var(--bg-surface)',
                color: 'var(--text-primary)'
              }} 
            />
          </div>
          
          <div>
            <label style={{ display: 'block', marginBottom: '0.5rem', color: 'var(--text-secondary)' }}>Description</label>
            <textarea 
              placeholder="Additional details..." 
              rows={4}
              value={formData.description}
              onChange={(e) => setFormData({...formData, description: e.target.value})}
              style={{ 
                width: '100%', 
                padding: '0.75rem', 
                borderRadius: '6px', 
                border: '1px solid var(--border-color)',
                background: 'var(--bg-surface)',
                color: 'var(--text-primary)',
                resize: 'none'
              }} 
            />
          </div>
          
          <div style={{ marginTop: '1rem', display: 'flex', justifyContent: 'flex-end' }}>
            <button id="submit-form-btn" type="submit" className="btn btn-primary">
              Submit Form
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default Forms;
