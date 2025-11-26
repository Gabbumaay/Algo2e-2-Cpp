# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project overview

This repo implements a small pseudo-code to C++ converter with:
- A Python backend that lexes/parses a custom pseudo-language using PLY and generates C++ code.
- A Flask HTTP API that exposes the converter.
- A React single-page frontend that talks to the Flask API and provides a two-pane UI (pseudo-code in, C++ out).

## High-level architecture

### Backend: lexer, parser, and code generation (Python)

- `lexer.py`
  - Defines the token set for the pseudo-language using PLY (e.g. `\Fn`, `\While`, `\For`, `\If`, `\Else`, `\KwRet`, `\gets`, logical operators, comparison operators, and literals for numbers, strings, chars, and booleans).
  - Handles single-line (`// ...`) and multi-line (`/* ... */`) comments and tracks line numbers.
  - Builds and exports a PLY lexer instance as `lexer`.

- `parser.py`
  - Uses PLY yacc and imports `tokens` from `lexer.py`.
  - Maintains global state:
    - `symbol_table`: maps variable names to inferred/declared C++ types.
    - `has_return`: tracks whether the single parsed function has a `return` to decide its C++ return type (`int` vs `void`).
  - Type handling:
    - `infer_type(value)` infers a basic type (`int`, `float`, `string`, `char`) for constants.
    - `ask_type(var)` prompts on stdin for a datatype when it cannot infer a type and the variable is new.
    - `handle_assignment(var, value, is_expression)` centralizes symbol table updates and when to ask the user for types.
  - Grammar / AST:
    - Top level is a single `program` consisting of a single `function` with no parameters.
    - `statement` variants include:
      - Assignments: to numbers/identifiers and to arbitrary expressions (with expression grammar for `+`, `-`, `*`, `/`, `%` and parentheses).
      - Control flow: `if`, `while`, and C-style `for` loops with `init; condition; update` clauses, each represented as a small AST node (e.g. `{ "type": "for", "init": ..., "condition": ..., "update": ..., "body": [...] }`).
      - `return` of an identifier or number.
    - `condition` rules build string expressions like `"a < b"` using the expression grammar on both sides and relational operators (`<`, `>`, `<=`, `>=`, `==`, `!=`).
  - Code generation:
    - `generate_cpp(parsed, indent=0)` walks the parsed AST and produces C++ code, handling indentation for nested blocks.
    - `_format_for_assignment(assign_node, include_type)` renders assignments; `include_type` is used to avoid redeclaring types in `for` loop update clauses.
    - `to_cpp(parsed)` prepends a header (`#include <bits/stdc++.h>`, `using namespace std;`), appends a `main()` that calls the single parsed function, and returns the full C++ translation unit.
    - Exposes a PLY parser instance as `parser = yacc.yacc()`.
  - Important caveats for future changes:
    - `symbol_table` and `has_return` are module-level globals that are not automatically reset between parses, so repeated calls to `parser.parse(...)` in the same process may leak type/return-type information across requests.
    - `ask_type` uses `input()`, which is fine for CLI usage (`app.py`) but will block under `server.py` if the grammar path triggers a type prompt; expressions that rely on unknown variable types will currently cause this behavior.

- `app.py`
  - Simple CLI wrapper for the parser:
    - Reads pseudo-code from `input.txt` in the repo root.
    - Calls `parser.parse(...)` and then `to_cpp(...)`.
    - Prints the resulting C++ code and writes it to `output.cpp`.
  - Intended for local/manual experimentation with the pseudo-language.

- `server.py`
  - Flask application that wraps the parser for use by the React frontend (or other HTTP clients).
  - Endpoints:
    - `POST /convert`
      - Expects JSON `{ "code": "...pseudo-code..." }`.
      - Validates that `code` is non-empty.
      - Runs `parser.parse(code)` and `to_cpp(parsed)`.
      - On success: returns `{ "cpp": "...generated C++..." }` (HTTP 200).
      - On syntax errors: catches `SyntaxError` and returns `{ "error": "..." }` (HTTP 400).
      - On unexpected errors: returns `{ "error": "Internal error: ..." }` (HTTP 500).
    - `GET /health`
      - Simple health check that returns `{ "status": "ok" }`.
  - CORS:
    - Uses `flask_cors.CORS` to allow `http://localhost:3000` (React dev server) and `*` origins on the `/convert` route.
  - Runs as a dev server on `0.0.0.0:5000` with `debug=True` when executed as `python server.py`.

### Frontend: React single-page app (CRA-style)

- Located under `frontend/` and bootstrapped with `react-scripts`.
- `frontend/src/index.js`
  - Standard React entrypoint that renders `<App />` into `#root` in `public/index.html` and imports `App.css` for styling.
- `frontend/src/App.js`
  - Main UI component with local state for:
    - `code`: pseudo-code in a left-hand textarea (pre-populated with an example).
    - `cpp`: generated C++ for the right-hand textarea.
    - `loading` and `error` flags for request status.
  - `handleConvert`:
    - Sends `POST http://localhost:5000/convert` with `{ code }` using `axios`.
    - On success, populates the C++ output; on failure, surfaces the backend error message.
  - `handleCopy`:
    - Copies the generated C++ to the clipboard using the browser `clipboard` API.
  - Layout:
    - Two-pane responsive layout (pseudo-code left, C++ right) with a footer containing action buttons and an error banner.
- `frontend/src/App.css`
  - Provides the “modern” glassmorphism-style UI, with a centered shell, responsive grid for panes, styled textarea editors, and button/error styles.
- `frontend/public/index.html`
  - Minimal HTML shell with `<div id="root"></div>` and a title matching the app.

## Dependencies

- Python (backend)
  - Managed via `requirements.txt` at the repo root:
    - `ply` (lexing/parsing)
    - `flask` (HTTP server)
    - `flask-cors` (CORS configuration)
- Node.js (frontend)
  - `frontend/package.json` dependencies:
    - `react`, `react-dom`, `react-scripts` (React app runtime and dev tooling).
    - `axios` (HTTP client).
    - `concurrently` (runs Flask backend and React dev server in one command).

## Common setup and development commands

All commands below assume the repo root is `btp`.

### Python backend

From the repo root:

- Install backend dependencies (global or into an active virtual environment):
  - `pip install -r requirements.txt`
- Run the Flask HTTP server only (for API testing without the React dev server):
  - `python server.py`
- Use the CLI converter against `input.txt` and write `output.cpp`:
  - `python app.py`

> Note: when using the HTTP API via `server.py`, avoid pseudo-code constructs that cause `ask_type` to be invoked (i.e., assignments to expressions introducing previously unseen variables), or refactor `parser.py` to make type resolution non-interactive.

### React frontend and full-stack dev workflow

From the `frontend/` directory:

- Install frontend dependencies:
  - `npm install`
- Start both Flask backend and React dev server (primary dev entrypoint):
  - `npm start`
  - This uses the `start` script in `frontend/package.json`:
    - Runs `python server.py` from the repo root.
    - Starts `react-scripts start` on port 3000.
  - The frontend expects the backend at `http://localhost:5000` and calls `/convert` and `/health` there.
- Run frontend tests (once test files are added under `frontend/src`):
  - `npm test`
  - This launches Jest in watch mode via `react-scripts test`; you can filter to a single test file or test name using the interactive prompts (`p` for filename pattern, `t` for test name pattern).
- Build a production bundle of the frontend:
  - `npm run build`

### Testing and linting status

- Python backend:
  - There is currently no dedicated automated test suite or lint configuration for the Python code. Future changes may want to introduce `pytest` and a linter/formatter (e.g. `ruff`, `black`, or `flake8`) and wire them into project scripts.
- Frontend:
  - `react-scripts` provides Jest-based testing via `npm test`; there are no custom test files in `frontend/src/` yet, but this is the mechanism to use once tests are added.
