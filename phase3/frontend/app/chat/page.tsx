'use client';

import { useState, useEffect, useRef } from 'react';
import { useRouter } from 'next/navigation';
import { chatAPI } from '../../lib/chat';
import { isAuthenticated, removeAuthToken, getUserFromToken } from '../../lib/auth';

interface Message {
  id: number;
  content: string;
  role: 'user' | 'assistant';
  created_at: string;
}

interface Conversation {
  id: number;
  title: string;
  created_at: string;
}

interface ChatResponse {
  conversation_id: number;
  response: string;
  tool_calls: Array<any>; // Array of tool calls made during the interaction
}

const ChatPage = () => {
  const [inputMessage, setInputMessage] = useState('');
  const [messages, setMessages] = useState<Message[]>([]);
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [activeConversation, setActiveConversation] = useState<number | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const router = useRouter();
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!isAuthenticated()) {
      router.push('/login');
      return;
    }

    // Load conversations
    loadConversations();
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const loadConversations = async () => {
    try {
      // For now, we'll just initialize the conversations state
      // In a real implementation, we would fetch from the API
      // We'll leave this as is since the sidebar isn't actively used
      // and conversations are managed by the active conversation state
    } catch (err) {
      setError('Failed to load conversations');
      console.error('Error loading conversations:', err);
    }
  };

  const handleStartNewChat = async () => {
    try {
      const convData = {
        title: `Chat ${new Date().toLocaleString()}`
      };

      const response = await chatAPI.startConversation(convData);
      setActiveConversation(response.id);
      setMessages([]);
      setError('');
    } catch (err) {
      setError('Failed to start new conversation');
      console.error('Error starting conversation:', err);
    }
  };

  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!inputMessage.trim() || isLoading) return;

    const userFromToken = getUserFromToken();
    if (!userFromToken || !userFromToken.userId) {
      setError('User not authenticated');
      return;
    }

    const currentUserId = userFromToken.userId;

    // If no active conversation, create one first
    let conversationId = activeConversation;
    if (!conversationId) {
      try {
        const convData = {
          title: `Chat ${new Date().toLocaleString()}`
        };
        const response = await chatAPI.startConversation(convData);
        conversationId = response.id;
        setActiveConversation(response.id);
        setError('');
      } catch (err) {
        setError('Failed to start new conversation');
        console.error('Error starting conversation:', err);
        setIsLoading(false);
        return;
      }
    }

    const userMessage: Message = {
      id: Date.now(), // Temporary ID
      content: inputMessage,
      role: 'user',
      created_at: new Date().toISOString()
    };

    // Add user message to UI immediately
    setMessages(prev => [...prev, userMessage]);
    const messageToSend = inputMessage;
    setInputMessage('');
    setIsLoading(true);
    setError('');

    try {
      // Use the new API endpoint that follows the updated specification
      const response: ChatResponse = await chatAPI.sendChatMessage(currentUserId, messageToSend, conversationId);

      // Update active conversation if it changed (should be the same, but just in case)
      if (response.conversation_id !== activeConversation) {
        setActiveConversation(response.conversation_id);
      }

      // Add AI response to messages
      const aiMessage: Message = {
        id: Date.now() + 1, // Temporary ID
        content: response.response,
        role: 'assistant',
        created_at: new Date().toISOString()
      };

      setMessages(prev => [...prev, aiMessage]);

      // Optionally display tool calls information to the user
      if (response.tool_calls && response.tool_calls.length > 0) {
        console.log('Tool calls made:', response.tool_calls);
        // You could optionally show a notification about tool calls
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to send message');
      console.error('Error sending message:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleLogout = () => {
    removeAuthToken();
    router.push('/login');
  };

  const formatTime = (dateString: string) => {
    return new Date(dateString).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex flex-col">
      {/* Header */}
      <header className="bg-white shadow-sm z-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <h1 className="text-2xl font-bold text-indigo-600">AI Chat Assistant</h1>
            </div>
            <div className="flex items-center space-x-4">
              <button
                onClick={handleStartNewChat}
                className="px-4 py-2 rounded-md text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 transition-colors duration-200"
              >
                New Chat
              </button>
              <button
                onClick={() => router.push('/dashboard')}
                className="px-4 py-2 rounded-md text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 transition-colors duration-200 mr-2"
              >
                Back to Dashboard
              </button>
              <button
                onClick={handleLogout}
                className="px-4 py-2 rounded-md text-sm font-medium text-white bg-red-500 hover:bg-red-600 transition-colors duration-200"
              >
                Logout
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Notification Banner */}
      <div className="bg-green-50 border-l-4 border-green-400 p-4">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex">
            <div className="flex-shrink-0">
              <svg className="h-5 w-5 text-green-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
              </svg>
            </div>
            <div className="ml-3">
              <p className="text-sm text-green-700">
                <strong>Real-time Sync:</strong> All tasks you manage here (add, update, complete, delete) are instantly synchronized with your dashboard. Changes appear in real-time!
              </p>
            </div>
          </div>
        </div>
      </div>

      <div className="flex flex-1 overflow-hidden max-w-7xl mx-auto w-full px-4 sm:px-6 lg:px-8 py-6">
        {/* Sidebar - Conversations List */}
        <div className="w-64 bg-white rounded-xl shadow-md p-4 mr-6 hidden md:block">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Conversations</h2>
          <div className="space-y-2">
            {conversations.length === 0 ? (
              <p className="text-gray-500 text-sm">No conversations yet</p>
            ) : (
              conversations.map(conversation => (
                <button
                  key={conversation.id}
                  onClick={() => setActiveConversation(conversation.id)}
                  className={`w-full text-left p-3 rounded-lg text-sm ${
                    activeConversation === conversation.id
                      ? 'bg-indigo-100 text-indigo-700'
                      : 'hover:bg-gray-100'
                  }`}
                >
                  <div className="font-medium truncate">{conversation.title}</div>
                  <div className="text-gray-500">{new Date(conversation.created_at).toLocaleDateString()}</div>
                </button>
              ))
            )}
          </div>
        </div>

        {/* Main Chat Area */}
        <div className="flex-1 flex flex-col bg-white rounded-xl shadow-md overflow-hidden">
          {/* Messages Container */}
          <div className="flex-1 overflow-y-auto p-6">
            {messages.length === 0 ? (
              <div className="h-full flex flex-col items-center justify-center text-center">
                <div className="mb-6">
                  <div className="mx-auto h-16 w-16 bg-indigo-100 rounded-full flex items-center justify-center">
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8 text-indigo-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
                    </svg>
                  </div>
                </div>
                <h3 className="text-xl font-semibold text-gray-900 mb-2">Welcome to AI Chat Assistant</h3>
                <p className="text-gray-600 max-w-md">
                  I'm here to help you manage your tasks. You can ask me to add, list, update, complete, or delete tasks.
                </p>
                <div className="mt-6 grid grid-cols-1 md:grid-cols-2 gap-3 max-w-lg">
                  <div className="bg-blue-50 p-3 rounded-lg">
                    <p className="text-sm font-medium text-blue-800">Try asking:</p>
                    <p className="text-xs text-blue-600 mt-1">"Add a task to buy groceries"</p>
                  </div>
                  <div className="bg-green-50 p-3 rounded-lg">
                    <p className="text-sm font-medium text-green-800">Or:</p>
                    <p className="text-xs text-green-600 mt-1">"Show me my tasks"</p>
                  </div>
                  <div className="bg-yellow-50 p-3 rounded-lg">
                    <p className="text-sm font-medium text-yellow-800">Maybe:</p>
                    <p className="text-xs text-yellow-600 mt-1">"Complete task 1"</p>
                  </div>
                  <div className="bg-purple-50 p-3 rounded-lg">
                    <p className="text-sm font-medium text-purple-800">Also:</p>
                    <p className="text-xs text-purple-600 mt-1">"Update task 2 to have a new title"</p>
                  </div>
                </div>
              </div>
            ) : (
              <div className="space-y-6">
                {messages.map((message) => (
                  <div
                    key={message.id}
                    className={`flex ${
                      message.role === 'user' ? 'justify-end' : 'justify-start'
                    }`}
                  >
                    <div
                      className={`max-w-[80%] rounded-2xl px-4 py-3 ${
                        message.role === 'user'
                          ? 'bg-indigo-600 text-white rounded-tr-none'
                          : 'bg-gray-100 text-gray-800 rounded-tl-none'
                      }`}
                    >
                      <div className="whitespace-pre-wrap">{message.content}</div>
                      <div
                        className={`text-xs mt-1 ${
                          message.role === 'user' ? 'text-indigo-200' : 'text-gray-500'
                        }`}
                      >
                        {formatTime(message.created_at)}
                      </div>
                    </div>
                  </div>
                ))}
                {isLoading && (
                  <div className="flex justify-start">
                    <div className="max-w-[80%] bg-gray-100 text-gray-800 rounded-2xl rounded-tl-none px-4 py-3">
                      <div className="flex items-center">
                        <div className="h-2 w-2 bg-gray-500 rounded-full animate-bounce mr-1"></div>
                        <div className="h-2 w-2 bg-gray-500 rounded-full animate-bounce mr-1 delay-75"></div>
                        <div className="h-2 w-2 bg-gray-500 rounded-full animate-bounce delay-150"></div>
                      </div>
                    </div>
                  </div>
                )}
                <div ref={messagesEndRef} />
              </div>
            )}
          </div>

          {/* Input Area */}
          <div className="border-t border-gray-200 p-4">
            {error && (
              <div className="mb-3 rounded-md bg-red-50 p-3">
                <p className="text-sm text-red-700">{error}</p>
              </div>
            )}
            <form onSubmit={handleSendMessage} className="flex gap-3">
              <input
                type="text"
                value={inputMessage}
                onChange={(e) => setInputMessage(e.target.value)}
                placeholder="Type your message here..."
                className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                disabled={isLoading}
              />
              <button
                type="submit"
                disabled={isLoading || !inputMessage.trim()}
                className="px-6 py-3 bg-indigo-600 text-white font-medium rounded-lg hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors duration-200"
              >
                Send
              </button>
            </form>
            <p className="text-xs text-gray-500 mt-2 text-center">
              AI Assistant can help you manage your tasks. Ask to add, list, update, complete, or delete tasks.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChatPage;