# Flower Shop Capstone Project Plan

## Project Overview
The Flower Shop is a fictional florist business that wants a customer-facing website with a RAG chatbot. The chatbot should answer questions using the shop's dummy data, such as flower types, care instructions, seasonal availability, pricing, and delivery policies.

## Required Stack
- **Backend:** Python with FastAPI.
- **Frontend:** HTML, CSS, and minimal JavaScript served by FastAPI.
- **Database:** SQL database (SQLite) with at least six tables.
- **RAG Layer:** Retrieval over a dummy Flower Shop dataset (care instructions, flower descriptions).
- **LLM Usage:** OpenRouter with a free model for the chatbot.
- **Testing:** Python unit and integration tests.
- **Security:** Documented security testing and remediation.
- **Observability:** Health/status endpoint and structured logging.

## Component Structure (Based on reference)
- `Backend/`: FastAPI implementation.
- `Frontend/`: HTML/CSS/JS files.
- `Database/`: SQL schema and seed data.
- `Observability/`: Status page and logs.
- `Security/`: Security reports and tests.
- `Tests/`: Unit, integration, and eval tests.
- `Reports/`: Self-evaluation and evidence.
- `ADLC/`: AI Scope Statement and Prompt Review Checklist.
- `scripts/`: Evaluation and build scripts.

## Implementation Steps (Step-by-Step)

### Phase 1: Plan & Scope
1. Create the project directory structure.
2. Write the AI Scope Statement (`ADLC/ai-scope-statement.md`).
3. Define the `skill.md` for the AI Ask endpoint.
4. Update `.github/copilot-instructions.md`.

### Phase 2: Build
1. **Database:** Create `Database/schema.sql` with 6+ tables (flowers, categories, care_instructions, orders, customers, staff).
2. **Backend:** Implement FastAPI routes (auth, flowers, orders, chatbot).
3. **RAG & Text2SQL:** Implement the intelligent routing for qualitative (care) vs quantitative (price/stock) queries.
4. **Frontend:** Create the UI with a chatbot widget and flower catalog.
5. **Auth:** Implement signup/login and protected routes.

### Phase 3: Protect & Validate
1. **Security:** Conduct security testing (input validation, SQL injection checks).
2. **Testing:** Add unit and integration tests.
3. **Evaluation:** Run RAG and Text2SQL correctness checks.

### Phase 4: Present & Reflect
1. Generate the self-evaluation report.
2. Document the AI-assisted SDLC.
