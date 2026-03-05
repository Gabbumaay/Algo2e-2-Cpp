# Set Data Type Testing Documentation

## Overview
This document describes all test cases for Set support in the Pseudo to C++ Converter.

## Test Cases

### Test 1: set_basic.txt - Basic Set Declaration
**Description:** Tests basic set variable declaration and simple assignments.
**Input:**
```
\Fn testSet() {
    s \gets 1;
    s \gets 2;
    s \gets 3;
    \KwRet 1;
}
```
**Expected Type Hint:** Set variable `s` should be marked as `set` type.
**Expected C++ Output:**
```cpp
set<int> s;
s.insert(1);
s.insert(2);
s.insert(3);
```

---

### Test 2: set_operations.txt - Set with Multiple Operations
**Description:** Tests set creation with multiple element insertions.
**Input:**
```
\Fn setOps() {
    s \gets 1;
    s \gets 2;
    s \gets 3;
    count \gets 3;
    \KwRet count;
}
```
**Type Hints:** `s` → set, `count` → int
**Key Features:** Mixed set and integer variables

---

### Test 3: set_with_loop.txt - Set in Loop Context
**Description:** Tests set variable usage within loops.
**Input:**
```
\Fn setWithLoop() {
    s \gets 1;
    s \gets 2;
    s \gets 3;
    s \gets 4;
    s \gets 5;
    sum \gets 0;
    i \gets 0;
    \While (i < 5) {
        sum \gets sum + i;
        i \gets i + 1;
    }
    \KwRet sum;
}
```
**Type Hints:** `s` → set, `sum` → int, `i` → int
**Key Features:** Loop logic with set operations

---

### Test 4: set_multiple_types.txt - Multiple Set Variables
**Description:** Tests multiple distinct set variables in same function.
**Input:**
```
\Fn multipleSetTypes() {
    s1 \gets 1;
    s1 \gets 2;
    s1 \gets 3;
    s2 \gets 5;
    s2 \gets 10;
    s2 \gets 15;
    total \gets 6;
    \KwRet total;
}
```
**Type Hints:** `s1` → set, `s2` → set, `total` → int
**Key Features:** Multiple set declarations with different element values

---

### Test 5: set_advanced.txt - Advanced Set Operations
**Description:** Tests set operations combined with control flow.
**Input:**
```
\Fn advancedSet() {
    numbers \gets 1;
    numbers \gets 5;
    numbers \gets 3;
    numbers \gets 7;
    numbers \gets 9;
    size \gets 5;
    max_val \gets 9;
    \If (size > 3) {
        \KwRet max_val;
    }
    \KwRet 0;
}
```
**Type Hints:** `numbers` → set, `size` → int, `max_val` → int
**Key Features:** Set with conditional logic

---

## Running the Tests

### Via CLI (app.py):
```bash
# Edit input.txt with test pseudo-code
# Then run:
python app.py
```

### Via Web UI (Frontend):
1. Start both servers:
   ```bash
   # Terminal 1: Backend
   python server.py
   
   # Terminal 2: Frontend
   cd frontend
   npm start
   ```

2. Navigate to http://localhost:3000

3. Paste test code from any test file

4. When prompted for types:
   - Select 'set' for set variables
   - Select 'int' for integer variables

5. Click "Convert to C++" to generate code

---

## Expected Behavior

### Type Prompting:
- Variables assigned numeric literals multiple times → prompt for 'set' type
- Variables assigned single values → prompt for 'int' type

### C++ Generation:
- `set<int> varname;` declaration for set types
- `varname.insert(value);` for each assignment
- Proper scope and declaration placement

### Error Handling:
- Missing type specifications trigger frontend dialog
- Syntax errors show in error banner
- Backend offline status displayed in header

---

## Implementation Notes

1. **Parser:** `valid_dtypes` includes "set"
2. **Frontend:** `VALID_TYPES` includes "set"
3. **Type System:** Set types are treated like any other type in symbol table
4. **Code Gen:** Sets are declared with proper C++ `set<int>` syntax
5. **Backend:** All routes have CORS enabled for frontend access

---
