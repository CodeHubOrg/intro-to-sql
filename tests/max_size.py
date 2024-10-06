import csv
import sys

# List of field size limits to try, from largest to smaller values
max_limit = sys.maxsize
while max_limit > 0:
    try:
        # Attempt to set the field size limit
        csv.field_size_limit(max_limit)
        print(f"Field size limit set to {max_limit}")
        break  # Exit the loop if successful
    except OverflowError:
        print(f"OverflowError: {max_limit} is too large, trying a smaller value.")
        max_limit = max_limit // 2
        
if max_limit <= 0:
    print("Failed to set suitable field size limit.")