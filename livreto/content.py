# -*- coding: utf-8 -*-
"""Conteúdo do livreto do baterponto — 95% das mudanças acontecem AQUI.

Fonte da verdade factual, nesta ordem de precedência:
  1. o site https://baterponto.app (repo deste arquivo) — é o mais novo
  2. ~/workspace/foundry/projeto/packages/spinoffs/baterponto/pack.yml
  3. ~/workspace/baterponto (app Flutter + backend)

DIVERGÊNCIAS CONHECIDAS (o site venceu, o pack está velho):
  - grátis até **2** pessoas (o pack.yml ainda diz 3; commit 53ff8d5 baixou pra 2)
  - roxo de marca **#7C3AED** (o pack.yml ainda diz #8E2DDB; commit cc1e7a2 fixou 7C3AED)

REGRAS DE COPY (do pack.yml → comunicacao):
  - PROIBIDO prova social: nada de "X empresas", "Y mil funcionários", "99% de acerto".
    O produto é novo. Vende-se a DOR e o MECANISMO, nunca o tamanho.
  - Nunca citar concorrente pelo nome. Usar "relógio de parede", "cartão e planilha",
    "app que cobra por faixa".
  - O funcionário NÃO é suspeito. O ângulo é PROVA pros dois lados, nunca vigilância.
  - Nunca dizer que a empresa "apaga" ou "corrige" batida no app — ela aprova um PEDIDO.
  - Nunca dizer que o funcionário "escolhe" entrada/saída — quem classifica é o backend.
  - Nunca prometer eSocial, folha, push ou integração pronta com folha.
"""

WA = "https://wa.me/5562996701278"
WA_TXT = "?text=Ol%C3%A1%21%20Vi%20o%20livreto%20do%20baterponto%20e%20quero%20conhecer."
SITE = "https://www.baterponto.app"

# ---------------------------------------------------------------- hero / credo
HERO = {
    "eyebrow": "Livreto",
    "h1": "O ponto bate no celular. A prova sai na hora.",
    "sub": "O funcionário abre o app, confirma o rosto e bate. O registro sai com NSR na "
           "tela dele, no mesmo segundo, e nasce imutável. Sem relógio na parede, sem "
           "cartão de papel, sem planilha no fim do mês.",
}

CREDO = ('Ninguém apaga uma batida. <span class="g">Nem a gente.</span>')

# ---------------------------------------------------------------- storyboards
# (chave, capítulo-cor, título, [(cena, título, legenda)])
BOARDS = {
    "batida": ("roxo", "Da tela ao comprovante, em uns oito segundos", [
        ("app",   "Abre o app",        "O relógio já corre e o app mostra qual é a próxima batida."),
        ("rosto", "Confirma o rosto",  "Só quando a empresa exige: rosto no oval e o desafio de virar."),
        ("toque", "Bate",              "Um toque. O app não escolhe o tipo — quem classifica é o servidor."),
        ("nsr",   "Sai o NSR",         "“Entrada registrada às 09:24 · NSR 418.” Uma frase, um número."),
    ]),
    "offline": ("verde", "Sem sinal, a batida não se perde", [
        ("subsolo", "Bate sem rede",     "Subsolo, elevador, obra sem cobertura. O app aceita a batida."),
        ("cofre",   "Guarda a hora real","A marcação fica no aparelho com a hora em que de fato aconteceu."),
        ("sync",    "Sobe sozinha",      "Voltou o sinal, sincroniza — sem o funcionário fazer nada."),
    ]),
    "correcao": ("ambar", "A correção que a lei permite (e a que ela não permite)", [
        ("pedido",  "O funcionário pede",  "Esqueceu de bater? Ele abre um pedido de correção. Não apaga nada."),
        ("gestor",  "O gestor decide",     "O pedido cai pro gestor, que aprova ou recusa."),
        ("historico","Fica o histórico",   "O antes e o depois ficam registrados. É isso que dá valor à prova."),
    ]),
}

# ---------------------------------------------------------------- capítulos
# (título, descrição, selo)  — selo "" = produção. Nunca vender roadmap como pronto.
BATIDA = [
    ("Uma batida, um toque",
     "O funcionário não escolhe se é entrada, intervalo ou saída. Ele só bate — o servidor "
     "classifica pela jornada dele e pela última marcação. Menos erro, menos discussão.", ""),
    ("Selfie com prova de vida",
     "Quando a empresa exige: rosto no oval e, no modo ativo, um segundo quadro virando o "
     "rosto. É prova de vida de dois passos, não uma foto que qualquer um repete.", ""),
    ("Geofence",
     "Ligado, a marcação guarda se o funcionário estava dentro da área do trabalho no momento "
     "da batida. Fora da área, o gestor vê.", ""),
    ("Apontamento",
     "Quando a operação precisa, a batida entra amarrada a uma obra ou centro de custo.", ""),
    ("Mais de um vínculo",
     "Quem trabalha em duas empresas ou unidades troca no topo da tela e bate no lugar certo. "
     "Cada vínculo tem sua jornada e seu espelho.", ""),
    ("Android e iOS",
     "App em Flutter, roda no celular que o funcionário já tem — inclusive em Android antigo.", ""),
]

PROVA = [
    ("NSR na tela, no ato",
     "Número Sequencial de Registro. Ele aparece pro funcionário no segundo da batida — a prova "
     "não fica trancada num sistema que só o RH abre.", ""),
    ("Registro imutável",
     "A batida nasce imutável. Nem o funcionário nem o gestor apagam. Nem nós.", ""),
    ("Comprovante do trabalhador",
     "Cada batida gera o comprovante que a Portaria 671 manda entregar a quem bateu.", ""),
    ("Correção é pedido, não edição",
     "Ninguém “conserta” uma marcação. Abre-se um pedido, o gestor aprova, e o histórico guarda "
     "o antes e o depois.", ""),
]

ESPELHO = [
    ("O mês inteiro, na mão dele",
     "Horas trabalhadas, previsto, atraso, falta, extra e o saldo do banco de horas — dia a dia, "
     "com as batidas de cada dia.", ""),
    ("Acaba o “me manda meu ponto?”",
     "O funcionário confere sozinho, sem pedir pro RH e sem esperar o fim do mês.", ""),
    ("Pedido de correção pelo app",
     "Achou que faltou uma batida, ele mesmo abre o pedido — que cai pro gestor.", ""),
]

# Setores: (slug da foto, rótulo, dor concreta do ICP)
SETORES = [
    ("setor-cafe",       "Comércio",   "Turnos que abrem cedo e fecham tarde, com gente entrando e saindo o dia todo."),
    ("setor-clinica",    "Saúde",      "Plantão, escala e hora extra — tudo precisa fechar certo na folha."),
    ("setor-obra",       "Obra",       "Equipe em campo, sem relógio na parede e, muitas vezes, sem sinal."),
    ("setor-escritorio", "Escritório", "Jornada flexível e banco de horas que ninguém consegue auditar na planilha."),
]

DORES = [
    "Fim do mês, e o ponto vira discussão: “não bati”, “esqueci”, “o relógio tava errado”.",
    "Relógio de parede é caro, quebra — e não cobre quem trabalha em campo ou em rota.",
    "Cartão de papel e planilha não valem nada numa reclamatória trabalhista.",
    "O funcionário passa o mês pedindo “me manda meu espelho de ponto?”.",
    "O app que cobra por faixa: entra o 11º funcionário e a conta pula pro plano de 25.",
    "Gente em obra, subsolo ou guarita sem sinal simplesmente não consegue registrar.",
]

# Compliance — o que sustenta a prova numa audiência.
COMPLIANCE = [
    ("Portaria 671/2021 — REP-P",
     "NSR sequencial, registro imutável e comprovante entregue ao trabalhador. É o padrão de "
     "ponto por aplicativo, e o produto foi desenhado em cima dele.", ""),
    ("O empregador não altera marcação",
     "A lei não deixa apagar nem editar. Só registrar um ajuste auditável — e é exatamente assim "
     "que o sistema se comporta, por design.", ""),
    ("LGPD: só coleta o que a empresa liga",
     "Selfie e localização são dado pessoal (e biométrico). Só entram quando a empresa exige, com "
     "finalidade declarada — nunca por padrão.", ""),
    ("A imagem não viaja à toa",
     "A prova de vida roda na captura, no próprio aparelho.", ""),
]

# ---------------------------------------------------------------- preço
PRECO = [
    ("Começar", "Grátis", "até 2 pessoas",
     "Para sempre — não é teste de 14 dias. Todos os recursos, sem cartão de crédito."),
    ("Empresa", "R$ 4,90", "por pessoa/mês",
     "Preço único, do terceiro funcionário ao centésimo. Você paga por quem bate ponto, "
     "não por uma faixa que sobra."),
    ("Escala", "100+", "sob proposta",
     "Preço por volume abaixo de R$ 4,90, várias unidades e centros de custo."),
]

NAOS = [
    ("Sem faixa",
     "No modelo por faixa, a décima primeira pessoa te joga no plano de 25 — e você paga por 14 "
     "que não existem. Aqui, onze pessoas custam onze pessoas."),
    ("Sem implantação",
     "Não tem relógio pra comprar, obra pra fazer nem taxa de setup. O celular que o funcionário "
     "já tem no bolso é o ponto."),
    ("Sem fidelidade",
     "Mês a mês, sem carência e sem multa. O produto tem que segurar você — não o contrato."),
]

# ---------------------------------------------------------------- honestidade
# O capítulo mais importante do livreto. Vem direto de pack.yml > nao_features.
# Nunca vender roadmap como pronto: se não roda hoje, está aqui.
NAO_FAZ = [
    ("Não é folha de pagamento",
     "Não calcula nem emite holerite, não gera guia. O baterponto é a coleta da hora — a folha é outra coisa.", ""),
    ("Não faz eSocial",
     "Não transmite S-1200 nem os S-2xxx. Se alguém te prometeu isso, não foi a gente.", ""),
    ("Não substitui o REP-C",
     "Onde a empresa optou pelo relógio físico homologado, ele continua. O baterponto é REP-P — ponto por aplicativo.", ""),
    ("Não tem push hoje",
     "O app não empurra notificação. Está aberto no roadmap, e roadmap não se vende como pronto.", ""),
    ("Não é integração pronta com toda folha",
     "“Integração com a sua folha” é conversa do plano Escala, com escopo — não é um botão que já existe.", ""),
    ("Não faz facial 1:N",
     "O app não descobre quem é a pessoa sem login. Ele confere 1:1 o rosto contra o cadastro de "
     "quem está logado.", ""),
]

# ---------------------------------------------------------------- lineup
# (nome, descrição, cor, selo)
TILES = [
    ("Batida no celular",    "App Android e iOS, no aparelho que ele já tem.",              "roxo",   ""),
    ("NSR imutável",         "A prova na tela do funcionário, no ato.",                     "verde",  ""),
    ("Selfie + prova de vida","Liveness de dois passos, quando a empresa exige.",           "roxo",   ""),
    ("Geofence",             "Guarda se ele estava na área do trabalho.",                   "ciano",  ""),
    ("Fila offline",         "Sem sinal, bate igual — e sobe sozinha depois.",              "ciano",  ""),
    ("Espelho do mês",       "Horas, saldo, atraso e falta na mão do funcionário.",         "ambar",  ""),
    ("Pedido de correção",   "Ninguém apaga; o gestor aprova e o histórico fica.",          "ambar",  ""),
    ("Apontamento",          "A batida amarrada à obra ou ao centro de custo.",             "verde",  ""),
    ("Multi-vínculo",        "Duas empresas, um app — cada uma com sua jornada.",           "roxo",   ""),
]

CTA = ("Seu time bate o ponto amanhã de manhã.",
       "Grátis até 2 pessoas. R$ 4,90 por pessoa depois disso. Conte como é a operação da sua "
       "empresa e a gente mostra o app rodando.")
