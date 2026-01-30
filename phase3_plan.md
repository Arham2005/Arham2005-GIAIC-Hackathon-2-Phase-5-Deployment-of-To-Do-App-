# Phase III Implementation Plan: Todo AI Chatbot

## Objective
Update the existing Phase III Todo AI Chatbot to meet the new specifications using OpenAI Agents SDK and MCP server architecture.

## Current State Analysis
- Existing implementation uses custom agent logic in `phase3/backend/app/ai/agent.py`
- MCP server exists in `phase3/backend/app/mcp/server.py` with basic tools
- Database models for conversations and messages are implemented
- Frontend chat interface exists in `phase3/frontend/app/chat/page.tsx`
- API endpoints are in `phase3/backend/app/api/routes/chat.py`

## Implementation Steps

### Step 1: Update MCP Server to use Official MCP SDK
- Replace current MCP server implementation with official MCP SDK
- Ensure proper tool registration and schema generation
- Update tool calling mechanism to match OpenAI Agents SDK expectations

### Step 2: Update MCP Tools to Match New Specifications
- Modify existing tools to match new parameter requirements
- Add proper return value formatting as specified
- Ensure all tools accept `user_id` as a required parameter
- Update `add_task` to return proper format: `{task_id, status, title}`
- Update `list_tasks` to support status filtering parameter
- Update `complete_task`, `delete_task`, and `update_task` to return proper format

### Step 3: Integrate OpenAI Agents SDK
- Replace current custom agent logic with OpenAI Agents SDK
- Configure the agent to use MCP tools for all task operations
- Implement proper tool calling and response handling

### Step 4: Update Chat API Endpoint
- Modify the chat endpoint to match new API specification
- Ensure proper handling of `conversation_id` and `message` parameters
- Add support for returning `tool_calls` array in response
- Maintain backward compatibility where possible

### Step 5: Update Database Models (if needed)
- Ensure Task, Conversation, and Message models match new specifications
- Add `updated_at` timestamp fields if missing
- Verify all required fields exist

### Step 6: Update Frontend to Handle New API Format
- Modify frontend to work with updated API response format
- Handle the new `tool_calls` array in responses
- Ensure proper error handling for tool failures

### Step 7: Testing and Validation
- Test all MCP tools individually
- Test end-to-end chat functionality
- Validate natural language command processing
- Verify user isolation and security requirements

## Detailed Implementation Tasks

### 1. MCP Server Update
- [ ] Install official MCP SDK packages
- [ ] Replace current MCPServer implementation with MCP-compliant server
- [ ] Update tool registration to match OpenAI Agents format
- [ ] Implement proper JSON schema generation for tools

### 2. MCP Tool Updates
- [ ] Update `add_task` tool to match specification
- [ ] Update `list_tasks` tool to accept status parameter
- [ ] Update `complete_task` tool to return correct format
- [ ] Update `delete_task` tool to return correct format
- [ ] Update `update_task` tool to return correct format

### 3. OpenAI Agent Integration
- [ ] Install OpenAI Python SDK
- [ ] Create agent configuration with MCP tools
- [ ] Implement proper message processing pipeline
- [ ] Handle tool call responses appropriately

### 4. API Endpoint Updates
- [ ] Update `/api/{user_id}/chat` endpoint
- [ ] Modify request/response format to match specification
- [ ] Add tool_calls array to response
- [ ] Ensure proper error handling

### 5. Frontend Updates
- [ ] Update chat API library to handle new response format
- [ ] Modify UI to display tool call information if needed
- [ ] Test all functionality end-to-end

## Dependencies and Order
- Task 1 (MCP Server) must be completed before Task 2 (MCP Tools)
- Task 2 (MCP Tools) must be completed before Task 3 (OpenAI Agent)
- Task 4 (API Updates) depends on Tasks 1-3
- Task 5 (Frontend) depends on Task 4

## Success Criteria
- All MCP tools function correctly with OpenAI Agents SDK
- Natural language commands work as specified
- API endpoints match the new specification
- Database models include all required fields
- Frontend displays responses correctly
- User isolation is maintained
- Error handling works appropriately