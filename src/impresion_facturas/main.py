from fastapi import FastAPI,UploadFile, File
from typing import List

import os

from fastapi.responses import JSONResponse

app = FastAPI()

# ruta de la carpeta
TMP_RUTA = "/fotos/facturas_temp"

# verificamos que este creada

os.makedirs(TMP_RUTA, exist_ok=True)

app.post('/upload')
async def upload_file(archivos: List[UploadFile] = File(...)):
    rutas_guardadas = []
    try:
        for archivo in archivos:
                ruta_destino = os.path.join(TMP_RUTA, archivo.filename)

                contenido = await archivo.read()

                with open(ruta_destino, 'wb') as f:
                    f.write(contenido)

                rutas_guardadas.append(ruta_destino)
        return JSONResponse(content={
            'saved': True
        }, status_code=200)
    except FileNotFoundError:
        return JSONResponse(content={
            'saved':False
        }, status_code=404)
