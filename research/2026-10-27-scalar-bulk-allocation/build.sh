#!/bin/sh
# Ordinary local LaTeX build with shell escape disabled.
set -eu
cd "$(dirname "$0")"
mkdir -p build
export SOURCE_DATE_EPOCH=1793059200
export FORCE_SOURCE_DATE=1
for pass in 1 2 3; do
    pdflatex -no-shell-escape -interaction=nonstopmode -halt-on-error -output-directory=build scalar_bulk_allocation.tex
done
cp build/scalar_bulk_allocation.pdf scalar_bulk_allocation.pdf
