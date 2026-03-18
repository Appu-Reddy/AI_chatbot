import React, { useState } from 'react';
import { HelpCircle, ChevronDown, ChevronUp, Mail, ExternalLink } from 'lucide-react';

const FAQItem = ({ question, answer }) => {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <div style={{ 
      borderBottom: '1px solid var(--border-color)',
      padding: '1rem 0'
    }}>
      <button 
        onClick={() => setIsOpen(!isOpen)}
        style={{ 
          width: '100%', 
          display: 'flex', 
          justifyContent: 'space-between', 
          alignItems: 'center',
          background: 'none',
          border: 'none',
          color: 'var(--text-primary)',
          fontSize: '1rem',
          fontWeight: 500,
          cursor: 'pointer',
          textAlign: 'left'
        }}
      >
        {question}
        {isOpen ? <ChevronUp size={20} color="var(--text-secondary)" /> : <ChevronDown size={20} color="var(--text-secondary)" />}
      </button>
      
      {isOpen && (
        <div style={{ 
          marginTop: '1rem', 
          color: 'var(--text-secondary)',
          lineHeight: '1.6',
          paddingRight: '2rem'
        }}>
          {answer}
        </div>
      )}
    </div>
  );
};

function Help() {
  const faqs = [
    {
      question: "How do I create a new report?",
      answer: "Navigate to the Reports tab using the sidebar on the left. Once there, click the 'Create Report' button. A form will appear where you can enter the title of your report and generate it instantly."
    },
    {
      question: "Can I edit a form after submitting it?",
      answer: "Currently, submitted forms are final and cannot be edited. If you made a mistake, please submit a new form with the correct information."
    },
    {
      question: "How do I use the chatbot?",
      answer: "Click the purple chat icon in the bottom right corner of any page. You can ask questions like 'how to create a report' or 'how to submit a form' and the bot will provide step-by-step visual guidance."
    },
    {
      question: "Where can I see my recent activity?",
      answer: "Your recent activity overview is visible on the main Dashboard. It shows high-level metrics like total reports created and total forms submitted."
    }
  ];

  return (
    <div className="page-container">
      <div className="page-header">
        <h1 className="page-title">Help Center</h1>
        <p className="page-subtitle">Find answers to common questions or get in touch with our team.</p>
      </div>
      
      <div style={{ display: 'flex', gap: '2rem', flexWrap: 'wrap' }}>
        {/* FAQ Section */}
        <div className="card" style={{ flex: '1 1 60%', minWidth: '400px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '1.5rem' }}>
            <HelpCircle color="var(--accent-color)" size={24} />
            <h3 style={{ color: 'var(--text-primary)', margin: 0 }}>Frequently Asked Questions</h3>
          </div>
          
          <div style={{ display: 'flex', flexDirection: 'column' }}>
            {faqs.map((faq, idx) => (
              <FAQItem key={idx} question={faq.question} answer={faq.answer} />
            ))}
          </div>
        </div>

        {/* Contact Support Section */}
        <div className="card" style={{ flex: '1 1 30%', minWidth: '300px', alignSelf: 'flex-start' }}>
          <h3 style={{ color: 'var(--text-primary)', marginBottom: '1rem' }}>Still need help?</h3>
          <p style={{ color: 'var(--text-secondary)', marginBottom: '1.5rem' }}>
            If you couldn't find the answer you were looking for, our support team is ready to help you out.
          </p>
          
          <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
            <button className="btn" style={{ 
              width: '100%', 
              justifyContent: 'center', 
              background: 'rgba(59, 130, 246, 0.1)', 
              color: 'var(--accent-color)',
              border: '1px solid rgba(59, 130, 246, 0.2)'
            }}>
              <Mail size={18} />
              Email Support
            </button>
            <button className="btn" style={{ 
              width: '100%', 
              justifyContent: 'center', 
              background: 'var(--bg-surface)', 
              color: 'var(--text-primary)',
              border: '1px solid var(--border-color)'
            }}>
              <ExternalLink size={18} />
              Read Documentation
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Help;
