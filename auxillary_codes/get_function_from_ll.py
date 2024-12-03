import re

def extract_function_definitions(input_file, output_file):
    """
    Extracts function definitions from an LLVM IR (.ll) file and writes them to a new file.

    :param input_file: Path to the input .ll file
    :param output_file: Path to the output .ll file with only function definitions
    """
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        inside_function = False  # Flag to indicate if we're inside a function
        brace_count = 0  # Counter to track opening and closing braces

        for line in infile:
            stripped_line = line.strip()

            # Check for the start of a function definition
            if stripped_line.startswith("define") and "{" in stripped_line:
                inside_function = True
                brace_count += stripped_line.count("{") - stripped_line.count("}")
                outfile.write(line)  # Write the line containing "define"
                continue

            # If we're inside a function, write the lines and track braces
            if inside_function:
                brace_count += stripped_line.count("{") - stripped_line.count("}")
                outfile.write(line)

                # If brace_count reaches 0, the function definition ends
                if brace_count == 0:
                    inside_function = False


def demangle_and_write(input_file, output_file):
    """
    Demangles function names in a .ll file and writes the updated file to a new file.

    :param input_file: Path to the input .ll file
    :param output_file: Path to the output .ll file with demangled function names
    """
    # Define the regex pattern for demangling
    pattern = r"@_Z[A-Za-z\d]+(\d+[a-zA-Z0-9_]+)17h.*?\("

    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            # Search for mangled names in the line
            match = re.search(pattern, line)
            if match:
                demangled_name = match.group(1)
                # Remove the leading digits before the actual name
                demangled_name = re.sub(r"^\d+", "", demangled_name)
                # Replace the mangled name with the demangled name, preserving the parenthesis
                line = re.sub(pattern, f"@{demangled_name}(", line)
            outfile.write(line)


import os
import glob

def process_ll_files(directory_path):
    """
    Process all .ll files in the specified directory.
    
    Args:
        directory_path (str): Path to the directory containing .ll files
    """
    # Get all .ll files in the directory
    ll_files = glob.glob(os.path.join(directory_path, "*.ll"))
    
    if not ll_files:
        print(f"No .ll files found in {directory_path}")
        return
    
    for input_ll in ll_files:
        try:
            # Create paths for temporary and output files
            base_name = os.path.basename(input_ll)
            extracted_ll = os.path.join(directory_path, f"temp_{base_name}")
            demangled_ll = os.path.join(directory_path, base_name)
            
            print(f"\nProcessing: {base_name}")
            
            # Extract function definitions
            extract_function_definitions(input_ll, extracted_ll)
            print(f"Function definitions extracted to {extracted_ll}")
            
            # Demangle function names
            demangle_and_write(extracted_ll, demangled_ll)
            print(f"Demangled function names written to {demangled_ll}")
            
            # Clean up temporary file
            if os.path.exists(extracted_ll):
                os.remove(extracted_ll)
                print(f"Temporary file {extracted_ll} removed")
                
        except Exception as e:
            print(f"Error processing {base_name}: {str(e)}")
            continue

if __name__ == "__main__":
    # Directory containing .ll files
    directory_path = "/Users/mushtaqshaikh/Downloads/GAI4SE/Project/code_snippets_c/test_clean/test_ir_input"  # Current directory, modify as needed
    
    # Process all .ll files
    process_ll_files(directory_path)