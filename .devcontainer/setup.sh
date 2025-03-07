!# /usr/bin/bash
echo "Updating and upgrading Ubuntu packages"
sudo apt-get update
sudo apt-get upgrade -y
# echo "Installing build-essential, wget, gzip, and pipx Ubuntu packages"
# sudo apt-get install -y build-essential wget gzip pipx npm
# Feature to install git lfs fails so adding it here
# git lfs install
git lfs pull
pipx ensurepath
echo "Installing poetry and rust-just pipx packages"
pipx install poetry rust-just
echo "Using poetry to create a virtual environment"
# Install the python environment used for building the database
poetry install
# Install the node.js modules for SQLTools
npm install sqlite3@5.1.7
# git lfs pull
gunzip -k -q /workspaces/intro-to-sql/prebuilt/imdb.sqlite.gz