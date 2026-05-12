"""Entry point da CLI do Log Sentinel."""
from __future__ import annotations
import typer

app = typer.Typer(help="Log Sentinel - Analise post-mortem de logs Apache")


@app.command()
def analyze(arquivo: str) -> None:
    """Analisa um unico arquivo de log."""
    typer.echo(f"Analisando {arquivo}... (nao implementado ainda)")


@app.command()
def batch(diretorio: str) -> None:
    """Analisa multiplos arquivos de um diretorio."""
    typer.echo(f"Batch em {diretorio}... (nao implementado ainda)")


if __name__ == "__main__":
    app()
