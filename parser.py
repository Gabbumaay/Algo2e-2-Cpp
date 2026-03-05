import ply.yacc as yacc
from lexer import tokens
import sys
import importlib
import re

_if_mod = importlib.import_module("control_flow.if")
_for_mod = importlib.import_module("control_flow.for")
_while_mod = importlib.import_module("control_flow.while")
symbol_table = {}
has_return = False

valid_dtypes = [
    "int", "float", "string", "long", "char", "array", "vector",
    "set", "set_int", "set_float", "set_double", "set_char", "set_string"
]

class MissingTypeError(Exception):
    """Raised when the parser needs a datatype for a variable but none is provided.

    The intention is that higher layers (CLI, HTTP server, UI) catch this and
    ask the user for the datatype in an appropriate way (terminal prompt,
    frontend dialog, etc.).
    """


# Optional callback that external callers can register to supply types.
type_provider = None

def parse_code(code):
    """Parse pseudo-code and return AST. Reset state before parsing."""
    global symbol_table, has_return
    symbol_table = {}
    has_return = False
    return parser.parse(code)

def register_type_provider(fn):
    """Register a callback used to resolve unknown variable types.

    The callback should have the signature ``fn(var_name: str, valid: list[str])``
    and return a string from ``valid``. If it cannot provide a type it should
    raise ``MissingTypeError``.
    """

    global type_provider
    type_provider = fn
# Detect datatype automatically based on assigned value
def infer_type(value):
    if isinstance(value, int):
        return "int"
    if isinstance(value, float):
        return "float"
    if isinstance(value, str):
        if value.startswith('"') and value.endswith('"'):
            return "string"
        if value.startswith("'") and value.endswith("'"):
            return "char"
    return None


# Ask datatype from a registered provider (no direct stdin usage here).
def ask_type(var):
    if type_provider is None:
        # No provider registered – force the caller to handle this case.
        raise MissingTypeError(var)

    dtype = type_provider(var, valid_dtypes).strip()
    if dtype not in valid_dtypes:
        raise MissingTypeError(var)
    return dtype

def handle_assignment(var, value, is_expression=False):
    """Update symbol_table for an assignment and return normalized value string.

    For complex expressions we mostly fall back to asking the user for the type
    when the variable has not been seen before.

    This also ensures both the assigned variable and any source identifier
    (e.g. in "b = a") have datatypes recorded.
    
    Priority: Type provider (if registered) > Type inference (if no provider)
    """
    global symbol_table

    # If variable already has a type (from type provider or previous assignment), keep it
    if var in symbol_table:
        return str(value)

    # If a type provider is registered, ALWAYS use it (don't fall back to inference)
    # If the provider can't provide a type, let that error propagate to the frontend
    if type_provider is not None:
        symbol_table[var] = ask_type(var)  # Will raise MissingTypeError if provider doesn't have it
        return str(value)

    # Type provider not registered - use type inference for simple cases
    # Simple constants can be type-inferred
    if isinstance(value, (int, float)):
        inferred = infer_type(value)
        if inferred:
            symbol_table[var] = inferred
            return str(value)
    
    # Handle string values (identifiers or expressions)
    if isinstance(value, str):
        # If RHS is a single identifier (not an expression like "x + y")
        if not is_expression and value.isidentifier():
            # Ensure the source identifier has a type.
            if value not in symbol_table:
                symbol_table[value] = ask_type(value)

            # Propagate type from source to target variable.
            symbol_table[var] = symbol_table[value]
            return str(value)
        else:
            # For unknown or expression-based assignments, ask for var's type
            symbol_table[var] = ask_type(var)
            return str(value)

    # Fallback: ask the type provider or user
    symbol_table[var] = ask_type(var)
    return str(value)


_id_pattern = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")


def _identifiers_in_expr(expr):
    """Return a list of identifier-like names found in an expression string."""
    if not isinstance(expr, str):
        return []
    return _id_pattern.findall(expr)


# -------- Grammar Rules --------

def p_program(p):
    """program : function_list"""
    p[0] = p[1]


def p_function_list(p):
    """function_list : function_list function
                     | function"""
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]


def p_function_header(p):
    """function_header : FN ID LPAREN param_list_opt RPAREN"""
    global symbol_table, has_return

    # Start a fresh scope for each function while parsing its body.
    symbol_table = {}
    has_return = False
    p[0] = {"name": p[2], "params": p[4] or []}

def p_function(p):
    """function : function_header LBRACE stmt_list RBRACE"""
    global has_return, symbol_table

    fn_info = p[1]

    # Get return type from symbol table or default to void
    if has_return and "__return_type__" in symbol_table:
        ret_type = symbol_table.pop("__return_type__")  # Remove special key
    else:
        ret_type = "void"

    params = fn_info["params"]

    # Ensure parameter types are known at parse time
    for param in params:
        if param not in symbol_table:
            symbol_table[param] = ask_type(param)

    function_symbols = dict(symbol_table)

    p[0] = {
        "type": "function",
        "name": fn_info["name"],
        "params": params,
        "body": p[3],
        "return_type": ret_type,
        "symbols": function_symbols,
    }

    # Reset parse state for safety before the next function.
    symbol_table = {}
    has_return = False
def p_param_list_opt(p):
    """param_list_opt : param_list
                      | empty"""
    if p[1] is None:
        p[0] = []
    else:
        p[0] = p[1]


def p_param_list(p):
    """param_list : ID
                  | param_list COMMA ID"""
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]


def p_stmt_list(p):
    """stmt_list : stmt_list statement
                 | statement
                 | empty"""
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    elif p[1] is None:
        p[0] = []
    else:
        p[0] = [p[1]]


def p_statement_assign_simple(p):
    """statement : ID ASSIGN NUMBER SEMICOLON
                 | ID ASSIGN ID SEMICOLON"""
    var = p[1]
    val = p[3]
    normalized = handle_assignment(var, val, is_expression=False)
    p[0] = {"type": "assign", "var": var, "value": normalized}


def p_statement_assign_expr(p):
    """statement : ID ASSIGN expression SEMICOLON"""
    var = p[1]
    val = p[3]
    normalized = handle_assignment(var, val, is_expression=True)
    p[0] = {"type": "assign", "var": var, "value": normalized}


def p_statement_declare(p):
    """statement : DECL ID SEMICOLON"""
    var = p[2]
    
    # If variable not yet typed, ask the type provider
    if var not in symbol_table:
        symbol_table[var] = ask_type(var)
    
    # Declare-only statement: no initialization
    p[0] = {"type": "declare", "var": var}


def p_statement_if(p):
    """statement : IF LPAREN condition RPAREN LBRACE stmt_list RBRACE"""
    p[0] = {"type": "if", "condition": p[3], "body": p[6]}


def p_statement_while(p):
    """statement : WHILE LPAREN condition RPAREN LBRACE stmt_list RBRACE"""
    p[0] = {"type": "while", "condition": p[3], "body": p[6]}


def p_statement_for(p):
    """statement : FOR LPAREN for_init_opt SEMICOLON condition_opt SEMICOLON for_update_opt RPAREN LBRACE stmt_list RBRACE"""
    p[0] = {
        "type": "for",
        "init": p[3],
        "condition": p[5],
        "update": p[7],
        "body": p[10],
    }


def p_for_init_opt(p):
    """for_init_opt : ID ASSIGN NUMBER
                     | ID ASSIGN ID
                     | ID ASSIGN expression
                     | empty"""
    if len(p) == 1 or p[1] is None:
        p[0] = None
        return

    var = p[1]
    val = p[3]
    is_expr = not isinstance(val, (int, float)) and not (isinstance(val, str) and val.isidentifier())
    normalized = handle_assignment(var, val, is_expression=is_expr)
    p[0] = {"type": "assign", "var": var, "value": normalized}


def p_condition_opt(p):
    """condition_opt : condition
                      | empty"""
    p[0] = p[1]


def p_for_update_opt(p):
    """for_update_opt : ID ASSIGN NUMBER
                       | ID ASSIGN ID
                       | ID ASSIGN expression
                       | empty"""
    if len(p) == 1 or p[1] is None:
        p[0] = None
        return

    var = p[1]
    val = p[3]
    # Update should never redeclare the type, but should still track it
    is_expr = not isinstance(val, (int, float)) and not (isinstance(val, str) and val.isidentifier())
    normalized = handle_assignment(var, val, is_expression=is_expr)
    p[0] = {"type": "assign", "var": var, "value": normalized}


def p_statement_return(p):
    """statement : RETURN expression SEMICOLON
                 | RETURN NUMBER SEMICOLON
                 | RETURN ID SEMICOLON"""
    global has_return
    has_return = True
    
    ret_val = p[2]
    
    # Always ask for return type - no inference
    if "__return_type__" not in symbol_table:
        symbol_table["__return_type__"] = ask_type("function_return_type")
    
    p[0] = {"type": "return", "value": ret_val}

def p_statement_function_call(p):
    """statement : ID LPAREN argument_list_opt RPAREN SEMICOLON"""
    func_name = p[1]
    args = p[3] or []
    
    # Ensure all argument identifiers have types
    for arg in args:
        if isinstance(arg, str) and arg.isidentifier() and arg not in symbol_table:
            symbol_table[arg] = ask_type(arg)
    
    args_str = ", ".join(str(arg) for arg in args)
    p[0] = {"type": "function_call", "name": func_name, "args": args_str}


def p_expression_binop_addsub(p):
    """expression : expression PLUS term
                  | expression MINUS term"""
    p[0] = f"{p[1]} {p[2]} {p[3]}"


def p_expression_term(p):
    """expression : term"""
    p[0] = p[1]


def p_term_binop(p):
    """term : term TIMES factor
             | term DIVIDE factor
             | term MOD factor"""
    p[0] = f"{p[1]} {p[2]} {p[3]}"


def p_term_factor(p):
    """term : factor"""
    p[0] = p[1]


def p_factor_number(p):
    """factor : NUMBER"""
    p[0] = str(p[1])


def p_factor_string(p):
    """factor : STRING"""
    # STRING tokens have quotes already removed by lexer
    # Re-add quotes for C++ output
    p[0] = f'"{p[1]}"'


def p_factor_char(p):
    """factor : CHAR"""
    # CHAR tokens have quotes already removed by lexer
    # Re-add single quotes for C++ output
    p[0] = f"'{p[1]}'"


def p_factor_id(p):
    """factor : ID"""
    var = p[1]
    # Ensure any identifier used in an expression has a datatype.
    if var not in symbol_table:
        symbol_table[var] = ask_type(var)
    p[0] = var


def p_factor_group(p):
    """factor : LPAREN expression RPAREN"""
    p[0] = f"({p[2]})"


def p_condition(p):
    """condition : expression LT expression
                 | expression GT expression
                 | expression LE expression
                 | expression GE expression
                 | expression EQ expression
                 | expression NE expression"""
    p[0] = f"{p[1]} {p[2]} {p[3]}"


def p_empty(p):
    """empty :"""
    p[0] = None


def p_error(p):
    """PLY error handler.

    We raise an exception instead of exiting so that callers (CLI or server)
    can decide how to surface the error.
    """
    if p:
        raise SyntaxError(f"Syntax error near '{p.value}'")
    raise SyntaxError("Syntax error at EOF")

def p_factor_function_call(p):
    """factor : ID LPAREN argument_list_opt RPAREN"""
    func_name = p[1]
    args = p[3] or []
    
    # Ensure all argument identifiers have types
    for arg in args:
        if isinstance(arg, str) and arg.isidentifier() and arg not in symbol_table:
            symbol_table[arg] = ask_type(arg)
    
    # Format as C++ function call
    args_str = ", ".join(str(arg) for arg in args)
    p[0] = f"{func_name}({args_str})"


def p_argument_list_opt(p):
    """argument_list_opt : argument_list
                         | empty"""
    p[0] = p[1] if p[1] is not None else []


def p_argument_list(p):
    """argument_list : argument
                     | argument_list COMMA argument"""
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]


def p_argument(p):
    """argument : expression"""
    p[0] = p[1]

# -------- C++ Code Generation --------

def _get_cpp_type(dtype):
    """Convert pseudo-code type to proper C++ type string.
    
    Handles: set -> set<int>, array -> vector, and typed sets.
    """
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
    elif dtype == "array":
        return "vector<int>"  # array maps to vector
    else:
        return dtype  # int, float, string, etc. stay as-is


def _format_for_assignment(assign_node, include_type=True, var_dtype=None):
    """Format an assignment node as a C++ snippet without redeclaration.

    For set types with scalar values, generates var.insert(value).
    For set-to-set copies or complex expressions, uses var = value.
    For regular types, always uses var = value.
    """
    var = assign_node["var"]
    value = assign_node["value"]
    
    # Check if this is any kind of set type
    is_set_type = var_dtype in ["set", "set_int", "set_float", "set_double", "set_char", "set_string"]
    
    # Only use .insert() for set types when assigning scalar literals
    if is_set_type:
        # Check if value is a simple literal (number, char, or string)
        # vs an identifier or complex expression
        value_str = str(value)
        
        # Simple scalars: numbers, char literals 'x', string literals "text"
        is_simple_literal = False
        
        # Check for numeric literal (int or float)
        try:
            float(value_str)
            is_simple_literal = True
        except (ValueError, TypeError):
            pass
        
        # Check for char literal 'x'
        if value_str.startswith("'") and value_str.endswith("'") and len(value_str) == 3:
            is_simple_literal = True
        
        # Check for string literal "text"
        if value_str.startswith('"') and value_str.endswith('"'):
            is_simple_literal = True
        
        if is_simple_literal:
            return f"{var}.insert({value})"
        else:
            # For non-literal values (identifiers, expressions), use assignment
            # This handles set-to-set copies and function returns correctly
            return f"{var} = {value}"
    
    # For regular types, use assignment
    return f"{var} = {value}"


def generate_cpp(parsed, indent=0, declared=None):
    """Generate C++ code from parsed AST with proper declaration handling."""
    cpp = ""
    if declared is None:
        declared = set()
    space = " " * (indent * 4)

    for stmt in parsed:
        stype = stmt["type"]

        if stype == "function":
            params = stmt.get("params", [])
            fn_symbols = stmt.get("symbols", {})

            # Build parameter signature with types
            param_parts = []
            for param in params:
                dtype = fn_symbols.get(param, "")
                if not dtype:
                    dtype = ask_type(param)
                    fn_symbols[param] = dtype
                cpp_type = _get_cpp_type(dtype)  # Map pseudo type to C++
                param_parts.append(f"{cpp_type} {param}")
            param_sig = ", ".join(param_parts)

            # Map return type to C++
            ret_cpp_type = _get_cpp_type(stmt['return_type'])
            cpp += f"{ret_cpp_type} {stmt['name']}({param_sig}) {{\n"

            # Parameters are pre-declared, mark them as dict with types
            func_declared = {param: fn_symbols.get(param, "int") for param in params}
            
            # Collect ALL variables that need declaration (excluding parameters)
            vars_to_declare = []
            for var, dtype in fn_symbols.items():
                if var.startswith("__"):
                    continue
                if var not in func_declared and dtype:
                    vars_to_declare.append((var, dtype))
                    func_declared[var] = dtype
            
            # Emit all variable declarations at the top of function
            if vars_to_declare:
                for var, dtype in vars_to_declare:
                    cpp_type = _get_cpp_type(dtype)
                    cpp += " " * ((indent + 1) * 4) + f"{cpp_type} {var};\n"
                # Add blank line after declarations for readability
                cpp += "\n"
            
            # Generate function body (no more declarations will happen)
            cpp += generate_cpp(stmt["body"], indent + 1, declared=func_declared)
            cpp += "}\n\n"

        elif stype == "assign":
            # Assignment - check if variable is a set type
            var = stmt.get("var")
            # Get dtype from declared dict (func_declared)
            var_dtype = declared.get(var) if isinstance(declared, dict) else None
            # Try to get dtype from function symbols if not in declared
            if not var_dtype and var in symbol_table:
                var_dtype = symbol_table.get(var)
            cpp += space + _format_for_assignment(stmt, include_type=False, var_dtype=var_dtype) + ";\n"

        elif stype == "declare":
            # Declaration-only statement: no code generation needed
            # (variable was already registered in symbol_table during parsing)
            pass

        elif stype == "if":
            def _gen_if(body, ind):
                return generate_cpp(body, ind, declared=declared)
            cpp += _if_mod.generate_if_cpp(stmt, indent, _gen_if)

        elif stype == "while":
            def _gen_while(body, ind):
                return generate_cpp(body, ind, declared=declared)
            cpp += _while_mod.generate_while_cpp(stmt, indent, _gen_while)

        elif stype == "for":
            def _gen_for(body, ind):
                return generate_cpp(body, ind, declared=declared)
            # Create wrapper for _format_for_assignment that includes dtype info
            def format_assign_with_type(assign_node, include_type=True):
                var = assign_node.get("var")
                # Use declared dict (function scope) instead of global symbol_table
                var_dtype = declared.get(var) if isinstance(declared, dict) else None
                return _format_for_assignment(assign_node, include_type, var_dtype)
            cpp += _for_mod.generate_for_cpp(
                stmt,
                indent,
                format_assign_with_type,
                _gen_for,
            )
        elif stype == "function_call":
            cpp += space + f"{stmt['name']}({stmt['args']});\n"
            
        elif stype == "return":
            cpp += space + f"return {stmt['value']};\n"

    return cpp

def to_cpp(parsed):
    """Generate complete C++ program from parsed AST."""
    header = "#include <bits/stdc++.h>\nusing namespace std;\n\n"
    body = generate_cpp(parsed)

    # If user already defined main, don't emit another entry point.
    has_main = any(fn.get("name") == "main" for fn in parsed if fn.get("type") == "function")
    if has_main:
        return header + body

    callable_target = None
    for fn in parsed:
        if fn.get("type") == "function" and not fn.get("params"):
            callable_target = fn["name"]
            break

    main_lines = ["int main() {"]
    if callable_target:
        main_lines.append(f"    {callable_target}();")
    main_lines.append("    return 0;")
    main_lines.append("}")
    main = "\n".join(main_lines) + "\n"
    return header + body + main

parser = yacc.yacc()
