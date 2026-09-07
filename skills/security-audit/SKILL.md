---
name: security-audit
description: >
  Must use when the user asks for security issues, audit for vulnerabilities, review auth/authz, or harden the application. Do not use for general code review (use review skill).
---

**The core principle:** Security is not a feature, it is a property. Every input is hostile until proven otherwise. Every error is an information leak until handled. Every dependency is a supply chain risk until verified.

## Rules
1. NEVER assume input is safe. Every external input (user, API, file, env var, database) is hostile until validated and sanitized.
2. NEVER store secrets in code or logs. API keys, tokens, passwords, connection strings MUST NOT appear in source code, log output, error messages, or commit history.
3. NEVER trust client-side validation alone. All validation MUST be enforced server-side. Client-side is UX, not security.
4. NEVER use `eval()`, `exec()`, or dynamic code execution with user-controlled input. This is always an injection vector.
5. ALWAYS check: injection, auth, secrets, CORS, rate limiting, error leakage, dependency vulnerabilities, and session management.

## Workflow

1. Check all API endpoints and their auth requirements, all user input points (forms, query params, headers, body, files), all external integrations (APIs, webhooks, email, file storage), all secrets and credentials (env vars, config files, keychains), session management (cookies, tokens, expiry, refresh)
2. Are queries parameterized or string-concatenated? Are ORM queries using raw queries safely? Is user input used in any shell commands, file paths, or regex?
3. Is password hashing bcrypt/scrypt/argon2 (not MD5/SHA)? Is there rate limiting on login attempts? Are session tokens cryptographically random? Is session expiry enforced? Are password reset tokens time-limited and single-use?
4. Is authorization checked on EVERY endpoint? Can user A access user B's resources by changing an ID? Are admin routes protected with role checks? Is authorization enforced server-side, not just in the UI?
5. Search for hardcoded keys, tokens, passwords in source code. Check `.env` files are in `.gitignore`. Check secrets don't appear in log messages or error output. Check API keys aren't in client-side code (visible in browser)
6. Is the origin whitelist explicit (not `*`)? Are credentials handled correctly? Is the preflight response minimal?
7. Are auth endpoints rate-limited? Are expensive operations (search, export) rate-limited? Are there per-user and per-IP limits?
8. Do error messages expose internal details (stack traces, DB errors)? Are 500 errors generic (not revealing implementation)? Are validation errors specific but not enumeration-enabling?
9. Check for known CVEs in dependencies (npm audit, pip check, etc.) Check for unmaintained dependencies with security implications
10. Are cookies `HttpOnly`, `Secure`, `SameSite`? Is session invalidation enforced on logout? Are tokens rotated on privilege change?
11. Check for the following based on the project type:
  - **Web app:** XSS (stored, reflected, DOM-based), CSRF, clickjacking
  - **API:** BOLA/IDOR, mass assignment, excessive data exposure
  - **File upload:** File type validation, size limits, virus scanning
  - **Payment:** PCI compliance, amount validation, idempotency
  - **Real-time:** WebSocket auth, message validation, subscription scoping
12. For each vulnerability:
  - **Severity:** Critical / High / Medium / Low / Info
  - **Category:** OWASP classification
  - **Location:** file:line
  - **Description:** what the vulnerability is
  - **Trigger:** how to exploit it
  - **Impact:** what an attacker gains
  - **Fix:** specific remediation
13. Present findings sorted by severity. Critical and High MUST be fixed before deployment. Medium should be fixed this sprint. Low and Info are backlog items.
