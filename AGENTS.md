# AGENTS.md

## Overview
Full-stack single-origin app: FastAPI serves both the API and the 3-screen mobile PWA in `static/`.
- `src/impresion_facturas/main.py` — POST `/upload` (ImageMagick threshold → merged PDF) + static mount.
- `static/` — Spanish UI built from `static/prd_impresi_n_de_facturas_mobile.md`; the upload flow is wired to the API.

## Commands
```bash
uv sync
uv run uvicorn impresion_facturas.main:app --reload   # app + API on :8000
```
Open `http://localhost:8000/` for the PWA. There are no tests, lint, typecheck, or CI configured — do not invent commands.

## Backend
- Upload field name is `archivos` (`List[UploadFile]`); a bare POST returns 422.
- Needs ImageMagick (`magick`/`convert`) and Ghostscript for PDF output; otherwise `/upload` returns 500 with the error text.
- Output goes to `$FACTURAS_TMP` (default `<repo>/fotos/facturas_temp`), always as `facturas_procesadas.pdf` (fixed name, overwritten each run). Temp images are deleted; the PDF is not.
- Every input file, PDFs included, goes through the ImageMagick raster/threshold pipeline before merging.
- Routes must use decorators: `@app.get` / `@app.post`. `app.get(...)` without `@` silently registers nothing (past 404 bug).
- The static mount is registered last so API routes and `/docs` keep working.
- CORS is `allow_origins=["*"]`, which lets the optional preview server on :8017 post to :8000.

## Docker
```bash
docker compose up --build   # app on http://localhost:8000
docker compose down
```
- Base image `ghcr.io/astral-sh/uv:python3.14-bookworm-slim` + ImageMagick 6 (`convert`, not `magick`) + Ghostscript.
- `./salida` is bind-mounted to `/tmp/facturas_temp`, so the generated PDF shows up there on the host.
- The Dockerfile rewrites `/etc/ImageMagick-*/policy.xml` to allow the `PDF` coder. Debian blocks it by default and `/upload` fails with "not authorized" — do not remove that step.
- `uv sync` installs the project editable, which is why `static/` resolves to `/app/static`; `STATIC_DIR` can override it.
- Runs as non-root user `app`; build-arg `UID` (default 1000) must match the owner of `./salida`.

## Frontend
- Flow: `index.html` → `revision.html` → `procesando.html`. Plain HTML/CSS/JS, no build step; Tailwind + fonts load from CDN (needs network).
- Selected `File` objects live in IndexedDB (`facturas-db` → `archivos`, keyPath `id` = index). Thumbnails/selection/notices live in `sessionStorage` (`fp_files`, `fp_sel`, `fp_notice`). Do not put blobs in `sessionStorage` (quota).
- `procesando.html` posts multipart `archivos` with XHR for real progress; it uses same-origin `/upload` unless the page is not on :8000 (then `hostname:8000`).
- `revision.html` with no files shows 6 demo invoices and its CTA returns to upload; keep that guard so demo data never hits the API.
- Cancel aborts the XHR and returns to `revision.html` keeping the selection intact (FR-05).
- The Tailwind theme config is duplicated inline in all 3 HTML files; change them together.
- Design source of truth is the Stitch project "Image Print Manager".
- No service worker → not installable as a PWA yet (Chrome requires one with a fetch handler).
- `uv run impresion-facturas` only prints `Hello from impresion-facturas!`; it does not start the server.
- `README.md` is an empty placeholder.
