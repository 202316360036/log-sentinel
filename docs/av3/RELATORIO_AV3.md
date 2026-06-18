# Relatório Consolidado — AV3

> Engenharia de Software II (IFBA 2026.1) · Equipe Log Sentinel
> Data de elaboração: 2026-06-10 · Última revisão: 2026-06-18
> **Apresentação: 2026-07-08** (adiada pelo professor a partir do prazo original 17/06/2026) · Prazo interno: 06/07/2026

---

## 1. Identificação do projeto

- **Nome:** Log Sentinel
- **Repositório:** https://github.com/202316360036/log-sentinel
- **Branch principal:** `master`
- **Branch desta entrega (AV3):** `docs/av3-especificacao`
- **CI status:** verde (lint, tests, build) — ver badges no [README](../../README.md)
- **Documentação geral:** [docs/PROJETO.md](../PROJETO.md)
- **Arquitetura:** [docs/architecture/ARQUITETURA.md](../architecture/ARQUITETURA.md)

---

## 2. Entregáveis AV3 (mapeamento)

| Entregável solicitado | Documento | Estado |
|------------------------|-----------|--------|
| Barreiras, salvaguardas e condições latentes | [01_BARREIRAS_SALVAGUARDAS.md](01_BARREIRAS_SALVAGUARDAS.md) | ✅ entregue |
| Propriedades emergentes funcionais e não-funcionais | [02_PROPRIEDADES_EMERGENTES.md](02_PROPRIEDADES_EMERGENTES.md) | ✅ entregue |
| Dimensões de confiança do sistema | [03_DIMENSOES_CONFIANCA.md](03_DIMENSOES_CONFIANCA.md) | ✅ entregue |
| Perigos, acidentes e danos | [04_PERIGOS_ACIDENTES_DANOS.md](04_PERIGOS_ACIDENTES_DANOS.md) | ✅ entregue |
| Ativos, vulnerabilidades, ataques, ameaças, exposições | [05_AMEACAS_VULNERABILIDADES.md](05_AMEACAS_VULNERABILIDADES.md) | ✅ entregue |
| Link do GitHub | seção 1 deste doc | ✅ |
| Quantidade de commits por integrante | seção 3 deste doc | ✅ |
| Issues finalizados | seção 4 deste doc | ⏳ pendente `gh login` |
| Percentuais dos milestones | seção 5 deste doc | ⏳ pendente `gh login` |
| Atualização das previsões | seção 6 deste doc + [GANTT.md](../GANTT.md) | ✅ |
| Demonstração breve do app | seção 7 deste doc | ⚠️ esqueletos CLI+GUI |
| Roteiro da apresentação | [APRESENTACAO.md](APRESENTACAO.md) | ✅ |

---

## 3. Commits por integrante

> Fonte: `git shortlog -sn --all --no-merges --since=2026-04-01 --until=2026-06-11`
> Atualizado em 2026-06-10. O número final será refeito na véspera da apresentação.

| Integrante | Papel principal | Commits | Observação |
|------------|------------------|--------:|------------|
| **Elder** (`202316360036`) | CI/CD, releases, documentação | **9** | inclui setup do PyInstaller, SonarCloud opcional, fix de ruff/pyright, docs AV2 |
| **Aryan Souza Assis** | Core (parsers, modelos) | **8** | inclui commit inicial e setup de SonarCloud; primeiro `LogEntry` + TDD |
| **Rodrigo Cruz** | CLI (Typer) | **4** | pacote CLI + esqueleto `analyze`/`batch` |
| **Helena Santos Freitas** | GUI (PySide6) | **2** | pacote GUI + esqueleto `MainWindow` |

Notas:
- `Andre` (1 commit) é o autor do **template** original (`andre-romano/python_pdm_template`); **não conta** como integrante da equipe.
- `Aryan Assis` (1 commit "Add as coisas") é a mesma pessoa que `Aryan Souza Assis` — autoria duplicada por config local de git diferente. Total real do Aryan: **9 commits**.

**Total da equipe (sem o template): ~24 commits** entre 08/04/2026 e 12/05/2026.

> ⚠️ Lacuna evidente: **nenhum commit entre 13/05 e 10/06**. O grupo precisa retomar trabalho de Core/CLI/GUI antes da apresentação. Roteiro de retomada está na seção 6.

Detalhe individual por commit em [APENDICE_COMMITS.md](APENDICE_COMMITS.md).

---

## 4. Issues finalizadas

> ⏳ Esta seção depende de `gh auth login` para puxar dados do GitHub. Está em forma de placeholder a ser preenchido assim que o token estiver ativo.

Estrutura prevista (após autenticação):

```
Total de issues abertas no período: __
Total de issues fechadas: __
Issues fechadas por integrante:
  - Elder:   __
  - Aryan:   __
  - Rodrigo: __
  - Helena:  __
```

Comando para preencher quando `gh` estiver autenticado:

```bash
gh issue list --repo 202316360036/log-sentinel --state all --limit 200 \
  --json number,title,state,assignees,milestone,closedAt,labels
```

---

## 5. Percentuais dos milestones

> ⏳ Depende de `gh auth login`. Placeholder estruturado abaixo.

Marcos planejados (do [GANTT.md](../GANTT.md)):

| Milestone | Data alvo | % esperado em 2026-06-10 | % real | Observação |
|-----------|-----------|---------------------------|--------|------------|
| AV1 Ambiente | 15/04/2026 | 100% | **100%** ✅ | template + CI configurados |
| AV2 Testes | 13/05/2026 | 100% | **100%** ✅ | docs e TDD inicial entregues |
| Sprint 1 — Core MVP | 13/05 → 08/06 | 100% | ~15% | só `LogEntry` + teste |
| Sprint 2 — CLI & GUI | 13/05 → 30/06 | ~60% | ~10% | só esqueletos |
| AV3 Falhas | 17/06/2026 | 80% (hoje) | **80%** ✅ docs prontos | falta demo |
| Polimento & Release | a partir de 15/07 | 0% | 0% | dentro do prazo |
| AV5 Final | 12/08/2026 | 0% | 0% | dentro do prazo |

Comando para refinar percentuais quando `gh` estiver ativo:

```bash
gh api repos/202316360036/log-sentinel/milestones --jq '.[] | {title, open_issues, closed_issues}'
```

---

## 6. Atualização das previsões de entrega

### 6.1 Diagnóstico (revisado em 2026-06-18)
- AV1 e AV2 estão em dia. ✅
- AV3 (este documento): **docs prontos**, falta **demo funcional**. ⚠️
- **A Sprint 1.5 de recuperação (11–14/06) NÃO foi cumprida**: o `git log` confirma zero commits entre 13/05 e 18/06 em Core/CLI/GUI.
- Core/CLI/GUI continuam em **esqueleto** (`LogEntry` + Typer `--help` + `MainWindow` "Em construcao").
- **Boa notícia:** o professor adiou a AV3 de 17/06 para **08/07/2026**. A equipe ganhou 21 dias.

### 6.2 Replanejamento para chegar à AV3 (Sprint pré-AV3 — 18/06 → 06/07)

| Período | Foco | Responsável |
|---------|------|-------------|
| **18/06 (hoje)** | Atualizar GANTT + relatório com novo prazo; abrir 1 issue por integrante | Elder |
| **18/06 → 22/06** | `ApacheParser` (Common + Combined) + testes unitários | Aryan |
| **19/06 → 23/06** | `LogFileDAO` streaming linha-a-linha + hash SHA-256 | Aryan |
| **20/06** | Criar entry point `pdm run gui` no `pyproject.toml` | Helena |
| **22/06** | `BruteForceDetector` (janela de tempo + threshold) + teste com `tests/fixtures/sample_brute_force.log` | Aryan |
| **22/06 → 25/06** | CLI `analyze` real (substitui stub) chamando ApacheParser | Rodrigo |
| **23/06 → 26/06** | GUI: QThread worker + QTableView com resultados do parser | Helena |
| **25/06 → 27/06** | CLI `detect brute-force` + saída Rich | Rodrigo |
| **26/06 → 30/06** | `ScannerDetector` + 1ª iteração de `TrafficSpikeDetector` | Aryan |
| **27/06 → 01/07** | GUI: drag&drop de `.log` + filtros básicos | Helena |
| **27/06 → 02/07** | CLI `batch` + `--output json` | Rodrigo |
| **01/07 → 03/07** | `Pipeline` + `Aggregator` consolidando detectores | Aryan |
| **02/07 → 05/07** | Flags hardening CLI (`--anonymize-ips`, `--max-lines`) | Rodrigo |
| **05/07** | Branch protection no `master` + atualizar `APENDICE_COMMITS.md` | Elder |
| **06/07** | Smoke test E2E (CLI + GUI sobre fixtures) + gravar demo curta (3 min) | todos |
| **07/07** | Ensaio da apresentação cronometrado (alvo 25 min); revisar slides | todos |
| **08/07** | **Apresentação AV3** 🎯 | todos |

### 6.3 Replanejamento para AV4 / AV5 (após 08/07)

| Período | Entrega | Responsável |
|---------|---------|-------------|
| 09/07 → 22/07 | Detectores complementares + Aggregator final | Aryan |
| 09/07 → 22/07 | CLI completa (`--format`, paginação Rich) | Rodrigo |
| 09/07 → 22/07 | GUI: exportar JSON + barra de progresso | Helena |
| 15/07 → 29/07 | PyInstaller release v0.1.0 (Linux + Windows) | Elder |
| 15/07 → 22/07 | Preparar AV4 (Seminário) | todos |
| 22/07 → 12/08 | Hardening (B4/B5/S1/S5/S6/anonymize) + cobertura ≥ 80% para AV5 | Aryan + Elder |

---

## 7. Demonstração breve do app — estado atual (2026-06-10)

### O que **roda** hoje
```bash
# CLI (esqueleto Typer)
pdm run python -m python_pdm_template --help                # ainda printa "Hello"
pdm run python -m python_pdm_template.cli.main --help       # mostra subcomandos analyze e batch
pdm run python -m python_pdm_template.cli.main analyze access.log
# Saída: "Analisando access.log... (nao implementado ainda)"

# GUI (esqueleto PySide6)
pdm run python -c "from python_pdm_template.gui.main_window import MainWindow; from PySide6.QtWidgets import QApplication; import sys; a=QApplication(sys.argv); w=MainWindow(); w.show(); a.exec()"
# Abre janela 1024x768 com texto "Em construcao"

# Testes
pdm run pytest -q
# 1 teste verde: test_log_entry_armazena_campos_obrigatorios
```

### Roteiro de demo (3 min) — versão mínima honesta
1. **Abrir terminal** e mostrar `git log --oneline -10` (ritmo do projeto).
2. **CLI:** rodar `--help` mostrando os 2 subcomandos planejados.
3. **GUI:** abrir a janela vazia e dizer "esqueleto pronto, próxima sprint conecta ao Core".
4. **Testes:** rodar `pytest` e mostrar a saída verde + `--cov`.
5. **Pipeline CI:** abrir a aba Actions no GitHub mostrando build verde.
6. **Docs AV3:** abrir os 5 documentos novos no GitHub.

### Se até 14/06 o Core estiver pronto (Aryan), substituir os passos 2 e 3 por:
1. Mostrar análise real de `tests/fixtures/sample_brute_force.log` na CLI.
2. Reproduzir a mesma análise na GUI (paridade — propriedade emergente PEF-05).
3. Exportar JSON e mostrar hash + versão (cadeia de custódia).

---

## 8. Onde está cada documento

```
docs/
├── PROJETO.md              ← visão geral
├── ESCOPO.md               ← in/out scope
├── REQUISITOS.md           ← RF/RNF
├── CASOS_DE_USO.md
├── GANTT.md                ← cronograma (atualizado)
├── architecture/
│   ├── ARQUITETURA.md
│   ├── CORE_API.md
│   ├── CLI_DESIGN.md
│   └── GUI_DESIGN.md
├── testing/
│   ├── ESTRATEGIA_TESTES.md
│   └── CRITERIOS_ACEITACAO.md
├── team/
│   ├── PAPEIS.md
│   └── CONVENCOES.md
└── av3/                    ← ENTREGA DESTA AVALIAÇÃO
    ├── 01_BARREIRAS_SALVAGUARDAS.md
    ├── 02_PROPRIEDADES_EMERGENTES.md
    ├── 03_DIMENSOES_CONFIANCA.md
    ├── 04_PERIGOS_ACIDENTES_DANOS.md
    ├── 05_AMEACAS_VULNERABILIDADES.md
    ├── APRESENTACAO.md
    ├── APENDICE_COMMITS.md
    └── RELATORIO_AV3.md    ← (este arquivo)
```
