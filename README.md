# Pseudo to C++ Converter

Convert simple pseudo-code into C++ via a Flask API and a React UI.

## Features
- Parse pseudo-code into an AST and emit C++
- Supports multiple `\\Fn` blocks in one input
- **New**: Clean declaration syntax with `\\Decl` keyword (separate from `\\gets` assignments)
- **New**: Typed sets: `set_int`, `set_float`, `set_double`, `set_char`, `set_string`
- Frontend prompts for missing variable types
- Input editor state persists across browser refresh
- Backend health is checked every 10 seconds in UI
- Copy-to-clipboard with a toast notification

## Requirements
- Python 3.9+
- Node.js 18+

## Setup

### Backend
```bash
pip install -r requirements.txt
```

Start the Flask server:
```bash
python server.py
```
The API runs on http://localhost:5000.

### Frontend
```bash
cd frontend
npm install
npm start
```
The UI runs on http://localhost:3000.

## Usage
1. Paste or write pseudo-code in the left pane.
2. Click "Convert to C++".
3. If the parser needs types, select them in the prompt.
4. Click "Copy C++" to copy the output.

## API

### POST /convert
Request:
```json
{
  "code": "\\Fn Foo() { a \\gets 1; }",
  "types": { "a": "int" }
}
```

Responses:
- 200 OK
```json
{ "cpp": "..." }
```

- 400 Missing type
```json
{
  "error": "missing_type",
  "variable": "a",
  "valid_types": ["int", "float", "string", "long", "char", "array", "vector"]
}
```

- 400 Syntax error
```json
{ "error": "Syntax error near '...'" }
```

### GET /health
Response:
```json
{ "status": "ok" }
```

## Project Structure
```
server.py
lexer.py
parser.py
control_flow/
frontend/
```

## Notes
- The backend never reads from stdin; missing types are handled by the UI.
- Example inputs are in the test/ folder.
- **Declaration Syntax**: See [DECLARATION_SYNTAX.md](DECLARATION_SYNTAX.md) for details on using `\Decl` to declare variables separately from `\gets` assignments.
- **Typed Sets**: See [TYPED_SETS.md](TYPED_SETS.md) for details on using `set_int`, `set_float`, `set_double`, `set_char`, and `set_string`.
