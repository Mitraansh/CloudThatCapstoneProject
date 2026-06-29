# AI Scope Statement

## Task
Implement the Flower Shop capstone project with a FastAPI backend, SQLite database, protected customer chat, authenticated image upload, and a simple user-facing frontend.

## Files In Scope
- `Backend/app.py`
- `Backend/db.py`
- `Backend/auth.py`
- `Backend/ai.py`
- `Frontend/*.html`
- `Database/schema.sql`
- `Database/seed.py`
- `Tests/test_app.py`
- `Reports/*`
- `.github/copilot-instructions.md`
- `.github/skills/flower-shop-ai-chatbot.md`
- `prompt.md`

## Files Out Of Scope
- `.env` and any local secret files.
- External CI workflows beyond `.github/workflows/ci.yml` unless required for tests.
- System or OS configuration outside this repository.
- Any third-party service integration not already in project requirements.

## UAT-Locked Items
- Preserve existing API route signatures for signup, login, chat, upload, and status.
- Do not change the frontend navigation flow or page contract unless adding a new page.
- Keep the database schema coherent and only evolve it when necessary to support required features.
- Keep `prompt.md` focused on the final OpenRouter chatbot prompt.

## Test Requirements
- Add or update tests for signup, login, protected chat access, upload validation, and status endpoint.
- Do not delete or weaken existing tests to make the suite pass.
- Run the smallest relevant tests after changes and verify the results.

## Review Notes
- After editing, copy the output of `git diff --stat HEAD` into this file or report it in `Reports/self-evaluation.md`.
- If a proposed change touches more than the intended files, stop and refine the prompt.
