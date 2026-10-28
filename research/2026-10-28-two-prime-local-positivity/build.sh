#!/bin/sh
set -eu
cd "$(dirname "$0")"
pdflatex -no-shell-escape -interaction=nonstopmode -halt-on-error two_prime_certificate.tex
pdflatex -no-shell-escape -interaction=nonstopmode -halt-on-error two_prime_certificate.tex
# This script compiles the manuscript only. It does not execute the certificate producer.
