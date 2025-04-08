# Intro to SQL

## Code Hub Decodering

This repo contains code and information for the **Intro to SQL** talks hosted by [CodeHub](https://www.codehub.org.uk). If you'd like to learn more or have questions, please join our [Discord server](https://discord.gg/pQMc4AAHuj).

## load_imdb.py

This script will load and clean data from the IMDb TSV files, before outputting it to either a CSV
file or a SQLite database.

You can download the TSV from [IMDb Non-Commercial Datasets](https://developer.imdb.com/non-commercial-datasets/)

### Command-line arguments

``` shell
usage: load_imdb.py [-h] [--output_format {csv,sqlite}] [--db_file DB_FILE] [--output_dir OUTPUT_DIR] input_dir

Process TSV files from IMDb and save to CSV or SQLite.

positional arguments:
  input_dir             Directory that contains the input TSV files

options:
  -h, --help            show this help message and exit
  --output_format {csv,sqlite}
                        Output format: csv or sqlite
  --db_file DB_FILE     Path to the SQLite database file (required if output is sqlite)
  --output_dir OUTPUT_DIR
                        Path to the output CSV file (required if output is csv)
```
