# The first target in the Justfile is the default target, which I call
# "default". This target is executed when you run `just` without any
# arguments. In this case, the default target is a help message that
# lists the available targets and their descriptions.
[private]
default:
    @just --list

# Define the directory for imports
import_dir := "import"

# Recipe to fetch files from IMDB and put them in the import folder and
# then extract them, leaving the originals (so repeated fetching does not
# re-download the files.)
fetch:
    make import/name.basics.tsv \
        import/title.basics.tsv \
        import/title.crew.tsv \
        import/title.principals.tsv \
        import/title.ratings.tsv

# Remove all the artefacts, including the expensive downloads.
deepclean: clean
    rm -rf import

# Remove all the artefacts, except the expensive downloads.
clean:
    rm -rf export

# Recipe to create CSV files from the imported data
csv:
    echo "Creating CSV files from imported data..."
    mkdir -p export
    poetry run python load_imdb.py {{import_dir}} --output_format=csv --output_dir=export

# Recipe to build the SQLITE database from the CSV files
sqlite:
    echo "Creating SQLITE file from imported data..."
    mkdir -p export
    poetry run python load_imdb.py {{import_dir}} --output_format=sqlite --output_dir=export --db_file=imdb.sqlite
