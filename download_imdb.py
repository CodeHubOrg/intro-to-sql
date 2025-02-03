"""Download dataset files from IMDb and then decompress them."""

import os
import gzip
import argparse
import requests
from tqdm import tqdm

# Default configuration settings
SETTINGS = {
    "data_location": "https://datasets.imdbws.com/",
    "download_dir": "downloads",
    "block_size": 1024,
    "data_files": {
        # "name.basics.tsv.gz",
        # "title.akas.tsv.gz",
        # "title.basics.tsv.gz",
        "title.crew.tsv.gz",
        "title.episode.tsv.gz",
        # "title.principals.tsv.gz",
        "title.ratings.tsv.gz",
    },
}


def download_data_file(
    data_file, data_location, download_dir="downloads", block_size=1024
):
    """Download non-commercial data sets from IMDb."""
    url = data_location + data_file
    response = requests.get(url)

    # Streaming, so we can iterate over the response.
    response = requests.get(url, stream=True)

    # Format for tqdm progress bar
    bar_format = "Progress: {l_bar}{bar} | Completed: {n_fmt} | Time: [{elapsed}]"

    # Sizes in bytes.
    total_size = int(response.headers.get("content-length", 0))

    # Create the download directory if it doesn't exist
    os.makedirs(download_dir, exist_ok=True)
    download_path = os.path.join(download_dir, data_file)

    with tqdm(
        total=total_size,
        unit="B",
        unit_scale=True,
        desc=data_file,
        bar_format=bar_format,
    ) as progress_bar:
        with open(download_path, "wb") as f_out:
            for data in response.iter_content(block_size):
                progress_bar.update(len(data))
                f_out.write(data)

    if total_size != 0 and progress_bar.n != total_size:
        raise RuntimeError("Could not download file")


def decompress_file(file_name, input_dir, output_dir):
    """Decompress the gzipped datasets"""

    # Create the import directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    input_file = os.path.join(input_dir, file_name)
    # Remove the file extension for the uncompressed output file
    output_file = os.path.join(output_dir, os.path.splitext(file_name)[0])

    with gzip.open(input_file, "rb") as f_in:
        with open(output_file, "wb") as f_out:
            f_out.write(f_in.read())


if __name__ == "__main__":

    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description="Download non-commercial data sets from IMDb."
    )
    parser.add_argument(
        "--data_location",
        type=str,
        default="https://datasets.imdbws.com/",
        help="Location of the IMDb non-commercial data files",
    )
    parser.add_argument(
        "--download_dir",
        type=str,
        default="downloads",
        help="Directory to save downloaded files",
    )
    parser.add_argument(
        "--output_dir",
        type=str,
        default="import",
        help="Directory to save unzipped dataset files",
    )
    parser.add_argument(
        "--block_size",
        type=int,
        default=1024,
        help="Block size when downloading files",
    )
    parser.add_argument(
        "--no_download", action="store_true", help="Don't download dataset files"
    )
    parser.add_argument(
        "--no_decompress", action="store_true", help="Don't decompress dataset files"
    )
    args = parser.parse_args()

    SETTINGS["data_location"] = args.data_location
    SETTINGS["download_dir"] = args.download_dir
    SETTINGS["output_dir"] = args.output_dir
    SETTINGS["block_size"] = args.block_size

    if not args.no_download:

        for file in tqdm(
            SETTINGS["data_files"],
            total=len(SETTINGS["data_files"]),
            desc=f"Downloading files from {SETTINGS["data_location"]}",
        ):
            download_data_file(
                data_file=file,
                data_location=SETTINGS["data_location"],
                download_dir=SETTINGS["download_dir"],
                block_size=SETTINGS["block_size"],
            )

    if not args.no_decompress:

        for file in tqdm(
            SETTINGS["data_files"],
            total=len(SETTINGS["data_files"]),
            desc=f"Decompressing files in {SETTINGS["download_dir"]}",
        ):
            decompress_file(file, SETTINGS["download_dir"], SETTINGS["output_dir"])
