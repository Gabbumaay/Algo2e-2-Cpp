#!/usr/bin/env python3
"""
Regression test suite for set data structure implementation.
Tests all set_*.txt examples to catch regressions.
"""

import sys
import os
import json
from pathlib import Path

# Add parent dir to path
sys.path.insert(0, str(Path(__file__).parent))

from parser import parse_code, to_cpp, register_type_provider, MissingTypeError

# Setup type provider with common set variable names
SET_HINTS = {
    # Set variables (generic set maps to set<int>)
    's': 'set', 's1': 'set', 's2': 'set', 's3': 'set',
    'mySet': 'set', 'nums': 'set', 'numbers': 'set', 'values': 'set',
    'primes': 'set', 'evens': 'set', 'favorites': 'set', 'validIds': 'set',
    'scores': 'set', 'uniqueValues': 'set', 'data1': 'set', 'data2': 'set',
    
    # Typed set variables
    'intSet': 'set_int', 'floatSet': 'set_float', 'doubleSet': 'set_double',
    'charSet': 'set_char', 'stringSet': 'set_string',
    
    # Int variables
    'i': 'int', 'j': 'int', 'x': 'int', 'count': 'int', 'total': 'int', 'sum': 'int',
    'counter': 'int', 'max': 'int', 'max_val': 'int', 'min': 'int',
    'unique': 'int', 'size': 'int', 'userId': 'int', 'isValid': 'int',
    'minScore': 'int', 'maxScore': 'int', 'result': 'int',
    
    # Standard return type
    'function_return_type': 'int'
}

def make_provider():
    """Create a type provider function."""
    def provider(var, allowed):
        hint = SET_HINTS.get(var)
        if hint is None:
            from parser import MissingTypeError
            raise MissingTypeError(var)
        return hint
    return provider

def test_file(filepath, verbose=False):
    """Test a single pseudo-code file."""
    try:
        # Read file
        with open(filepath, 'r', encoding='utf-8') as f:
            code = f.read()
        
        if not code.strip():
            return "SKIP", "Empty file"
        
        # Register provider
        register_type_provider(make_provider())
        
        # Parse and generate
        parsed = parse_code(code)
        cpp = to_cpp(parsed)
        
        # Validation checks
        checks = []
        
        # Check 1: Has include guards
        if '#include <bits/stdc++.h>' in cpp:
            checks.append(("includes", True))
        else:
            checks.append(("includes", False))
        
        # Check 2: Has main function
        if 'int main()' in cpp:
            checks.append(("main", True))
        else:
            checks.append(("main", False))
        
        # Check 3: No bare "set " declarations (should be "set<int>")
        if ' set ' in cpp and 'set<' not in cpp:
            checks.append(("set_template", False))
        else:
            checks.append(("set_template", True))
        
        # Check 4: No bare "vector " declarations (should be "vector<int>")
        if ' vector ' in cpp and 'vector<' not in cpp:
            checks.append(("vector_template", False))
        else:
            checks.append(("vector_template", True))
        
        # Check 5: Proper C++ syntax (basic check)
        has_syntax_errors = cpp.count('{') != cpp.count('}')
        checks.append(("syntax_balance", not has_syntax_errors))
        
        all_passed = all(check[1] for check in checks)
        
        if verbose:
            print(f"  Checks: {checks}")
            print(f"  C++ Preview:\n{chr(10).join('    ' + line for line in cpp.split(chr(10))[:10])}")
            if len(cpp.split('\n')) > 10:
                print("    ...")
        
        if all_passed:
            return "PASS", None
        else:
            failed = [c[0] for c in checks if not c[1]]
            return "WARN", f"Failed checks: {', '.join(failed)}"
        
    except MissingTypeError as e:
        return "FAIL", f"Missing type for: {e}"
    except SyntaxError as e:
        return "FAIL", str(e)
    except Exception as e:
        return "FAIL", f"{type(e).__name__}: {e}"

def main():
    test_dir = Path(__file__).parent / 'test'
    
    # Find all set_*.txt and decl_*.txt files
    test_files = sorted(list(test_dir.glob('set_*.txt')) + list(test_dir.glob('decl_*.txt')))
    
    if not test_files:
        print("No test files found!")
        return 1
    
    print("="*70)
    print("SET DATA STRUCTURE REGRESSION TEST SUITE")
    print("="*70)
    print(f"\nFound {len(test_files)} test file(s)\n")
    
    results = {}
    passed = 0
    warned = 0
    failed = 0
    
    verbose = '--verbose' in sys.argv or '-v' in sys.argv
    
    for filepath in test_files:
        status, message = test_file(filepath, verbose=verbose)
        results[filepath.name] = (status, message)
        
        status_symbol = {
            "PASS": "[OK]",
            "WARN": "[!]",
            "FAIL": "[X]",
            "SKIP": "[~]"
        }.get(status, "[ ]")
        
        print(f"{status_symbol} {filepath.name}", end="")
        
        if message:
            print(f" - {message}")
        else:
            print()
        
        if status == "PASS":
            passed += 1
        elif status == "WARN":
            warned += 1
        elif status == "FAIL":
            failed += 1
    
    print("\n" + "="*70)
    print(f"RESULTS: {passed} passed, {warned} warned, {failed} failed")
    print("="*70)
    
    return 0 if failed == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
