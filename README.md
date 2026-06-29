# Flower Shop Capstone Project

A Flower Shop website with a FastAPI backend, SQLite database, protected chatbot, image upload, health status, and frontend pages.

## Project Structure
- `Backend/` — FastAPI app, auth, chatbot, database access.
- `Frontend/` — HTML pages for homepage, login, chat, and status.
- `Database/` — SQL schema and seed data.
- `ADLC/` — AI Scope Statement and prompt review checklist.
- `Reports/` — self-evaluation and security report.
- `Observability/` — status and logging notes.
- `Tests/` — pytest coverage for auth, chat, upload, and status.
- `.github/` — Copilot instructions and skill file.
- `scripts/` — submission and evaluation helpers.

## Setup
1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Copy environment variables:

```bash
copy .env.example .env
```

3. Start the app:

```bash
python Backend/app.py
```

4. Run the promptfoo evaluation:

```bash
npx promptfoo eval --config promptfooconfig.yaml
```

5. Open the app in your browser:

```text
http://127.0.0.1:8000
```

## Notes
- The app uses SQLite and initializes `Database/flower_shop.db` automatically.
- Protected routes require a bearer token returned from `/api/login`.
- The chatbot supports Flower Shop questions using a simple RAG and Text2SQL classifier.
