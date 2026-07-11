# Livreto do baterponto — playbook

Peça de vendas do comercial: página pública (`/livreto`) + PDF baixável (`/livreto.pdf`).
Documento de vida longa. Roadmap: [`../ROADMAP_livreto.md`](../ROADMAP_livreto.md).

Herda a doutrina do livreto do SeuCondomínio (`~/workspace/seucondominio/livreto/CLAUDE.md`),
mas **na marca do baterponto e no domínio dele** — o `pack.yml` do spinoff define o produto
como "isolado, **fora do nicho condomínio**", então a peça não vive sob `seucondominio.com.br`.

## A regra de ouro (o "espelho")

> **Edite `content.py` e dê push. Só isso.**
> O HTML e o PDF se regeneram sozinhos no CI e o bot commita o espelho.

- **NÃO rode `build.py` nem `build_pdf.sh` na mão.** Se rodar, o CI só confirma que já estava
  em dia. Se esquecer, não acontece nada de ruim — o CI faz.
- O espelho é o workflow [`.github/workflows/livreto.yml`](../.github/workflows/livreto.yml).

**Por que CI e não runtime:** o SeuCondomínio gera o PDF sob demanda (Gotenberg, cacheado pelo
hash do HTML). Isso exige servidor. Este site é **estático** (GitHub Pages, sem runtime), então
o espelho acontece no CI. As duas restrições que fizeram *eles* descartarem CI (branch protection
no master + ausência de Chromium na imagem de prod) **não existem aqui**.

**O que o CI faz:**
1. gera o HTML (`build.py`)
2. compara um **fingerprint do conteúdo** (`livreto/.espelho.sha` = sha do HTML + todos os assets)
3. só refaz o PDF se o conteúdo mudou
4. **abre o PDF e barra o build se alguma página sair em branco**
5. commita `index.html` + `livreto.pdf` + `.espelho.sha`

## Onde editar (nunca no HTML gerado)

| Quero mudar | Arquivo |
|---|---|
| Texto/dados (cards, listas, storyboards, tiles, preço) — **95% das mudanças** | `content.py` |
| Um capítulo (composição de blocos), CSS, print CSS | `build.py` |
| Cenas dos storyboards (line-art SVG) | `build.py` → `SCENES` |
| Fotos | ver "Imagens" no [`../CLAUDE.md`](../CLAUDE.md) |

`livreto/index.html` e `livreto.pdf` são **gerados** — nunca edite à mão (o CI sobrescreve).

## Conteúdo é aterrado (não invente)

Fonte da verdade, nesta ordem: **o site** → `pack.yml` do spinoff
(`~/workspace/foundry/projeto/packages/spinoffs/baterponto/pack.yml`) → o app
(`~/workspace/baterponto`).

Regras de copy que vêm do `pack.yml > comunicacao` (**não negociáveis**):

- **PROIBIDO prova social.** Nada de "X empresas", "Y mil funcionários", "99% de acerto".
  O produto é novo, não há base pública. Vende-se a **dor** e o **mecanismo**, nunca o tamanho.
- **Nunca citar concorrente pelo nome.** Use "relógio de parede", "cartão e planilha",
  "app que cobra por faixa".
- **O funcionário não é suspeito.** O ângulo é **prova para os dois lados**, nunca vigilância.
- **A empresa não "apaga" nem "corrige" batida** — ela **aprova um pedido**.
- **O funcionário não "escolhe"** entrada/saída — quem classifica é o backend.
- **Nunca prometer** eSocial, folha, push ou integração pronta com folha
  (→ é o capítulo "O que o baterponto não faz", que vem de `pack.yml > nao_features`).

**Se o preço mudar no site, atualize o `pack.yml` no mesmo dia.** Ele alimenta ads, carrossel e
outreach — preço errado ali não fica parado, ele **sai**. (Já aconteceu: o pack passou semanas
dizendo "grátis até 3 pessoas" depois que o site baixou para 2.)

## Pegadinhas (quebram em silêncio)

- **`@media print` — as três travas.** Mexer aqui quebra o PDF sem erro nenhum:
  1. `.rev{opacity:1}` — **sem isto o PDF sai EM BRANCO** (o reveal nunca dispara sem scroll).
  2. `print-color-adjust:exact` — sem isto hero/CTA/fotos saem sem cor.
  3. `break-inside:avoid` **só nas unidades atômicas** (card, painel). Nunca por capítulo —
     gera páginas quase vazias.
  4. `@page{size:A4}` — sem isto o Chrome imprime em **Letter** (padrão americano).
  → O CI tem uma trava para o item 1: mede o desvio-padrão das páginas 1 e 5. Página em branco
    dá desvio 0; página real dá ~26.000. Mas ele **só olha as páginas 1 e 5** — uma quebra no
    meio do documento passaria.

- **Traço de SVG.** Use `stroke` explícito no elemento. (No repo original, classes utilitárias
  `.s`/`.w` forçavam `stroke:none` e o traço sumia calado.)

- **O PDF do Chrome não é determinístico.** Ele carimba `CreationDate`/`ModDate`, então dois
  builds do *mesmo* conteúdo dão bytes diferentes. É por isso que o gate do CI compara um
  fingerprint do **conteúdo**, não os bytes do PDF — sem isso, o CI commitaria 1,5 MB de binário
  a cada push, para sempre.

- **O fingerprint precisa ser reproduzível.** `cat assets/*` **não era**: a ordem do glob depende
  da colação do locale (em `LC_ALL=C`, `faixa-mob.jpg` vem antes de `faixa.jpg`; em `en_US` a
  pontuação é ignorada e inverte). Hoje é `find + LC_ALL=C sort + sha por arquivo`. Para auditar:

  ```bash
  find livreto/index.html assets -type f | LC_ALL=C sort | xargs sha256sum | sha256sum | cut -c1-16
  # tem que bater com o conteúdo de livreto/.espelho.sha
  ```

- **Gatear o PDF só pelo HTML seria um bug:** trocar uma foto muda o PDF sem mudar uma linha de
  HTML. Por isso o fingerprint inclui `assets/`.

## Conferir localmente (opcional, antes do push)

```bash
python3 livreto/build.py && bash livreto/build_pdf.sh
python3 -m http.server 8899   # abrir localhost:8899/livreto/
pdftoppm -jpeg -r 40 -f 1 -l 3 livreto.pdf /tmp/pg   # olhar 2–3 páginas
```
