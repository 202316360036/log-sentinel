# syntax=docker/dockerfile:1.7

# Etapa 1: builder. Instala dependencias e empacota o binario da CLI
# com PyInstaller. Nao inclui PySide6/GUI para manter a imagem pequena.
# Bookworm em ambas as etapas garante o mesmo glibc. Sem essa fixacao, o
# binario compilado com PyInstaller em uma imagem base mais nova falha
# ao carregar libm com "GLIBC_2.38 not found" na imagem final.
FROM python:3.14-slim-bookworm AS builder

WORKDIR /build

RUN apt-get update && apt-get install -y --no-install-recommends \
        binutils \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir --upgrade pip setuptools

# Copia so o que interessa para o build da CLI. LICENSE e exigido pela
# validacao de license-files do backend PDM declarada no pyproject.
COPY pyproject.toml README.md LICENSE ./
COPY src/ ./src/

# Instala em modo editable sem resolver deps declaradas no pyproject
# (PySide6 nao vai pra imagem final). Depois instala as deps de runtime
# efetivas da CLI mais o PyInstaller e o setuptools que ele exige.
RUN pip install --no-cache-dir --no-deps -e . \
    && pip install --no-cache-dir "pyinstaller>=6.10" setuptools typer rich

RUN pyinstaller --onefile --name log-sentinel \
        src/python_pdm_template/__main__.py \
    && test -f dist/log-sentinel

# Etapa 2: runtime minimo. Apenas o binario, sem Python nem toolchain.
FROM debian:bookworm-slim AS runtime

RUN groupadd --system app && useradd --system --gid app --home /home/app app \
    && mkdir -p /logs && chown app:app /logs

COPY --from=builder /build/dist/log-sentinel /usr/local/bin/log-sentinel

USER app
WORKDIR /logs

ENTRYPOINT ["log-sentinel"]
CMD ["--help"]
