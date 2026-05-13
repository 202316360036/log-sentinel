# Cronograma de Implementação — Log Sentinel 2026.1

Gráfico de Gantt com as cinco milestones do projeto, distribuídas entre abril e agosto de 2026. Datas alinhadas ao cronograma oficial da disciplina Engenharia de Software II.

```mermaid
gantt
    title Log Sentinel - 2026.1
    dateFormat YYYY-MM-DD
    axisFormat %d/%m

    section AV1 Ambiente
    Setup do repositorio     :done, 2026-04-01, 2026-04-15

    section AV2 Testes
    DEF (RF/RNF/RN)          :done, 2026-04-15, 2026-05-05
    TDD e criterios          :active, 2026-05-05, 2026-05-13
    Apresentacao AV2         :milestone, 2026-05-13, 0d

    section Core (Aryan)
    Models e Parsers         :2026-05-13, 12d
    Detectors                :2026-05-25, 14d
    Pipeline e Factories     :2026-06-08, 7d

    section CLI (Rodrigo)
    Comandos analyze/batch   :2026-05-20, 15d
    Comando detect           :2026-06-05, 10d

    section GUI (Helena)
    MainWindow e workers     :2026-05-20, 20d
    Filtros e exportacao     :2026-06-10, 14d

    section CI/CD (Elder)
    Pipeline e cobertura     :2026-04-15, 30d
    PyInstaller e releases   :2026-06-15, 30d

    section AV3 e AV5
    AV3 Falhas               :milestone, 2026-06-17, 0d
    Polimento e Release      :2026-07-15, 30d
    AV5 Final                :milestone, 2026-08-12, 0d
```

## Marcos da disciplina

| AV | Tema | Data |
|---|---|---|
| AV1 | Configuração do ambiente | 15/04/2026 ✅ |
| AV2 | Testes de Software | 13/05/2026 |
| AV3 | Falhas de Software | 17/06/2026 |
| AV4 | Seminário | 22/07/2026 |
| AV5 | Riscos e Qualidade | 12/08/2026 |
| Prova final | — | 19/08/2026 |

## Sprints internas

| Sprint | Período | Foco | Responsáveis |
|---|---|---|---|
| Sprint 0 — Setup & Documentação | até 11/05/2026 ✅ | Fork, CI/CD, docs, página de estudo | Elder, Rodrigo |
| Sprint 1 — Core MVP | 13/05 → 08/06/2026 | LogEntry, parsers, detectores, DAOs | Aryan |
| Sprint 2 — CLI & GUI | 13/05 → 30/06/2026 | Comandos reais, MainWindow PySide6 | Rodrigo, Helena |
| Sprint 3 — Polimento & Release | a partir de 15/07/2026 | PyInstaller, hardening, documentação final | Elder |

## Notas

- As previsões serão revisadas a cada AV. Atualizações vão direto nos campos `due_on` das milestones do GitHub.
- O Gantt é renderizado nativamente pelo GitHub na visualização do `.md` (suporte a Mermaid habilitado por padrão).
