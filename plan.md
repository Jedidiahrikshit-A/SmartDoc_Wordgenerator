# SmartDocAI implementation plan

## Architecture

SmartDocAI is a two-part application with a Flask API and a Vite-built React client. Flask owns authentication, SQLite persistence, template seeding, AI-provider calls, reference-file extraction, sanitization, and DOCX/PDF generation. The production/preview process serves the built React files from the same Flask origin, so API calls remain relative and cookie sessions work consistently. The data layer uses SQLAlchemy models and a small initialization/seed path that can later be replaced by Alembic migrations and PostgreSQL.

The AI boundary is an `AIService` that prefers the managed Manus OpenAI-compatible API (`MANUS_API_URL` + `MANUS_API_KEY`) and can also use an explicitly configured OpenAI-compatible endpoint. It returns provider failures honestly; the app never substitutes canned generated content. Passwords are hashed with Werkzeug, document ownership is checked on every request, mutation requests use a double-submit CSRF token, and uploads are extracted in memory/temporary storage with size and type checks.

## Project structure

- `backend/app.py`: Flask application factory, models, routes, services, export helpers, startup seed.
- `backend/tests/`: pytest coverage for auth, ownership, CRUD, exports, validation, and AI credential failures.
- `frontend/src/App.jsx`: route-aware product shell and core screens.
- `frontend/src/api.js`: centralized JSON/file API client.
- `frontend/src/styles.css`: dark premium SaaS design system and responsive layout.
- `frontend/public/manus-routes.json`: route manifest for Preview.
- Root config files: `.env.example`, `Dockerfile`, `README.md`, `app.config.ts`.

## Design

Candidate styles (tail probabilities):
- Editorial command center — 0.06
- Quiet luxury SaaS — 0.04
- Industrial document atelier — 0.08

Chosen style: **Quiet luxury SaaS**.

- **Design Movement:** Quiet luxury editorial software: dense enough for work, restrained enough to feel premium.
- **Core Principles:** hierarchy before decoration; emerald only for intent and progress; generous breathing room; every action has a visible state.
- **Color Philosophy:** charcoal and ink surfaces create focus, while a single mineral emerald signals authorship, completion, and trustworthy action.
- **Layout Paradigm:** a persistent left rail and asymmetric workbench: navigation and context stay stable while the main document surface carries the task.
- **Signature Elements:** emerald “signal” lines, paper-like document canvas, and compact status chips that report saved/generated state.
- **Interaction Philosophy:** actions feel deliberate: primary actions are high-contrast, destructive actions are explicit, and loading states preserve context instead of replacing it.
- **Animation:** short 160–220ms opacity/translate transitions; no looping decoration; skeletons shimmer only while data is genuinely loading.
- **Typography System:** Inter for UI and IBM Plex Serif for document/editor headings; 12–14px labels, 16px body, 32–60px page headlines with tight tracking.
- **Brand Essence:** a calm AI workspace for turning rough ideas into documents people can send; focused, capable, composed.
- **Brand Voice:** precise, encouraging, never inflated. Example lines: “Start with the brief. Leave with the document.” and “Your work is saved when the status says saved.”
- **Wordmark & Logo:** a monogram formed from two offset paper corners around a small emerald cursor, paired with a tight SmartDocAI wordmark.
- **Signature Brand Color:** Mineral Emerald `#56d6a0`.
