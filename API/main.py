import io
import shutil
import zipfile

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse
from pathlib import Path
import os

from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/extracted", StaticFiles(directory="API/extracted"), name="extracted")


@app.get("/")
async def root():
    return {"Boo!"}


@app.post("/publish")
async def publish(file: UploadFile = File(...)):
    with zipfile.ZipFile(file.file, "r") as f:
        f.extractall(f"API/extracted/{file.filename}")
    return {}

