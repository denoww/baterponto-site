# baterponto-site — playbook

Site institucional do **baterponto** (ponto eletrônico no celular do funcionário).
Estático, sem build de framework. Servido por **GitHub Pages** em `https://www.baterponto.app`.

O produto é uma **spinoff do foundry**, definida como "produto isolado, **fora do nicho
condomínio**" — pack em `~/workspace/foundry/projeto/packages/spinoffs/baterponto/pack.yml`
(fonte da verdade de posicionamento, ICP, preço, não-features e regras de copy).
App Flutter em `~/workspace/baterponto`.

## Deploy

> **Deploy = `git push`.** Não existe passo separado.

GitHub Pages publica o `main` direto. Leva ~40–60s + cache do CDN. Para conferir que produção
já serve o seu commit (não confie no "subiu"):

```bash
diff <(curl -s https://www.baterponto.app/index.html) index.html && echo "prod == HEAD"
```

**Domínio:** o `CNAME` do repo é `www.baterponto.app` — é ele que define o host canônico.
O apex (`baterponto.app`) **redireciona 301 para o www** (HTTP e HTTPS), e o *Enforce HTTPS*
está ligado. Se um dia inverter isso, lembre de atualizar junto: `canonical`, `og:url`,
`sitemap.xml` e `robots.txt` — senão eles apontam para uma URL que redireciona.

## IndexNow — a chave que faltava na raiz

O arquivo `7b3e9c1a4f6d24b8e0a5c7d9f1234567.txt` na raiz é o token de posse do **IndexNow**:
ele prova ao Bing que este host é nosso, e é o que permite AVISAR o buscador de uma página
nova em vez de esperar o rastreio. ⛔ Não apagar, não renomear, não esconder — o protocolo
exige que ele seja público, e o valor é o mesmo em todos os nossos hosts, por design.

⚠️ **Ele só chegou aqui em 24/09/2026.** Até então a chave existia apenas nos hosts servidos
pelo ERP (os blogs, via `BlogRootFiles`), e os SITES respondiam 404 nela — ou seja, nenhuma
página deste site jamais pôde ser submetida ao IndexNow. O Bing é o índice que o ChatGPT
consulta, e o ChatGPT é de onde vêm ~50% das sessões das marcas
(`ROADMAP_multi_produto.md` §8.6), então isso não é detalhe de SEO: é o canal principal.

Para avisar o Bing de uma página nova ou alterada deste site:

```bash
curl -s -X POST https://api.indexnow.org/IndexNow \
  -H 'Content-Type: application/json' \
  -d '{"host":"www.baterponto.app","key":"7b3e9c1a4f6d24b8e0a5c7d9f1234567",
       "keyLocation":"https://www.baterponto.app/7b3e9c1a4f6d24b8e0a5c7d9f1234567.txt",
       "urlList":["https://www.baterponto.app/a-pagina"]}' -w '%{http_code}\n'
```

`200` ou `202` = aceito. `403` = a chave não está respondendo na raiz (confira o link acima
antes de investigar qualquer outra coisa).

## Estrutura

| O quê | Onde |
|---|---|
| Landing (tudo num arquivo: CSS + HTML + JS) | `index.html` |
| Livreto de vendas (gerado) | `livreto/` → ver [`livreto/CLAUDE.md`](livreto/CLAUDE.md) |
| Política de privacidade | `privacidade.html` |
| Imagens finais (JPEG otimizado) | `assets/` |
| Mockup da tela do app + pipeline de díptico | `tools/` |

## A demo interativa da landing (não quebre)

A seção "O app" **não é um vídeo** — é o app rodando: relógio ao vivo, câmera real
(`getUserMedia`) com prova de vida de 2 passos, comprovante com NSR sequencial, calculadora de
preço e FAQ. Tudo em JS puro no fim do `index.html`.

**Se mexer no HTML, preserve os IDs** — o JS os procura por `getElementById`:
`relogio`, `data`, `estado`, `proxTipo`, `cfgSelfie`, `btnBater`, `pills`, `fitaArea`,
`fTipo`, `fQuando`, `fNsr`, `fSelfie`, `fLive`, `fThumbs`, `cam*`, `cRange`, `cPessoas`,
`cTotal`, `cNota`.

Teste rápido no browser (deve bater a entrada e imprimir o NSR):

```js
document.getElementById('cfgSelfie').checked = false;   // pula a câmera
document.getElementById('btnBater').click();
// depois: fNsr deve ter incrementado e fitaArea deve ter a classe 'aberta'
```

**Privacidade:** a imagem da selfie **nunca sai do navegador** (`getUserMedia` → `<canvas>`).
Não introduza upload aqui — a página afirma isso ao usuário.

## Design — padrão Apple

Os números vieram do CSS de produção da apple.com, não de estimativa:

- **Tipografia**: tracking **não é monotônico** — `-.015em` em 80px, ~zero em 40px, **positivo**
  (`+.011em`) em 21px, e `-.022em` em 17px (abaixo de 20px a Apple troca SF Pro Display por Text).
  Peso de título é **600**, nunca 700. Stack: `-apple-system` (renderiza SF Pro de verdade em
  Apple) com Inter de fallback.
- **Superfícies**: branco ↔ `#f5f5f7` ↔ preto, alternando. **Sem borda entre seções** — o
  divisor é o contraste de fundo.
- **Cards**: radius 28px e **`box-shadow: none`** (a separação é por contraste, não por sombra).
- **Botões**: pill `border-radius: 980px`, padding 12/22, peso 400; hover só troca a cor.
- **Movimento**: `opacity 0→1` + `translateY(30px)→0`, **900ms**, `cubic-bezier(.45,0,.55,1)`,
  stagger 150ms, dispara uma vez (IntersectionObserver + `unobserve`).
- **Respiro**: 144 / 120 / 112px por seção.

## Imagens

**Doutrina (do foundry): foto = gpt-image-1, UI = HTML/CSS.** Nunca peça a interface ao gerador —
ele aluciona texto ("Entrda 09:2A") e borra a tipografia.

- **Geradores** (no foundry, `scripts/`): `gen-baterponto-selfie.ts` (as pessoas batendo ponto) e
  `gen-baterponto-apple-images.ts` (os 3 tiles onde o gesto não é o assunto).
  As travas de prompt são compartilhadas em `scripts/lib/baterponto-arte.ts` — **importe, não
  reescreva**. Cada uma existe porque uma imagem foi para o ar errada.
- **Díptico** (`tools/build-dipticos.sh`): recorta o rosto da foto (haar cascade,
  `tools/faces.py`) → renderiza `tools/mockup/phone.html` no Chrome headless com esse rosto
  dentro do oval → cola os dois quadros. **O rosto do quadro 2 sai do quadro 1** — é sempre a
  mesma pessoa. Gerar o rosto à parte daria outra pessoa e a peça mentiria.

**Antes de aprovar qualquer foto gerada: AMPLIE o celular.**
No tamanho da página o erro é invisível — foi assim que uma foto com o **celular de costas para o
próprio dono** (tela apontando para a câmera) foi para o ar e o cliente viu. Regra que ficou:
**quanto mais fechado o plano, maior o risco de o modelo girar o aparelho.**

## Cicatrizes (bugs reais desta base)

- **Foto de fundo atrás de texto no mobile** → vira um borrão sujo. O hero e a faixa fazem
  `column-reverse`: texto em campo sólido, foto inteira embaixo. Não "resolva" com opacidade.
- **Carrossel horizontal trava o scroll.** O espectro de setores era `overflow-x:auto` +
  `scroll-snap: x mandatory` com cards de ~600px: o dedo subia **sempre** dentro de um contêiner
  que rola na horizontal, e o Chrome no Android prendia o gesto. Virou grade 2×2. **Evite
  scroll-snap horizontal em blocos altos.**
- **Díptico lado a lado no celular** deixa a tela do app ilegível (~200px por quadro) e some o NSR
  — que é o que a peça vende. Abaixo de 820px entra a versão **empilhada** via `<picture>`
  (`faixa-mob.jpg`).
- **Escopo de CSS vaza**: `.ft a{text-decoration:underline}` grifou o logotipo do rodapé.

## Como verificar (o que salvou esta base)

Não confie em "parece certo" — **rode e confira contra uma expectativa concreta**:

- **Layout**: screenshot em 1440px **e** em 412px. Vários bugs só existiam no mobile.
- **Scroll travando**: só aparece com **gesto**, não em screenshot. Cheque no DOM se algum
  contêiner captura o gesto: `el.scrollWidth > el.clientWidth` com `overflow-x` rolável.
- **Produção**: compare o **hash** do artefato local com o que o servidor entrega. "O commit
  subiu" não é o mesmo que "o CDN está servindo".
- **CI**: um workflow que nunca foi executado não vale nada. Os 4 bugs do espelho do livreto
  (ImageMagick ausente, corrida de push, rebase sujo, fingerprint dependente de locale) só
  apareceram **rodando**.

## Regra de copy que vale para as 5 marcas

### ⚠️ Não-feature entregue: a regra sai no MESMO dia

O guard existe para impedir que a copy prometa o que não existe. No dia em que a coisa passa
a existir, **ele passa a proibir a verdade** — e o sintoma é o CI reprovando quem tenta
consertar, o que faz a pessoa desistir e o texto errado ficar.

Caso real (24/09/2026): o app do atendeaqui foi publicado nas duas lojas em **11/08**. Seis
semanas depois o site ainda dizia "o aplicativo está sendo feito", o livreto dizia "não está
na loja", e **duas regras** — uma no `seo.py` daqui, outra no registry do ERP — bloqueavam a
correção. O bloco `verdades` do mesmo registry, a dois metros dali, dizia o certo.

Ao entregar algo que estava na lista de não-features, o mesmo commit tem de: tirar a linha de
`nao_features` e a regra de `REGRAS_PROIBIDAS` no registry do ERP; tirar a regra equivalente
do `seo.py`; corrigir a copy do site **e do livreto** (`livreto/content.py`); e acrescentar o
que agora existe.

⚠️ Armadilha vizinha, em página de PERGUNTAS: o guard procura o negador nos 80 caracteres
**anteriores** ao termo proibido, e ali o "Não." mora na resposta, depois da pergunta. Aí o
certo é reescrever a pergunta — a regra continua válida.
