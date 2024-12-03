import json
from datasets import load_dataset

# Load the dataset with the desired split
ds = load_dataset("UKPLab/SLTrans", "C")

# Choose the desired split (either 'Perf_Optimized' or 'Size_Optimized')
split = 'Perf_Optimized'

# Initialize an empty list to hold the compile commands
compile_commands = []

start_row = 10001  # Start of the range (inclusive)
end_row = 10100 
# Iterate over the first 10,000 rows of the chosen split
for i in range(start_row, end_row):
    # Get the filename based on the row index
    filename = f'train{i}.c'

    # Create the compile command entry for the current file
    command_entry = {
        "directory": "/Users/mushtaqshaikh/Downloads/GAI4SE/Project/code_snippets_c",
        "command": f"gcc -c {filename} -o {filename.replace('.c', '.o')}",
        "file": filename
    }
    
    # Append the command entry to the list
    compile_commands.append(command_entry)

# Write the compile commands to a JSON file
with open('compile_commands.json', 'w') as json_file:
    json.dump(compile_commands, json_file, indent=4)

print("compile_commands.json has been generated.")

