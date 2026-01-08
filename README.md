# python_pdm_template

Este repositório é um template para projetos Python utilizando o [PDM](https://pdm.fming.dev/), uma ferramenta moderna de gerenciamento de pacotes e ambientes.

## Como usar este template

1. **Copiar o template**:
   - No GitHub, clique no botão ``Use this template`` (ou ``Usar este template``) na página do repositório.
   - Siga as instruções para criar um novo repositório baseado neste template.

2. **Clonar o repositório**:
   - Clone o novo repositório para sua máquina local:
     ```bash
     git clone https://github.com/seu-usuario/seu-repositorio.git
     cd seu-repositorio
     ```

## Configuração do ambiente

1. **Instalar o PDM**:
   - Certifique-se de que o PDM está instalado. Caso não esteja, instale-o com o seguinte comando:
     ```bash
     python -m pip install pdm
     ```

2. **Instalar dependências**:
   - Execute o comando abaixo para instalar as dependências do projeto:
     ```bash
     python -m pdm install
     ```

3. **Adicionar novas dependências**:
   - Para adicionar uma nova dependência ao projeto, use o comando:
     ```bash
     python -m pdm add nome-da-dependencia
     ```
   - Para adicionar dependências de desenvolvimento (instaladas apenas no ambiente de desenvolvimento - nunca em produção), utilize:
     ```bash
     python -m pdm add -d nome-da-dependencia
     ```

## Executar o projeto

1. **Rodar o projeto**:
   - Após instalar as dependências, você pode executar o projeto diretamente usando:
     ```bash
     python -m pdm run python -m python_pdm_template
     ```

## Build do projeto

1. **Construir o projeto**:
   - Para criar um pacote instalável do projeto, utilize o comando:
     ```bash
     python -m pdm build
     ```
   - O pacote `.whl` será gerado na pasta `dist/`.

2. **Publicar o pacote (opcional)**:
   - Para publicar o pacote no PyPI (para que qualquer pessoa possa utilizar seu programa), use o comando:
     ```bash
     python -m pdm publish
     ```
  - Certifique-se de ter uma conta no PyPI antes de publicar.

## Estrutura do projeto

- **``.github/``**: Configurações do GitHub, como workflows de CI/CD.
- **``.vscode/``**: Configurações do Visual Studio Code.
- **``src/``**: Contém o código-fonte do projeto.
- **``tests/``**: Contém os testes do projeto.
- **``pyproject.toml``**: Arquivo de configuração do projeto, incluindo dependências e metadados.
Para mais informações sobre o PDM, consulte a [documentação oficial](https://pdm.fming.dev/).
