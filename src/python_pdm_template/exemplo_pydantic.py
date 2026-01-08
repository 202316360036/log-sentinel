"""
Exemplo de uso do Pydantic para coerção e validação automática de tipos de dados.

O [Pydantic](https://docs.pydantic.dev/) é uma biblioteca que permite criar modelos de dados com validação automática de tipos, conversão (coerção) e validação de valores.

Instalação:
    pdm add pydantic

Exemplo básico:
"""

from pydantic import BaseModel, ValidationError


class Usuario(BaseModel):
    id: int
    nome: str
    ativo: bool = True


def exemplo_uso():
    """Exemplo de criação de um usuário com validação automática."""
    try:
        usuario = Usuario(id=1, nome="João")
        print(usuario)
        # Saída: id=1 nome='João' ativo=True
    except ValidationError as e:
        print("Erro de validação:", e)


def exemplo_coercao():
    """Exemplo de coerção automática de tipos."""
    try:
        usuario = Usuario(id="123", nome=456, ativo="true")  # pyright: ignore[reportArgumentType]
        print(usuario)
        # Saída: id=123 nome='456' ativo=True
    except ValidationError as e:
        print("Erro de validação:", e)


"""
Explicação:
- O Pydantic converte automaticamente tipos compatíveis (ex: string para int, int para string, string 'true' para bool).
- Se um valor não puder ser convertido, um ValidationError será lançado.
- O uso de modelos Pydantic é ideal para validação de dados de entrada em APIs, scripts e aplicações.

Para mais exemplos e validações avançadas, consulte a documentação oficial: https://docs.pydantic.dev/
"""
