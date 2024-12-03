import os
import shutil

def move_split_files(source_dir, target_dir):
    # Create the target directory if it doesn't exist
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    # Iterate through files in the source directory
    for file_name in os.listdir(source_dir):
        # Check if the file name contains an underscore and ends with .rs or .ll
        if "_" in file_name and (file_name.endswith(".rs") or file_name.endswith(".ll")):
            # Construct full file path
            source_file = os.path.join(source_dir, file_name)
            target_file = os.path.join(target_dir, file_name)

            # Move the file to the target directory
            shutil.move(source_file, target_file)
            print(f"Moved {file_name} to {target_dir}")

input_dir = "/Users/mushtaqshaikh/Downloads/GAI4SE/Project/code_snippets_c/test_clean/test_input"
output_dir  = "/Users/mushtaqshaikh/Downloads/GAI4SE/Project/code_snippets_c/FINAL_TEST_TO_CREATE_DATASET/SPLIT_RUST_CODES/"

move_split_files(input_dir, output_dir)