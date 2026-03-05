# Quick Test Guide - Set Data Structure

## Test Files Created

The following test files are ready to use in the **`test/`** directory:

1. **set_example_simple.txt** - Basic set with one variable and duplicates
2. **set_example_multiple.txt** - Two independent sets in same function
3. **set_example_loop.txt** - Set combined with while loop
4. **set_example_conditional.txt** - Set with if statement
5. **set_example_duplicates.txt** - Set demonstrating duplicate handling
6. **set_example_mixed_types.txt** - Mix of set, array, and int types
7. **set_example_complex.txt** - Complex logic with nested conditionals
8. **set_example_multifunc.txt** - Multiple functions with separate sets

---

## How to Test via Web UI

### Setup
1. Make sure both servers are running:
   - Backend: `python server.py` (port 5000)
   - Frontend: `npm start` in frontend folder (port 3000)

2. Open browser: `http://localhost:3000`

### Test Procedure

**For each test file:**

1. **Open the file** from `test/` folder
2. **Copy all the pseudo-code** (the \Fn...}  block)
3. **Paste into the left text area** in the web UI
4. **Click somewhere to trigger type prompt** or look for a "Convert" button
5. **When asked for types:**
   - For `set` variables (like `mySet`, `nums`, `primes`, `evens`, etc.), select **"set"**
   - For `int` variables (like `count`, `total`, `sum`, etc.), select **"int"**
   - For `array` variables (like `allValues[...]`), select **"array"**
   - For return type, select **"int"**

6. **Verify the generated C++ code** on the right side shows:
   - `set<int> varname;` for set declarations
   - `varname.insert(value);` for set assignments
   - `int varname;` for int declarations
   - `varname = value;` for int assignments

---

## Expected Results

### Test 1: Simple Set
**Input**: `mySet` gets values 5, 10, 5, 15

**Expected Output**:
```cpp
set<int> mySet;
mySet.insert(5);
mySet.insert(10);
mySet.insert(5);      // Duplicate preserved in code
mySet.insert(15);
```
✅ **Result**: Set declaration and all .insert() calls present

---

### Test 2: Multiple Sets
**Input**: `primes` gets 2,3,5,7 and `evens` gets 2,4,6,8

**Expected Output**:
```cpp
set<int> primes;
set<int> evens;
int total;

primes.insert(2);
primes.insert(3);
primes.insert(5);
primes.insert(7);
evens.insert(2);
evens.insert(4);
evens.insert(6);
evens.insert(8);
total = 4;
```
✅ **Result**: Each set maintains separate identity with own .insert() calls

---

### Test 3: Set with Loop
**Input**: `numbers` gets 1-5, loop accumulates with `sum`

**Expected Output**:
```cpp
set<int> numbers;
int i;
int sum;

numbers.insert(1);
numbers.insert(2);
numbers.insert(3);
numbers.insert(4);
numbers.insert(5);
i = 0;
sum = 0;
while (i < 5) {
    sum = sum + i;
    i = i + 1;
}
return sum;
```
✅ **Result**: Set variables use .insert(), other variables use = assignment

---

### Test 4: Set with Conditional
**Input**: `favorites` set, conditionals check count and max value

**Expected Output**:
```cpp
set<int> favorites;
int count;
int max;

favorites.insert(10);
favorites.insert(25);
favorites.insert(42);
count = 3;
max = 42;
if (count > 2) {
    return max;
}
return 0;
```
✅ **Result**: Set operations work inside conditional blocks

---

### Test 5: Duplicates Showcase
**Input**: `nums` with intentional duplicates (1, 2, 1, 3, 2, 4, 1)

**Expected Output**:
```cpp
set<int> nums;
int total;
int unique;

nums.insert(1);
nums.insert(2);
nums.insert(1);        // Preserved in generated code
nums.insert(3);
nums.insert(2);        // Preserved in generated code
nums.insert(4);
nums.insert(1);        // Preserved in generated code
total = 7;
unique = 4;
```
✅ **Result**: Generated code includes all inserts (C++ set naturally ignores duplicates at runtime)

---

### Test 6: Mixed Types
**Input**: `uniqueValues` (set), `allValues` (array), `counter` (int)

**Expected Output**:
```cpp
set<int> uniqueValues;
vector<int> allValues;
int counter;

uniqueValues.insert(100);
uniqueValues.insert(200);
uniqueValues.insert(300);
allValues[0] = 100;
allValues[1] = 200;
counter = 3;
```
✅ **Result**: Each type uses correct syntax (set uses .insert(), array uses [], int uses =)

---

### Test 7: Complex Logic
**Input**: `scores` set with duplicates, conditionals, multiple int variables

**Expected Output**:
```cpp
set<int> scores;
int unique;
int minScore;
int maxScore;

scores.insert(85);
scores.insert(92);
scores.insert(85);
scores.insert(78);
scores.insert(92);
scores.insert(95);
unique = 4;
minScore = 78;
maxScore = 95;
if (unique > 3) {
    return maxScore;
}
return minScore;
```
✅ **Result**: Complex logic with nested conditionals works correctly

---

### Test 8: Multiple Functions
**Input**: Two separate functions `firstFunction()` and `secondFunction()`, each with own set

**Expected Output**:
```cpp
int firstFunction() {
    set<int> data1;
    
    data1.insert(10);
    data1.insert(20);
    data1.insert(30);
    return 1;
}

int secondFunction() {
    set<int> data2;
    
    data2.insert(40);
    data2.insert(50);
    data2.insert(60);
    return 1;
}

int main() {
    firstFunction();
    secondFunction();
    return 0;
}
```
✅ **Result**: Multiple functions maintain separate scopes, each with own sets

---

## Validation Checklist

For each test, mark these as complete:

```
TEST 1 Simple Set:
[ ] Has set<int> declaration
[ ] Has .insert() calls (not = assignment)
[ ] Returns correct value
[ ] No syntax errors

TEST 2 Multiple Sets:
[ ] Both sets declared as set<int>
[ ] Each set has separate .insert() calls
[ ] Int variables use = assignment
[ ] Correct declaration order

TEST 3 Set with Loop:
[ ] Set uses .insert()
[ ] Loop variables use = assignment
[ ] While loop syntax correct
[ ] Return statement present

TEST 4 Conditional:
[ ] Set inside if block works
[ ] Declarations at function start
[ ] Multiple return paths work
[ ] Syntax is valid C++

TEST 5 Duplicates:
[ ] All insert calls present (even duplicates)
[ ] Code is valid C++ (duplicates handled at runtime)
[ ] Count matches pseudo-code inserts

TEST 6 Mixed Types:
[ ] set<int> for set variables
[ ] vector<int> for array variables
[ ] int for int variables
[ ] Correct access syntax for each

TEST 7 Complex:
[ ] Nested conditionals valid
[ ] Variables properly scoped
[ ] Return statements correct
[ ] No type conflicts

TEST 8 Multiple Functions:
[ ] Two functions with own sets
[ ] Each function declaration separate
[ ] main() calls both functions
[ ] No variable leaking between functions
```

---

## Command-Line Testing (Optional)

### Python Script Test
```python
import requests
import json

payload = {
    "code": r"\Fn simpleSet() { mySet \gets 5; mySet \gets 10; \KwRet 1; }",
    "types": {"mySet": "set", "function_return_type": "int"}
}

response = requests.post("http://localhost:5000/convert", json=payload)
print(response.json()["cpp"])
```

### cURL Test
```bash
curl -X POST http://localhost:5000/convert \
  -H "Content-Type: application/json" \
  -d '{"code":"\\Fn simpleSet(){mySet \\gets 5;\\KwRet 1;}","types":{"mySet":"set","function_return_type":"int"}}'
```

---

## Troubleshooting

**Issue**: Types not being recognized as "set"
- **Solution**: Make sure to select "set" from the dropdown, not type it manually

**Issue**: Getting "int" for set variables instead of "set<int>"
- **Solution**: Verify the type was sent to backend in the POST request

**Issue**: Assignments use `=` instead of `.insert()`
- **Solution**: Confirm the variable type is set to "set" in the types hint

**Issue**: Multiple functions not generating
- **Solution**: Ensure each function is wrapped in \Fn name() { ... }

**Issue**: Errors in generated C++
- **Solution**: Check that the pseudo-code syntax is correct (matching example files)

---

## Success Indicators

✅ All test files generate valid C++ code without errors  
✅ Set variables consistently use `set<int>` declarations  
✅ Set assignments consistently use `.insert()` method  
✅ Mixed types produce correct output for each type  
✅ Multiple functions maintain separate scopes  
✅ Conditional and loop structures work with sets  
✅ Duplicates are handled correctly (preserved in code, ignored by C++ at runtime)  

