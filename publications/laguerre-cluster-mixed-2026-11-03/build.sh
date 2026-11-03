#!/bin/sh
set -eu
cd "$(dirname "$0")"
mkdir -p build
if ! kpsewhich pdflatex.fmt >/dev/null 2>&1 || ! kpsewhich article.cls >/dev/null 2>&1; then
 mkdir -p build/tex-runtime
 export TEXINPUTS=".:/usr/share/texlive/texmf-dist/tex//:/usr/share/texmf/tex//:"
 export TFMFONTS="/usr/share/texlive/texmf-dist/fonts/tfm//:/usr/share/texmf/fonts/tfm//:"
 export T1FONTS="/usr/share/texlive/texmf-dist/fonts/type1//:/usr/share/texmf/fonts/type1//:"
 export ENCFONTS="/usr/share/texlive/texmf-dist/fonts/enc//:/usr/share/texmf/fonts/enc//:"
 export VFFONTS="/usr/share/texlive/texmf-dist/fonts/vf//:/usr/share/texmf/fonts/vf//:"
 export TEXFORMATS="$PWD/build/tex-runtime:"
 export TEXFONTMAPS="$PWD/build/tex-runtime:/usr/share/texlive/texmf-dist/fonts/map//:/usr/share/texmf/fonts/map//:"
 cat /usr/share/texmf/fonts/map/dvips/lm/lm.map /usr/share/texlive/texmf-dist/fonts/map/dvips/amsfonts/symbols.map /usr/share/texlive/texmf-dist/fonts/map/dvips/amsfonts/euler.map /usr/share/texlive/texmf-dist/fonts/map/dvips/rsfs/rsfs.map > build/tex-runtime/pdftex.map
 if test ! -f build/tex-runtime/pdflatex.fmt; then (cd build/tex-runtime && pdftex -ini -etex -no-shell-escape -interaction=nonstopmode -halt-on-error -jobname=pdflatex '\pdfoutput=1\input latex.ltx'); fi
fi
for pass in 1 2 3; do pdflatex -no-shell-escape -interaction=nonstopmode -halt-on-error -file-line-error -output-directory=build cluster_mixed.tex; done
cp build/cluster_mixed.pdf cluster_mixed.pdf
