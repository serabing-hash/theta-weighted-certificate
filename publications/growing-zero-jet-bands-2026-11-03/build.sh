#!/usr/bin/env sh
# Document-only build. No research computation, numerical data, or network access.
set -eu
cd "$(dirname "$0")"
mkdir -p build
for source in growing_zero_jet_bands.tex; do
  test -f "$source" || { echo "Missing manuscript source: $source" >&2; exit 1; }
done
if ! command -v pdflatex >/dev/null 2>&1; then
  echo 'Install a working TeX distribution with pdflatex and the packages listed in README.md.' >&2
  exit 1
fi
# Some minimal Debian images ship the complete TeX trees but no configured format
# or font map. Generate those document-engine assets locally, never system-wide.
if ! kpsewhich pdflatex.fmt >/dev/null 2>&1 || ! kpsewhich article.cls >/dev/null 2>&1; then
  test -f /usr/share/texlive/texmf-dist/tex/latex/base/latex.ltx || {
    echo 'The TeX installation lacks a configured pdflatex format; configure TeX locally.' >&2; exit 1;
  }
  mkdir -p build/tex-runtime
  export TEXINPUTS=".:/usr/share/texlive/texmf-dist/tex//:/usr/share/texmf/tex//:"
  export TFMFONTS="/usr/share/texlive/texmf-dist/fonts/tfm//:/usr/share/texmf/fonts/tfm//:"
  export T1FONTS="/usr/share/texlive/texmf-dist/fonts/type1//:/usr/share/texmf/fonts/type1//:"
  export ENCFONTS="/usr/share/texlive/texmf-dist/fonts/enc//:/usr/share/texmf/fonts/enc//:"
  export VFFONTS="/usr/share/texlive/texmf-dist/fonts/vf//:/usr/share/texmf/fonts/vf//:"
  export TEXFORMATS="$PWD/build/tex-runtime:"
  export TEXFONTMAPS="$PWD/build/tex-runtime:/usr/share/texlive/texmf-dist/fonts/map//:/usr/share/texmf/fonts/map//:"
  test -f /usr/share/texmf/fonts/map/dvips/lm/lm.map || {
    echo 'Install the Latin Modern fonts and their TeX font map.' >&2; exit 1;
  }
  cat /usr/share/texmf/fonts/map/dvips/lm/lm.map \
    /usr/share/texlive/texmf-dist/fonts/map/dvips/amsfonts/symbols.map \
    /usr/share/texlive/texmf-dist/fonts/map/dvips/amsfonts/euler.map \
    /usr/share/texlive/texmf-dist/fonts/map/dvips/rsfs/rsfs.map \
    > build/tex-runtime/pdftex.map
  if test ! -f build/tex-runtime/pdflatex.fmt; then
    (cd build/tex-runtime && pdftex -ini -etex -no-shell-escape -interaction=nonstopmode -halt-on-error -jobname=pdflatex '\pdfoutput=1\input latex.ltx')
  fi
fi
pdflatex -no-shell-escape -interaction=nonstopmode -halt-on-error -file-line-error -recorder -output-directory=build growing_zero_jet_bands.tex
pdflatex -no-shell-escape -interaction=nonstopmode -halt-on-error -file-line-error -recorder -output-directory=build growing_zero_jet_bands.tex
pdflatex -no-shell-escape -interaction=nonstopmode -halt-on-error -file-line-error -recorder -output-directory=build growing_zero_jet_bands.tex
cp build/growing_zero_jet_bands.pdf growing_zero_jet_bands.pdf
