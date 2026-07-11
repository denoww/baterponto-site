#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Acha o rosto em cada foto e devolve o object-position que centraliza o rosto
dentro do oval da UI (quadro 2 do díptico).

Por que detectar em vez de chutar coordenadas: cada foto sai com o sujeito num
lugar diferente. Um object-position fixo joga o rosto pra fora do oval — e o
mockup inteiro perde o sentido.

    /tmp/cvenv/bin/python tools/faces.py <img...>

Imprime uma linha por imagem: <arquivo> <pos-x%> <pos-y%> <zoom>
"""
import sys, cv2

casc = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

for path in sys.argv[1:]:
    img = cv2.imread(path)
    if img is None:
        print(f"{path} ERRO", file=sys.stderr); continue
    h, w = img.shape[:2]
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = casc.detectMultiScale(gray, scaleFactor=1.06, minNeighbors=6,
                                  minSize=(int(w * .06), int(w * .06)))
    if len(faces) == 0:
        print(f"{path} SEM_ROSTO", file=sys.stderr); continue

    # o maior rosto é o do sujeito (descarta ruído de fundo)
    x, y, fw, fh = max(faces, key=lambda f: f[2] * f[3])
    cx, cy = x + fw / 2, y + fh / 2

    # object-position em %: onde o ponto (cx,cy) deve encostar na moldura.
    # Fórmula do CSS: a % posiciona o MESMO % da imagem no MESMO % do container.
    px = cx / w * 100
    py = cy / h * 100

    # zoom: o rosto deve ocupar ~52% da altura do oval. O oval tem ~43% da tela.
    # Como a tela é bem mais estreita que a foto, precisamos ampliar.
    alvo = 0.30                      # altura desejada do rosto / altura da tela
    zoom = alvo / (fh / h)
    print(f"{path} {px:.1f} {py:.1f} {zoom:.2f} face={fw}x{fh}@{x},{y}")
