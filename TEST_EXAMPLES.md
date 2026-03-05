# Set Data Structure - Test Examples

Copy any of these pseudo-code examples into the web UI. When prompted for types, select "set" for the set variables.

---

## Example 1: Simple Set Insertion
**Purpose**: Basic set operations with duplicate handling

```
\Fn simpleSet() {
    mySet \gets 5;
    mySet \gets 10;
    mySet \gets 5;
    mySet \gets 15;
    \KwRet 1;
}
```

**Expected C++ Output**:
```cpp
set<int> mySet;
mySet.insert(5);
mySet.insert(10);
mySet.insert(5);      // Duplicate, set will ignore
mySet.insert(15);
```

**When Prompted**: Select "set" for `mySet`

---

## Example 2: Multiple Sets with Different Values
**Purpose**: Multiple independent sets in one function

```
\Fn multipleSetExample() {
    primes \gets 2;
    primes \gets 3;
    primes \gets 5;
    primes \gets 7;
    evens \gets 2;
    evens \gets 4;
    evens \gets 6;
    evens \gets 8;
    total \gets 8;
    \KwRet total;
}
```

**Expected C++ Output**:
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
total = 8;
```

**When Prompted**: Select "set" for both `primes` and `evens`

---

## Example 3: Set with Loop
**Purpose**: Combining sets with control flow

```
\Fn setWithLoop() {
    numbers \gets 1;
    numbers \gets 2;
    numbers \gets 3;
    numbers \gets 4;
    numbers \gets 5;
    i \gets 0;
    sum \gets 0;
    \While (i < 5) {
        sum \gets sum + i;
        i \gets i + 1;
    }
    \KwRet sum;
}
```

**Expected C++ Output**:
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

**When Prompted**: Select "set" for `numbers`

---

## Example 4: Set with Conditional
**Purpose**: Sets with if statements

```
\Fn setWithConditional() {
    favorites \gets 10;
    favorites \gets 25;
    favorites \gets 42;
    count \gets 3;
    max \gets 42;
    \If (count > 2) {
        \KwRet max;
    }
    \KwRet 0;
}
```

**Expected C++ Output**:
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

**When Prompted**: Select "set" for `favorites`

---

## Example 5: Complex Scenario - Processing Unique Values
**Purpose**: Realistic use case with mixed operations

```
\Fn findUnique() {
    scores \gets 85;
    scores \gets 92;
    scores \gets 85;
    scores \gets 78;
    scores \gets 92;
    scores \gets 95;
    unique \gets 4;
    minScore \gets 78;
    maxScore \gets 95;
    \If (unique > 3) {
        \KwRet maxScore;
    }
    \KwRet minScore;
}
```

**Expected C++ Output**:
```cpp
set<int> scores;
int unique;
int minScore;
int maxScore;

scores.insert(85);
scores.insert(92);
scores.insert(85);        // Duplicate
scores.insert(78);
scores.insert(92);        // Duplicate
scores.insert(95);
unique = 4;
minScore = 78;
maxScore = 95;
if (unique > 3) {
    return maxScore;
}
return minScore;
```

**When Prompted**: Select "set" for `scores`

---

## Example 6: Three Different Data Types
**Purpose**: Mix set, array, and int types

```
\Fn mixedDataTypes() {
    uniqueValues \gets 100;
    uniqueValues \gets 200;
    uniqueValues \gets 300;
    allValues[0] \gets 100;
    allValues[1] \gets 200;
    counter \gets 3;
    \KwRet counter;
}
```

**Expected C++ Output**:
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
return counter;
```

**When Prompted**: 
- Select "set" for `uniqueValues`
- Select "array" for `allValues`
- Select "int" for `counter`

---

## Example 7: Multiple Functions Using Sets
**Purpose**: Verify function scope isolation with sets

```
\Fn firstFunction() {
    data1 \gets 10;
    data1 \gets 20;
    \KwRet 1;
}

\Fn secondFunction() {
    data2 \gets 30;
    data2 \gets 40;
    \KwRet 1;
}
```

**Expected C++ Output**:
```cpp
int firstFunction() {
    set<int> data1;
    
    data1.insert(10);
    data1.insert(20);
    return 1;
}

int secondFunction() {
    set<int> data2;
    
    data2.insert(30);
    data2.insert(40);
    return 1;
}

int main() {
    firstFunction();
    secondFunction();
    return 0;
}
```

**When Prompted**: Select "set" for both `data1` and `data2`

---

## Example 8: Duplicate Handling Showcase
**Purpose**: Demonstrate that duplicates are automatically removed by C++ set

```
\Fn duplicates() {
    nums \gets 1;
    nums \gets 2;
    nums \gets 1;
    nums \gets 3;
    nums \gets 2;
    nums \gets 4;
    nums \gets 1;
    total \gets 7;
    unique \gets 4;
    \KwRet unique;
}
```

**Expected C++ Output**:
```cpp
set<int> nums;
int total;
int unique;

nums.insert(1);
nums.insert(2);
nums.insert(1);        // Ignored by set
nums.insert(3);
nums.insert(2);        // Ignored by set
nums.insert(4);
nums.insert(1);        // Ignored by set
total = 7;
unique = 4;
return unique;
```

**At runtime in C++**, the set will contain: `{1, 2, 3, 4}` (sorted, duplicates removed)

**When Prompted**: Select "set" for `nums`

---

## Example 9: Set in Loop with Accumulation
**Purpose**: Complex control flow with sets

```
\Fn setInLoop() {
    values \gets 10;
    values \gets 20;
    values \gets 30;
    counter \gets 0;
    result \gets 0;
    \While (counter < 3) {
        result \gets result + 10;
        counter \gets counter + 1;
    }
    \KwRet result;
}
```

**Expected C++ Output**:
```cpp
set<int> values;
int counter;
int result;

values.insert(10);
values.insert(20);
values.insert(30);
counter = 0;
result = 0;
while (counter < 3) {
    result = result + 10;
    counter = counter + 1;
}
return result;
```

**When Prompted**: Select "set" for `values`

---

## Example 10: Advanced - Nested Conditionals with Sets
**Purpose**: Multiple levels of control flow

```
\Fn advancedLogic() {
    validIds \gets 101;
    validIds \gets 102;
    validIds \gets 103;
    userId \gets 102;
    isValid \gets 1;
    \If (isValid) {
        \If (userId > 100) {
            \KwRet 1;
        }
    }
    \KwRet 0;
}
```

**Expected C++ Output**:
```cpp
set<int> validIds;
int userId;
int isValid;

validIds.insert(101);
validIds.insert(102);
validIds.insert(103);
userId = 102;
isValid = 1;
if (isValid) {
    if (userId > 100) {
        return 1;
    }
}
return 0;
```

**When Prompted**: Select "set" for `validIds`

---

## How to Test

### Option 1: Web UI Testing
1. Open browser to `http://localhost:3000`
2. Copy one of the examples above (the pseudo-code block)
3. Paste into the left text area
4. A dialog appears asking for variable types
5. For each set variable, select **"set"** from the dropdown
6. Click "Convert"
7. Check the right side for generated C++ code
8. Verify it shows `set<int> varname;` and `varname.insert(value);`

### Option 2: API Testing (cURL)
```bash
curl -X POST http://localhost:5000/convert \
  -H "Content-Type: application/json" \
  -d '{
    "code": "\\Fn test() { nums \\gets 10; nums \\gets 20; \\KwRet 1; }",
    "types": {"nums": "set", "function_return_type": "int"}
  }'
```

### Option 3: Python API Testing
```python
import requests
import json

payload = {
    "code": r"\Fn test() { nums \gets 10; nums \gets 20; \KwRet 1; }",
    "types": {"nums": "set", "function_return_type": "int"}
}

response = requests.post("http://localhost:5000/convert", json=payload)
print(json.dumps(response.json(), indent=2))
```

---

## Validation Checklist

For each test, verify:

- [ ] Set variables declare as `set<int> varname;`
- [ ] Set assignments use `varname.insert(value);`
- [ ] Regular variables stay as `int varname;`
- [ ] Regular assignments use `varname = value;`
- [ ] Multiple sets maintain separate identities
- [ ] Duplicates in insert calls are preserved in pseudo-code (C++ set will ignore duplicates at runtime)
- [ ] No syntax errors in generated C++
- [ ] Functions have correct scope isolation
- [ ] Return statements are correct
- [ ] Loops and conditionals work with sets

---

## Success Criteria

✅ All examples compile without errors in C++  
✅ Set variables show `set<int>` in declarations  
✅ Set assignments show `.insert()` method calls  
✅ Mixed types (set + int + array) work correctly  
✅ No type conflicts or warnings last command  
✅ Multiple functions maintain separate set scopes  

