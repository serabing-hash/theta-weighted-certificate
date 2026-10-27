#!/bin/sh
# Standard TeX Live or MiKTeX build; no shell escape or external data.
set -eu
cd "$(dirname "$0")"
mkdir -p build
pdflatex -no-shell-escape -interaction=nonstopmode -halt-on-error -output-directory=build signed_localization.tex
pdflatex -no-shell-escape -interaction=nonstopmode -halt-on-error -output-directory=build signed_localization.tex
pdflatex -no-shell-escape -interaction=nonstopmode -halt-on-error -output-directory=build signed_localization.tex
cp build/signed_localization.pdf signed_localization.pdf
