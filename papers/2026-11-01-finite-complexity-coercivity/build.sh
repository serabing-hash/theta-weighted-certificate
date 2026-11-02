#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
export SOURCE_DATE_EPOCH=1793491200
HERE=$(pwd)
# Local-only fallback for read-only TeX trees without generated format caches.
if ! kpsewhich article.cls >/dev/null 2>&1 && [ -d /usr/share/texlive/texmf-dist ]; then
  mkdir -p .texcache qa
  export TEXMF="{$HERE/.texcache,/etc/texmf,/usr/share/texmf,/usr/share/texlive/texmf-dist}"
  export TEXMFVAR="$HERE/.texcache" TEXMFCONFIG="$HERE/.texcache"
  export TEXINPUTS=".:/etc/texmf/tex//:/usr/share/texmf/tex//:/usr/share/texlive/texmf-dist/tex//:"
  export TEXFORMATS="$HERE/.texcache:"
  export TEXFONTMAPS="$HERE/.texcache:/usr/share/texmf/fonts/map//:/usr/share/texlive/texmf-dist/fonts/map//:"
  cat /usr/share/texmf/fonts/map/dvips/lm/lm.map \
      /usr/share/texlive/texmf-dist/fonts/map/dvips/amsfonts/cm.map \
      /usr/share/texlive/texmf-dist/fonts/map/dvips/amsfonts/symbols.map \
      /usr/share/texlive/texmf-dist/fonts/map/dvips/amsfonts/latxfont.map \
      /usr/share/texlive/texmf-dist/fonts/map/dvips/amsfonts/euler.map > .texcache/pdftex.map
  if [ ! -f .texcache/pdflatex.fmt ]; then
    (cd .texcache; pdftex -no-shell-escape -ini -jobname=pdflatex -progname=pdflatex "*pdflatex.ini") > qa/format-build.log 2>&1
  fi
fi
export FORCE_SOURCE_DATE=1
mkdir -p qa/pages
pdflatex -no-shell-escape -interaction=nonstopmode -halt-on-error -file-line-error finite_complexity_coercivity.tex > qa/build-pass1.txt
pdflatex -no-shell-escape -interaction=nonstopmode -halt-on-error -file-line-error finite_complexity_coercivity.tex > qa/build-pass2.txt
pdfinfo finite_complexity_coercivity.pdf > qa/pdfinfo.txt
pdftotext -layout finite_complexity_coercivity.pdf qa/extracted_text.txt
pdftoppm -r 110 -png finite_complexity_coercivity.pdf qa/pages/page
printf 'Built finite_complexity_coercivity.pdf and QA page renders.\n'
