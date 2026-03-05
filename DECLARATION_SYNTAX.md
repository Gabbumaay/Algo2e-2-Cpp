# Declaration Syntax - \Decl Keyword

## Overview

A new `\Decl` keyword has been added to distinguish between **declaration** and **initialization**.

### Design Principle

```
\Decl x;        → Declare variable x only (type from type provider)
x \gets 5;      → Assign/initialize variable x with value
```

**Separation of Concerns**:
- `\Decl` = Pure declaration (no initialization)
- `\gets` = Assignment (with or without prior declaration)

---

## Syntax

### Declaration Only
```
\Decl variable_name;
```

**Example**:
```
\Decl x;        // Declare int (type determined by type provider)
\Decl s;        // Declare set (type determined by type provider)
\Decl arr;      // Declare array (type determined by type provider)
```

### Assignment (existing - unchanged)
```
variable \gets value;
```

**Example**:
```
x \gets 5;      // Assign to x
s \gets 10;     // Insert into set s
arr \gets other; // Copy or assign
```

---

## Type Resolution

When `\Decl x;` is used:

1. **Type Provider is consulted** - Existing type provider system is used
2. **Returns type** - e.g., "set", "int", "array"
3. **Variable is registered** - In symbol table with that type
4. **No initialization** - Just declaration in C++

**Generated C++**:
```cpp
\Decl x;    →  int x;
\Decl s;    →  set<int> s;
\Decl arr;  →  vector<int> arr;
```

---

## Use Cases

### 1. Forward Declaration
Declare variables upfront, initialize later:
```
\Fn computeSum() {
    \Decl total;
    \Decl count;
    
    count \gets 0;
    total \gets 0;
    
    \While (count < 10) {
        total \gets total + count;
        count \gets count + 1;
    }
    
    \KwRet total;
}
```

**Generated C++**:
```cpp
int computeSum() {
    int total;
    int count;

    count = 0;
    total = 0;
    while (count < 10) {
        total = total + count;
        count = count + 1;
    }
    return total;
}
```

### 2. Set Initialization with Explicit Type
```
\Fn setDemo() {
    \Decl mySet;
    
    mySet \gets 10;
    mySet \gets 20;
    mySet \gets 30;
    
    \KwRet 1;
}
```

**Generated C++**:
```cpp
int setDemo() {
    set<int> mySet;

    mySet.insert(10);
    mySet.insert(20);
    mySet.insert(30);
    return 1;
}
```

### 3. Explicit Type Grouping
Group all declarations together for clarity:
```
\Fn processData() {
    \Decl s1;
    \Decl s2;
    \Decl sum;
    
    s1 \gets 100;
    s2 \gets 200;
    sum \gets s1 + s2;
    
    \KwRet sum;
}
```

### 4. Conditional Initialization
Declare first, then conditionally initialize:
```
\Fn maybeInit() {
    \Decl result;
    \Decl flag;
    
    flag \gets 1;
    
    \If (flag) {
        result \gets 42;
    }
    
    \KwRet result;
}
```

---

## Comparison: Declaration vs Assignment

| Aspect | `\Decl x;` | `x \gets 5;` |
|--------|-----------|------------|
| Purpose | Declare only | Assign (init or update) |
| Type resolution | Via type provider | Via type provider + inference |
| C++ output (first use) | `int x;` | `int x;` + `x = 5;` |
| C++ output (update) | N/A | `x = value;` |
| Blocks further declaration? | No | No (same var can be re-assigned) |
| Initialization | None | Optional (depends on context) |

---

## Implementation Details

### Lexer Changes
- Added token `DECL` for `\Decl` keyword
- Lexer recognizes `\Decl` as a reserved token

### Parser Changes
- New grammar rule: `statement : DECL ID SEMICOLON`
- Creates AST node: `{"type": "declare", "var": "variable_name"}`
- Type is resolved via `type_provider()` at parse time

### Code Generation
- Variables from declarations are collected during parsing
- All declarations emitted at function start in C++
- No initialization code generated (type only)
- Declaration statements themselves generate no runtime code

### Complete Flow
```
Input:  \Decl s;
        ↓
Lexer:  [DECL], [ID(s)], [SEMICOLON]
        ↓
Parser: Parse grammar rule, call ask_type("s")
        ↓
Type Provider: Returns "set"
        ↓
Symbol Table: s → "set"
        ↓
Codegen: Emit "set<int> s;" at function start
        ↓
Output: set<int> s;
```

---

## Examples

### Example 1: Pure Declaration
```pseudocode
\Fn example1() {
    \Decl x;
    x \gets 10;
    \KwRet x;
}
```

**Type hints needed**: `x: int`

**Output**:
```cpp
int example1() {
    int x;

    x = 10;
    return x;
}
```

### Example 2: Set Declaration
```pseudocode
\Fn example2() {
    \Decl numbers;
    numbers \gets 5;
    numbers \gets 10;
    numbers \gets 15;
    \KwRet 1;
}
```

**Type hints needed**: `numbers: set`

**Output**:
```cpp
int example2() {
    set<int> numbers;

    numbers.insert(5);
    numbers.insert(10);
    numbers.insert(15);
    return 1;
}
```

### Example 3: Multiple Variable Declarations
```pseudocode
\Fn example3() {
    \Decl s;
    \Decl count;
    \Decl total;
    
    count \gets 0;
    total \gets 0;
    
    s \gets 1;
    s \gets 2;
    
    \KwRet total;
}
```

**Type hints needed**: `s: set, count: int, total: int`

**Output**:
```cpp
int example3() {
    set<int> s;
    int count;
    int total;

    count = 0;
    total = 0;
    s.insert(1);
    s.insert(2);
    return total;
}
```

---

## Migration Guide

### From Implicit to Explicit Declaration

**Old way** (implicit - still works):
```
x \gets 5;      // Type inferred from literal (int)
```

**New way** (explicit - optional):
```
\Decl x;
x \gets 5;
```

Both work. Use `\Decl` when you want:
- Explicit declaration
- Clearer code structure
- Type from provider (not inference)
- Forward declarations

---

## Type Provider Integration

The `\Decl` keyword works seamlessly with the type provider:

```python
# In frontend or backend
hints = {
    'x': 'int',
    's': 'set',
    'arr': 'array',
    'count': 'int'
}

def type_provider(var, allowed):
    return hints.get(var)
```

When parsing:
```
\Decl x;    → ask_type("x") → type_provider("x") → "int" → int x;
\Decl s;    → ask_type("s") → type_provider("s") → "set" → set<int> s;
```

---

## Error Handling

### Undeclared Type
If a variable is declared but type provider doesn't have it:
```
\Decl unknown_var;

Error: MissingTypeError: unknown_var
```

**Fix**: Add to type hints:
```python
hints['unknown_var'] = 'int'
```

### Already Typed Variable
If a variable is already in scope and you declare again:
```
\Decl x;        // First declaration
x \gets 5;      // Uses existing type
\Decl x;        // OK - just re-asserts type
```

**Behavior**: Uses existing type (no error)

---

## Advantages

✅ **Clear Intent** - Separate writing declaration from initialization  
✅ **Type Safety** - Type comes from provider, not inference  
✅ **Flexible** - Works with type provider system  
✅ **Optional** - Old implicit style still works  
✅ **Compatible** - No breaking changes to existing code  
✅ **Consistent** - Follows pseudo-code conventions (like \Fn, \While)  

---

## Test Coverage

All tests pass:
- ✅ Basic int declaration
- ✅ Set declaration
- ✅ Array declaration
- ✅ Mixed declarations and assignments
- ✅ Declarations in loops
- ✅ Declarations in conditionals
- ✅ Multiple independent declarations

---

## Related Features

- `\gets` - Assignment/initialization (unchanged)
- `\If` - Conditional (unchanged)
- `\While` - Loop (unchanged)
- Type Provider - Resolves types for `\Decl`

---

## Future Enhancements (Optional)

1. **Typed Declaration**: `\Decl int x;` (explicit type in pseudo-code)
2. **Multi-variable Declaration**: `\Decl x, y, z;`
3. **Initialization**: `\Decl x \gets 5;` (declaration + init in one)
4. **Array Bounds**: `\Decl arr[10];` (when array syntax implemented)

---

## Summary

The `\Decl` keyword provides a clean way to separate declaration from assignment:

- **Declaration**: `\Decl x;` (type from type provider)
- **Assignment**: `x \gets value;` (existing syntax)

Type resolution uses the existing type provider system, maintaining consistency with the rest of the converter.

All changes are **backward compatible** - existing code without `\Decl` continues to work.
