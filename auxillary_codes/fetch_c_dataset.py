from datasets import load_dataset

# Load the dataset with a specific split, like "Perf_Optimized" or "Size_Optimized"
ds = load_dataset("UKPLab/SLTrans", "C")

# Choose the desired split (either 'Perf_Optimized' or 'Size_Optimized')
split = 'Perf_Optimized'

start_row = 10001  # Start of the range (inclusive)
end_row = 10100    # End of the range (exclusive)

# Iterate over the first 10,000 rows of the chosen split
for i in range(start_row, end_row):
    # Extract the source code from the current row of the selected split
    source_code = ds[split][i]['Source_Code']
    
    # Define the filename for the current row
    filename = f'train{i+1}.c'
    
    # Write the source code to a .c file
    with open(filename, 'w') as file:
        file.write(source_code)
