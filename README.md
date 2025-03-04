# Intro to SQL

## Code Hub Decodering

This repo contains code and information for the **Intro to SQL** talks hosted by [CodeHub](https://www.codehub.org.uk). If you'd like to learn more or have questions, please join our [Discord server](https://discord.gg/pQMc4AAHuj).

## load_imdb.py

This script will load and clean data from the IMDb TSV files, before outputting it to either a CSV
file or a SQLite database.

You can download the TSV from [IMDb Non-Commercial Datasets](https://developer.imdb.com/non-commercial-datasets/)

### Command-line arguments

``` shell
usage: load_imdb [-h] [-f {csv,sqlite}] [-d DB_FILE] [-o OUTPUT_DIR] [-c CHUNK_SIZE] input_dir

Process TSV files from IMDb and save to CSV or SQLite.

positional arguments:
  input_dir             Directory that contains the input TSV files (default: input)

options:
  -h, --help            show this help message and exit
  -f {csv,sqlite}, --output_format {csv,sqlite}
                        Output format: csv or sqlite (default: csv)
  -d DB_FILE, --db_file DB_FILE
                        Path to SQLite database file - required if output is sqlite (default:imdb.sqlite)
  -o OUTPUT_DIR, --output_dir OUTPUT_DIR
                        Path to the output CSV file - required if output is csv (default:data)
  -c CHUNK_SIZE, --chunk_size CHUNK_SIZE
                        Block size in bytes when processing files (default: 1048576)
                        Path to the output CSV file (required if output is csv)
```
