import os
import shutil
import re

def natural_sort_key(s):
    """
    Create a key for natural sorting of strings containing numbers.
    This will extract the number from strings like 'train44.ll' and return 44
    """
    return int(re.search(r'train(\d+)\.rs', s).group(1))

def copy_first_n_sorted_files(source_dir, dest_dir, n=100):
    """
    Copy the first n files after sorting them numerically by their names.
    
    Args:
        source_dir (str): Source directory containing the .ll files
        dest_dir (str): Destination directory where files will be copied
        n (int): Number of files to copy (default: 100)
    """
    # Create destination directory if it doesn't exist
    os.makedirs(dest_dir, exist_ok=True)
    
    # Get all .ll files
    ll_files = [f for f in os.listdir(source_dir) if f.endswith('.rs') and f.startswith('train')]
    
    if not ll_files:
        print(f"No .ll files found in {source_dir}")
        return
    
    # Sort files numerically
    sorted_files = sorted(ll_files, key=natural_sort_key)
    
    # Take first n files
    files_to_copy = sorted_files[:n]
    
    print(f"Found {len(sorted_files)} total files")
    print(f"Copying first {len(files_to_copy)} files...")
    
    # Copy files with progress indication
    for i, filename in enumerate(files_to_copy, 1):
        source_path = os.path.join(source_dir, filename)
        dest_path = os.path.join(dest_dir, filename)
        
        try:
            shutil.copy2(source_path, dest_path)
            if i % 10 == 0:  # Print progress every 10 files
                print(f"Copied {i} files...")
        except Exception as e:
            print(f"Error copying {filename}: {str(e)}")
            continue
    
    # Print first and last copied files for verification
    if files_to_copy:
        print("\nFirst copied file:", files_to_copy[0])
        print("Last copied file:", files_to_copy[-1])
        print(f"\nSuccessfully copied {len(files_to_copy)} files to {dest_dir}")

if __name__ == "__main__":
    # Directory paths
    source_directory = "/Users/mushtaqshaikh/Downloads/GAI4SE/Project/code_snippets_c/RS_CODE"  # Replace with your source directory path
    destination_directory = "/Users/mushtaqshaikh/Downloads/GAI4SE/Project/code_snippets_c/test_clean/test_input"  # Replace with your destination directory path
    
    # Copy first 100 sorted files
    copy_first_n_sorted_files(source_directory, destination_directory)
