import os
import csv
import glob

# Function to replace '\N' with an empty string
def replace_null(value):
    return '' if value == '\\N' else value

# Create the export directory if it doesn't exist
os.makedirs('export', exist_ok=True)

# Iterate through all .tsv files in the import directory
for tsv_file in glob.glob('import/*.tsv'):
    # Define the corresponding CSV file path in the export directory
    csv_file = os.path.join('export', os.path.basename(tsv_file).replace('.tsv', '.csv'))
    
    # Open the TSV file and the new CSV file with the correct encoding
    with open(tsv_file, 'r', encoding='utf-8') as tsv, open(csv_file, 'w', newline='', encoding='utf-8') as csvf:
        tsv_reader = csv.reader(tsv, delimiter='\t')
        csv_writer = csv.writer(csvf)

        # Write each row from the TSV file to the CSV file
        for row in tsv_reader:
            # Replace '\N' in each field
            new_row = [replace_null(field) for field in row]
            csv_writer.writerow(new_row)

print("Conversion complete!")
