from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import FileResponse
import os
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, Query
from fastapi.responses import FileResponse, JSONResponse
from SearchEngine.database.qdrant import retrieve_nearest_samples
from SearchEngine.ai.clip import load_clip
from SearchEngine.ai.mt import load_model, translate
from SearchEngine.utils.utils import detect_language
from pathlib import Path
from SearchEngine.utils.utils import read_config
from SearchEngine.database.meili import search
app = FastAPI()
load_model()
load_clip()
# Get the current directory of this file
current_directory = Path(__file__).parent.resolve()
static_directory = current_directory / 'static'

# Mount the static directory
app.mount("/static", StaticFiles(directory=static_directory), name="static")
config = read_config()

@app.get("/")
async def root():
    return FileResponse(static_directory / "index.html")

@app.get("/search_images")
async def search_images(query: str = Query(..., min_length=1), min_price: float = Query(0), max_price: float = Query(10000)):
    lang = detect_language(query)
    if lang == 'Persian':
        query = translate(query)
    result_semantic = retrieve_nearest_samples(query, min_price, max_price, top_k=int(config['search']['num_retrieve']))
    
    result_keyword = search(query)
    images = [{"image_url": a.payload['image_url'], "name": a.payload.get('name', ''), "caption": a.payload.get('caption', ''), "price": a.payload.get('price', 0)} for a in result_semantic]
    for item in result_keyword['hits']:
        doc = {"image_url": item['image'],
               "name": item['name'],
               'caption': item['description'],
               'price': item['current_price']}
        images.append(doc)
    return JSONResponse(content={"images": images})

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='localhost', port=8000)