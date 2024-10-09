"""Load IMDb TSV files"""

import os
import glob
import argparse
from pprint import pprint
from tqdm import tqdm
from imdb_cleaner import imdb_cleaner

# Default configuration settings
SETTINGS = {
    "input_dir": "import",
    "output": "csv",
    "csv_dir": "export",
    "db_file": "imdb.sqlite",
}


def main():
    """By default, read TSV files from the `import` directory, clean them up, convert them
    to CSV files and write them to the `export` directory
    Option to write to a SQLite database instead."""

    # Check command-line arguments
    if SETTINGS["output"] == "csv":
        # Create the export directory if it doesn't exist
        os.makedirs(SETTINGS["csv_dir"], exist_ok=True)

    elif SETTINGS["output"] == "sqlite":
        if not SETTINGS["db_file"]:
            raise ValueError(
                "SQLite database file path must be provided when output format is 'sqlite'"
            )

    # Get the list of all .tsv files in the import directory
    input_path = os.path.join(SETTINGS["input_dir"], "*.tsv")
    tsv_files = glob.glob(input_path)
    print("Loading files:")
    pprint(tsv_files, indent=1)

    # Format for progress bar
    bar_format = (
        "Progress: {l_bar}{bar} | Completed: {n_fmt}/{total_fmt} | Time: [{elapsed}]"
    )

    # Iterate through all .tsv files with a progress bar
    with tqdm(
        total=len(tsv_files), bar_format=bar_format, desc="Processing files"
    ) as files_progress:
        for tsv_file in tsv_files:
            # If output type is csv create CSV files
            if SETTINGS["output"] == "csv":
                # Define the corresponding CSV file path in the export directory
                csv_file = os.path.join(
                    SETTINGS["csv_dir"],
                    os.path.basename(tsv_file).replace(".tsv", ".csv"),
                )
                imdb_cleaner.tsv_to_csv(tsv_file=tsv_file, csv_file=csv_file)

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
        "--output",
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
        "--csv_dir",
        type=str,
        default="export",
        help="Path to the output CSV file (required if output is csv)",
    )
    args = parser.parse_args()

    # Configuration settings
    SETTINGS = {
        "input_dir": args.input_dir,
        "output": args.output,
        "csv_dir": args.csv_dir,
        "db_file": args.db_file,
    }
    main()
