#!/bin/sh
# Build with a standard TeX Live or MiKTeX installation.
set -eu
cd "$(dirname "$0")"
mkdir -p build
pdflatex -no-shell-escape -interaction=nonstopmode -halt-on-error -output-directory=build directional_mean.tex
pdflatex -no-shell-escape -interaction=nonstopmode -halt-on-error -output-directory=build directional_mean.tex
pdflatex -no-shell-escape -interaction=nonstopmode -halt-on-error -output-directory=build directional_mean.tex
cp build/directional_mean.pdf directional_mean.pdf
