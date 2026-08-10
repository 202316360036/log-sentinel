# Requisitos de seguranca e protecao - Log Sentinel

Este documento reune os requisitos de seguranca e de protecao adotados
pelo Log Sentinel e integra o pacote da AV5 (Riscos e Qualidade) da
disciplina de Engenharia de Software II. Cada requisito e apresentado
sob quatro angulos: a **afirmacao** formal do comportamento esperado, o
**argumento** que a sustenta, a **evidencia** (teste automatizado,
configuracao ou trecho de codigo) que permite verifica-lo e a
**situacao atual** em relacao ao master.

A hierarquia detalhada, com o desdobramento de cada afirmacao em
subafirmacoes menores ate chegar as evidencias, esta em
`docs/av5/AFIRMACOES.md`.

## Contexto de seguranca da aplicacao

O Log Sentinel opera como ferramenta de auditoria post-mortem. O usuario
tipico e um analista que recebeu um arquivo `.log` de origem confiavel
ou minimamente controlada e precisa inspeciona-lo em busca de
comportamento anomalo. Esse cenario define o modelo de ameaca que o
sistema efetivamente enderecca: o arquivo de entrada pode estar
corrompido, truncado ou parcialmente malformado, mas nao se assume que
seja um artefato explicitamente adversarial construido para explorar o
proprio analisador. Em contrapartida, o sistema nao pode alterar o
arquivo original nem transmitir seu conteudo para redes externas, sob
pena de comprometer a cadeia de custodia do material sob analise.

## RS1 - Integridade do arquivo analisado

**Afirmacao.** Todo relatorio emitido pelo Log Sentinel corresponde a
exatamente um arquivo `.log`, identificado de forma univoca pelo seu
hash SHA-256.

**Argumento.** A classe `LogFileDAO`
(`src/python_pdm_template/core/dao/log_file_dao.py`) le o arquivo em
streaming e alimenta, no mesmo passe, uma instancia de `hashlib.sha256`
com cada bloco lido. O hash final so fica disponivel apos o consumo
completo do generator `read_lines`, o que garante que o valor publicado
no relatorio corresponde ao arquivo efetivamente processado, e nao a
uma leitura anterior ou parcial.

**Evidencia.** O teste `test_log_file_dao_streaming_and_hash` em
`tests/core/test_log_file_dao.py` cria um arquivo com conteudo
conhecido, consome o generator e verifica que o campo `digest` do DAO
coincide com o hash SHA-256 calculado independentemente pelo teste. A
CLI (`src/python_pdm_template/cli/main.py`) imprime esse mesmo digest no
cabecalho do relatorio produzido pelo subcomando `analyze`.

**Situacao atual.** Requisito atendido.

## RS2 - Robustez contra entradas malformadas

**Afirmacao.** O Log Sentinel nunca aborta a analise inteira em resposta
a uma unica linha invalida do arquivo de entrada. Linhas invalidas sao
contabilizadas e o processamento prossegue nas linhas restantes.

**Argumento.** O `ApacheParser`
(`src/python_pdm_template/core/parsers/apache_parser.py`) levanta
`ParseError` por linha que nao case com o padrao esperado. A CLI e o
worker da GUI capturam essa excecao em cada iteracao, incrementam um
contador de descartadas e continuam. A politica de aceitabilidade
formalizada no risco R1 do documento `docs/av5/RISCOS.md` estabelece
que ate cinco por cento de linhas descartadas e considerado tolerancia
normal; acima desse patamar o relatorio deve destacar um aviso, sem
interromper a analise.

**Evidencia.** O teste `test_cli_analyze_conta_descartadas` em
`tests/cli/test_main.py` alimenta a CLI com um arquivo misto (uma linha
valida e duas invalidas) e verifica que o codigo de saida e zero, que o
relatorio informa "Linhas descartadas: 2" e que o pipeline nao lanca
excecao. O teste `test_apache_parser_linha_malformada` em
`tests/core/test_apache_parser.py` garante que o `ParseError` e a
excecao efetivamente levantada pelo parser, e nao um erro generico.

**Situacao atual.** Requisito atendido no que diz respeito ao
tratamento por linha. O aviso quando o percentual de descartadas
ultrapassa cinco por cento esta previsto pela politica de
aceitabilidade e sera incorporado a CLI em iteracao subsequente.

## RS3 - Sinalizacao clara do resultado

**Afirmacao.** Um consumidor programatico da CLI (script de shell,
pipeline de CI, sistema de orquestracao) consegue distinguir tres
desfechos apenas pelo codigo de saida do processo, sem precisar
interpretar o texto do relatorio.

**Argumento.** A CLI adota convencao inspirada no utilitario `grep`, em
que o codigo de saida carrega o resultado da analise:

| Codigo | Significado |
|--------|-------------|
| `0` | Arquivo analisado com sucesso, nenhuma anomalia identificada. |
| `1` | Arquivo analisado com sucesso, pelo menos uma anomalia identificada. |
| `2` | Nao foi possivel analisar o arquivo (por exemplo, caminho inexistente ou permissao negada). |

Essa distincao permite que a ferramenta seja usada como parte de um
pipeline maior sem que o consumidor precise fazer parsing textual da
saida padrao.

**Evidencia.** Tres testes em `tests/cli/test_main.py` cobrem os
codigos:

- `test_cli_analyze_sem_deteccao` garante codigo `0` quando o arquivo
  analisado nao produz deteccoes.
- `test_cli_analyze_detecta_brute_force` garante codigo `1` quando ha
  pelo menos uma deteccao.
- `test_cli_analyze_arquivo_inexistente` garante codigo `2` e mensagem
  em `stderr` para caminho invalido.

**Situacao atual.** Requisito atendido.

## RS4 - Isolamento do arquivo de entrada

**Afirmacao.** O Log Sentinel apenas le o arquivo indicado pelo
usuario. Nao modifica seu conteudo, nao o copia, nao o remove e nao
transmite dados para redes externas.

**Argumento.** O unico ponto de entrada e saida do Core esta
concentrado no `LogFileDAO`, que abre o arquivo em modo binario apenas
para leitura (`open(self.file_path, "rb")`). Nao ha operacoes de
escrita, truncamento ou remocao em nenhum modulo do Core, nem chamadas
para bibliotecas de rede. As familias de regras `S` (seguranca) do
Ruff estao habilitadas no `pyproject.toml` e alertariam sobre uso de
funcoes reconhecidamente perigosas como `subprocess` com `shell=True`,
`pickle.load`, `eval`, `exec` ou construcao dinamica de comandos.

**Evidencia.** A verificacao ocorre por dois mecanismos complementares.
Primeiro, por inspecao direta: uma busca por `open(` no diretorio
`src/` retorna apenas o uso em `LogFileDAO`, e sempre com o modo `"rb"`.
Segundo, por analise estatica automatizada: o step "Rodar ruff" do
workflow `.github/workflows/ci.yaml` executa a cada push e sinalizaria
qualquer regressao em regras da familia `S`.

**Situacao atual.** Requisito atendido.

## Referencias cruzadas

- Riscos que motivam ou sao mitigados por estes requisitos: R1 e R2 em
  `docs/av5/RISCOS.md`.
- Padroes de projeto que realizam a arquitetura pressuposta por estes
  requisitos, em particular o DAO (RS1, RS4) e o Pipe-and-Filter (RS2):
  `docs/av5/PADROES.md`.
- Hierarquia detalhada de afirmacoes com o desdobramento em
  subafirmacoes e evidencias: `docs/av5/AFIRMACOES.md`.
