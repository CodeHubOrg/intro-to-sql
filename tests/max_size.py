"""Calculate maximum value permitted by CSV module"""

import sys
import csv

# List of field size limits to try, from largest to smaller values
MAX_LIMIT = sys.maxsize
while MAX_LIMIT > 0:
    try:
        # Attempt to set the field size limit
        csv.field_size_limit(MAX_LIMIT)
        print(f"Field size limit set to {MAX_LIMIT}")
        break  # Exit the loop if successful
    except OverflowError:
        print(f"OverflowError: {MAX_LIMIT} is too large, trying a smaller value.")
        MAX_LIMIT = MAX_LIMIT // 2

if MAX_LIMIT <= 0:
    print("Failed to set suitable field size limit.")
