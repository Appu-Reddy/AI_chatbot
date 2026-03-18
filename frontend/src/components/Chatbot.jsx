import React, { useState, useRef, useEffect } from 'react';
import { MessageSquare, X, Send, Bot } from 'lucide-react';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8001/api/chat';

function Chatbot() {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([
    {
      id: 1,
      sender: 'bot',
      text: "Hi! I'm your product guide. Ask me how to navigate the app.",
      steps: null,
    },
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  const highlightElement = (selector) => {
    if (!selector) return;
    try {
      const el = document.querySelector(selector);
      if (el) {
        el.scrollIntoView({ behavior: 'smooth', block: 'center' });
        el.classList.add('highlight-element');
        setTimeout(() => {
          el.classList.remove('highlight-element');
        }, 3000);
      }
    } catch (e) {
      console.error(`Invalid selector: ${selector}`, e);
    }
  };

  const captureDomSnapshot = () => {
    try {
      const domClone = document.body.cloneNode(true);
      domClone
        .querySelectorAll('script, style, noscript, svg, .chatbot-widget, [aria-hidden="true"]')
        .forEach((el) => el.remove());

      const mainContent =
        domClone.querySelector('main, .main-content, #main, .page-container') ||
        domClone.querySelector('#app, #root') ||
        domClone;

      return mainContent.innerHTML
        .replace(/\s+/g, ' ')
        .trim()
        .substring(0, 5000);
    } catch (err) {
      console.warn('[chatbot] Could not capture DOM snapshot:', err);
      return '';
    }
  };

  const handleSend = async (e) => {
    e?.preventDefault();
    if (!input.trim()) return;

    const userMessage = { id: Date.now(), sender: 'user', text: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    const domSnapshot = captureDomSnapshot();

    try {
      const response = await fetch(API_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          query: userMessage.text,
          dom: domSnapshot,
        }),
      });

      if (!response.ok) throw new Error('Network response was not ok');

      const data = await response.json();

      const stepsWithSelectors = data.steps?.filter((s) => s.selector) || [];
      if (stepsWithSelectors.length > 0) {
        highlightElement(stepsWithSelectors[0].selector);
      }

      const botMessage = {
        id: Date.now() + 1,
        sender: 'bot',
        text: data.intent === 'general' ? '' : 'Here are the steps:',
        steps: data.steps,
      };

      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      console.error('Error communicating with chatbot', error);
      setMessages((prev) => [
        ...prev,
        {
          id: Date.now() + 1,
          sender: 'bot',
          text: "Oops, I'm having trouble connecting to the server.",
          steps: null,
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const isVideo = (url) =>
    typeof url === 'string' && url.match(/\.(mp4|webm|ogg)$/i);

  return (
    <div className="chatbot-widget">
      {isOpen && (
        <div className="chatbot-window">
          <div className="chatbot-header">
            <div className="chatbot-header-title">
              <Bot size={20} color="var(--accent-color)" />
              Product Guide
            </div>
            <button
              className="chatbot-close"
              onClick={() => setIsOpen(false)}
              aria-label="Close Chat"
            >
              <X size={20} />
            </button>
          </div>

          <div className="chatbot-messages">
            {messages.map((msg) => (
              <div
                key={msg.id}
                className={`message ${
                  msg.sender === 'user' ? 'message-user' : 'message-bot'
                }`}
              >
                <div style={{ display: 'flex', gap: '8px', alignItems: 'flex-start' }}>
                  {msg.sender === 'bot' && (
                    <Bot
                      size={16}
                      style={{ marginTop: '2px', flexShrink: 0 }}
                      opacity={0.7}
                    />
                  )}
                  <div style={{ flex: 1 }}>
                    {msg.text && <div>{msg.text}</div>}

                    {msg.steps && msg.steps.length > 0 && (
                      <div className="message-steps">
                        {msg.steps.map((step, idx) => (
                          <div key={idx} className="step-item">
                            <div
                              style={{
                                fontWeight: 500,
                                fontSize: '0.85rem',
                                marginBottom: step.media || step.selector ? '4px' : '0',
                              }}
                            >
                              {msg.steps.length > 1 && (
                                <span style={{ color: 'var(--text-secondary)', marginRight: '4px' }}>
                                  {idx + 1}.
                                </span>
                              )}
                              {step.text}
                            </div>

                            {step.selector && (
                              <button
                                onClick={() => highlightElement(step.selector)}
                                style={{
                                  background: 'none',
                                  border: 'none',
                                  color: 'var(--accent-color)',
                                  fontSize: '0.75rem',
                                  cursor: 'pointer',
                                  textDecoration: 'underline',
                                  padding: 0,
                                  marginTop: '4px',
                                }}
                              >
                                Show me where
                              </button>
                            )}

                            {step.media && (
                              <div className="step-media">
                                {isVideo(step.media) ? (
                                  <video src={step.media} autoPlay loop muted playsInline />
                                ) : (
                                  <img src={step.media} alt="Step visual guide" />
                                )}
                              </div>
                            )}
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                </div>
              </div>
            ))}

            {isLoading && (
              <div
                className="message message-bot"
                style={{ maxWidth: '80px', padding: '0.5rem 1rem' }}
              >
                <div className="typing-indicator">
                  <div className="typing-dot"></div>
                  <div className="typing-dot"></div>
                  <div className="typing-dot"></div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          <form className="chatbot-input-area" onSubmit={handleSend}>
            <input
              type="text"
              className="chatbot-input"
              placeholder="Ask me how to..."
              value={input}
              onChange={(e) => setInput(e.target.value)}
              disabled={isLoading}
            />
            <button
              type="submit"
              className="chatbot-send"
              disabled={!input.trim() || isLoading}
              aria-label="Send Message"
            >
              <Send size={16} style={{ marginLeft: '-2px' }} />
            </button>
          </form>
        </div>
      )}

      {!isOpen && (
        <button
          className="chatbot-toggle"
          onClick={() => setIsOpen(true)}
          aria-label="Open Chat"
        >
          <MessageSquare size={28} />
        </button>
      )}
    </div>
  );
}

export default Chatbot;