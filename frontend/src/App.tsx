
import React, { useState, useRef, useEffect } from 'react';
import { Sidebar } from './components/Sidebar';
import MessageBubble from './components/MessageBubble';
import type { Message } from './types';
import axios from 'axios';
import { Send, Loader2 } from 'lucide-react';
import { v4 as uuidv4 } from 'uuid';

const API_Base_URL = 'http://localhost:8000';

function App() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: 'welcome',
      role: 'assistant',
      content: 'Hello! I am your Research AI Assistant. Upload a PDF document using the sidebar to get started, or ask me questions about already uploaded documents.',
      timestamp: new Date(),
    }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim() || loading) return;

    const userMessage: Message = {
      id: uuidv4(),
      role: 'user',
      content: input,
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      const response = await axios.post(`${API_Base_URL}/query`, {
        query: userMessage.content,
        k: 3 // consistent with backend default
      });

      const botMessage: Message = {
        id: uuidv4(),
        role: 'assistant',
        content: response.data.answer,
        citations: response.data.context, // Backend returns context list
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      console.error('Query failed', error);
      const errorMessage: Message = {
        id: uuidv4(),
        role: 'assistant',
        content: "I'm sorry, I encountered an error while processing your request. Please try again.",
        timestamp: new Date(),
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="flex h-screen bg-gray-50 font-sans text-gray-900">
      <Sidebar
        onUploadSuccess={(filename) => {
          const msg: Message = {
            id: uuidv4(),
            role: 'assistant',
            content: `I've successfully indexed "${filename}". You can now ask questions about its content.`,
            timestamp: new Date(),
          };
          setMessages(prev => [...prev, msg]);
        }}
        onClear={() => {
          setMessages([
            {
              id: uuidv4(),
              role: 'assistant',
              content: 'Document history cleared. Please upload new documents to continue.',
              timestamp: new Date(),
            }
          ]);
        }}
      />

      <main className="flex-1 flex flex-col h-full relative">
        {/* Header */}
        <header className="h-16 border-b border-gray-200 bg-white flex items-center px-8 justify-between shadow-sm z-10">
          <h1 className="text-xl font-bold text-gray-800">Chat Interface</h1>
          <div className="text-sm text-gray-500">
            Powered by Gemini & RAG
          </div>
        </header>

        {/* Chat Messages */}
        <div className="flex-1 overflow-y-auto p-4 md:p-8 space-y-6 scroll-smooth">
          {messages.map(msg => (
            <MessageBubble key={msg.id} message={msg} />
          ))}
          {loading && (
            <div className="flex justify-start w-full mb-6">
              <div className="bg-gray-100 rounded-2xl p-4 flex items-center gap-3">
                <Loader2 className="animate-spin text-blue-600" size={20} />
                <span className="text-gray-500 text-sm">Analyzing documents...</span>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Input Area */}
        <div className="p-4 md:p-6 bg-white border-t border-gray-200">
          <div className="max-w-4xl mx-auto relative flex items-center gap-2">
            <input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyPress}
              placeholder="Ask a question about your documents..."
              className="flex-1 bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-4 pl-5 shadow-sm transition-all"
              disabled={loading}
            />
            <button
              onClick={handleSend}
              disabled={loading || !input.trim()}
              className="absolute right-3 top-1/2 -translate-y-1/2 p-2 text-blue-600 hover:text-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              <Send size={20} />
            </button>
          </div>
          <div className="text-center mt-2 text-xs text-gray-400">
            AI can make mistakes. Please verify important information.
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;
