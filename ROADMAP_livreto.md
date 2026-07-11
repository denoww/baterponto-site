# Roadmap — Livreto do baterponto

> Peça de vendas do comercial. Vive como página pública (`/livreto`) + PDF baixável
> (`/livreto.pdf`). Documento de vida longa.
> **Você só edita `livreto/content.py` e dá push** — o HTML e o PDF se regeneram no CI
> (`.github/workflows/livreto.yml`), que commita o espelho. Playbook operacional em
> [`livreto/CLAUDE.md`](livreto/CLAUDE.md).

## Princípios (não negociáveis)

- **Zero prova social.** O produto é novo e não há base pública. Vende-se a **dor** e o
  **mecanismo** (NSR na tela no ato, registro imutável), nunca o tamanho. Regra vem do
  `pack.yml > prova_social` do spinoff.
- **Só o que roda em produção.** O que não existe hoje vai para o capítulo *"O que o baterponto
  não faz"* — nunca vender roadmap como pronto.
- **A prova serve aos dois lados.** O funcionário nunca é tratado como suspeito. O ângulo é
  simetria (ninguém apaga nada, nem a gente), não vigilância.
- **A cor vem do produto** (fotos vibrantes, campo de cor saturado, tela do app), não de fundo
  colorido — padrão Apple.
- **Concorrente não tem nome.** É "relógio de parede", "cartão e planilha", "app que cobra por faixa".

## Onda 0 — As-built (FEITO · jul/2026)

- Página Apple long-scroll com 9 capítulos: a batida, a prova (NSR), o mundo real (offline/geofence),
  o espelho, para quem é, preço, **o que ele não faz**, a lei (REP-P/LGPD), lineup.
- 3 storyboards de fluxo em line-art SVG (batida, offline, correção).
- Dípticos "a pessoa batendo + a tela reconhecendo o rosto" (foto = gpt-image-1, UI = HTML/CSS).
- Rota `/livreto` + `/livreto.pdf` + botão de download. Versão carimbada no rodapé (data + hash).
- **Espelho automático em CI** ✅ — inclusive trava anti-PDF-em-branco e gate por fingerprint
  de conteúdo (o PDF do Chrome não é determinístico).

## Onda 1 — Manutenção de conteúdo

- **Feature nova entrou em prod** → 1 tile no lineup + 1 card no capítulo. Se for fluxo, um
  storyboard em `BOARDS`.
- **Saiu do "não faz"** (ex.: push, eSocial, integração de folha) → tirar do capítulo de
  honestidade e virar card. **Nunca antes de rodar em produção.**
- **Preço mudou** → mudar aqui **e no `pack.yml` do spinoff no mesmo dia** (ele alimenta ads,
  carrossel e outreach — preço errado ali *sai*).

## Onda 2 — Medir e segmentar

- **Variantes por público** — hoje há **um** livreto. O SeuCondomínio virou *profile-driven*
  (`/livreto/instalador`, `/livreto/financeiro`…). Aqui os recortes naturais do ICP seriam:
  **obra** (campo, sem sinal, apontamento por centro de custo), **saúde** (plantão/escala),
  **comércio** (turnos), **contador/RH** (compliance e prova em audiência).
- **Analytics** de leitura: quantos abrem, até onde rolam, cliques no CTA (UTM por origem).
- **CTA rastreável**: `wa.me` com texto pré-preenchido por variante (hoje já tem um texto fixo).

## Onda 3 — Elevar

- **Calculadora de economia** no livreto (a landing já tem a de preço) — custo do relógio de
  parede + horas de RH × equipe, levando ao WhatsApp com o número.
- **Vídeo curto** no hero (o spinoff já tem um spec de pitch 48s no foundry).
- Storyboards animados (o reveal já existe; animar o traço on-scroll).
- **A/B de manchete.**

## Onda 4 — Automatizar e white-label

- **Aviso no Telegram** quando o espelho regenerar (hoje o CI é silencioso quando dá certo).
- **Livreto white-label** por cliente/parceiro (injeta logo + cores) — casa com o white-label do
  app, que hoje é **build por flavor**, não self-service (não prometer).
- i18n (es-419).

## Dívidas conhecidas

- **A trava anti-PDF-em-branco só olha as páginas 1 e 5.** Uma quebra do `@media print` que
  afete só o miolo passaria batido.
- **O livreto tem um só perfil.** O ICP é largo (obra × clínica × loja × escritório) e o
  conteúdo é genérico para todos.
- **As fotos são revisadas por humano, no zoom.** Não há teste automatizado que impeça uma
  geração futura de sair torta — só as travas de prompt em
  `~/workspace/foundry/projeto/scripts/lib/baterponto-arte.ts` e o checklist de revisão.

## Distribuição (comercial)

- Link no rodapé de e-mail e proposta. QR em material impresso.
- **Preferir o link ao PDF anexado** — sempre atualizado, rastreável, 1 clique pro WhatsApp.
- O PDF é para quando o cliente pede offline.
