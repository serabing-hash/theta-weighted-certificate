#!/bin/sh
set -eu
cd "$(dirname "$0")"
pdflatex -no-shell-escape -interaction=nonstopmode -halt-on-error prime_defect_note.tex
pdflatex -no-shell-escape -interaction=nonstopmode -halt-on-error prime_defect_note.tex
# Manuscript build only; no numerical producer or arithmetic script is run.
