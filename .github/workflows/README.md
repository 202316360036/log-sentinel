# CI/CD com GitHub Actions

Este diretório deve conter os arquivos de workflow do GitHub Actions para automação de testes, builds e deploys do projeto.

## O que é GitHub Actions?
O [GitHub Actions](https://docs.github.com/pt/actions) permite criar pipelines de integração contínua (CI) e entrega contínua (CD) diretamente no repositório.

## Como funciona
- Os arquivos de workflow são escritos em YAML e ficam na pasta `.github/workflows/`.
- Cada arquivo define um ou mais jobs (tarefas) que são executados em eventos como push, pull request ou tags.
- Caso haja alguma falha em um job, o GitHub Actions para o workflow e notifica os colaboradores do repositório por email.

## Exemplo de pipeline para Python com PDM
```yaml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Instalar Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.14'

      - name: Instalar PDM
        run: python -m pip install pdm

      - name: Instalar dependências
        run: python -m pdm install

      - name: Rodar testes
        run: python -m pdm run pytest
```

## Dicas
- Crie arquivos como `test.yml`, `ci.yml`, ou `deploy.yml` para diferentes etapas.
  - O arquivo `test.yml` roda os testes automatizados e de cobertura com pytest (já incluído neste template).
  - O arquivo `ci.yml` pode ser usado para builds e verificações adicionais.
  - O arquivo `deploy.yml` pode ser configurado para publicar pacotes ou fazer deploy automático.
- Consulte a [documentação oficial](https://docs.github.com/pt/actions) para exemplos e boas práticas.
- Use secrets do GitHub para armazenar tokens e senhas de deploy.

## Recomendações
- Sempre automatize testes antes de merges.
- Gere relatórios de cobertura e artefatos para análise posterior.
- Adapte os workflows conforme as necessidades do seu projeto.
