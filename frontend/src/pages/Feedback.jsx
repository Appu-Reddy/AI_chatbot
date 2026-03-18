import React, { useState } from 'react';
import { MessageSquare, Star } from 'lucide-react';

function Feedback() {
  const [rating, setRating] = useState(0);
  const [hoverRating, setHoverRating] = useState(0);
  const [message, setMessage] = useState('');
  const [isSubmitted, setIsSubmitted] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (rating === 0) {
      alert("Please select a rating before submitting.");
      return;
    }
    
    setIsSubmitted(true);
    setRating(0);
    setMessage('');
    
    setTimeout(() => {
      setIsSubmitted(false);
    }, 4000);
  };

  return (
    <div className="page-container">
      <div className="page-header">
        <h1 className="page-title">Feedback</h1>
        <p className="page-subtitle">We value your input. Let us know how we can improve.</p>
      </div>
      
      <div className="card" style={{ maxWidth: '600px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '1.5rem' }}>
          <MessageSquare color="var(--accent-color)" size={24} />
          <h3 style={{ color: 'var(--text-primary)', margin: 0 }}>Send us Feedback</h3>
        </div>
        
        {isSubmitted && (
          <div style={{ padding: '1rem', marginBottom: '1.5rem', backgroundColor: '#d1fae5', color: '#065f46', borderRadius: '6px', border: '1px solid #34d399' }}>
            Thank you for your feedback! We appreciate your help in making our product better.
          </div>
        )}

        <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
          <div>
            <label style={{ display: 'block', marginBottom: '0.5rem', color: 'var(--text-secondary)', fontWeight: 500 }}>
              How would you rate your experience?
            </label>
            <div style={{ display: 'flex', gap: '0.5rem' }} id="feedback-rating">
              {[1, 2, 3, 4, 5].map((star) => (
                <button
                  key={star}
                  type="button"
                  onClick={() => setRating(star)}
                  onMouseEnter={() => setHoverRating(star)}
                  onMouseLeave={() => setHoverRating(0)}
                  style={{
                    background: 'none',
                    border: 'none',
                    cursor: 'pointer',
                    padding: '0.25rem',
                    color: (hoverRating || rating) >= star ? '#fbbf24' : '#d1d5db',
                    transition: 'color 0.2s ease'
                  }}
                >
                  <Star fill={(hoverRating || rating) >= star ? '#fbbf24' : 'none'} size={32} />
                </button>
              ))}
            </div>
          </div>
          
          <div>
            <label style={{ display: 'block', marginBottom: '0.5rem', color: 'var(--text-secondary)', fontWeight: 500 }}>
              Tell us more about it
            </label>
            <textarea 
              placeholder="What went well? What could be improved?" 
              rows={5}
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              style={{ 
                width: '100%', 
                padding: '0.75rem', 
                borderRadius: '6px', 
                border: '1px solid var(--border-color)',
                background: 'var(--bg-surface)',
                color: 'var(--text-primary)',
                resize: 'vertical',
                minHeight: '100px'
              }} 
            />
          </div>
          
          <div style={{ display: 'flex', justifyContent: 'flex-end' }}>
            <button id="submit-feedback-btn" type="submit" className="btn btn-primary">
              Submit Feedback
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default Feedback;
