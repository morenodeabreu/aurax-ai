/**
 * AURAX Frontend - Chat Interface Component
 * Main chat interface with message history and input
 */

/* eslint-disable @typescript-eslint/no-explicit-any */
'use client';

import React, { useState, useRef, useEffect, useCallback } from 'react';
import { ChatMessage } from '@/types/api';
import { api, APIError } from '@/lib/api';
import MessageBubble from './MessageBubble';

interface ChatInterfaceProps {
  className?: string;
}

export const ChatInterface: React.FC<ChatInterfaceProps> = ({ className = '' }) => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [systemStatus, setSystemStatus] = useState<unknown>(null);
  
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);

  // Auto-scroll to bottom when new messages arrive
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const addMessage = (
    type: ChatMessage['type'],
    content: string,
    metadata?: unknown
  ): ChatMessage => {
    const message: ChatMessage = {
      id: Date.now().toString() + Math.random().toString(36).substr(2, 9),
      type,
      content,
      timestamp: new Date(),
      metadata,
    };
    
    setMessages(prev => [...prev, message]);
    return message;
  };

  const addSystemMessage = useCallback((content: string, metadata?: unknown) => {
    return addMessage('system', content, metadata);
  }, []);

  const checkSystemStatus = useCallback(async () => {
    try {
      const status = await api.status();
      setSystemStatus(status);
      
      if (status.success) {
        addSystemMessage(
          `✅ AURAX is ready! Backend connected with ${status.components.llm.default_model}`,
          { status }
        );
      } else {
        addSystemMessage('⚠️ System check completed with issues', { status });
      }
    } catch (error) {
      console.error('System status check failed:', error);
      addSystemMessage('❌ Unable to connect to AURAX backend', { error });
    }
  }, [addSystemMessage]);

  // Check system status on component mount
  useEffect(() => {
    checkSystemStatus();
  }, [checkSystemStatus]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!inputValue.trim() || isLoading) {
      return;
    }

    const userMessage = inputValue.trim();
    setInputValue('');
    setIsLoading(true);

    // Add user message
    addMessage('user', userMessage);

    try {
      // Send request to backend
      const response = await api.generate({
        prompt: userMessage,
        context_threshold: 0.5,
      });

      if (response.success) {
        // Add assistant response
        addMessage('assistant', String(response.response || ''), {
          model_used: response.metadata?.model_used,
          response_type: response.response_type,
          context_docs_count: response.metadata?.context_docs_count,
          routing_info: response.routing_info,
        });
      } else {
        // Add error message
        addMessage('error', response.error || 'Unknown error occurred', {
          response_type: 'error',
        });
      }
    } catch (error) {
      console.error('Generation error:', error);
      
      let errorMessage = 'Failed to get response from AURAX';
      if (error instanceof APIError) {
        errorMessage = `API Error (${error.status}): ${error.message}`;
      } else if (error instanceof Error) {
        errorMessage = `Error: ${error.message}`;
      }
      
      addMessage('error', errorMessage, { response_type: 'error' });
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  const handleClearChat = () => {
    setMessages([]);
    addSystemMessage('💬 Chat cleared');
  };

  return (
    <div className={`flex flex-col h-full bg-gray-50 ${className}`}>
      {/* Header */}
      <div className="bg-white border-b border-gray-200 px-6 py-4 flex-shrink-0">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">AURAX AI</h1>
            <p className="text-sm text-gray-600">
              Autonomous AI System - Multi-Model Assistant
            </p>
          </div>
          <div className="flex items-center gap-2">
            {/* System status indicator */}
            <div className={`
              w-3 h-3 rounded-full
              ${(systemStatus as { success?: boolean })?.success ? 'bg-green-500' : 'bg-red-500'}
            `} title={(systemStatus as { success?: boolean })?.success ? 'System Online' : 'System Offline'} />
            <button
              onClick={handleClearChat}
              className="px-3 py-1 text-sm text-gray-600 hover:text-gray-800 hover:bg-gray-100 rounded"
              disabled={messages.length === 0}
            >
              Clear Chat
            </button>
          </div>
        </div>
      </div>

      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto px-6 py-4">
        {messages.length === 0 ? (
          <div className="text-center text-gray-500 mt-12">
            <div className="text-6xl mb-4">🤖</div>
            <h3 className="text-xl font-semibold mb-2">Welcome to AURAX</h3>
            <p className="mb-4">
              Your autonomous AI assistant with multi-model capabilities
            </p>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 max-w-2xl mx-auto text-sm">
              <div className="bg-white p-4 rounded-lg border">
                <div className="font-semibold mb-1">💬 General Chat</div>
                <div className="text-gray-600">Ask questions, get explanations</div>
              </div>
              <div className="bg-white p-4 rounded-lg border">
                <div className="font-semibold mb-1">💻 Code Generation</div>
                <div className="text-gray-600">Write, debug, and explain code</div>
              </div>
              <div className="bg-white p-4 rounded-lg border">
                <div className="font-semibold mb-1">🎨 Image Creation</div>
                <div className="text-gray-600">Generate images from descriptions</div>
              </div>
            </div>
          </div>
        ) : (
          <div className="space-y-2">
            {messages.map((message) => (
              <MessageBubble key={message.id} message={message} />
            ))}
            <div ref={messagesEndRef} />
          </div>
        )}
      </div>

      {/* Input Area */}
      <div className="bg-white border-t border-gray-200 px-6 py-4 flex-shrink-0">
        <form onSubmit={handleSubmit} className="flex gap-3">
          <div className="flex-1 relative">
            <textarea
              ref={inputRef}
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Ask AURAX anything... (Press Enter to send, Shift+Enter for new line)"
              className="w-full px-4 py-3 border border-gray-300 rounded-lg resize-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
              rows={1}
              style={{
                minHeight: '48px',
                maxHeight: '120px',
                height: 'auto',
              }}
              onInput={(e) => {
                const target = e.target as HTMLTextAreaElement;
                target.style.height = 'auto';
                target.style.height = Math.min(target.scrollHeight, 120) + 'px';
              }}
              disabled={isLoading}
            />
            {isLoading && (
              <div className="absolute right-3 top-3">
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-blue-500"></div>
              </div>
            )}
          </div>
          <button
            type="submit"
            disabled={!inputValue.trim() || isLoading}
            className="px-6 py-3 bg-blue-500 text-white rounded-lg hover:bg-blue-600 focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            {isLoading ? (
              <div className="flex items-center gap-2">
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                <span>Sending...</span>
              </div>
            ) : (
              'Send'
            )}
          </button>
        </form>
        
        {/* Model status info */}
        {(systemStatus as { success?: boolean })?.success && (
          <div className="mt-2 text-xs text-gray-500 text-center">
            Connected to {(systemStatus as any)?.components?.llm?.default_model} • 
            {(systemStatus as any)?.components?.rag?.knowledge_base?.total_points || 0} documents in knowledge base
          </div>
        )}
      </div>
    </div>
  );
};

export default ChatInterface;