"""Load IMDb TSV files"""

import os
import glob
from tqdm import tqdm
from imdb_cleaner import imdb_cleaner


def main():
    """Read TSV files from the `import` directory, clean them up, convert them
    to CSV files and write them to the `export` directory"""
    # Create the export directory if it doesn't exist
    os.makedirs("export", exist_ok=True)

    # Get the list of all .tsv files in the import directory
    tsv_files = glob.glob("import/*.tsv")

    # Format for progress bar
    bar_format = (
        "Progress: {l_bar}{bar} | Completed: {n_fmt}/{total_fmt} | Time: [{elapsed}]"
    )

    # Iterate through all .tsv files with a progress bar
    with tqdm(
        total=len(tsv_files), bar_format=bar_format, desc="Processing files"
    ) as files_progress:
        for tsv_file in tsv_files:
            # Define the corresponding CSV file path in the export directory
            csv_file = os.path.join(
                "export", os.path.basename(tsv_file).replace(".tsv", ".csv")
            )
            imdb_cleaner.tsv_to_csv(tsv_file=tsv_file, csv_file=csv_file)

            files_progress.update(1)

    print("Conversion complete!")


if __name__ == "__main__":
    main()
