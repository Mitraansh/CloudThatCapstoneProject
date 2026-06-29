# Prompt Review Checklist

Complete this checklist before asking Copilot to generate or modify code.

- [ ] The prompt clearly states the task and the expected behavior.
- [ ] The prompt names the files or folders that are in scope.
- [ ] The prompt lists files, routes, or features that must not be changed.
- [ ] The prompt includes the tests or behaviors that must remain passing.
- [ ] The prompt includes security constraints such as auth, upload validation, or secrets.
- [ ] The prompt uses a clear guardrail: Do not add unauthorized dependencies or remove tests.
- [ ] The prompt asks for a plan first when the task spans multiple files.

## Example Good Prompt

```text
Context: This is the Flower Shop FastAPI project. I need to add a protected chat route and improve query classification.
Instructions: Modify `Backend/app.py` and `Backend/ai.py` only. Preserve the existing signup/login API shape and existing frontend pages. Add or update tests in `Tests/test_app.py`.
Guardrails: Do not add large frontend frameworks. Do not remove or weaken existing tests. Do not commit secrets. Keep the diff small and review `git diff --stat HEAD` after editing.
```

## Notes
- Use this checklist before any Copilot code generation session.
- If the prompt is vague, ask for clarification first.
- Keep the project scope focused on Flower Shop auth, chat, upload, database, status, and simple frontend work.
