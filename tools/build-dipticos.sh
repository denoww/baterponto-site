#!/usr/bin/env bash
# Monta os dípticos "quadro 1 = a pessoa tirando a selfie · quadro 2 = a tela reconhecendo".
#
#   bash tools/build-dipticos.sh
#
# Pipeline (doutrina do foundry: foto = IA, UI = código):
#   1. faces.py acha o rosto na foto (haar cascade) — não se chuta coordenada
#   2. recorta um retrato em volta do rosto, no aspecto da tela, com o rosto no
#      ponto exato onde o oval da UI vai cair
#   3. Chrome headless renderiza tools/mockup/phone.html com esse rosto dentro do oval
#   4. ImageMagick cola foto + tela lado a lado
#
# O rosto do quadro 2 é recortado do quadro 1 ⇒ é SEMPRE a mesma pessoa. Se fosse
# gerado à parte, seria outro rosto e a peça mentiria.
set -euo pipefail

SRC="/home/rodrigo/workspace/foundry/projeto/output/baterponto/creative/selfie"
REPO="$(cd "$(dirname "$0")/.." && pwd)"
OUT="$REPO/assets"
TMP=$(mktemp -d); trap 'rm -rf "$TMP"' EXIT
PY=/tmp/cvenv/bin/python

# proporção da tela do mockup (interna) — o recorte tem que nascer nela
ASPECT=0.477
# O oval vive em top:26%, altura 38% da tela ⇒ seu CENTRO está em 45%.
ALVO_Y=0.45
# O haar-cascade mede só o ROSTO (testa→queixo), não o crânio com cabelo. Se eu
# pedir 30% da tela pro box do rosto, a cabeça inteira estoura o oval. 21% deixa
# a cabeça toda dentro, com folga — que é o que o app pede ("alinhe o rosto no oval").
ALVO_H=0.21

recorta_rosto() {           # $1=slug  → $TMP/face-$1.jpg
  local slug=$1 img="$SRC/$1.png"
  read -r _ px py _ rest < <($PY "$REPO/tools/faces.py" "$img")
  local fw fh fx fy
  eval "$(echo "$rest" | sed -E 's/face=([0-9]+)x([0-9]+)@([0-9]+),([0-9]+)/fw=\1 fh=\2 fx=\3 fy=\4/')"
  local W H
  W=$(identify -format "%w" "$img"); H=$(identify -format "%h" "$img")

  python3 - "$img" "$TMP/face-$slug.jpg" "$W" "$H" "$fx" "$fy" "$fw" "$fh" "$ASPECT" "$ALVO_H" "$ALVO_Y" <<'PY'
import subprocess, sys
img,out,W,H,fx,fy,fw,fh,asp,alvo_h,alvo_y = sys.argv[1:12]
W,H,fx,fy,fw,fh = map(int,(W,H,fx,fy,fw,fh)); asp,alvo_h,alvo_y = map(float,(asp,alvo_h,alvo_y))
cx, cy = fx+fw/2, fy+fh/2
ch = round(fh/alvo_h)                 # altura do recorte p/ o rosto valer alvo_h da tela
cw = round(ch*asp)
x0 = round(cx-cw/2); y0 = round(cy-alvo_y*ch)

# BUG QUE ISSO CORRIGE: o rosto costuma ficar perto do TOPO da foto, então y0 sai
# NEGATIVO — o recorte pede pixels que não existem acima dela. Clampar em 0 (o que
# eu fazia) empurra a cabeça pra cima e ela sai do oval. A saída certa é compor a
# foto sobre uma tela do tamanho do recorte, em offset negativo, e preencher o que
# falta com a cor do próprio fundo (é um campo de cor liso — ninguém percebe).
cor = subprocess.run(["convert", img, "-format", "%[pixel:p{2,2}]", "info:"],
                     capture_output=True, text=True, check=True).stdout.strip()
subprocess.run(["convert", "-size", f"{cw}x{ch}", f"xc:{cor}",
                img, "-geometry", f"{-x0:+d}{-y0:+d}", "-composite",
                "-resize", "538x1128!", "-quality", "92", out], check=True)
PY
}

# Renderiza o aparelho com fundo transparente e o compõe sobre um gradiente feito
# aqui. (O Chrome pinta branco abaixo do documento no screenshot; em vez de brigar
# com o CSS, o painel nasce no ImageMagick.)
tela() {                    # $1=slug $2=cor-topo $3=cor-base $4=WxH do painel (usa $NOME)
  local slug=$1 c1=$2 c2=$3 dim=$4
  google-chrome --headless=new --disable-gpu --no-sandbox --hide-scrollbars \
    --default-background-color=00000000 \
    --force-device-scale-factor=2 --window-size=1000,1400 \
    --screenshot="$TMP/raw-$slug.png" \
    "file://$REPO/tools/mockup/phone.html?face=file://$TMP/face-$slug.jpg&nome=$NOME" \
    >/dev/null 2>&1
  [ -s "$TMP/raw-$slug.png" ] || { echo "tela $slug falhou"; exit 1; }

  local W=${dim%x*} H=${dim#*x}
  local alvo_h=$(( H * 88 / 100 ))          # o aparelho ocupa 88% da altura do painel
  convert "$TMP/raw-$slug.png" -trim +repage -resize "x${alvo_h}" "$TMP/fone-$slug.png"
  convert -size "$dim" \
      "gradient:#${c1}-#${c2}" -rotate 0 \
      "$TMP/fone-$slug.png" -gravity center -composite \
      "$TMP/tela-$slug.png"
}

J="-strip -interlace Plane -sampling-factor 4:2:0 -quality 86"

# ---------- díptico 1: a FAIXA (full-bleed, 1600x1067) ----------
recorta_rosto sf-faixa
NOME=Marina; tela sf-faixa 2b0d63 12042e 800x1067
convert "$SRC/sf-faixa.png" -resize 800x1067^ -gravity center -extent 800x1067 "$TMP/l.png"
convert "$TMP/l.png" "$TMP/tela-sf-faixa.png" +append $J "$OUT/faixa.jpg"
echo "[dip] faixa.jpg"

# ---------- o mesmo díptico EMPILHADO, pro celular ----------
# Lado a lado num viewport de 412px, cada quadro fica com ~200px e a tela do app
# vira um borrão — some justamente o NSR, que é o que a peça vende. Empilhado, o
# aparelho ocupa a largura inteira e volta a ser legível. Servido via <picture>.
NOME=Marina; tela sf-faixa 2b0d63 12042e 900x1000
convert "$SRC/sf-faixa.png" -resize 900x620^ -gravity north -extent 900x620 "$TMP/t.png"
convert "$TMP/t.png" "$TMP/tela-sf-faixa.png" -append $J "$OUT/faixa-mob.jpg"
echo "[dip] faixa-mob.jpg (empilhado)"

# ---------- díptico 2: o TILE da prova de vida (900x900) ----------
recorta_rosto sf-tile
NOME=Diego;  tela sf-tile 3b1180 160a33 450x900
convert "$SRC/sf-tile.png" -resize 450x900^ -gravity center -extent 450x900 "$TMP/l.png"
convert "$TMP/l.png" "$TMP/tela-sf-tile.png" +append $J "$OUT/bento-selfie.jpg"
echo "[dip] bento-selfie.jpg"

# ---------- fotos simples (pose corrigida: selfie, não "digitando") ----------
convert "$SRC/sf-hero.png" -resize 1600x $J "$OUT/hero.jpg";                echo "[foto] hero.jpg"
convert "$SRC/sf-og.png"   -resize 1200x800^ -gravity center -extent 1200x630 $J "$OUT/og.jpg"; echo "[foto] og.jpg"
for s in cafe clinica obra escritorio; do
  convert "$SRC/sf-$s.png" -resize 700x1050^ -gravity center -extent 700x1050 $J "$OUT/setor-$s.jpg"
  echo "[foto] setor-$s.jpg"
done

echo; ls -la "$OUT"/*.jpg | awk '{printf "%-28s %s KB\n", $9, int($5/1024)}'
