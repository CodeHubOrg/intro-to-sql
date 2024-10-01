import csv

# Open the TSV file and the new CSV file
with open('name.basics.tsv', 'r', encoding='utf-8') as tsv_file, open('name.basics.csv', 'w', newline='', encoding='utf-8') as csv_file:
    tsv_reader = csv.reader(tsv_file, delimiter='\t')
    csv_writer = csv.writer(csv_file)

    # Write each row from the TSV file to the CSV file
    for row in tsv_reader:
        csv_writer.writerow(row)