# Typed Sets Implementation

## Overview

The converter now supports **typed sets** with full C++ template mapping. You can specify the element type of a set, and it generates the correct `set<T>` declaration.

## Supported Set Types

| Type | C++ Output | Example Values |
|------|-----------|-----------------|
| `set_int` | `set<int>` | 1, 5, 10 |
| `set_float` | `set<float>` | 1.5, 3.2, 7.8 |
| `set_double` | `set<double>` | 2.5, 4.7, 9.2 |
| `set_char` | `set<char>` | 'a', 'b', 'c' |
| `set_string` | `set<string>` | "apple", "banana", "mango" |
| `set` (legacy) | `set<int>` | 1, 5, 10 |

> **Note**: The legacy `set` type still works and defaults to `set<int>` for backward compatibility.

## Usage

### Type Provider Configuration

When using the converter (via API or UI), provide type hints for set variables:

```json
{
  "intSet": "set_int",
  "floatSet": "set_float",
  "charSet": "set_char",
  "stringSet": "set_string"
}
```

### Pseudo-Code Examples

#### Integer Set
```
\Fn intSetExample() {
    \Decl numbers;
    numbers \gets 1;
    numbers \gets 5;
    numbers \gets 10;
    \KwRet 1;
}
```

**Type hint**: `numbers: set_int`

**Generated C++**:
```cpp
int intSetExample() {
    set<int> numbers;

    numbers.insert(1);
    numbers.insert(5);
    numbers.insert(10);
    return 1;
}
```

#### Float Set
```
\Fn floatSetExample() {
    \Decl temperatures;
    temperatures \gets 23.5;
    temperatures \gets 24.8;
    temperatures \gets 22.1;
    \KwRet 1;
}
```

**Type hint**: `temperatures: set_float`

**Generated C++**:
```cpp
int floatSetExample() {
    set<float> temperatures;

    temperatures.insert(23.5);
    temperatures.insert(24.8);
    temperatures.insert(22.1);
    return 1;
}
```

#### Character Set
```
\Fn charSetExample() {
    \Decl vowels;
    vowels \gets 'a';
    vowels \gets 'e';
    vowels \gets 'i';
    vowels \gets 'o';
    vowels \gets 'u';
    \KwRet 1;
}
```

**Type hint**: `vowels: set_char`

**Generated C++**:
```cpp
int charSetExample() {
    set<char> vowels;

    vowels.insert('a');
    vowels.insert('e');
    vowels.insert('i');
    vowels.insert('o');
    vowels.insert('u');
    return 1;
}
```

#### String Set
```
\Fn stringSetExample() {
    \Decl fruits;
    fruits \gets "apple";
    fruits \gets "banana";
    fruits \gets "mango";
    \KwRet 1;
}
```

**Type hint**: `fruits: set_string`

**Generated C++**:
```cpp
int stringSetExample() {
    set<string> fruits;

    fruits.insert("apple");
    fruits.insert("banana");
    fruits.insert("mango");
    return 1;
}
```

#### Double Set
```
\Fn doubleSetExample() {
    \Decl measurements;
    measurements \gets 3.14159;
    measurements \gets 2.71828;
    measurements \gets 1.41421;
    \KwRet 1;
}
```

**Type hint**: `measurements: set_double`

**Generated C++**:
```cpp
int doubleSetExample() {
    set<double> measurements;

    measurements.insert(3.14159);
    measurements.insert(2.71828);
    measurements.insert(1.41421);
    return 1;
}
```

## Implementation Details

### Type Mapping

The type mapping happens in `parser.py` in the `_get_cpp_type()` function:

```python
def _get_cpp_type(dtype):
    if dtype == "set" or dtype == "set_int":
        return "set<int>"
    elif dtype == "set_float":
        return "set<float>"
    elif dtype == "set_double":
        return "set<double>"
    elif dtype == "set_char":
        return "set<char>"
    elif dtype == "set_string":
        return "set<string>"
    # ... other types
```

### Smart Literal Detection

The converter intelligently detects scalar literals and uses `.insert()` for:
- **Numbers**: `1`, `1.5`, `2.71828`
- **Characters**: `'a'`, `'x'`
- **Strings**: `"apple"`, `"text"`

For identifiers and expressions, it uses assignment:
- `mySet = otherSet` (set-to-set copy)
- `mySet = getSetFromFunction()` (function return)

### Parser Support

The grammar now includes rules for:
- `STRING` tokens: `"quoted strings"`
- `CHAR` tokens: `'single characters'`
- Expression factors that handle all literal types

## Frontend Support

The React UI includes all typed set options in the type selector:

```javascript
const VALID_TYPES = [
  "int",
  "float",
  "string",
  "long",
  "char",
  "array",
  "vector",
  "set",
  "set_int",
  "set_float",
  "set_double",
  "set_char",
  "set_string",
];
```

When you don't provide a type for a set variable, the UI prompts you to select one.

## Test Coverage

All typed sets have comprehensive test coverage:

- ✅ `set_int_test.txt` - Integer sets
- ✅ `set_float_test.txt` - Float sets
- ✅ `set_double_test.txt` - Double sets
- ✅ `set_char_test.txt` - Character sets
- ✅ `set_string_test.txt` - String sets

**Regression Status**: 24/24 tests passing (100%)

## Backward Compatibility

The legacy `set` type (without explicit element type) still works and behaves as `set<int>`. This ensures existing pseudo-code continues to work without modification.

```
// Old way - still works
\Decl s;            // Type hint: s: set
s \gets 10;         // Generates: set<int> s; s.insert(10);

// New way - explicit types
\Decl s;            // Type hint: s: set_int
s \gets 10;         // Generates: set<int> s; s.insert(10);
```

## Common C++ Set Methods

The generated `set<T>` objects support standard C++ methods:

```cpp
set<int> s;

// Insert elements
s.insert(10);       // Add element
s.insert(20);

// Check membership
if (s.find(10) != s.end()) { /* found */ }

// Size
int sz = s.size();

// Iterate
for (int x : s) { /* use x */ }

// Clear
s.clear();

// Remove
s.erase(10);
```

## Advanced Examples

### Multiple Different Set Types

```
\Fn multipleSetTypes() {
    \Decl intSet;
    \Decl floatSet;
    \Decl charSet;
    
    intSet \gets 1;
    intSet \gets 2;
    
    floatSet \gets 1.5;
    floatSet \gets 2.5;
    
    charSet \gets 'x';
    charSet \gets 'y';
    
    \KwRet 1;
}
```

**Type hints**: 
- `intSet: set_int`
- `floatSet: set_float`
- `charSet: set_char`

**Generated C++**:
```cpp
int multipleSetTypes() {
    set<int> intSet;
    set<float> floatSet;
    set<char> charSet;

    intSet.insert(1);
    intSet.insert(2);
    floatSet.insert(1.5);
    floatSet.insert(2.5);
    charSet.insert('x');
    charSet.insert('y');
    return 1;
}
```

### Set in Loops

```
\Fn setInLoop() {
    \Decl numbers;
    \Decl i;
    
    i \gets 1;
    \While (i <= 5) {
        numbers \gets i;
        i \gets i + 1;
    }
    
    \KwRet 1;
}
```

**Type hints**:
- `numbers: set_int`
- `i: int`

**Generated C++**:
```cpp
int setInLoop() {
    set<int> numbers;
    int i;

    i = 1;
    while (i <= 5) {
        numbers.insert(i);
        i = i + 1;
    }
    return 1;
}
```

## Migration from `set` to Typed Sets

**Before** (generic set - defaults to int):
```
\Decl data;
data \gets 100;
```

**After** (explicit type):
```
\Decl data;        // Provide type hint: data: set_int
data \gets 100;
```

The behavior is identical - just more explicit!

## Troubleshooting

### Issue: "Invalid type for variable"
**Cause**: Type hint not provided or unrecognized type name
**Solution**: Ensure type hint uses correct format: `set_int`, `set_float`, etc.

### Issue: Generated C++ has bare `set` (not `set<int>`)
**Cause**: Legacy `set` type used without `<type>` specifier
**Solution**: Use specific type like `set_int` or `set_float`

### Issue: Compilation error about missing `<string>` include
**Cause**: Using `set_string` requires the string include
**Solution**: This is handled automatically by `#include <bits/stdc++.h>` but ensure you're using a modern C++ compiler

## Summary

Typed sets provide:
- ✅ **Clear intent**: You know exactly what type of elements are in your set
- ✅ **Type safety**: Compile-time checking in generated C++
- ✅ **Flexible**: Supports int, float, double, char, and string
- ✅ **Backward compatible**: Old `set` type still works
- ✅ **Intuitive syntax**: Uses C++ template notation (`set<T>`)
