#!/bin/sh
# Build docs/explainer.pdf from docs/explainer.md with pandoc and typst.
# Needs pandoc 3.x, typst, and a directory with the DejaVu fonts for the
# symbols (matplotlib ships them: .../matplotlib/mpl-data/fonts/ttf).
#   sh docs/build/build_pdf.sh /path/to/dejavu/fonts
set -e
cd "$(dirname "$0")/.."
FONTS=${1:?font directory with DejaVuSans.ttf}
pandoc explainer.md -o explainer.pdf --pdf-engine=typst --shift-heading-level-by=-1 \
    --metadata-file=build/meta.yaml -H build/head.typ \
    --pdf-engine-opt=--font-path --pdf-engine-opt="$FONTS"
