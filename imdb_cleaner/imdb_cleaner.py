"""Clean data from IMDb site"""

import csv
import sys
import ctypes
from tqdm import tqdm


def replace_null(value):
    """Function to replace '\\N' which IMDb uses for null values with an empty string"""
    return "" if value == "\\N" else value


def tsv_to_csv(tsv_file, csv_file):
    """Take an IMDb TSV file, clean the rows and output a CSV file"""
    # Calculate maximum size of long in Windows (32-bit?) and assign it to CSV field_size_limit
    max_long = 2 ** (8 * ctypes.sizeof(ctypes.c_long) - 1) - 1
    csv.field_size_limit(max_long)

    # Count rows in file
    with open(tsv_file, "r", encoding="utf-8") as file:
        num_rows = sum(1 for row in file)

    # Open the TSV file and the new CSV file with the correct encoding
    with open(tsv_file, "r", encoding="utf-8") as tsv, open(
        csv_file, "w", newline="", encoding="utf-8"
    ) as csvf:
        tsv_reader = csv.reader(tsv, delimiter="\t")
        csv_writer = csv.writer(csvf)
        bar_format = (
            "Progress: {l_bar}{bar} | Completed: {n_fmt}/{total_fmt} "
            "| Time: [{elapsed}]"
        )

        with tqdm(
            total=num_rows,
            bar_format=bar_format,
            desc=f"Processing {csv_file}",
            leave=False,
        ) as rows_progress:
            # Write each row from the TSV file to the CSV file
            for i, row in enumerate(tsv_reader):
                # Test for integers exceeding `sys.maxsize`
                for item in row:
                    try:
                        value = int(item)
                        if value > sys.maxsize:
                            print(f"Large value found: {value}")
                    except ValueError:
                        pass
                # Replace '\N' in each field
                new_row = [replace_null(field) for field in row]
                csv_writer.writerow(new_row)

                if (i + 1) % 100 == 0:
                    rows_progress.update(100)

        # Ensure the progress bar completes if the total is not a multiple of 100
        remaining = len(num_rows) % 100
        if remaining > 0:
            rows_progress.update(remaining)
