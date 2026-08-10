# Hierarquia de afirmacoes - Log Sentinel

Este documento apresenta a hierarquia de afirmacoes com argumentos
estruturados adotada pelo Log Sentinel. Complementa o documento
`docs/av5/REQUISITOS_SEGURANCA.md`, no qual cada requisito e enunciado
como uma afirmacao formal, e integra o pacote da AV5 (Riscos e
Qualidade).

A hierarquia se organiza em quatro niveis. No topo esta a **afirmacao
de sistema**, que descreve o comportamento global esperado do Log
Sentinel. Ela se sustenta em **afirmacoes de subsistema**, uma para
cada requisito de seguranca ou de qualidade. Cada afirmacao de
subsistema, por sua vez, se decompoe em **afirmacoes de componente**,
que descrevem propriedades verificaveis de um modulo ou classe. Na
base da hierarquia estao as **evidencias**, que sao os testes
automatizados, as configuracoes ou os trechos de codigo que permitem
verificar cada afirmacao de componente.

## S - Afirmacao de sistema

**S.** O Log Sentinel produz relatorios de auditoria reproduziveis e
rastreaveis a partir de arquivos de log Apache, distinguindo com
clareza os desfechos "sem anomalia", "com anomalia" e "falha de
analise", sem modificar o arquivo de entrada nem interromper a analise
por conta de linhas malformadas isoladas.

A afirmacao de sistema se decompoe em cinco afirmacoes de subsistema,
identificadas de A1 a A5. As tres primeiras vem diretamente dos
requisitos de seguranca (RS1, RS2, RS3, RS4 do documento de requisitos)
e as duas ultimas cobrem propriedades de qualidade transversal (A4,
correcao das deteccoes; A5, capacidade de evolucao).

## A1 - Integridade da identificacao do arquivo

Corresponde a RS1 dos requisitos de seguranca.

**A1.** Todo relatorio emitido pelo Log Sentinel identifica de forma
univoca o arquivo analisado atraves do hash SHA-256 desse arquivo.

- **A1.1** O hash publicado no relatorio e calculado sobre o mesmo
  conteudo que foi consumido pelo pipeline, sem risco de descasamento
  entre uma leitura para hash e outra leitura para analise.
  - **Evidencia:** o metodo `read_lines` de `LogFileDAO`
    (`src/python_pdm_template/core/dao/log_file_dao.py`) faz um unico
    passe pelo arquivo, alimentando `hashlib.sha256` a cada bloco
    binario lido e produzindo, ao final, um digest disponivel pela
    propriedade `digest`. Verificado por
    `test_log_file_dao_streaming_and_hash` em
    `tests/core/test_log_file_dao.py`.

- **A1.2** O hash publicado corresponde a algoritmo padronizado e
  reprodutivel em outras ferramentas.
  - **Evidencia:** o Log Sentinel usa a implementacao de SHA-256 da
    biblioteca padrao (`hashlib.sha256`), cujo resultado pode ser
    conferido contra `sha256sum` no Linux ou `Get-FileHash -Algorithm
    SHA256` no PowerShell.

## A2 - Robustez contra entradas malformadas

Corresponde a RS2 dos requisitos de seguranca.

**A2.** Uma linha invalida no meio do arquivo de entrada nao interrompe
a analise das linhas restantes.

- **A2.1** O parser distingue entre linha invalida (que deve ser
  descartada) e falha real de leitura (que deve interromper).
  - **Evidencia:** o `ApacheParser` levanta `ParseError` para linha
    invalida e nunca captura excecoes de I/O, deixando-as propagar.
    Verificado por `test_apache_parser_linha_malformada` em
    `tests/core/test_apache_parser.py`.

- **A2.2** A CLI captura `ParseError`, contabiliza a descartada e
  segue.
  - **Evidencia:** o subcomando `analyze`
    (`src/python_pdm_template/cli/main.py`) reporta o total de linhas
    descartadas no final do relatorio. Verificado por
    `test_cli_analyze_conta_descartadas` em `tests/cli/test_main.py`.

- **A2.3** A politica de aceitabilidade tolera ate cinco por cento de
  linhas descartadas em silencio; acima disso o relatorio precisa
  destacar um aviso.
  - **Evidencia:** politica formalizada no risco R1 do documento
    `docs/av5/RISCOS.md`. O aviso ainda esta previsto para iteracao
    subsequente da CLI.

## A3 - Sinalizacao clara do resultado

Corresponde a RS3 dos requisitos de seguranca.

**A3.** O codigo de saida do processo permite a um consumidor
programatico distinguir "sem anomalia", "com anomalia" e "falha de
analise" sem interpretar o texto do relatorio.

- **A3.1** Codigo de saida zero significa analise concluida sem
  deteccao.
  - **Evidencia:** `test_cli_analyze_sem_deteccao` em
    `tests/cli/test_main.py`.

- **A3.2** Codigo de saida um significa analise concluida com pelo
  menos uma deteccao.
  - **Evidencia:** `test_cli_analyze_detecta_brute_force` em
    `tests/cli/test_main.py`.

- **A3.3** Codigo de saida dois significa falha de leitura ou de
  acesso ao arquivo indicado, com mensagem em `stderr`.
  - **Evidencia:** `test_cli_analyze_arquivo_inexistente` em
    `tests/cli/test_main.py`.

## A4 - Correcao dos detectores

**A4.** Cada detector implementado reconhece corretamente os padroes
de anomalia que se propoe a detectar, sem confundi-los com trafego
legitimo.

- **A4.1** O `BruteForceDetector` reconhece uma sequencia de
  tentativas com falha de autenticacao originadas do mesmo IP em
  janela curta de tempo.
  - **Evidencia:** `test_brute_force_detector_positivo` e
    `test_brute_force_detector_negativo` em
    `tests/core/test_brute_force_detector.py`.

- **A4.2** O `ScannerDetector` reconhece exploracao sistematica de
  caminhos ou portas por parte de um mesmo IP.
  - **Evidencia:** `test_scanner_detector_positivo` em
    `tests/core/test_scanner_detector.py`.

- **A4.3** O `TrafficSpikeDetector` reconhece picos de trafego acima
  do esperado dentro de janelas configuraveis.
  - **Evidencia:** `test_traffic_spike_detector_iteracao_1` em
    `tests/core/test_traffic_spike_detector.py`.

- **A4.4** A integracao entre parser, detectores e agregador produz o
  mesmo resultado que a soma dos comportamentos individuais.
  - **Evidencia:** `test_pipeline_completo` em
    `tests/integration/test_pipeline.py`.

## A5 - Capacidade de evolucao

**A5.** Adicionar um novo tipo de deteccao ao Log Sentinel nao exige
alteracao do Pipeline, do DAO nem dos detectores existentes.

- **A5.1** O contrato de deteccao esta declarado como interface
  abstrata unica.
  - **Evidencia:** classe abstrata `BaseDetector` em
    `src/python_pdm_template/core/detectors/base.py`, com o metodo
    `process(entries) -> Iterator[Detection]` marcado como
    `@abstractmethod`.

- **A5.2** Cada detector concreto implementa exclusivamente esse
  contrato, sem depender das demais subclasses.
  - **Evidencia:** as classes `BruteForceDetector`, `ScannerDetector` e
    `TrafficSpikeDetector` em `src/python_pdm_template/core/detectors/`
    herdam de `BaseDetector` e nao se referenciam entre si.

- **A5.3** O Pipeline consome os detectores exclusivamente pela
  interface abstrata.
  - **Evidencia:** a classe `Pipeline` em
    `src/python_pdm_template/core/pipeline.py` recebe uma lista tipada
    como `list[BaseDetector]` e itera com `for detector in self.detectors:
    yield from detector.process(entries)`, sem inspecao do tipo
    concreto.

## Verificacao consolidada

A tabela abaixo resume, para cada afirmacao de sistema e subsistema, o
tipo de evidencia disponivel e o local em que ela pode ser inspecionada
ou executada.

| Afirmacao | Tipo de evidencia | Local |
|-----------|-------------------|-------|
| A1 | Teste automatizado + inspecao | `tests/core/test_log_file_dao.py`, `src/.../log_file_dao.py` |
| A2 | Testes automatizados + politica documentada | `tests/core/test_apache_parser.py`, `tests/cli/test_main.py`, `docs/av5/RISCOS.md` |
| A3 | Testes automatizados | `tests/cli/test_main.py` |
| A4 | Testes unitarios + teste de integracao | `tests/core/`, `tests/integration/` |
| A5 | Inspecao de codigo | `src/.../detectors/`, `src/.../pipeline.py` |

Todas as evidencias baseadas em teste sao executadas em cada push pelos
workflows `.github/workflows/test.yaml` e `.github/workflows/ci.yaml`.
As evidencias baseadas em inspecao ficam versionadas junto com o codigo
e sao revisadas pelo SonarCloud no projeto `AryanAssis_ENGS2`.

## Referencias cruzadas

- Requisitos formais de seguranca e protecao:
  `docs/av5/REQUISITOS_SEGURANCA.md`.
- Padroes de projeto que sustentam as afirmacoes A1, A4 e A5:
  `docs/av5/PADROES.md`.
- Riscos que motivam a formalizacao de A2 e A3:
  `docs/av5/RISCOS.md`.
