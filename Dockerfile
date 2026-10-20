FROM ghcr.io/astral-sh/uv:python3.14-bookworm-slim

ENV PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=never

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        imagemagick \
        ghostscript \
        fonts-dejavu-core \
    && rm -rf /var/lib/apt/lists/*

# Debian's ImageMagick policy blocks the PDF coder; /upload writes a PDF with it.
RUN set -eux; \
    for policy in /etc/ImageMagick-*/policy.xml; do \
        [ -f "$policy" ] || continue; \
        sed -i -E '/pattern="[^"]*PDF[^"]*"/ s/rights="none"/rights="read|write"/' "$policy"; \
    done

ARG UID=1000
RUN useradd --create-home --uid "$UID" app \
    && mkdir -p /tmp/facturas_temp \
    && chown -R app:app /tmp/facturas_temp

WORKDIR /app

COPY pyproject.toml uv.lock .python-version README.md ./
RUN uv sync --frozen --no-dev --no-install-project

COPY src ./src
COPY static ./static
RUN uv sync --frozen --no-dev \
    && chown -R app:app /app

ENV PATH="/app/.venv/bin:$PATH"

USER app

EXPOSE 8000

CMD ["uvicorn", "impresion_facturas.main:app", "--host", "0.0.0.0", "--port", "8000"]
