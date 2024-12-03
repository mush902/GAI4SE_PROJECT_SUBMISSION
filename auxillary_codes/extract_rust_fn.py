import os
import re
import subprocess


def extract_rust_function_definitions(rust_file_path):
    """
    Extract complete function definitions from a Rust source file.
    Returns a dictionary with function names as keys and their definitions as values.
    """
    function_definitions = {}

    with open(rust_file_path, 'r') as file:
        lines = file.readlines()

    for i, line in enumerate(lines):
        # Modified to include main() function
        if "fn " in line and line.strip().endswith("{"):  # Look for lines containing 'fn'
            start_line = i
            function_def = extract_function(lines, start_line)
            if function_def:
                function_name = extract_function_name(line)
                if function_name:
                    print(f'function name is {function_name}')
                    function_definitions[function_name] = function_def

    return function_definitions


def extract_function(lines, start_line):
    """
    Extract a complete function definition starting from the given line index.
    Uses brace matching to find the end of the function.
    """
    function_body = []
    brace_count = 0
    in_function = False

    for line in lines[start_line:]:
        function_body.append(line)
        if '{' in line:
            brace_count += line.count('{')
            in_function = True
        if '}' in line and in_function:
            brace_count -= line.count('}')
            if brace_count == 0:
                break

    if brace_count == 0 and in_function:
        return ''.join(function_body)
    return None


def extract_function_name(line):
    """
    Extract the function name from a line containing 'fn'.
    Handles generics and type constraints correctly.
    """
    match = re.search(r'fn\s+([a-zA-Z_][a-zA-Z0-9_]*)', line)
    if match:
        return match.group(1)
    return None


def extract_ir_for_functions(ir_file_path, function_names):
    """
    Extract LLVM IR for specific functions from the IR file.
    Returns a dictionary mapping function names to their IR.
    """
    ir_dict = {}
    current_function = None
    current_ir = []

    with open(ir_file_path, 'r') as file:
        lines = file.readlines()

    for line in lines:
        # Look for function definitions in IR
        define_match = re.search(r'define\s+(?:.*?\s+)?@([a-zA-Z0-9_]+)\s*\(', line)

        if define_match:
            print(f'printing define_match {define_match}')
            if current_function and current_ir:
                ir_dict[current_function] = ''.join(current_ir)
                current_ir = []

            ir_func_name = define_match.group(1)
            print(f'printing ir_func_name {ir_func_name}')
            found_function = None

            for rust_func in function_names:
                if rust_func in ir_func_name:
                    found_function = rust_func
                    break

            current_function = found_function
            if current_function:
                current_ir.append(line)

        elif current_function and line.strip():
            current_ir.append(line)
            if line.strip() == '}':
                ir_dict[current_function] = ''.join(current_ir)
                current_function = None
                current_ir = []

    return ir_dict



import os

def write_files_for_functions(rust_file_path, ir_file_path, function_definitions, ir_dict):
    """
    Write separate files for each function's Rust definition and IR.
    Ensures main and main_0 are written to the same numbered files.
    """
    base_name = os.path.splitext(rust_file_path)[0]
    
    # Sort function definitions by function name
    sorted_function_names = sorted(function_definitions.keys())
    
    # Create a mapping to ensure main and main_0 get the same file number
    file_number_map = {}
    current_idx = 1
    
    # First, assign numbers to main and main_0 if they exist
    if 'main' in function_definitions or 'main_0' in function_definitions:
        if 'main' in function_definitions:
            file_number_map['main'] = current_idx
        if 'main_0' in function_definitions:
            file_number_map['main_0'] = current_idx
        current_idx += 1
    
    # Then assign numbers to remaining functions
    for func_name in sorted_function_names:
        if func_name not in file_number_map:
            file_number_map[func_name] = current_idx
            current_idx += 1

    # Write the files using the mapping
    for func_name in sorted_function_names:
        func_def = function_definitions[func_name]
        file_idx = file_number_map[func_name]
        
        # File names for Rust and IR
        rust_func_file = f"{base_name}_{file_idx}.rs"
        ir_func_file = f"{base_name}_{file_idx}.ll"

        # For main/main_0, append to existing file if it exists
        if func_name in ['main', 'main_0'] and os.path.exists(rust_func_file):
            mode = 'a'  # append mode
        else:
            mode = 'w'  # write mode

        # Write Rust function definition
        with open(rust_func_file, mode) as rust_file:
            rust_file.write(func_def)

        # Write IR definition (if exists)
        ir_code = ir_dict.get(func_name, "")
        if ir_code:
            if func_name in ['main', 'main_0'] and os.path.exists(ir_func_file):
                mode = 'a'  # append mode
            else:
                mode = 'w'  # write mode
                
            with open(ir_func_file, mode) as ir_file:
                ir_file.write(ir_code)


def main():
    rust_file_path = 'train353.rs'
    ir_file_path = 'train353.ll'

    # Step 1: Extract function definitions from the Rust file
    function_definitions = extract_rust_function_definitions(rust_file_path)

    # Step 2: Extract IR for the functions
    ir_dict = extract_ir_for_functions(ir_file_path, function_definitions.keys())

    # Step 3: Write separate files for each function
    write_files_for_functions(rust_file_path, ir_file_path, function_definitions, ir_dict)


if __name__ == "__main__":
    main()