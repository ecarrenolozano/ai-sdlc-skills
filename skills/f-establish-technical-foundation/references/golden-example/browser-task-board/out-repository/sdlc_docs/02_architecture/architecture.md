# Browser Task Board Product Architecture

## Document Control

- **Architecture state:** Complete
- **Unresolved material decisions:** 0

## Approved Technical Constraints

- Browser Frontend uses HTML, CSS, and JavaScript.
- Flask Backend uses Python.
- Frontend communicates with backend only through HTTP/JSON.
- SQLite remains behind a backend persistence port.
- Flask serves frontend and API from one local origin.
- Flask binds only to `127.0.0.1`.
- Frontend and backend source, tests, documentation, and commands remain separable.
