import csv
import sys
import os
import glob
import ctypes
import tqdm


def replace_null(value):
    # Function to replace '\N' which IMDb uses for null values with an empty string
    return '' if value == '\\N' else value


def tsv_to_csv():
    # Increase the field size limit to system max size: 9223372036854775807
    # csv.field_size_limit(sys.maxsize)
    
    # Calculate maximum size of long in Windows (32-bit?) and assign it to CSV field_size_limit
    max_long = 2 ** (8*ctypes.sizeof(ctypes.c_long) - 1) - 1
    csv.field_size_limit(max_long)

    # Create the export directory if it doesn't exist
    os.makedirs('export', exist_ok=True)

    # Get the list of all .tsv files in the import directory
    tsv_files = glob.glob('import/*.tsv')

    # Format for progress bar
    bar_format = "Progress: {l_bar}{bar} | Completed: {n_fmt}/{total_fmt} | Time: [{elapsed}<{remaining}] | Speed: {rate_fmt}{postfix}"
    # Iterate through all .tsv files with a progress bar
    for tsv_file in tqdm.tqdm(tsv_files, bar_format=bar_format, desc="Processing files"):
        # Define the corresponding CSV file path in the export directory
        csv_file = os.path.join('export', os.path.basename(tsv_file).replace('.tsv', '.csv'))
        
        # Display the current file name
        print(f"Processing {tsv_file}")

        # Open the TSV file and the new CSV file with the correct encoding
        with open(tsv_file, 'r', encoding='utf-8') as tsv, open(csv_file, 'w', newline='', encoding='utf-8') as csvf:
            tsv_reader = csv.reader(tsv, delimiter='\t')
            csv_writer = csv.writer(csvf)

            # Write each row from the TSV file to the CSV file
            for row in tsv_reader:
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
                
    print("Conversion complete!")


if __name__ == "__main__":
    tsv_to_csv()
    