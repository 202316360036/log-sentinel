# Estrutura de Projeto Python Modular

Este diretório segue o padrão moderno de organização de projetos Python, utilizando uma pasta `src/` para separar o código-fonte principal dos demais arquivos do projeto.

## Por que usar a pasta `src/`?

- **Evita conflitos de importação:** Ao manter o código dentro de `src/`, você garante que os testes e scripts externos não importem acidentalmente arquivos do diretório raiz.
- **Facilita a modularização:** Permite que o projeto seja organizado em múltiplos módulos e subpacotes, tornando o código mais limpo e escalável.
- **Melhora a manutenção:** Separar o código-fonte dos arquivos de configuração, documentação e testes facilita a navegação e manutenção do projeto.


## Arquivos `__init__.py` 

- Torna a pasta um pacote Python, permitindo importações entre módulos e subpacotes.
- **Deve estar presente em TODAS as pastas e subpastas** que contenham arquivos Python `.py`.
  - Sem esse arquivo, o Python não reconhece o diretório como parte do pacote, o que pode causar erros de importação.
- Pode ser vazio ou conter código de inicialização do pacote.

## Arquivo `__main__.py`

- Permite que o pacote seja executado diretamente como um programa, usando o comando:
  ```bash
  python -m nome_do_pacote
  ```
- O código dentro de `__main__.py` será executado quando o pacote for chamado dessa forma.
- Ideal para definir pontos de entrada do projeto, como scripts CLI ou inicialização de aplicações.

## Estrutura típica

```
raiz-do-projeto/
│   README.md
│   pyproject.toml
│   ...
├── src/
│   └── nome_do_pacote/
│       ├── __init__.py
│       ├── __main__.py
│       ├── modulo1.py
│       ├── modulo2.py
│       ├── modulo3/
│       │   ├── __init__.py
│       │   ├── submodulo1.py
│       │   └── ...
│       └── ...
├── tests/
│   ├── test_modulo1.py
│   ├── test_modulo2.py
|   ├── modulo3/
│   │   ├── test_submodulo1.py
│   │   └── ...
│   └── ...
```

## Vantagens para projetos profissionais

- Facilita publicação no PyPI
- Evita problemas de importação durante testes (ex: pacotes não encontrados, versões erradas, etc.)
  - Todos os pacotes são instalados corretamente no ambiente virtual (pasta `.venv/`), seguindo as versões especificadas no `pyproject.toml`
- Permite crescimento do projeto sem bagunça
- Adota boas práticas recomendadas pela comunidade Python

