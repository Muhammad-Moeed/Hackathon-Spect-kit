import React, { useState } from 'react';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import './Chatbot.css';

export default function Chatbot() {
  // ✅ Docusaurus context se backend URL lena
  const { siteConfig } = useDocusaurusContext();
  const API_URL = siteConfig.customFields?.backendUrl
  console.log('🔗 Backend URL:', API_URL);
  
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([
    { type: 'bot', text: 'Hi! Ask me anything about Physical AI & Humanoid Robotics.' }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = { type: 'user', text: input };
    setMessages([...messages, userMessage]);
    const currentInput = input;
    setInput('');
    setLoading(true);

    try {
      // Backend API call
     const response = await fetch(`${API_URL}/api/v1/query`, {
  method: 'POST',
  headers: { 
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({ 
    query: currentInput,        
    mode: 'full_book',            
    selected_text: '',           
    user_id: 'guest'             
  })
});


      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      
      // Bot response
      const botMessage = { 
        type: 'bot', 
        text: data.answer || data.response || 'Sorry, I could not process that.' 
      };
      setMessages(prev => [...prev, botMessage]);
      
    } catch (error) {
      console.error('Chatbot Error:', error);
      const errorMessage = { 
        type: 'bot', 
        text: 'Error connecting to server. Please try again later.' 
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <>
      {/* Floating Button */}
      <div 
        className="chatbot-button" 
        onClick={() => setIsOpen(!isOpen)}
        title="Ask AI Assistant"
      >
        💬
      </div>

      {/* Chat Window */}
      {isOpen && (
        <div className="chatbot-window">
          <div className="chatbot-header">
            <h3>🤖 AI Assistant</h3>
            <button 
              onClick={() => setIsOpen(false)}
              aria-label="Close chat"
            >
              ✕
            </button>
          </div>

          <div className="chatbot-messages">
            {messages.map((msg, idx) => (
              <div key={idx} className={`message ${msg.type}`}>
                {msg.text}
              </div>
            ))}
            {loading && (
              <div className="message bot typing-indicator">
                <span></span>
                <span></span>
                <span></span>
              </div>
            )}
          </div>

          <div className="chatbot-input">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Ask about the book..."
              disabled={loading}
            />
            <button 
              onClick={sendMessage}
              disabled={loading || !input.trim()}
            >
              {loading ? '...' : 'Send'}
            </button>
          </div>
        </div>
      )}
    </>
  );
}