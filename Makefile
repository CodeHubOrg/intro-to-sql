################################################################################
### Standard Makefile intro
################################################################################

# Important check
MAKEFLAGS+=--warn-undefined-variables

# Causes the commands in a recipe to be issued in the same shell (beware cd commands not executed in a subshell!)
.ONESHELL:
SHELL:=/bin/bash

# When using ONESHELL, we want to exit on error (-e) and error if a command fails in a pipe (-o pipefail)
# When overriding .SHELLFLAGS one must always add a tailing `-c` as this is the default setting of Make.
.SHELLFLAGS:=-e -o pipefail -c

# Invoke the all target when no target is explicitly specified.
.DEFAULT_GOAL:=help

# Delete targets if their recipe exits with a non-zero exit code.
.DELETE_ON_ERROR:

################################################################################
### The actual Makefile
################################################################################

# Rule to generate .tsv files from .tsv.gz files
%.tsv: %.tsv.gz
	gunzip -c $< > $@


# Rule to download .tsv.gz files using wget
import/%.tsv.gz:
	mkdir -p import
	wget --timestamping -P import "https://datasets.imdbws.com/$*.tsv.gz"

