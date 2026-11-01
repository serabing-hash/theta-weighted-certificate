#!/bin/sh
# Build the manuscript only. No numerical research or external data is used.
set -eu
cd "$(dirname "$0")"
mkdir -p build
for pass in 1 2; do
  pdflatex -no-shell-escape -interaction=nonstopmode -halt-on-error \
    -output-directory=build theta_confining_pencil_v01.tex > "build/pass-$pass.log" 2>&1
done
cp build/theta_confining_pencil_v01.pdf theta_confining_pencil_v01.pdf
