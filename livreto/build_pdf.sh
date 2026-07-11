#!/usr/bin/env bash
# Gera livreto.pdf a partir do HTML já buildado.
#
#   bash livreto/build_pdf.sh
#
# Por que aqui e não em runtime: o SeuCondomínio gera o PDF sob demanda (Gotenberg,
# cacheado pelo hash do HTML). Este site é estático (GitHub Pages, sem runtime), então
# o PDF é um artefato de build — commitado. Consequência: ao mudar o conteúdo é preciso
# rodar os DOIS (`build.py` e depois este). Se esquecer, o PDF fica velho em silêncio.
#
# --print-to-pdf respeita o `@media print` (as 3 travas estão em build.py > CSS).
# --no-pdf-header-footer tira o "about:blank / data" que o Chrome carimba por padrão.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
HTML="$ROOT/livreto/index.html"
PDF="$ROOT/livreto.pdf"

[ -f "$HTML" ] || { echo "HTML não existe — rode 'python3 livreto/build.py' antes."; exit 1; }

# serve local: file:// quebra as imagens absolutas (/assets/...) do livreto
python3 -m http.server 8891 --directory "$ROOT" >/dev/null 2>&1 &
SRV=$!
trap 'kill $SRV 2>/dev/null || true' EXIT
sleep 1

google-chrome \
  --headless=new \
  --disable-gpu \
  --no-sandbox \
  --no-pdf-header-footer \
  --print-to-pdf="$PDF" \
  --virtual-time-budget=10000 \
  "http://localhost:8891/livreto/" >/dev/null 2>&1

[ -s "$PDF" ] || { echo "PDF saiu vazio."; exit 1; }
echo "[livreto] $PDF — $(du -h "$PDF" | cut -f1)"
