"""Load IMDb TSV files"""

import os
import argparse
import re
from pprint import pprint
from tqdm import tqdm
from imdb_cleaner import imdb_cleaner

# Default configuration settings
SETTINGS = {
    "input_dir": "import",
    "input_names": ["title.crew.tsv", "title.episode.tsv", "title.ratings.tsv"],
    "output_format": "csv",
    "output_dir": "export",
    "db_file": "imdb.sqlite",
}


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


def main():
    """By default, read TSV files from the `import` directory, clean them up, convert them
    to CSV files and write them to the `export` directory
    Option to write to a SQLite database instead."""

    # Check command-line arguments
    if SETTINGS["output_format"] == "csv":
        # Create the export directory if it doesn't exist
        os.makedirs(SETTINGS["output_dir"], exist_ok=True)

    elif SETTINGS["output_format"] == "sqlite":
        if not SETTINGS["db_file"]:
            raise ValueError(
                "SQLite database file path must be provided when output format is 'sqlite'"
            )
    else:
        raise ValueError("Invalid output format: ", SETTINGS["output_format"])

    pprint(SETTINGS)

    print("Loading files:")
    pprint(SETTINGS["input_names"], indent=1)

    # Format for progress bar
    bar_format = "Progress: {l_bar}{bar} | Completed: {n_fmt} | Time: [{elapsed}]"

    # Iterate through all TSV files with a progress bar
    with tqdm(
        total=len(SETTINGS["input_names"]),
        bar_format=bar_format,
        desc="Processing files",
    ) as files_progress:
        for tsv_name in SETTINGS["input_names"]:
            tsv_path = os.path.join(SETTINGS["input_dir"], tsv_name)
            if SETTINGS["output_format"] == "csv":
                # If output format is csv create CSV files
                # Define the corresponding CSV file path in the export directory
                csv_path = os.path.join(
                    SETTINGS["output_dir"], tsv_name.replace(".tsv", ".csv")
                )
                imdb_cleaner.tsv_to_csv(tsv_path=tsv_path, csv_path=csv_path)
            elif SETTINGS["output_format"] == "sqlite":
                # If output format is SQLite create a SQLite database
                # Define the corresponding table name in the SQLite database
                db_table = sanitise_table_name(os.path.splitext(tsv_name)[0])
                imdb_cleaner.tsv_to_sqlite(
                    tsv_path=tsv_path, db_file=SETTINGS["db_file"], db_table=db_table
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
