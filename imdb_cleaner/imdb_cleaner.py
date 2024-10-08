"""Clean data from IMDb site"""

import pandas as pd
from tqdm import tqdm


def replace_null(dataframe):
    """Function to replace '\\N' which IMDb uses for null values with an empty string"""
    dataframe.replace("\\N", "", inplace=True)


def tsv_to_csv(tsv_file, csv_file):
    """Take an IMDb TSV file, clean the rows and output a CSV file"""
    # Count rows in file
    with open(tsv_file, "r", encoding="utf-8") as file:
        num_rows = sum(1 for row in file)

    # Read the TSV file in chunks
    chunksize = 1000
    chunks = pd.read_csv(tsv_file, sep="\t", chunksize=chunksize)
    bar_format = (
        "Progress: {l_bar}{bar} | Completed: {n_fmt}/{total_fmt} | Time: [{elapsed}]"
    )

    with tqdm(
        total=num_rows,
        bar_format=bar_format,
        desc=f"Processing {csv_file}",
    ) as rows_progress:
        # Write each row from the TSV file to the CSV file
        for i, chunk in enumerate(chunks):
            # Test for integers exceeding `sys.maxsize`
            # Replace '\N' in each field
            replace_null(chunk)

            # Save the processed chunk to a CSV file
            if i == 0:
                # For the first chunk, write the header
                chunk.to_csv(csv_file, index=False, mode="w")
            else:
                # For subsequent chunks, append without writing the header
                chunk.to_csv(csv_file, index=False, mode="a", header=False)

            if (i + 1) * chunksize <= num_rows:
                rows_progress.update(chunksize)
            else:
                # Ensure the progress bar completes if the total is not a multiple of 100
                remaining = num_rows % chunksize
                rows_progress.update(remaining)
