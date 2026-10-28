#!/bin/sh
# Build the manuscript only; never execute the numerical evidence.
set -eu
cd "$(dirname "$0")"
mkdir -p build
for pass in 1 2 3; do
  pdflatex -no-shell-escape -interaction=nonstopmode -halt-on-error \
    -output-directory=build radius_stability.tex > "build/pass-$pass.log" 2>&1
done
cp build/radius_stability.pdf radius_stability.pdf
