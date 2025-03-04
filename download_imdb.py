"""Download dataset files from IMDb and then decompress them."""

import os
import gzip
import argparse
import requests
from tqdm import tqdm

# Default configuration settings
SETTINGS = {
    "data_files": {
        "name.basics.tsv.gz",
        "title.basics.tsv.gz",
        "title.crew.tsv.gz",
        "title.episode.tsv.gz",
        "title.principals.tsv.gz",
        "title.ratings.tsv.gz",
    },
}


class IMDbDownloader:
    """Base downloader for IMDb data sets"""

    def __init__(self, download_dir, zip_file, chunk_size=1024):
        """Initialise IMDbDownloader object

        Args:
            download_dir (string): Directory to download data file to
            zip_file (string): Name of compressed data file to download
            chunk_size (int, optional): Chunk size when downloading and decompressing data files.

            Defaults to 1024.
        """
        self.download_dir = download_dir
        self.zip_file = zip_file
        self.unzip_file = os.path.splitext(zip_file)[0]
        self.chunk_size = chunk_size

    def download_file(self, data_location):
        """Download non-commercial data sets from IMDb.

        Args:
            data_location (string): URL where files are located to download
        """
        url = data_location + self.zip_file

        # Streaming, so we can iterate over the response.
        response = requests.get(url, stream=True, timeout=60)
        total_size = int(response.headers.get("content-length", 0))

        # Format for tqdm progress bar
        bar_format = "Progress: {l_bar}{bar} | Completed: {n_fmt} | Time: [{elapsed}]"

        # Create the download directory if it doesn't exist
        os.makedirs(self.download_dir, exist_ok=True)
        download_path = os.path.join(self.download_dir, self.zip_file)

        with tqdm.wrapattr(
            open(download_path, "wb"),
            "write",
            total=total_size,
            unit="B",
            unit_scale=True,
            desc=f"Downloading {self.zip_file}",
            bar_format=bar_format,
            leave=False,
        ) as f_out:
            for chunk in response.iter_content(chunk_size=self.chunk_size):
                f_out.write(chunk)

    def decompress_file(self, output_dir):
        """Decompress the gzipped datasets

        Args:
            output_dir (string): Directory to write decompressed files to
        """

        # Create the import directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        input_file = os.path.join(self.download_dir, self.zip_file)

        # Remove the file extension for the uncompressed output file
        output_file = os.path.join(output_dir, self.unzip_file)

        # Format for tqdm progress bar
        bar_format = "Completed: {n_fmt} | Time: [{elapsed}]"
        with gzip.open(input_file, "rb") as f_in:
            with open(output_file, "wb") as f_out:
                p_bar = tqdm(
                    unit="B",
                    unit_scale=True,
                    desc=f"Decompressing {self.zip_file}",
                    bar_format=bar_format,
                    leave=False,
                )
                while True:
                    block = f_in.read(self.chunk_size)
                    if not block:
                        break
                    f_out.write(block)
                    p_bar.update(len(block))


if __name__ == "__main__":

    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        prog="download_imdb",
        description="Download non-commercial data sets from IMDb.",
        epilog="You can process the files with load_imdb.",
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
        help="Directory to save unzipped dataset files (default:import)",
    )
    parser.add_argument(
        "--chunk_size",
        type=int,
        default=1048576,
        help="Block size in bytes when downloading files (default: 1048576)",
    )
    parser.add_argument(
        "--no_download", action="store_true", help="Don't download dataset files"
    )
    parser.add_argument(
        "--no_decompress", action="store_true", help="Don't decompress dataset files"
    )
    args = parser.parse_args()

    for file in tqdm(
        SETTINGS["data_files"],
        total=len(SETTINGS["data_files"]),
        desc="Processing IMDb dataset files",
    ):
        imdb_downloader = IMDbDownloader(args.download_dir, file)
        if not args.no_download:
            imdb_downloader.download_file(data_location=args.data_location)

        if not args.no_decompress:
            imdb_downloader.decompress_file(args.output_dir)
