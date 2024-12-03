import re

def demangle_function_names(test_names):
    """
    Demangles function names based on the pattern @_Z...<digits><name>17h.

    :param test_names: A list of strings containing mangled function names
    :return: A list of tuples (original_name, demangled_name or None if not matched)
    """
    # Define the regex pattern
    pattern = r"@_Z[A-Za-z\d]+(\d+[a-zA-Z0-9_]+)17h"

    results = []
    for name in test_names:
        match = re.search(pattern, name)
        if match:
            demangled_name = match.group(1)  # Extract the name inside the pattern
            # Remove the leading digits before the actual name
            demangled_name = re.sub(r"^\d+", "", demangled_name)
            results.append((name, demangled_name))
        else:
            results.append((name, None))  # No match found
    return results

if __name__ == "__main__":
    # List of test names to check the pattern
    test_names = [
        "@_ZN9train48406main_017h472af9ca814a5c7dE()"
    ]
    
    # Test the function
    results = demangle_function_names(test_names)
    for original, demangled in results:
        if demangled:
            print(f"Original: {original} => Demangled: {demangled}")
        else:
            print(f"Original: {original} => No match found")

