# SmartDocAI

SmartDocAI is a full-stack AI document workspace. It combines a React/Vite interface with a Flask REST API, SQLite persistence, secure account sessions, real configurable AI generation, reference-file extraction, and DOCX/PDF exports.

## Architecture

The backend lives in `backend/app.py` and owns the database models, authentication, document ownership checks, CSRF protection, AI provider boundary, upload extraction, and exports. The frontend lives in `frontend/src`, builds with Vite, and is served by Flask from `frontend/dist` for the single-port preview/runtime. The SQLite URL can be replaced with a PostgreSQL-compatible SQLAlchemy URL later.

## Windows PowerShell setup

From PowerShell:

```powershell
cd SmartDocAI
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r backend\requirements.txt
cd frontend
npm install
npm run build
cd ..
Copy-Item .env.example .env
python -m backend.app --seed
```

Set a real secret in `.env`:

```powershell
python -c "import secrets; print(secrets.token_hex(32))"
```

Copy the output into `SECRET_KEY`. Keep `COOKIE_SECURE=false` for plain local HTTP. For an HTTPS embedded preview or production HTTPS deployment, use `COOKIE_SECURE=true`; the application uses `SameSite=None; Secure` for the session cookie in that mode.

## AI configuration

SmartDocAI does not fake a draft when AI is unavailable. The managed Manus environment supplies `MANUS_API_URL` and `MANUS_API_KEY`; set `AI_PROVIDER=manus` and optionally `AI_MODEL`. For an external OpenAI-compatible provider, use `AI_PROVIDER=openai`, set `OPENAI_API_KEY`, optionally change `OPENAI_BASE_URL`, and set `AI_MODEL` to a model supported by that endpoint. Never commit `.env` or expose server credentials to the frontend. Content sent for generation may be processed by the configured provider under its policies.

## Run locally

Use two PowerShell terminals. In terminal one:

```powershell
.\.venv\Scripts\Activate.ps1
python -m backend.app
```

In terminal two, use the Vite development server for a hot-reloading frontend:

```powershell
cd frontend
npm run dev
```

For the single-port production-like mode, build the frontend and open `http://localhost:3000` after starting Flask. The backend creates the SQLite database and seeds the ten structural templates on first start; it does not reset the database on later starts. `python -m backend.app --seed` is a repeatable, idempotent seed command.

## Tests

```powershell
.\.venv\Scripts\Activate.ps1
pytest backend\tests -q
cd frontend
npm test
npm run build
```

The backend tests use a temporary database and mock the missing-provider boundary by verifying the honest configuration error. Provider-backed generation requires configured credentials and should be exercised manually after setup. The app validates TXT, PDF, and DOCX uploads; scanned PDFs are reported as unreadable because OCR is not implemented.

## API overview

Authentication endpoints are `/api/auth/register`, `/api/auth/login`, `/api/auth/logout`, `/api/auth/me`, `/api/auth/forgot-password`, `/api/profile`, and `/api/profile/password`. Document endpoints are `/api/documents` and `/api/documents/<id>`, with duplicate, export, and ownership checks. AI endpoints are `/api/ai/generate` and `/api/ai/assist`; templates are `/api/templates`; reference extraction is `/api/files/extract`; health is `/api/health`.

## Troubleshooting

If a browser shows a CSRF error, refresh the page so the non-HTTP-only `csrf_token` cookie is issued. If cookies do not persist on local HTTP, set `COOKIE_SECURE=false`; do not use that setting for public HTTPS. If exports fail, reinstall `python-docx` and `reportlab` in the active virtual environment. If AI requests fail, inspect the provider URL, key, model identifier, timeout, and returned error; SmartDocAI intentionally reports provider failures rather than producing placeholder content.
