# SmartDocAI delivery checklist

- [ ] Users can register with server-side validation, duplicate-email prevention, secure password hashing, login, logout, current-user lookup, profile update, password change, CSRF protection, and protected routes.
- [ ] The landing page presents the SmartDocAI value proposition, real auth links, supported document types, workflow, privacy note, FAQ, and responsive navigation without fabricated claims.
- [ ] The authenticated dashboard derives document counts, recent documents, type groupings, search, and quick actions from persisted records.
- [ ] Users can create, open, edit, save, autosave, rename, duplicate, delete, search, filter, sort, tag, preview, and reopen owned documents; every document operation verifies ownership.
- [ ] AI generation and writing assistance call a configured real provider, validate input and limits, accept optional reference context, and report missing credentials/provider failures without fake output.
- [ ] The editor supports title editing, rich text controls, counts, save status, preview, AI assistance, download actions, and unsaved-change protection.
- [ ] Saved document content exports through authenticated DOCX and PDF endpoints with safe filenames and correct content types.
- [ ] The seeded template library includes the requested structural templates and routes into the generation workflow.
- [ ] TXT, PDF, and DOCX reference files are size/type validated, extracted safely, and clearly report unsupported/scanned/corrupt content.
- [ ] README documents Windows PowerShell setup, environment configuration, provider setup, database initialization, seeding, frontend/backend commands, tests, and known limitations.
- [ ] Automated backend tests cover auth, ownership, CRUD, exports, invalid upload, validation, and missing AI credentials; frontend production build and route manifest are verified.
