#!/bin/sh
# Document-only compilation. No numerical research, external data, or network.
set -eu
cd "$(dirname "$0")"
mkdir -p build
for pass in 1 2 3; do
  pdflatex -no-shell-escape -interaction=nonstopmode -halt-on-error \
    -output-directory=build theta_weighted_spectral_synthesis_v1_3.tex > "build/pass-$pass.log" 2>&1
done
cp build/theta_weighted_spectral_synthesis_v1_3.pdf theta_weighted_spectral_synthesis_v1_3.pdf
