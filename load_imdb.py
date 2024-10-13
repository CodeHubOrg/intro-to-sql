"""Load IMDb TSV files
1 Load the TSV files a chunk at time
2 Clean the chunk
3 Write the chunk to either a CSV file or SQLite database table
"""

import os
import argparse
import re
import sqlite3 as sqlite
import pandas as pd
from tqdm import tqdm
from imdb_cleaner import IMDbCleaner, TitleBasicsCleaner

# Default configuration settings
SETTINGS = {
    "input_dir": "import",
    "output_format": "csv",
    "output_dir": "export",
    "db_file": "imdb.sqlite",
    "chunksize": 10000,
}
CLEANER_CLASSES = {
    "name.basics.tsv": IMDbCleaner,
    "title.basics.tsv": TitleBasicsCleaner,
    "title.crew.tsv": IMDbCleaner,
    "title.episode.tsv": IMDbCleaner,
    "title.principals.tsv": IMDbCleaner,
    "title.ratings.tsv": IMDbCleaner,
    # "title.akas.tsv": IMDbCleaner,
}


def tsv_load(tsv_file, chunksize):
    """Load the data from the TSV file in chunks."""
    return pd.read_csv(tsv_file, sep="\t", chunksize=chunksize)


def sanitise_table_name(table_name):
    """Converts a string to a valid table name."""
    # From Claude Haiku
    # Remove special characters and spaces
    table_name = re.sub(r"[^a-zA-Z0-9_]", "_", table_name)

    # Convert to lowercase
    table_name = table_name.lower()

    # Truncate the name if necessary
    max_length = 63  # Maximum table name length in SQLite
    if len(table_name) > max_length:
        table_name = table_name[:max_length]

    return table_name


def df_to_csv(data_generator, csv_path):
    """Take rows from an IMDb TSV file, clean the rows and output a CSV file"""

    with open(csv_path, "w", encoding="utf-8", newline="") as csv_file:
        # Read the TSV file in chunks
        # Write the data frames to a CSV file using a writer
        for chunk in data_generator:
            # csv_file.tell() returns the current position in the file of the `csv_file` pointer
            if csv_file.tell() == 0:
                # For the first chunk, overwrite the file and include a header
                chunk.to_csv(csv_file, index=False, mode="w")
            else:
                # For subsequent chunks, append without writing the header
                chunk.to_csv(csv_file, index=False, mode="a", header=False)


def df_to_sqlite(data_generator, db_path, db_table):
    """Take rows from an IMDb TSV file, clean the rows and output to a SQLite database"""
    db_conn = sqlite.connect(db_path)

    with db_conn:
        # Read the TSV file in chunks
        # Write the data frames to a SQLite table
        for i, chunk in enumerate(data_generator):
            if i == 0:
                # For the first create or replace the table
                chunk.to_sql(
                    db_table,
                    db_conn,
                    if_exists="replace",
                    index=False,
                    chunksize=SETTINGS["chunksize"],
                )
            else:
                # For subsequent chunks, append without writing the header
                chunk.to_sql(
                    db_table,
                    db_conn,
                    if_exists="append",
                    index=False,
                    chunksize=SETTINGS["chunksize"],
                )


def main():
    """By default, read TSV files from the `import` directory, clean them up, convert them
    to CSV files and write them to the `export` directory
    Option to write to a SQLite database instead."""

    # Create the export directory if it doesn't exist
    os.makedirs(SETTINGS["output_dir"], exist_ok=True)
    # Check command-line arguments
    if SETTINGS["output_format"] == "sqlite":
        if not SETTINGS["db_file"]:
            raise ValueError(
                "SQLite database file path must be provided when output format is 'sqlite'"
            )
    elif SETTINGS["output_format"] != "csv":
        raise ValueError("Invalid output format: ", SETTINGS["output_format"])

    # Format for progress bar
    bar_format = "Progress: {l_bar}{bar} | Completed: {n_fmt} | Time: [{elapsed}]"

    # Iterate through all TSV files with a progress bar
    with tqdm(
        total=len(CLEANER_CLASSES),
        bar_format=bar_format,
        desc="Processing files",
    ) as files_progress:
        for tsv_name, cleaner_class in CLEANER_CLASSES.items():
            tsv_path = os.path.join(SETTINGS["input_dir"], tsv_name)
            # Create a generator to supply the TSV data in chunks as data frames
            data_generator = tsv_load(tsv_path, SETTINGS["chunksize"])
            # Create a generator to supply the cleaned data frames from a class based on the file
            # names mapped in CLEANER_CLASSES
            cleaner = cleaner_class(data_generator, tsv_name)
            if SETTINGS["output_format"] == "csv":
                # If output format is csv create CSV files
                # Define the corresponding CSV file path in the export directory
                csv_path = os.path.join(
                    SETTINGS["output_dir"], tsv_name.replace(".tsv", ".csv")
                )
                # Write the data frames as a CSV file
                df_to_csv(data_generator=cleaner.clean_data(), csv_path=csv_path)
            elif SETTINGS["output_format"] == "sqlite":
                # If output format is SQLite create a SQLite database
                db_path = os.path.join(SETTINGS["output_dir"], SETTINGS["db_file"])
                # Define the corresponding table name in the SQLite database
                db_table = sanitise_table_name(os.path.splitext(tsv_name)[0])
                # Write the data frames to a SQLite table
                df_to_sqlite(
                    data_generator=cleaner.clean_data(),
                    db_path=db_path,
                    db_table=db_table,
                )

            files_progress.update(1)

    print("Conversion complete!")


if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description="Process TSV files from IMDb and save to CSV or SQLite."
    )
    parser.add_argument(
        "input_dir",
        type=str,
        default="input",
        help="Directory that contains the input TSV files",
    )
    parser.add_argument(
        "--output_format",
        type=str,
        choices=["csv", "sqlite"],
        default="csv",
        help="Output format: csv or sqlite",
    )
    parser.add_argument(
        "--db_file",
        type=str,
        default="imdb.sqlite",
        help="Path to the SQLite database file (required if output is sqlite)",
    )
    parser.add_argument(
        "--output_dir",
        type=str,
        default="export",
        help="Path to the output CSV file (required if output is csv)",
    )
    args = parser.parse_args()

    # Configuration settings
    SETTINGS["input_dir"] = args.input_dir
    SETTINGS["output_format"] = args.output_format
    SETTINGS["output_dir"] = args.output_dir
    SETTINGS["db_file"] = args.db_file

    main()
