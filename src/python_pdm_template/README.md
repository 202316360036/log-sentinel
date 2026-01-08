# Estrutura de Projeto Python Modular

Este diretório segue o padrão moderno de organização de projetos Python, utilizando uma pasta `src/` para separar o código-fonte principal dos demais arquivos do projeto.

## Por que usar a pasta `src/`?

- **Evita conflitos de importação:** Ao manter o código dentro de `src/`, você garante que os testes e scripts externos não importem acidentalmente arquivos do diretório raiz.
- **Facilita a modularização:** Permite que o projeto seja organizado em múltiplos módulos e subpacotes, tornando o código mais limpo e escalável.
- **Melhora a manutenção:** Separar o código-fonte dos arquivos de configuração, documentação e testes facilita a navegação e manutenção do projeto.

## Estrutura típica

```
raiz-do-projeto/
│   README.md
│   pyproject.toml
│   ...
├── src/
│   └── nome_do_pacote/
│       ├── __init__.py
│       ├── modulo1.py
│       ├── modulo2.py
│       └── ...
├── tests/
│   └── test_modulo1.py
│   └── ...
```

## Vantagens para projetos profissionais

- Facilita publicação no PyPI
- Evita problemas de importação durante testes (pacotes não encontrados)
  - Todos os pacotes são instalados corretamente no ambiente virtual (pasta `.venv/`), seguindo as versões especificadas no `pyproject.toml`
- Permite crescimento do projeto sem bagunça
- Adota boas práticas recomendadas pela comunidade Python

