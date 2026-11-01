#!/bin/sh
# Compile the manuscript only; no numerical research or external data.
set -eu
cd "$(dirname "$0")"
mkdir -p build
for pass in 1 2 3; do
  pdflatex -no-shell-escape -interaction=nonstopmode -halt-on-error \
    -output-directory=build theta_half_state_obstructions_v1.tex > "build/pass-$pass.log" 2>&1
done
cp build/theta_half_state_obstructions_v1.pdf theta_half_state_obstructions_v1.pdf
