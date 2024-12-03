
import re
import os
import subprocess
from pathlib import Path

def remove_blank_lines(text):
    """Remove blank lines from the text while preserving indentation"""
    lines = text.split('\n')
    non_blank_lines = [line for line in lines if line.strip()]
    return '\n'.join(non_blank_lines)

def extract_function_name(function_text):
    """Extract function name from C function text"""
    # Match function name pattern
    pattern = r'^[a-zA-Z_]\w*\s+([a-zA-Z_]\w*)\s*\('
    match = re.search(pattern, function_text.strip())
    if match:
        return match.group(1)
    return None

def extract_ir_function_name(ir_text):
    """Extract function name from LLVM IR function text"""
    # Match function name pattern in LLVM IR
    pattern = r'define\s+.*?\s*@([a-zA-Z_]\w*)\('
    match = re.search(pattern, ir_text.strip())
    if match:
        return match.group(1)
    return None

def extract_c_functions(file_path):
    """Extract complete function definitions from a C file"""
    try:
        with open(file_path, 'r') as file:
            content = file.read()
        
        # Remove comments
        content = re.sub(r'//.*?\n', '\n', content)
        content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
        
        functions = []
        brace_count = 0
        current_function = ""
        recording = False
        
        func_start_pattern = r'^[a-zA-Z_]\w*\s+[a-zA-Z_]\w*\s*\([^;]*\)\s*{?$'
        
        lines = content.split('\n')
        # And modify the recording logic in the function extraction loop:
        for line in lines:
            if not recording:
                if re.search(func_start_pattern, line.strip()):
                    recording = True
                    brace_count = line.count('{')  # Count braces in function signature line
                    current_function = line + '\n'
                    if brace_count > 0:
                        continue
                    
            elif recording and not brace_count and line.strip().startswith('{'):
                # Handle opening brace on its own line
                current_function += line + '\n'
                brace_count += 1
                continue
                
            elif recording:
                current_function += line + '\n'
                brace_count += line.count('{')
                brace_count -= line.count('}')
                
                if brace_count == 0 and current_function:
                    functions.append(current_function)
                    current_function = ""
                    recording = False
        
        # Return list of tuples with function number, text, and name
        return [(i+1, func, extract_function_name(func)) 
                for i, func in enumerate(functions)]
    
    except Exception as e:
        print(f"Error processing file {file_path}: {str(e)}")
        return []

def generate_and_extract_ir(c_file):
    """Generate LLVM IR for complete file and extract functions"""
    base_name = os.path.splitext(c_file)[0]
    temp_ll = f"{base_name}_temp.ll"
    temp_clean_ll = f"{base_name}_temp_clean.ll"
    
    try:
        # Generate LLVM IR
        subprocess.run(['clang', '-Oz', '-emit-llvm', '-S', c_file, '-o', temp_ll], 
                      check=True, stderr=subprocess.PIPE)
        
        # Clean and strip debug info
        subprocess.run(['opt', '-strip-debug', '-S', temp_ll, '-o', temp_clean_ll],
                      check=True, stderr=subprocess.PIPE)
        
        # Extract functions from IR
        ir_functions = []
        with open(temp_clean_ll, 'r') as f:
            content = f.read()
        
        current_function = []
        in_function = False
        
        for line in content.split('\n'):
            if line.startswith('define '):
                in_function = True
                current_function = [line]
            elif in_function:
                current_function.append(line)
                if line.strip() == '}':
                    func_text = '\n'.join(current_function)
                    func_name = extract_ir_function_name(func_text)
                    if func_name:
                        ir_functions.append((func_name, func_text))
                    in_function = False
                    current_function = []
        
        # Cleanup temporary files
        os.remove(temp_ll)
        os.remove(temp_clean_ll)
        
        return ir_functions
    
    except subprocess.CalledProcessError as e:
        print(f"Error generating LLVM IR for {c_file}: {e.stderr.decode()}")
        # Cleanup any temporary files
        for f in [temp_ll, temp_clean_ll]:
            if os.path.exists(f):
                os.remove(f)
        return []
    except Exception as e:
        print(f"Error in generate_and_extract_ir: {str(e)}")
        return []

def process_file(c_file, output_dir):
    """Process a single C file, matching C functions with their IR"""
    try:
        base_filename = Path(c_file).stem
        print(f"\nProcessing {c_file}...")
        
        # First, generate IR and extract IR functions
        ir_functions = generate_and_extract_ir(c_file)
        if not ir_functions:
            print(f"Failed to generate IR for {c_file}")
            return
        
        # Create a dictionary of IR functions by name
        ir_dict = {name: ir for name, ir in ir_functions}
        
        # Extract C functions
        c_functions = extract_c_functions(c_file)
        if not c_functions:
            print(f"No functions found in {c_file}")
            return
        
        # Process each function
        for number, c_func_text, c_func_name in c_functions:
            if not c_func_name:
                print(f"Could not extract name for function {number}")
                continue
            
            # Write C function
            c_output = os.path.join(output_dir, f"{base_filename}_{number}.c")
            with open(c_output, 'w') as f:
                f.write(remove_blank_lines(c_func_text))
            print(f"Created {c_output}")
            
            # Find and write corresponding IR
            if c_func_name in ir_dict:
                ll_output = os.path.join(output_dir, f"{base_filename}_{number}.ll")
                with open(ll_output, 'w') as f:
                    f.write(ir_dict[c_func_name])
                print(f"Created {ll_output}")
            else:
                print(f"Warning: No matching IR found for function {c_func_name}")
    
    except Exception as e:
        print(f"Error processing file {c_file}: {str(e)}")

def process_directory(input_dir, output_dir):
    """Process all .c files in the input directory"""
    try:
        # Create output directory if it doesn't exist
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        # Get all .c files from input directory
        c_files = list(Path(input_dir).glob('*.c'))
        
        if not c_files:
            print(f"No .c files found in {input_dir}")
            return
        
        print(f"Found {len(c_files)} .c files to process")
        
        # Process each file
        for c_file in c_files:
            process_file(str(c_file), output_dir)
    
    except Exception as e:
        print(f"Error processing directory: {str(e)}")

def main():
    # You can modify these paths as needed
    input_dir = "/home/mshaikh2/test_C_IR_generation"
    output_dir = "/home/mshaikh2/test_C_IR_generation/output"
    
    if not os.path.isdir(input_dir):
        print(f"Error: Input directory '{input_dir}' does not exist")
        return
    
    process_directory(input_dir, output_dir)
    print("\nProcessing complete!")

if __name__ == "__main__":
    main()


