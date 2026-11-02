#!/usr/bin/env sh
set -eu
cd "$(dirname "$0")"
mkdir -p build
pdflatex -no-shell-escape -interaction=nonstopmode -halt-on-error -file-line-error -output-directory=build mean_adapted_interface_bounds.tex
pdflatex -no-shell-escape -interaction=nonstopmode -halt-on-error -file-line-error -output-directory=build mean_adapted_interface_bounds.tex
cp build/mean_adapted_interface_bounds.pdf mean_adapted_interface_bounds.pdf
