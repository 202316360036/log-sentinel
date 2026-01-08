"""
Arquivos de teste precisam ser nomeados com o prefixo `test_` ou sufixo `_test` para que o pytest os reconheça automaticamente.

Este arquivo contém exemplos de testes utilizando pytest, incluindo:
- Um teste simples para validar uma função.
- Um teste que utiliza o recurso de monkeypatching do pytest para modificar comportamentos durante o teste.

O objetivo é demonstrar como usar o pytest e seus recursos para criar testes eficazes.
"""

from src.python_pdm_template.utils import somar, obter_mensagem

# Teste simples
def test_somar():
    """Teste simples para a função somar."""
    resultado = somar(2, 3)
    assert resultado == 5, "A soma de 2 e 3 deve ser 5"

# Teste com monkeypatching
def test_obter_mensagem(monkeypatch):
    """Teste que utiliza monkeypatching para modificar o comportamento da função obter_mensagem."""

    # Função substituta para o monkeypatch
    def mensagem_alternativa(prompt):
        return "Mensagem modificada"

    # Aplicando o monkeypatch para substituir a função obter_mensagem
    monkeypatch.setattr("builtins.input", mensagem_alternativa)

    # Verificando se a função foi substituída corretamente
    resultado = obter_mensagem()
    assert resultado == "Mensagem modificada", "A mensagem deve ser modificada pelo monkeypatch"

# Comentários adicionais:
# - O pytest é um framework de testes poderoso e fácil de usar para Python.
# - O recurso de monkeypatching permite substituir funções, métodos ou atributos durante o teste, útil para isolar dependências externas.
# - O uso de asserts no pytest é direto e fornece mensagens úteis em caso de falha.
# - Para rodar os testes, use o comando `pytest tests/` no terminal.
