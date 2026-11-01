#!/bin/sh
set -eu
cd "$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
mkdir -p build
pdflatex -no-shell-escape -interaction=nonstopmode -halt-on-error -output-directory=build theta_delta_scaled_schur_v1.tex
pdflatex -no-shell-escape -interaction=nonstopmode -halt-on-error -output-directory=build theta_delta_scaled_schur_v1.tex
cp build/theta_delta_scaled_schur_v1.pdf theta_delta_scaled_schur_v1.pdf
