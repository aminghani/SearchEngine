from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import FileResponse
import os
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, Query
from fastapi.responses import FileResponse, JSONResponse
from SearchEngine.ai.clip import load_clip
from SearchEngine.ai.mt import load_model, translate
from SearchEngine.service.search import search_images_db
from pathlib import Path
from SearchEngine.utils.utils import read_config

app = FastAPI()
load_model()
load_clip()

current_directory = Path(__file__).parent.resolve()
static_directory = current_directory / 'static'

app.mount("/static", StaticFiles(directory=static_directory), name="static")
config = read_config()

@app.get("/")
async def root():
    return FileResponse(static_directory / "index.html")

@app.get("/search_images")
async def search_images(query: str = Query(..., min_length=1), 
                        min_price: float = Query(0), max_price: float = Query(10000)):
    images = search_images_db(query, min_price, max_price, config)

    return JSONResponse(content={"images": images})

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='localhost', port=8000)