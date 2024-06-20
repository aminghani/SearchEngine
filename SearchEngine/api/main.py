from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import FileResponse
import os
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, Query
from fastapi.responses import FileResponse, JSONResponse
from SearchEngine.database.qdrant import retrieve_nearest_samples
from pathlib import Path

app = FastAPI()

# Get the current directory of this file
current_directory = Path(__file__).parent.resolve()
static_directory = current_directory / 'static'

# Mount the static directory
app.mount("/static", StaticFiles(directory=static_directory), name="static")

@app.get("/")
async def root():
    return FileResponse(static_directory / "index.html")

@app.get("/search_images")
async def search_images(query: str = Query(..., min_length=1)):
    result = retrieve_nearest_samples(query)

    images = [a.payload['image_url'] for a in result]
    return JSONResponse(content={"images": images})

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='localhost', port=8000)