"""Load IMDb TSV files
1 Download the files if they're not present
2 Load the TSV files a chunk at time
3 Clean the chunk
4 Write the chunk to either a CSV file or SQLite database table
"""

import os
import argparse
import re
import sqlite3 as sqlite
import pandas as pd
from tqdm import tqdm
from imdb_cleaner import (
    IMDbCleaner,
    TitleBasicsCleaner,
    TitleCrewCleaner,
    TitleEpisodeCleaner,
)


class IMDbLoader:
    """Load the IMDb data sets either into CSV files or a SQLite database"""

    def __init__(self, tsv_file, chunk_size):
        self.tsv_file = tsv_file
        self.chunk_size = chunk_size

    def tsv_load(self):
        """Load the data from the TSV file in chunks."""
        return pd.read_csv(
            self.tsv_file, sep="\t", chunksize=self.chunk_size, low_memory=False
        )

    def sanitise_table_name(self, table_name):
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

    def df_to_csv(self, data_generator, csv_path):
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

    def df_to_sqlite(self, data_generator, db_path, db_table):
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
                        chunksize=self.chunk_size,
                    )
                else:
                    # For subsequent chunks, append without writing the header
                    chunk.to_sql(
                        db_table,
                        db_conn,
                        if_exists="append",
                        index=False,
                        chunksize=self.chunk_size,
                    )


def main(input_dir, output_dir, output_format, db_file, chunk_size):
    """By default, read TSV files from the `import` directory, clean them up, convert them
    to CSV files and write them to the `export` directory
    Option to write to a SQLite database instead."""

    cleaner_classes = {
        "name.basics.tsv": IMDbCleaner,
        "title.basics.tsv": TitleBasicsCleaner,
        "title.crew.tsv": TitleCrewCleaner,
        "title.episode.tsv": TitleEpisodeCleaner,
        "title.principals.tsv": IMDbCleaner,
        "title.ratings.tsv": IMDbCleaner,
    }

    # Create the export directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    # Check command-line arguments
    if output_format == "sqlite":
        if not db_file:
            raise ValueError(
                "SQLite database file path must be provided when output format is 'sqlite'"
            )
    elif output_format != "csv":
        raise ValueError("Invalid output format: ", output_format)

    # Format for progress bar
    bar_format = "Progress: {l_bar}{bar} | Completed: {n_fmt} | Time: [{elapsed}]"

    # Iterate through all TSV files with a progress bar
    with tqdm(
        total=len(cleaner_classes),
        bar_format=bar_format,
        desc="Processing files",
    ) as files_progress:
        for tsv_name, cleaner_class in cleaner_classes.items():
            tsv_path = os.path.join(input_dir, tsv_name)
            # Create a generator to supply the TSV data in chunks as data frames
            loader = IMDbLoader(tsv_file=tsv_path, chunk_size=chunk_size)
            data_generator = loader.tsv_load()
            # Create a generator to supply the cleaned data frames from a class based on the file
            # names mapped in cleaner_classes
            cleaner = cleaner_class(data_generator, tsv_name)
            if output_format == "csv":
                # If output format is csv create CSV files
                # Define the corresponding CSV file path in the export directory
                csv_path = os.path.join(output_dir, tsv_name.replace(".tsv", ".csv"))
                # Write the data frames as a CSV file
                loader.df_to_csv(data_generator=cleaner.clean_data(), csv_path=csv_path)
            elif output_format == "sqlite":
                # If output format is SQLite create a SQLite database
                db_path = os.path.join(output_dir, db_file)
                # Define the corresponding table name in the SQLite database
                db_table = "load_" + loader.sanitise_table_name(
                    os.path.splitext(tsv_name)[0]
                )
                # Write the data frames to a SQLite table
                loader.df_to_sqlite(
                    data_generator=cleaner.clean_data(),
                    db_path=db_path,
                    db_table=db_table,
                )

            files_progress.update(1)

    print("Conversion complete!")


if __name__ == "__main__":

    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        prog="load_imdb",
        description="Process TSV files from IMDb and save to CSV or SQLite.",
        epilog="You can download files using download_imdb",
    )
    parser.add_argument(
        "input_dir",
        type=str,
        default="input",
        help="Directory that contains the input TSV files (default: input)",
    )
    parser.add_argument(
        "-f",
        "--output_format",
        type=str,
        choices=["csv", "sqlite"],
        default="csv",
        help="Output format: csv or sqlite (default: csv)",
    )
    parser.add_argument(
        "-d",
        "--db_file",
        type=str,
        default="imdb.sqlite",
        help="Path to SQLite database file - required if output is sqlite (default:imdb.sqlite)",
    )
    parser.add_argument(
        "-o",
        "--output_dir",
        type=str,
        default="data",
        help="Path to the output CSV file - required if output is csv (default:data)",
    )
    parser.add_argument(
        "-c",
        "--chunk_size",
        type=int,
        default=1048576,
        help="Block size in bytes when processing files (default: 1048576)",
    )
    args = parser.parse_args()

    main(
        input_dir=args.input_dir,
        output_dir=args.output_dir,
        output_format=args.output_format,
        db_file=args.db_file,
        chunk_size=args.chunk_size,
    )
