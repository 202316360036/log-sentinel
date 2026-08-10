# Roteiro da apresentacao AV5 — Log Sentinel

Documento produzido em 2026-08-10 para a apresentacao presencial da AV5
da disciplina de Engenharia de Software II (IFBA 2026.1), marcada para
12/08/2026. Duracao alvo de 25 minutos, com folga de ate 5 minutos para
perguntas do professor. Cada bloco identifica um responsavel principal e
um substituto, atendendo a mitigacao organizacional do risco R6 do
documento `docs/av5/RISCOS.md`.

## Ordem consolidada dos blocos

| Bloco | Tema | Duracao | Responsavel | Substituto |
|-------|------|---------|-------------|------------|
| 1 | Abertura e visao do sistema | 2 min | Elder | Aryan |
| 2 | Padroes de projeto e OO | 5 min | Aryan | Elder |
| 3 | Interface grafica e Observer | 4 min | Helena | Elder |
| 4 | Requisitos de seguranca e afirmacoes | 4 min | Rodrigo | Aryan |
| 5 | Especificacao de riscos | 3 min | Elder | Rodrigo |
| 6 | Qualidade e integracao continua | 3 min | Elder | Aryan |
| 7 | Demonstracao do binario | 4 min | Helena e Rodrigo | Elder |
| 8 | Fechamento | 30 s | Aryan | Helena |
| **Total** | | **25,5 min** | | |

---

## Bloco 1 — Abertura e visao do sistema

Responsavel: Elder. Substituto: Aryan. Duracao: 2 minutos.

O bloco de abertura serve para situar o professor no dominio da
aplicacao antes de qualquer detalhe tecnico. A ideia e comecar pelo
problema que o Log Sentinel resolve, nao pela arquitetura.

Sugestao de fala:

> "Bom dia, professor. Somos o grupo do Log Sentinel, uma ferramenta de
> auditoria post-mortem de logs Apache. A partir de um arquivo `.log`
> bruto, o sistema identifica automaticamente tres tipos de anomalia:
> tentativas de brute-force em endpoints de autenticacao, comportamento
> de varredura de portas ou caminhos, e picos anormais de trafego. O
> relatorio final traz o total de linhas processadas, o hash SHA-256 do
> arquivo analisado e a lista de deteccoes, cada uma acompanhada do IP
> envolvido e da evidencia que motivou a marcacao."

Ao encerrar, anunciar a divisao dos proximos blocos para que o professor
saiba o que esperar:

> "Nos proximos vinte e cinco minutos, o Aryan abre a parte de
> arquitetura e padroes de projeto, a Helena mostra a camada de
> interface grafica, o Rodrigo aprofunda os requisitos de seguranca e a
> hierarquia de afirmacoes, e eu volto no final para falar de riscos, de
> qualidade e para demonstrar o binario rodando em Windows sem Docker."

Nao abrir o diagrama de arquitetura neste bloco. O Aryan usa esse
diagrama na abertura do proximo bloco e a repeticao empobrece a
apresentacao.

---

## Bloco 2 — Padroes de projeto e codigo orientado a objetos

Responsavel: Aryan. Substituto: Elder. Duracao: 5 minutos.

Este e o bloco tecnico mais longo. A recomendacao e trabalhar com dois
arquivos em split no editor: `src/python_pdm_template/core/pipeline.py`
a esquerda e `src/python_pdm_template/core/detectors/base.py` a direita,
mudando para os detectores concretos apenas quando for citar
polimorfismo.

Sequencia sugerida de topicos.

1. **Pipeline como Pipe-and-Filter.** Descrever que cada estagio do
   Core — leitura via DAO, parse via `ApacheParser`, aplicacao dos
   detectores — e uma etapa independente, encaixada pela classe
   `Pipeline`. Mostrar o trecho em que o `for detector in self.detectors`
   itera pela lista injetada no construtor, ilustrando que adicionar um
   quarto detector nao exige tocar no Pipeline.

2. **Strategy com heranca e polimorfismo.** Abrir `base.py` e apresentar
   o `BaseDetector` como classe abstrata que define o contrato
   `process(entries) -> Iterator[Detection]`. Em seguida, mostrar que
   `BruteForceDetector`, `ScannerDetector` e `TrafficSpikeDetector`
   herdam dessa base e implementam algoritmos distintos. O Pipeline nao
   conhece qual algoritmo cada subclasse aplica — chama sempre o mesmo
   `process`. Este e o argumento de polimorfismo em codigo real. Vale
   mencionar que essa refatoracao entrou pelo pull request numero 38.

3. **DAO como camada de acesso a dados.** Abrir
   `core/dao/log_file_dao.py`. Destacar duas propriedades pouco
   convencionais deste DAO: le o arquivo em streaming, sem carregar todo
   o conteudo na memoria, e calcula o hash SHA-256 no mesmo passe da
   leitura. Ganho arquitetural: performance e integridade coexistem sem
   que o parser precise conhecer nenhum dos dois assuntos.

4. **Encapsulamento e imutabilidade.** Abrir `core/models.py` e mostrar
   que `LogEntry` e `Detection` sao `@dataclass` com `frozen=True`.
   Comentar que entradas de log parseadas nao podem ser mutadas ao longo
   do pipeline, o que elimina uma classe inteira de bugs de estado
   compartilhado.

Passagem para o proximo bloco:

> "Essa arquitetura em camadas e o que permite ao Log Sentinel expor o
> mesmo Core atraves de uma CLI e de uma interface grafica sem duplicar
> logica. A Helena vai mostrar agora como a GUI se conecta a esse Core."

---

## Bloco 3 — Interface grafica e Observer

Responsavel: Helena. Substituto: Elder. Duracao: 4 minutos.

O bloco discute a GUI a partir do codigo, sem executar o binario ainda.
A execucao fica reservada para o bloco 7.

1. **MVC com Qt.** Abrir `src/python_pdm_template/gui/main_window.py` e
   `src/python_pdm_template/gui/models.py`. Explicar o mapeamento:
   `LogEntryTableModel` no papel de Model estendendo
   `QAbstractTableModel`, a `QTableView` da `MainWindow` no papel de
   View, e a propria `MainWindow` no papel de Controller, respondendo a
   drag-and-drop, filtros e botoes.

2. **Observer via sinais e slots.** Abrir
   `src/python_pdm_template/gui/workers.py`. O `ParserWorker` herda de
   `QThread` e emite dois sinais: `progress`, disparado enquanto o
   arquivo e consumido, e `finished`, disparado com a lista final de
   entradas parseadas. A `MainWindow` assina esses sinais e reage:
   atualiza a barra de progresso e joga o resultado na tabela. Este e o
   padrao Observer implementado pela mecanica nativa do Qt — o worker
   publica eventos sem saber quem escuta.

3. **Filtragem sem tocar no modelo.** Comentar rapidamente o
   `QSortFilterProxyModel` que peneira as linhas por IP ou status sem
   alterar o `LogEntryTableModel` original. Reforca o argumento de
   separacao de responsabilidades.

4. **Cobertura da GUI por testes.** Abrir
   `tests/gui/test_workers.py`. Explicar que a suite usa `pytest-qt` para
   exercitar componentes Qt sem abrir janela. O teste apresentado cria
   um `ParserWorker` real, roda contra um arquivo em disco criado por
   `tmp_path` e verifica que o sinal `finished` chega com a entrada
   parseada corretamente. Este e um teste de integracao GUI + Core.

Passagem para o proximo bloco:

> "A demonstracao do binario no fim da apresentacao vai mostrar essa GUI
> em funcionamento. O Rodrigo agora vai discutir os requisitos de
> seguranca que essa arquitetura satisfaz."

---

## Bloco 4 — Requisitos de seguranca e hierarquia de afirmacoes

Responsavel: Rodrigo. Substituto: Aryan. Duracao: 4 minutos.

O bloco atende a dois itens da rubrica ao mesmo tempo: requisitos de
seguranca e protecao, e hierarquia de afirmacoes com argumentos
estruturados. Cada requisito e apresentado como uma afirmacao
verificavel, seguida do argumento que a sustenta.

**RS1 — Integridade do arquivo analisado.**

- Afirmacao: todo relatorio emitido corresponde a exatamente um arquivo,
  identificado pelo seu hash SHA-256.
- Argumento: o `LogFileDAO` calcula o hash SHA-256 no mesmo passe da
  leitura e expoe o valor apos o consumo completo do generator. A CLI
  imprime esse hash no cabecalho do relatorio final. Se o arquivo for
  substituido entre analises, o hash muda e a evidencia fica rastreavel.

**RS2 — Robustez contra entradas malformadas.**

- Afirmacao: o sistema nunca aborta a analise inteira por causa de uma
  unica linha invalida.
- Argumento: o `ApacheParser` levanta `ParseError` por linha invalida; a
  CLI captura, contabiliza descartadas e prossegue. Comportamento
  coberto pelo teste `test_cli_analyze_conta_descartadas` em
  `tests/cli/test_main.py`.

**RS3 — Sinalizacao clara do resultado.**

- Afirmacao: um pipeline consumindo a CLI consegue distinguir tres
  desfechos — "analisou e nao achou nada", "analisou e achou anomalia"
  e "nao conseguiu analisar" — apenas pelo codigo de saida.
- Argumento: convencao inspirada no `grep`, com codigos de saida 0, 1 e
  2 respectivamente. Comportamento coberto por
  `test_cli_analyze_sem_deteccao`, `test_cli_analyze_detecta_brute_force`
  e `test_cli_analyze_arquivo_inexistente`.

**RS4 — Isolamento do arquivo de entrada.**

- Afirmacao: o Log Sentinel apenas le o arquivo indicado; nao modifica,
  nao move, nao transmite conteudo pela rede.
- Argumento: o unico ponto de entrada e saida do Core esta no DAO, que
  abre o arquivo em modo binario apenas para leitura. As regras de
  seguranca da familia `S` do Ruff estao ativadas no `pyproject.toml`
  e verificam a ausencia de chamadas perigosas no restante do codigo.

Passagem para o proximo bloco:

> "As quatro afirmacoes acima sao verificaveis pela suite de testes ou
> por inspecao direta do codigo. O Elder agora fecha com a parte de
> riscos e de qualidade que sustenta essas afirmacoes ao longo das
> evolucoes do projeto."

---

## Bloco 5 — Especificacao de riscos

Responsavel: Elder. Substituto: Rodrigo. Duracao: 3 minutos.

Abrir `docs/av5/RISCOS.md` projetado. Nao ler o documento inteiro. O
bloco expoe o metodo e destaca tres riscos de niveis diferentes.

Introducao do metodo:

> "Catalogamos seis riscos. A avaliacao usa uma escala qualitativa de
> probabilidade e impacto, cada uma em tres niveis, cruzadas em uma
> matriz que produz cinco niveis gerais: baixo, moderado, alto e
> critico. Cada risco descreve a causa-raiz, a mitigacao adotada e a
> declaracao formal de aceitabilidade. Vou destacar tres casos que
> ilustram como tratamos cada nivel."

**R3, critico — Ambiente Windows sem Python.** A demo ocorre em maquina
sem Docker; um binario incompleto trava a apresentacao. Mitigacao: o
workflow `release.yaml` empacota via PyInstaller com
`--collect-all PySide6` e executa um smoke test do proprio `.exe`
antes de publicar o artefato.

**R2, alto e parcialmente aceito — Falso negativo.** Os detectores usam
thresholds fixos e janelas de tempo curtas; ataques distribuidos ou
lentos escapam. E limitacao consciente do escopo, aceita porque o
relatorio publica o hash do arquivo e o total de linhas, permitindo
reprocessamento com outras calibracoes.

**R6, moderado — Ausencia de integrante.** Sem mitigacao tecnica
possivel. A mitigacao e organizacional: cada bloco deste roteiro tem
um substituto explicitamente nomeado; a demo do binario foi ensaiada
por mais de uma pessoa.

Fechamento do bloco:

> "Todos os seis riscos entraram na AV5 com aceitabilidade declarada
> favoravel. Passo agora para a parte de qualidade, que e o que sustenta
> essa declaracao ao longo do tempo."

---

## Bloco 6 — Qualidade e integracao continua

Responsavel: Elder. Substituto: Aryan. Duracao: 3 minutos.

Sem slide. Abrir o navegador na aba Actions do repositorio.

1. **Analise estatica.** Ruff configurado com as familias de regras A,
   B, D, F, N, S, DOC, SLF, RET, ARG, PIE, PLE, PLW, PLR, SIM, C90 e
   C4. Pyright em modo `strict`. Ambos vivem no `pyproject.toml` e
   rodam no CI.

2. **Testes automatizados.** Vinte testes, cobrindo Core — parsers,
   detectores, DAO, aggregator, pipeline — CLI e GUI. A cobertura no
   ultimo run do master esta em noventa e cinco por cento.

3. **Integracao continua multissistema.** Matriz de tres sistemas
   operacionais (Ubuntu, macOS e Windows) executa a suite de testes a
   cada push. Mostrar o painel Actions com os checks verdes do commit
   mais recente do master.

4. **SonarCloud.** O projeto `AryanAssis_ENGS2` recebe o `coverage.xml`
   automaticamente. Mostrar o dashboard.

5. **Empacotamento automatizado.** O workflow `release.yaml` empacota
   dois binarios (CLI e GUI) via PyInstaller para Windows e Linux, faz
   smoke test do binario da CLI contra uma fixture, publica os arquivos
   como artefato. Mostrar o run mais recente com os dois `.exe`
   disponiveis para download.

Passagem para a demo:

> "Para provar que isso tudo termina em algo executavel, a Helena e o
> Rodrigo vao rodar agora o mesmo binario que esta publicado como
> artefato no ultimo release do repositorio."

---

## Bloco 7 — Demonstracao do binario

Responsaveis: Helena e Rodrigo. Substituto: Elder. Duracao: 4 minutos.

Pre-requisito: os dois executaveis, `log-sentinel.exe` e
`log-sentinel-gui.exe`, precisam estar baixados na area de trabalho da
maquina de apresentacao antes do inicio. E a mitigacao concreta do
risco R5 do documento de riscos — build local no dia da apresentacao
esta proibido.

**Etapa CLI (Rodrigo, um minuto e meio).**

1. Abrir o PowerShell na pasta que contem o `.exe` e os arquivos de
   fixture.
2. Executar `.\log-sentinel.exe analyze .\sample_brute_force.log`.
3. Apontar na tela: cabecalho do relatorio, total de linhas processadas,
   hash SHA-256, secao de deteccoes com o IP `10.0.0.99` e a mensagem
   de brute-force.
4. Rodar `echo $LASTEXITCODE`. O valor exibido e `1`, evidenciando a
   convencao estilo `grep` descrita na afirmacao RS3.
5. Executar `.\log-sentinel.exe analyze .\sample.log`. O relatorio
   informa "Nenhuma anomalia identificada" e o `$LASTEXITCODE` mostra
   `0`.

**Etapa GUI (Helena, dois minutos).**

1. Duplo clique em `log-sentinel-gui.exe`.
2. Arrastar o arquivo `sample_brute_force.log` para dentro da janela.
3. Comentar, enquanto a barra de progresso avanca, que a UI continua
   responsiva porque o parse roda em `QThread` e a atualizacao chega
   via sinais.
4. Ao terminar, digitar `10.0.0.99` no campo "Filtrar IP" e mostrar que
   as linhas correspondentes sao isoladas na tabela sem alterar o
   modelo original.
5. Limpar o filtro de IP, digitar `401` no campo "Filtrar Status" e
   mostrar todas as tentativas com falha de autenticacao.

**Fechamento da demo (Rodrigo, trinta segundos).**

> "O binario que acabou de rodar e o mesmo publicado no ultimo release
> do repositorio. Nao ha build local envolvido na demonstracao."

**Plano B, caso algo trave na hora.**

- Falha da CLI: rodar direto `python -m python_pdm_template analyze` a
  partir do fonte no PowerShell. A saida e identica.
- Falha da GUI: apresentar a sequencia de capturas de tela gravadas na
  vespera, guardadas em `notes/demo_gui/`.
- Falha total do ambiente: abrir o repositorio no navegador, entrar na
  aba Actions, mostrar o run mais recente com todos os testes verdes.

---

## Bloco 8 — Fechamento

Responsavel: Aryan. Substituta: Helena. Duracao: trinta segundos.

Sugestao de fala:

> "Recapitulando a entrega: especificacao de riscos com matriz e
> declaracao de aceitabilidade, requisitos de seguranca apresentados
> como afirmacoes verificaveis, quatro padroes de projeto identificados
> e presentes no codigo, orientacao a objetos com heranca, polimorfismo
> e encapsulamento, e verificacao continua por Pyright, Ruff,
> SonarCloud e por uma suite de testes com cobertura em noventa e cinco
> por cento. O binario demonstrado veio do proprio pipeline de release
> do repositorio. Estamos abertos as perguntas do professor."

O bloco de fechamento nao deve conter pedidos de desculpa nem lista de
itens que ficaram de fora. A entrega esta completa; o roteiro fala do
que foi feito.

---

## Checklist da vespera (11/08 ate as 22h)

Antes de considerar o roteiro fechado, cada item abaixo precisa ter uma
confirmacao no grupo. A ausencia de qualquer item obriga a repactuar o
bloco correspondente.

- [ ] Automatic Analysis do SonarCloud desligada no projeto
      `AryanAssis_ENGS2`, para que o CI do master fique verde.
- [ ] Tag `v0.5.0` criada no commit revisado; workflow `release.yaml`
      executado com sucesso; artefatos `log-sentinel-windows-latest` e
      `log-sentinel-ubuntu-latest` disponiveis na aba Actions.
- [ ] Documentos `docs/av5/REQUISITOS_SEGURANCA.md` e
      `docs/av5/AFIRMACOES.md` finalizados e mergeados no master, para
      que o Bloco 4 tenha material formal a projetar.
- [ ] `log-sentinel.exe` e `log-sentinel-gui.exe` baixados na maquina
      de apresentacao. Testar cada um com `sample.log` e
      `sample_brute_force.log` antes de encerrar o dia.
- [ ] Sequencia de capturas de tela da GUI (arrastar arquivo, tabela
      populada, filtros ativos) gravadas na vespera e guardadas em
      `notes/demo_gui/` como plano B.
- [ ] Cada integrante leu em voz alta os blocos 1, 5 e 8, que sao
      falados por mais de uma pessoa, e o proprio bloco atribuido a si,
      pelo menos uma vez em ensaio cronometrado.

## Referencias no repositorio

- Especificacao de riscos: `docs/av5/RISCOS.md`.
- Padroes de projeto e arquitetura: `docs/av5/PADROES.md`.
- Requisitos de seguranca e hierarquia de afirmacoes:
  `docs/av5/REQUISITOS_SEGURANCA.md` e `docs/av5/AFIRMACOES.md`.
- Workflows de CI, testes e release: `.github/workflows/`.
- Dashboard SonarCloud: projeto `AryanAssis_ENGS2` em `sonarcloud.io`.
