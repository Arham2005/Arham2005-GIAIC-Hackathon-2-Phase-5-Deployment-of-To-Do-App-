// frontend/lib/chat.ts
const CHAT_API_BASE_URL = process.env.NEXT_PUBLIC_CHAT_API_URL || 'http://localhost:8000'; // Base URL without '/chat' to match the router prefix

// Helper function to get auth token from localStorage
const getAuthToken = (): string | null => {
  if (typeof window !== 'undefined') {
    return localStorage.getItem('auth_token');
  }
  return null;
};

// Generic API request function
const chatApiRequest = async (endpoint: string, options: RequestInit = {}) => {
  const token = getAuthToken();

  const headers = {
    'Content-Type': 'application/json',
    ...(token && { 'Authorization': `Bearer ${token}` }),
    ...options.headers,
  };

  const response = await fetch(`${CHAT_API_BASE_URL}${endpoint}`, {
    ...options,
    headers,
  });

  if (!response.ok) {
    // Try to get the error message from the response
    let errorMessage = `Chat API request failed: ${response.status}`;
    try {
      const errorData = await response.json();
      if (errorData.detail) {
        errorMessage += ` - ${errorData.detail}`;
      }
    } catch (e) {
      // If we can't parse the error, just use the status code
    }

    throw new Error(errorMessage);
  }

  return response.json();
};

// Chat API functions
export const chatAPI = {
  startConversation: (convData: { title: string }) =>
    chatApiRequest('/chat/start', {
      method: 'POST',
      body: JSON.stringify(convData),
    }),

  sendMessage: (conversationId: number, messageData: { content: string }) =>
    chatApiRequest(`/chat/${conversationId}/message`, {
      method: 'POST',
      body: JSON.stringify(messageData),
    }),

  // New API endpoint following the updated specification
  sendChatMessage: (userId: number, message: string, conversationId?: number) => {
    const requestData = {
      message: message,
      conversation_id: conversationId || null
    };

    return chatApiRequest(`/chat/${userId}/chat`, {
      method: 'POST',
      body: JSON.stringify(requestData),
    });
  },

  getConversation: (conversationId: number) =>
    chatApiRequest(`/chat/${conversationId}`),
};