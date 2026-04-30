# Diretório de Distribuição (`dist/`)

Este diretório é destinado ao armazenamento dos artefatos compilados e empacotados do projeto. Aqui você encontrará (ou irá gerar) os pacotes instaláveis Python (`.whl` e `.tar.gz`) e os executáveis binários nativos (`.exe`).

**Sumário**
- [Diretório de Distribuição (`dist/`)](#diretório-de-distribuição-dist)
  - [1. Pré-requisitos](#1-pré-requisitos)
  - [2. Compilando projeto (.WHL e .TAR.GZ)](#2-compilando-projeto-whl-e-targz)
  - [3. Compilando um Executável Standalone (.exe, etc)](#3-compilando-um-executável-standalone-exe-etc)
  - [4. Limpendo os arquivos de build](#4-limpendo-os-arquivos-de-build)
  - [5. Incorporando distribuicao no processo de CI/CD](#5-incorporando-distribuicao-no-processo-de-cicd)


## 1. Pré-requisitos

Antes de compilar o projeto, instale as dependências no ambiente virtual (pasta `.venv`) gerenciado pelo ``PDM``.
```bash
pdm add -d pyinstaller
pdm install
```

## 2. Compilando projeto (.WHL e .TAR.GZ)

Essa etapa e feita se o objetivo é distribuir o projeto como uma *biblioteca ou ferramenta de linha de comando* instalável via ``pip``. Para isso, utilizamos o próprio construtor nativo do ``PDM``.

Para gerar os arquivos .whl (Wheel) e .tar.gz (Source Distribution), execute na raiz do projeto:
```bash
pdm build
```

Os arquivos compilados aparecerão automaticamente nesta pasta ``dist/``.
Você pode instalá-los no computador usando o comando:
```bash
pip install dist/*.whl
```

ou, caso esteja usando o `pipx`, voce pode instalar da seguinte forma:
```bash
python -m pipx install dist/*.whl
```
**OBS**: O `pipx` facilita a execução de ferramentas  CLI (linha de comando), permitindo que você as execute diretamente no terminal sem precisar ativar um ambiente virtual específico.
  - **Ex**: `python -m pipx install pdm` e depois `pdm --version` para verificar a instalação.    
  - Para isso, o `pipx` irá criar um ambiente virtual isolado (``.venv``) para a instalação de ferramenta/pacote CLI, garantindo que ele não interfira com outras dependências do sistema (de maneira similar ao que o PDM faz, porém permitindo o acesso a ferramenta CLI para qualquer pessoa do computador). 

## 3. Compilando um Executável Standalone (.exe, etc)

Se o objetivo é distribuir a aplicação para usuários finais que não possuem o Python instalado em suas máquinas, utilizamos o ``pyinstaller`` para empacotar o interpretador e todas as dependências em um único arquivo ``.exe``.

Para gerar o executável, rode o comando abaixo:
```bash
pdm run pyinstaller --onefile --windowed --name "Nome_Do_Meu_App" src/python_pdm_template/__main__.py
```
- ``--onefile``: Empacota tudo em um único arquivo ``.exe`` (mais fácil para distribuir entre os usuários).
- ``--windowed``: (Opcional) Remove a janela preta do terminal ao abrir o app. Use isso apenas se o seu app tiver uma Interface Gráfica (GUI). Se for um app de terminal (CLI), remova esta flag.
- ``--name``: O nome final do seu arquivo executável.
- ``src/python_pdm_template/__main__.py``: O caminho para o script principal (entrypoint) do seu projeto (equivale ao arquivo que contem a função ``main()`` do Java, C, C++). Ajuste conforme o seu projeto (pastas e arquivos do projeto).

O PyInstaller colocará o ``.exe`` gerado diretamente dentro desta pasta ``dist/``.
- **OBS**: O processo do PyInstaller também criará uma pasta ``build/`` na raiz do projeto e um arquivo ``.spec``. Eles são arquivos temporários e de configuração da build, e geralmente devem ser ignorados pelo Git (através do arquivo ``.gitignore``).

**IMPORTANTE**: A depender das bibliotecas utilizadas no projeto, o processo de empacotamento pode ser mais complexo, exigindo a inclusão de arquivos adicionais (como arquivos de configuração, recursos, etc). 
  - Neste case, voce pode usar as flags abaixo ao rodar o ``pyinstaller``:
    - ``--collect-all``: Inclui todos os arquivos relacionados a um pacote específico (útil para bibliotecas que possuem recursos adicionais).
    - ``--add-data``: Permite adicionar arquivos ou pastas específicas ao executável. O formato é `caminho_origem;caminho_destino` (ex: `config:config` para incluir a pasta `config` dentro do executável).
```bash
pdm run pyinstaller --onefile --windowed --name "Nome_Do_Meu_App" --collect-all pyside6 --add-data "config:config" src/python_pdm_template/__main__.py
```
  
## 4. Limpendo os arquivos de build

Após gerar os arquivos de distribuição, você pode limpar os arquivos temporários criados durante o processo de build. Isso é imporante pois esses arquivos podem gerar problemas de compatibilidade e conflitos em builds futuros, além de ocupar espaço desnecessário no projeto.

Para isso, basta remover as pastas ``build/`` e os arquivos ``.spec`` gerados pelo PyInstaller:

```bash
# No Bash (Linux/Mac), execute:
rm -rf build/
rm -rf *.spec
```

```pwsh
# No PowerShell (Windows), execute:
Remove-Item -Recurse -Force build/*
Remove-Item -Force *.spec
```

Em caso de duvidas, consulte a documentação oficial do [PyInstaller](https://pyinstaller.org/en/stable/).

## 5. Incorporando distribuicao no processo de CI/CD

Para automatizar o processo de build e distribuição, você pode configurar um pipeline de CI/CD (Integração Contínua/Entrega Contínua) usando ferramentas como GitHub Actions (pasta `[.github/workflows](../github/workflows)`).

Para isso, modifique o arquivo de workflow (ex: `test.yml`) e adicione as seguintes etapas após a etapa de testes:

```yaml
    - name: Build Distribution
      run: |
        pdm build
        pdm run pyinstaller --onefile --windowed --name "Nome_Do_Meu_App" src/python_pdm_template/__main__.py

    - name: Upload Distribution Artifacts
      uses: actions/upload-artifact@v3
      with:
        name: dist-${{ runner.os }}
        path: dist/
```

Depois crie um novo job para publicar os artefatos gerados no GitHub Releases:

```yaml
  publish:
    needs: test_build
    runs-on: ubuntu-latest
    steps:
    - name: Download Distribution Artifacts
      uses: actions/download-artifact@v3
      with:
        name: dist-${{ runner.os }}
        merge: true    

    - name: Publish to GitHub Releases
      uses: softprops/action-gh-release@v1
      with:
        files: dist/*
```