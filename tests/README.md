# Testes com Pytest

Esta pasta contém os testes do projeto e está configurada para ser utilizada com o framework de testes [pytest](https://docs.pytest.org/).

## Como usar

1. Certifique-se de que o pytest está instalado no ambiente Python do projeto. Caso não esteja, instale-o com o seguinte comando:

   ```bash
   python -m pdm add -d pytest
   ```

2. Para executar todos os testes desta pasta, utilize o seguinte comando na raiz do projeto:

   ```bash
   python -m pdm run pytest
   ```

3. Para executar um teste específico, forneça o caminho do arquivo de teste ou da pasta. Por exemplo:

   ```bash
   python -m pdm run pytest tests/test_exemplo.py
   ```

4. Utilize a opção `-v` para obter mais detalhes sobre os testes executados:

   ```bash
   python -m pdm run pytest -v
   ```

## Cobertura de Código (Coverage)

O projeto está configurado para usar o [pytest-cov](https://pytest-cov.readthedocs.io/) para medir a cobertura de código durante a execução dos testes.

### Como funciona

- O **coverage** (cobertura) mede qual porcentagem do código-fonte é executada durante os testes.
- Isso ajuda a identificar partes do código que não estão sendo testadas.
- O projeto está configurado para gerar automaticamente relatórios de cobertura ao executar os testes.

### Relatórios gerados

Ao executar `pdm run pytest`, três tipos de relatórios são gerados automaticamente:

1. **Relatório no terminal**: Exibe a cobertura diretamente no console após a execução dos testes.

2. **Relatório HTML** (pasta `htmlcov/`):
   - Contém um relatório visual detalhado em formato HTML.
   - Para visualizar, abra o arquivo `htmlcov/index.html` no navegador.
   - Mostra linha por linha qual código foi executado (verde) e qual não foi (vermelho).

3. **Arquivo XML** (`coverage.xml`):
   - Formato XML usado por ferramentas de integração contínua (CI/CD).
   - Útil para integração com plataformas como GitHub Actions, GitLab CI, etc.

### Configuração

A configuração do coverage está no arquivo `pyproject.toml`:

```toml
[tool.pytest.ini_options]
addopts = "--cov=src --cov-report=html --cov-report=term --cov-report=xml"
```

## Estrutura

- **`conftest.py`**: Arquivo de configuração do pytest, onde podem ser definidas fixtures e hooks globais.
- **Arquivos de teste**: Devem seguir o padrão `test_*.py` ou `*_test.py` para serem automaticamente descobertos pelo pytest.

Para mais informações, consulte a [documentação oficial do pytest](https://docs.pytest.org/).