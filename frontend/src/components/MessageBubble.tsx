/**
 * AURAX Frontend - Message Bubble Component
 * Displays individual chat messages with proper styling
 */

import React from 'react';
import { ChatMessage } from '@/types/api';

interface MessageBubbleProps {
  message: ChatMessage;
}

export const MessageBubble: React.FC<MessageBubbleProps> = ({ message }) => {
  const isUser = message.type === 'user';
  const isError = message.type === 'error';
  const isSystem = message.type === 'system';

  // Format timestamp
  const formatTime = (date: Date) => {
    return date.toLocaleTimeString('en-US', { 
      hour: '2-digit', 
      minute: '2-digit' 
    });
  };

  // Get message styling based on type
  const getMessageStyles = () => {
    if (isError) {
      return 'bg-red-100 border-red-300 text-red-800';
    }
    if (isSystem) {
      return 'bg-gray-100 border-gray-300 text-gray-700';
    }
    if (isUser) {
      return 'bg-blue-500 text-white';
    }
    return 'bg-white border border-gray-200 text-gray-800 shadow-sm';
  };

  // Get response type indicator
  const getResponseTypeIndicator = () => {
    const metadata = message.metadata as { response_type?: string } | undefined;
    const responseType = metadata?.response_type;
    if (!responseType || responseType === 'text') return null;

    const indicators = {
      code: { icon: '💻', label: 'Code', color: 'bg-green-100 text-green-800' },
      image: { icon: '🎨', label: 'Image', color: 'bg-purple-100 text-purple-800' },
      error: { icon: '❌', label: 'Error', color: 'bg-red-100 text-red-800' },
    };

    const indicator = indicators[responseType as keyof typeof indicators];
    if (!indicator) return null;

    return (
      <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${indicator.color} mr-2 mb-1`}>
        <span className="mr-1">{indicator.icon}</span>
        {indicator.label}
      </span>
    );
  };

  // Get model info
  const getModelInfo = () => {
    const metadata = message.metadata as { model_used?: string; context_docs_count?: number } | undefined;
    const modelUsed = metadata?.model_used;
    const contextCount = metadata?.context_docs_count;
    
    if (!modelUsed && !contextCount) return null;

    return (
      <div className="text-xs text-gray-500 mt-1 flex items-center gap-2">
        {modelUsed && (
          <span className="bg-gray-100 px-2 py-1 rounded">
            {modelUsed}
          </span>
        )}
        {contextCount && contextCount > 0 && (
          <span className="bg-blue-100 text-blue-700 px-2 py-1 rounded">
            📚 {contextCount} docs
          </span>
        )}
      </div>
    );
  };

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-4`}>
      <div className={`max-w-[70%] ${isUser ? 'order-2' : 'order-1'}`}>
        {/* Message header with type indicator */}
        <div className="flex items-center mb-1">
          {!isUser && getResponseTypeIndicator()}
          <span className="text-xs text-gray-500">
            {isUser ? 'You' : isSystem ? 'System' : 'AURAX'} • {formatTime(message.timestamp)}
          </span>
        </div>
        
        {/* Message content */}
        <div className={`
          px-4 py-3 rounded-lg border
          ${getMessageStyles()}
          ${isUser ? 'rounded-br-sm' : 'rounded-bl-sm'}
        `}>
          {/* Handle different content types */}
          {(message.metadata as { response_type?: string } | undefined)?.response_type === 'code' ? (
            <pre className="whitespace-pre-wrap font-mono text-sm overflow-x-auto">
              <code>{message.content}</code>
            </pre>
          ) : (
            <div className="whitespace-pre-wrap break-words">
              {message.content}
            </div>
          )}
        </div>

        {/* Model and context info */}
        {!isUser && getModelInfo()}
      </div>
    </div>
  );
};

export default MessageBubble;