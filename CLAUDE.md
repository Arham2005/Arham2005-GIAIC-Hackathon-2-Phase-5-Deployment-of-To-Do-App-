# CLAUDE.md — Phase II & Phase III (Spec-Driven)

You are **Claude Code**, operating as a **principal-level systems engineer**.

Your job is **not** speed, convenience, or creativity.
Your job is **architectural correctness, phase integrity, and spec compliance**.

This repository follows **Spec-Driven Development (SDD)**.
No implementation is allowed unless it is **explicitly permitted by the current phase specification**.

---

## COMBINED PROJECT STRUCTURE

For clarity, the full project layout combining shared resources, Phase II, and Phase III is:

```
project-root/
├── .claude/
├── .specify/
├── .venv/
├── .python-version
├── CLAUDE.md
├── README.md
├── pyproject.toml
├── .env.example
├── specs/
│   ├── overview.md
│   ├── architecture.md
│   ├── database/schema.md
│   ├── api/rest.md
│   ├── api/chat.md
│   ├── features/authentication.md
│   ├── features/task-crud.md
│   ├── features/chatbot.md
│   └── ai/agent-behavior.md
├── shared/
│   ├── core/settings.py
│   ├── core/config.py
│   ├── core/security.py
│   ├── db/base.py
│   ├── db/session.py
│   ├── models/user.py
│   └── models/task.py
├── phase2/
│   ├── README.md
│   ├── backend/app/main.py
│   ├── backend/app/api/deps.py
│   ├── backend/app/api/routes/auth.py
│   ├── backend/app/api/routes/tasks.py
│   ├── backend/app/services/auth_service.py
│   ├── backend/app/services/task_service.py
│   ├── backend/app/schemas/user.py
│   ├── backend/app/schemas/task.py
│   ├── frontend/app/login/
│   ├── frontend/app/signup/
│   ├── frontend/app/dashboard/
│   ├── frontend/lib/api.ts
│   ├── frontend/lib/auth.ts
│   └── frontend/middleware.ts
├── phase3/
│   ├── README.md
│   ├── backend/app/api/routes/chat.py
│   ├── backend/app/models/conversation.py
│   ├── backend/app/models/message.py
│   ├── backend/app/services/conversation_service.py
│   ├── backend/app/ai/agent.py
│   ├── backend/app/ai/prompts.py
│   ├── backend/app/ai/runner.py
│   ├── backend/app/mcp/server.py
│   └── backend/app/mcp/tools/
│       ├── add_task.py
│       ├── list_tasks.py
│       ├── update_task.py
│       ├── complete_task.py
│       └── delete_task.py
│   ├── frontend/app/chat/page.tsx
│   └── frontend/lib/chat.ts
├── main.py
```

---

## GLOBAL PRINCIPLES (NON-NEGOTIABLE)

1. **Separation of Concerns**

   * Frontend never owns business logic
   * Backend never trusts frontend input
   * AI never touches the database directly

2. **User Isolation is Sacred**

   * Every request is scoped by `user_id`
   * Any data leakage = hard failure

3. **Stateless Servers**

   * No in-memory user state
   * All state lives in PostgreSQL

4. **Spec > Code**

   * If behavior is wrong → fix spec first
   * Claude Code must refuse undocumented features

---

# PHASE II — Full‑Stack Multi‑User Web Application

## Phase Objective

Transform a single-user / CLI-style app into a **production-grade, authenticated, multi-user web system** with strict boundaries.

Phase II must be **fully correct** before Phase III begins.

---

## Phase II — Functional Guarantees

* Authenticated users only
* Strict per-user data isolation
* Persistent storage (PostgreSQL)
* Stable REST API
* Restart-safe system

---

## Phase II — Technology Constraints

* **Backend:** FastAPI
* **Database:** Neon PostgreSQL
* **ORM:** SQLModel
* **Auth:** JWT (via Better Auth or equivalent)
* **Frontend:** Next.js

No substitutions allowed without spec change.

---

## Phase II — Backend Specification

### Backend Responsibilities

* JWT verification
* User identity extraction
* Authorization enforcement
* Business rule execution
* Database interaction

### Required REST Endpoints

All endpoints require a valid JWT.

* `POST /tasks` → Create task
* `GET /tasks` → List user tasks
* `GET /tasks/{id}` → Get single task (user‑scoped)
* `PUT /tasks/{id}` → Update task
* `DELETE /tasks/{id}` → Delete task
* `POST /tasks/{id}/complete` → Mark complete

Backend **must** enforce:

```
WHERE tasks.user_id == current_user.id
```

---

## Phase II — Database Specification

### Tables

#### users

* id (PK)
* email (unique)
* hashed_password
* created_at

#### tasks

* id (PK)
* title
* description
* completed
* user_id (FK → users.id)
* created_at

Foreign key enforcement is mandatory.

---

## Phase II — Frontend Specification

### Frontend Responsibilities

* Auth UI (login / signup)
* JWT storage (secure)
* Attach JWT to every API request
* Render backend responses faithfully

Frontend **must never**:

* Assume authorization success
* Implement business logic

---

## Phase II — Project Structure

```
phase2/
├── README.md
├── backend/app/main.py
├── backend/app/api/deps.py
├── backend/app/api/routes/auth.py
├── backend/app/api/routes/tasks.py
├── backend/app/services/auth_service.py
├── backend/app/services/task_service.py
├── backend/app/schemas/user.py
├── backend/app/schemas/task.py
├── frontend/app/login/
├── frontend/app/signup/
├── frontend/app/dashboard/
├── frontend/lib/api.ts
├── frontend/lib/auth.ts
└── frontend/middleware.ts
```

---

# PHASE III — AI‑Powered Todo Chat System

## Phase Objective

Convert a CRUD web app into an **AI‑native, conversational system** where natural language triggers structured backend actions **safely**.

---

## Phase III — Core Guarantees

* AI never touches database directly
* All AI actions go through tools
* Stateless server architecture
* Conversation history persisted
* Deterministic, auditable behavior

---

## Phase III — Mental Model Shift

* UI → Conversation
* Buttons → Intent
* Endpoints → Tools

AI is an **operator**, not a text generator.

---

## Phase III — MCP Tool Contract

AI may only interact via the following tools:

* `add_task(title, description)`
* `list_tasks()`
* `update_task(id, fields)`
* `complete_task(id)`
* `delete_task(id)`

Tools reuse **existing Phase II backend logic**.

Any attempt to bypass tools = spec violation.

---

## Phase III — Stateless Chat Architecture

Per message:

1. Load conversation from DB
2. Execute agent reasoning
3. Call tools if required
4. Persist messages + actions
5. Return response

No memory lives in RAM.

---

## Phase III — Agent Governance

* Uses OpenAI Agents SDK
* Converts language → tool calls
* Confirms actions explicitly
* Handles multi-step reasoning

AI behavior must be **bounded and predictable**.

---

## Phase III — Frontend Specification

* Minimal chat UI
* Message send
* Message receive
* Conversation resume

No UI intelligence beyond display

---

## Phase III — Project Structure

```
phase3/
├── README.md
├── backend/app/api/routes/chat.py
├── backend/app/models/conversation.py
├── backend/app/models/message.py
├── backend/app/services/conversation_service.py
├── backend/app/ai/agent.py
├── backend/app/ai/prompts.py
├── backend/app/ai/runner.py
├── backend/app/mcp/server.py
└── backend/app/mcp/tools/
    ├── add_task.py
    ├── list_tasks.py
    ├── update_task.py
    ├── complete_task.py
    └── delete_task.py
├── frontend/app/chat/page.tsx
└── frontend/lib/chat.ts
```

---

## FINAL ENFORCEMENT

Claude Code must:

* Reject features not defined here
* Enforce phase boundaries strictly
* Prioritize correctness over speed

Phase II answers:
**“Can this software be trusted?”**

Phase III answers:
**“Can AI operate this software safely?”**

No shortcuts. No improvisation.
