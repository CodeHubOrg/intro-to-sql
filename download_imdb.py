import os
import argparse
import requests
from tqdm import tqdm

# Default configuration settings
SETTINGS = {
    "data_location": "https://datasets.imdbws.com/",
    "download_dir": "downloads",
    "block_size": 1024,
}

DATA_FILES = {
    # "name.basics.tsv.gz",
    # "title.akas.tsv.gz",
    # "title.basics.tsv.gz",
    "title.crew.tsv.gz",
    "title.episode.tsv.gz",
    # "title.principals.tsv.gz",
    "title.ratings.tsv.gz",
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
        with open(download_path, "wb") as file:
            for data in response.iter_content(block_size):
                progress_bar.update(len(data))
                file.write(data)

    if total_size != 0 and progress_bar.n != total_size:
        raise RuntimeError("Could not download file")


if __name__ == "__main__":

    for file in tqdm(
        DATA_FILES,
        total=len(DATA_FILES),
        desc=f"Downloading files from {SETTINGS["data_location"]}",
    ):
        download_data_file(
            data_file=file,
            data_location=SETTINGS["data_location"],
            download_dir=SETTINGS["download_dir"],
            block_size=SETTINGS["block_size"],
        )

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
        "--block_size",
        type=int,
        default=1024,
        help="Block size when downloading files",
    )
