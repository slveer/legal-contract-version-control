import io
import shutil
import zipfile

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse
from pathlib import Path
import os

app = FastAPI()


@app.get("/")
async def root():
    return {"Boo!"}

@app.post("/publish")
async def publish(file: UploadFile = File(...)):
    with open(f"{file.filename}", "wb") as f:
        shutil.copyfileobj(file.file, f)
    return {"filename": file.filename, "path": os.path.abspath(f"{file.filename}")}