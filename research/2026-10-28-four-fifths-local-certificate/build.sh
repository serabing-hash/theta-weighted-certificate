#!/bin/sh
set -eu
cd "$(dirname "$0")"
pdflatex -no-shell-escape -interaction=nonstopmode -halt-on-error prime_gamma_local_certificate.tex
pdflatex -no-shell-escape -interaction=nonstopmode -halt-on-error prime_gamma_local_certificate.tex
# Manuscript only; no numerical producer or certificate replay is invoked.
