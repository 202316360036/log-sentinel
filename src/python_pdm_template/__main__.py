"""
Este arquivo é o ponto de entrada principal do pacote `python_pdm_template`.

Função principal:
- Define a função `main`, que é executada quando o pacote é chamado diretamente pela linha de comando.

Como construir e usar:
1. Certifique-se de que o projeto está configurado corretamente com o PDM.
2. Instale seu pacote no ambiente virtual usando:
   ```bash
    pdm install
    ```
3. Execute o comando abaixo para rodar o pacote diretamente:
   ```bash
   pdm run python -m python_pdm_template
   ```
4. O arquivo `__main__.py` permite que o pacote seja executado como um script, exibindo a mensagem "Hello, Python PDM Template!".
Este arquivo é útil para fornecer uma interface de linha de comando simples para o pacote.
"""

from python_pdm_template.exemplo_pydantic import Usuario, exemplo_uso, exemplo_coercao


def main():
    """Função principal que exibe uma mensagem de boas-vindas."""
    print("Hello, Python PDM Template!")
    print()

    print("Exemplo de uso do pydantic:")
    exemplo_uso()
    print()

    print("Exemplo de coerção automática de tipos:")
    exemplo_coercao()
    print()


# Verifica se o arquivo está sendo executado diretamente
if __name__ == "__main__":
    main()
