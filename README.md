# Facturas a PDF

Convierte fotos o archivos de facturas en **un solo PDF en blanco y negro, listo para imprimir**.

La app corre en el navegador como PWA móvil: eliges las facturas, las revisas, y el servidor limpia cada página con ImageMagick (las pasa a escala de grises y aplica un umbral para dejar el texto negro y el fondo blanco) y las une en un único PDF.

## Cómo funciona

1. Seleccionas las imágenes o PDFs en la pantalla de inicio.
2. En la revisión puedes quitar las que no quieras y confirmar.
3. El navegador sube los archivos a `POST /upload`; el servidor:
   - guarda cada archivo en el directorio temporal,
   - detecta si la imagen es oscura y aplica el umbral correspondiente (`-negate` + `35%` para fondos oscuros, `70%` para claros),
   - une todas las páginas procesadas en `facturas_procesadas.pdf`,
   - borra las imágenes intermedias.

El PDF queda siempre con el mismo nombre y se sobrescribe en cada ejecución.

## Stack

- **Backend**: FastAPI + Uvicorn (`src/impresion_facturas/main.py`).
- **Frontend**: HTML/CSS/JS sin build, Tailwind y fuentes por CDN (`static/`).
- **Procesamiento**: ImageMagick (6 en Docker, 7 en local) + Ghostscript para leer PDFs de entrada.
- **Gestión de Python**: [uv](https://docs.astral.sh/uv/) (Python 3.14).

## Requisitos

- Python 3.14 y `uv`.
- ImageMagick (`magick` o `convert`) y Ghostscript (`gs`).
- Opcional: Docker + Docker Compose.

## Uso local

```bash
uv sync
uv run uvicorn impresion_facturas.main:app --reload
```

Abre <http://localhost:8000/>. El PDF se guarda por defecto en `fotos/facturas_temp/facturas_procesadas.pdf`.

Variables de entorno útiles:

| Variable        | Default                          | Descripción                                  |
|-----------------|----------------------------------|----------------------------------------------|
| `FACTURAS_TMP`  | `<repo>/fotos/facturas_temp`     | Directorio de trabajo y destino del PDF      |
| `STATIC_DIR`    | `<repo>/static` o `/app/static`  | Carpeta del frontend                         |

## Docker

```bash
docker compose up --build
```

La app queda en <http://localhost:8000/> y el PDF aparece en `./salida/facturas_procesadas.pdf` (el directorio está montado en `/tmp/facturas_temp`).

La imagen corre como usuario no-root `app` (`UID=1000` por defecto); si tu usuario tiene otro UID, compila con `docker compose build --build-arg UID=$(id -u)` para que pueda escribir en `./salida`.

## API

### `POST /upload`

Multipart con el campo repetible `archivos`.

```bash
curl -X POST http://localhost:8000/upload \
  -F "archivos=@factura1.jpg" \
  -F "archivos=@factura2.pdf"
```

Respuesta correcta:

```json
{
  "saved": true,
  "archivos_cargados": 2,
  "pdf_generado": true,
  "ruta_pdf": "/ruta/a/facturas_procesadas.pdf"
}
```

En caso de error responde `500` con `{"saved": false, "error": "..."}`.

## Estructura

```
├── src/impresion_facturas/main.py   # API, pipeline de ImageMagick, montaje de static/
├── static/
│   ├── index.html                   # selección de archivos (guardados en IndexedDB)
│   ├── revision.html                # cuadrícula, selección y reordenamiento
│   ├── procesando.html              # subida con progreso real (XHR)
│   ├── manifest.json                # manifiesto PWA
│   └── icons/
├── Dockerfile
├── docker-compose.yml
└── salida/                          # salida del contenedor (PDF)
```

## Notas y limitaciones

- El nombre del PDF es fijo: cada ejecución sobrescribe al anterior.
- Las imágenes temporales se eliminan, pero el PDF no.
- No hay service worker, así que la app no es instalable como PWA todavía (Chrome lo requiere).
- El frontend necesita red para cargar Tailwind y las fuentes desde CDN.
- No hay tests ni CI configurados.

## Problemas comunes

- **`not authorized` al generar el PDF**: la política de ImageMagick de Debian bloquea el coder PDF. En Docker ya se parchea `policy.xml` en el build; en local revisa `/etc/ImageMagick-*/policy.xml`.
- **`ImageMagick no está instalado`**: instala `imagemagick` (y `ghostscript` si vas a subir PDFs).
- **`422` en `/upload`**: el campo del formulario debe llamarse `archivos`.
