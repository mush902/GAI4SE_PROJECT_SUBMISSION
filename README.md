# GAI4SE_PROJECT_SUBMISSION

The directory auxillary_codes contains scripts and utilities for processing datasets of C source code, LLVM Intermediate Representation (IR), and Rust source code. The workflow involves downloading the C dataset, generating Rust code using RustC, generating IR from the C and Rust source code using clang++ and RustC. This is followed by extracting function definitions, demangling function names, and creating a structured dataset for further analysis. Below is an overview of the provided files and their functionality.


File Descriptions

1. fetch_c_dataset.py
This script fetches a subset of C code files from a pre-existing dataset hosted on HuggingFace Datasets (UKPLab/SLTrans) and writes the source code to individual .c files.

Key Features:
Allows customization of the dataset split (Perf_Optimized or Size_Optimized).
Writes a specific range of rows to .c files in a standardized format.

Usage:
Customize start_row and end_row to define the desired range of rows.
The output files are named as train<row_number>.c.


2. get_function_from_ll.py
This script handles the extraction of function definitions from LLVM IR files and demangles mangled function names.

Key Components:
extract_function_definitions
Extracts all function definitions from an input .ll file and writes them to an output file.

demangle_and_write
Replaces mangled function names with demangled names for readability and consistency.

Additional Utility:
process_ll_files(directory_path) iterates through all .ll files in a specified directory and performs extraction and demangling.

Usage:
Provide the directory containing .ll files.
The script processes each file, extracts functions, demangles names, and writes the output back.


3. test_demangle.py
A small utility script to test the demangling of function names using predefined patterns.

Key Features:
Accepts a list of mangled function names as input.
Uses regex to extract and demangle function names.
Prints the original and demangled names for verification.

Usage:
Populate the test_names list with examples to test regex-based demangling.

4. test_fetch_rs_ll_pairs.py
This script processes Rust source code files and their corresponding LLVM IR files, extracting and organizing data for individual functions.

Key Steps:
Extract Function Definitions from Rust Files:
Identifies function definitions in .rs files using brace matching.

Extract Corresponding IR for Functions:
Maps each Rust function to its corresponding IR by matching function names.

Write Function Files:
Writes each function's Rust definition and IR to separate files for dataset organization. Special handling ensures main and main_0 are written to the same files.

Usage:
Specify the input directories for Rust and IR files.
The script processes each .rs and .ll file pair, generating organized outputs.

5. process_ll_files Function
A utility embedded within get_function_from_ll.py for batch processing of .ll files.

Workflow:
Extracts function definitions.
Demangles function names.
Cleans up intermediate files.

Usage:
Specify the directory containing .ll files.
