#!/bin/sh
# A standard TeX Live or MiKTeX installation suffices. No shell escape is used.
set -eu
cd "$(dirname "$0")"
mkdir -p build
export SOURCE_DATE_EPOCH=1793059200
export FORCE_SOURCE_DATE=1
for pass in 1 2 3; do
  pdflatex -no-shell-escape -interaction=nonstopmode -halt-on-error -output-directory=build collective_central_band.tex
done
cp build/collective_central_band.pdf collective_central_band.pdf
