# API

Except `/health`, endpoints require `Authorization: Bearer <session>`.
Sessions are printed by the local CLI for the two synthetic users.

| Method | Route | Description |
| --- | --- | --- |
| GET | /health | Process health |
| GET | /api/issues?q=printer | Search the current user's tickets |
| POST | /api/issues | JSON with title and optional body |
| GET | /api/issues/{id} | Ticket detail |
| GET | /issues/{id} | HTML ticket detail |

Titles: 1-200 characters after trimming. Bodies: up to 4000 characters.
Owner is assigned from the server session on creation.
Incoming HTTP bodies are limited to 16 KiB. Search returns at most 50 rows.
Error statuses: 400 invalid input, 401 missing session, 404 not found.
