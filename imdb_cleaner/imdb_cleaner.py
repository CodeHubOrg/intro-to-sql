"""Clean data from IMDb site"""

import sqlite3
import pandas as pd
from tqdm import tqdm


def _replace_null(dataframe):
    """Function to replace '\\N' which IMDb uses for null values with an empty string"""
    dataframe.replace("\\N", "", inplace=True)


def tsv_to_csv(tsv_path, csv_path):
    """Take an IMDb TSV file, clean the rows and output a CSV file"""
    with open(tsv_path, "r", encoding="utf-8") as tsv_file:
        # Count rows in file
        chunksize = 1000

        # Create a progress bar
        bar_format = "Progress: {l_bar}{bar} | Completed: {n_fmt} | Time: [{elapsed}]"
        rows_progress = tqdm(
            bar_format=bar_format,
            desc=f"Processing {tsv_path}",
        )

        with open(csv_path, "w", encoding="utf-8") as csv_file:
            # Read the TSV file in chunks
            # Write each row from the TSV file to the CSV file
            for i, chunk in enumerate(
                pd.read_csv(tsv_file, sep="\t", chunksize=chunksize)
            ):
                # Replace '\N' in each field
                _replace_null(chunk)

                if i == 0:
                    # For the first chunk, write the header
                    chunk.to_csv(csv_file, index=False, mode="w")
                else:
                    # For subsequent chunks, append without writing the header
                    chunk.to_csv(csv_file, index=False, mode="a", header=False)

                rows_progress.update(len(chunk))


def tsv_to_sqlite(tsv_path, db_file, db_table):
    """Take an IMDb TSV file, clean the rows and output to a SQLite database"""
    with open(tsv_path, "r", encoding="utf-8") as tsv_file:
        # Count rows in file
        chunksize = 1000

        # Create a progress bar
        bar_format = "Progress: {l_bar}{bar} | Completed: {n_fmt} | Time: [{elapsed}]"
        rows_progress = tqdm(
            bar_format=bar_format,
            desc=f"Processing {tsv_path}",
        )
        db_conn = sqlite3.connect(db_file)

        with db_conn:
            # Read the TSV file in chunks
            # Write each row from the TSV file to the CSV file
            for i, chunk in enumerate(
                pd.read_csv(tsv_file, sep="\t", chunksize=chunksize)
            ):
                # Replace '\N' in each field
                _replace_null(chunk)

                if i == 0:
                    # For the first create or replace the table
                    chunk.to_sql(
                        db_table,
                        db_conn,
                        if_exists="replace",
                        index=False,
                        chunksize=chunksize,
                    )
                else:
                    # For subsequent chunks, append without writing the header
                    chunk.to_sql(
                        db_table,
                        db_conn,
                        if_exists="append",
                        index=False,
                        chunksize=chunksize,
                    )

                rows_progress.update(len(chunk))
