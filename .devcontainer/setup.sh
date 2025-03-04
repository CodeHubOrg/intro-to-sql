!# /usr/bin/bash
echo "Updating and upgrading Ubuntu packages"
apt-get update
apt-get upgrade -y
echo "Installing build-essential, wget, gzip, and pipx Ubuntu packages"
apt-get install -y build-essential wget gzip pipx
pipx ensurepath
echo "Installing poetry and rust-just pipx packages"
pipx install poetry rust-just
echo "Using poetry to create a virtual environment"
poetry install
