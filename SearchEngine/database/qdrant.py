from qdrant_client import models, QdrantClient
from qdrant_client.models import Filter, FieldCondition, Range
import json
import requests
from PIL import Image
from io import BytesIO
from typing import List
from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct
from SearchEngine.ai.clip import load_clip, embed_image, embed_text
from os import listdir
from os.path import isfile, join
import os

def connect_qdrant():
    current_dir = os.getcwd()
    file_path = os.path.join(current_dir, 'SearchEngine', 'database', 'cache')
    client = QdrantClient(path=file_path)
    return client

def read_json():
    current_dir = os.getcwd()
    file_path = os.path.join(current_dir, 'SearchEngine', 'data', 'products.json')
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def download_images(image_urls: List[str], save_dir: str, counter) -> List[str]:
    image_paths = []
    for i, url in enumerate(image_urls):
        try:
            response = requests.get(url)
            image = Image.open(BytesIO(response.content))
            image_path = f"{save_dir}/image_{counter}.jpg"
            image.save(image_path)
            image_paths.append(image_path)
            counter +=1
        except Exception:
            pass

    return image_paths

def create_qdrant_collection(client, collection_name="image_collection"):
    client.recreate_collection(
        collection_name=collection_name,
        vectors_config = models.VectorParams(
        size=512,  # Vector size is defined by used model
        distance="Cosine",
    ),
    )

def save_to_qdrant(client, collection_name, name, description,image_features, image_path, full_urls: List[str], counter, price):
    points = []
    for i, feature in enumerate(image_features):
        point = PointStruct(
            id=counter,
            vector=feature.tolist(),
            payload={
                "name": name,
                "description": description,
                "image_path": image_path[i],
                "image_url": full_urls[i],
                "price": price
            }
        )
        points.append(point)
        counter+=1
    client.upsert(
        collection_name=collection_name,
        points=points
    )

def populate_qdrant(num_images: int):
    client = connect_qdrant()
    create_qdrant_collection(client)
    model, processor = load_clip()
    data = read_json()

    for item in data:
        image_urls = item["images"]
        name = item["name"]
        description = item["description"]
        price = item['current_price']
        files = [f for f in listdir('SearchEngine/data/images') if isfile(join('SearchEngine/data/images', f))]
        if len(files) > num_images:
            break
        len_file = len(files)
        image_paths = download_images(image_urls, save_dir="SearchEngine/data/images", counter=len_file)
        image_features = embed_image(model, processor, image_paths)

        save_to_qdrant(client, "image_collection", name, description, image_features, image_paths, image_urls, len_file, price)

def retrieve_nearest_samples(text, min_price, max_price, top_k=5, collection_name='image_collection'):
    model, processor = load_clip()
    embedding = embed_text(model, processor, [text])
    client = connect_qdrant()
    if len(embedding.shape) == 2:
        embedding = embedding.flatten()
    
    price_filter = Filter(
        must=[
            FieldCondition(
                key="price",
                range=Range(
                    gte=min_price,
                    lte=max_price
                )
            )
        ]
    )

    search_result = client.search(
        collection_name=collection_name,
        query_vector=embedding.tolist(),
        limit=top_k,
        query_filter=price_filter
    )
    return search_result