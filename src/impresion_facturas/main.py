import os
import shutil
import subprocess
from pathlib import Path
from typing import List

from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parents[2]


def _static_dir() -> Path:
    candidates = []
    if os.environ.get("STATIC_DIR"):
        candidates.append(Path(os.environ["STATIC_DIR"]))
    candidates.extend([BASE_DIR / "static", Path("/app/static")])
    for candidate in candidates:
        if candidate.is_dir():
            return candidate
    return BASE_DIR / "static"


STATIC_DIR = _static_dir()

TMP_RUTA = os.environ.get("FACTURAS_TMP", str(BASE_DIR / "fotos" / "facturas_temp"))
os.makedirs(TMP_RUTA, exist_ok=True)

ejecutable_magick = shutil.which("magick") or shutil.which("convert")


def es_imagen_oscura(ruta_imagen: str) -> bool:
    """Calcula el brillo promedio de la imagen para determinar si es Modo Oscuro."""
    try:
        comando = [
            ejecutable_magick,
            ruta_imagen,
            "-colorspace",
            "Gray",
            "-format",
            "%[fx:mean]",
            "info:",
        ]
        resultado = subprocess.run(
            comando, capture_output=True, text=True, check=True
        )
        brillo_promedio = float(resultado.stdout.strip())
        return brillo_promedio < 0.4
    except Exception as e:
        print(f"Error detectando brillo: {e}")
        return False


@app.post("/upload")
async def upload_file(archivos: List[UploadFile] = File(...)):
    rutas_guardadas = []
    rutas_procesadas = []

    try:
        if not ejecutable_magick:
            raise RuntimeError(
                "ImageMagick no está instalado (no se encontró 'magick' ni 'convert')."
            )

        # 1. Guardar archivos recibidos
        os.makedirs(TMP_RUTA, exist_ok=True)
        for archivo in archivos:
            nombre_seguro = os.path.basename(archivo.filename or "")
            if not nombre_seguro:
                nombre_seguro = f"archivo_{len(rutas_guardadas)}"
            ruta_destino = os.path.join(TMP_RUTA, nombre_seguro)
            contenido = await archivo.read()

            with open(ruta_destino, "wb") as f:
                f.write(contenido)

            rutas_guardadas.append(ruta_destino)

        # 2. Procesamiento enfocado en forzar el fondo blanco
        for i, ruta_img in enumerate(rutas_guardadas):
            ruta_salida_temp = os.path.join(TMP_RUTA, f"temp_proc_{i}.png")

            if es_imagen_oscura(ruta_img):
                # Modo oscuro: Invierte el color y aplica un umbral (threshold)
                # para enviar todos los tonos oscuros/grises a blanco absoluto.
                filtros = [
                    "-colorspace",
                    "Gray",
                    "-negate",
                    "-threshold",
                    "35%",  # Ajuste clave: todo lo que no sea texto se vuelve blanco 100%
                ]
            else:
                # Modo claro: Blanquea fondos grises/sombras sin invertir texto
                filtros = [
                    "-colorspace",
                    "Gray",
                    "-threshold",
                    "70%",
                ]

            comando_individual = (
                [ejecutable_magick, ruta_img] + filtros + [ruta_salida_temp]
            )
            subprocess.run(comando_individual, check=True)
            rutas_procesadas.append(ruta_salida_temp)

        # 3. Unir en el PDF final
        pdf_salida = os.path.join(TMP_RUTA, "facturas_procesadas.pdf")
        comando_pdf = [ejecutable_magick] + rutas_procesadas + [pdf_salida]
        subprocess.run(comando_pdf, check=True)

        # 4. Limpieza de imágenes intermedias
        for r in rutas_guardadas + rutas_procesadas:
            if os.path.exists(r):
                os.remove(r)

        return JSONResponse(
            content={
                "saved": True,
                "archivos_cargados": len(rutas_guardadas),
                "pdf_generado": os.path.exists(pdf_salida),
                "ruta_pdf": pdf_salida,
            },
            status_code=200,
        )

    except Exception as e:
        return JSONResponse(
            content={"saved": False, "error": str(e)}, status_code=500
        )


if STATIC_DIR.is_dir():
    app.mount("/", StaticFiles(directory=STATIC_DIR, html=True), name="static")
