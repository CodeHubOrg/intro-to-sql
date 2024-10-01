import csv

# Function to replace '\N' with an empty string
def replace_null(value):
    return '' if value == '\\N' else value

# Open the TSV file and the new CSV file with the correct encoding
with open('name.basics.tsv', 'r', encoding='utf-8') as tsv_file, open('name.basics.csv', 'w', newline='', encoding='utf-8') as csv_file:
    tsv_reader = csv.reader(tsv_file, delimiter='\t')
    csv_writer = csv.writer(csv_file)

    # Write each row from the TSV file to the CSV file
    for row in tsv_reader:
        # Replace '\N' in each field
        new_row = [replace_null(field) for field in row]
        csv_writer.writerow(new_row)
