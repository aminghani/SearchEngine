import meilisearch
from SearchEngine.utils.utils import read_config
import uuid

config = read_config()
client = meilisearch.Client(config['meili']['client'], config['meili']['master_key'])

def index_(collection):
    index = client.index(collection)
    return index

def add_document(document, collection):
    index = index_(collection)
    index.add_documents(document)

def search(query, collection='image_collection', min=0, max=10000, limit=5):
    index = index_(collection)

    results = index.search(query, {'limit': limit, 
                                   'filter': [f'current_price > {str(min)} AND current_price < {str(max)}']})
    return results

def save2meili(document, collection):
    name = document["name"]
    description = document["description"]
    current_price = document["current_price"]
    
    documents_to_add = []
    for image in document["images"]:
        new_document = {
            "id": str(uuid.uuid4()),
            "name": name,
            "image": image,
            "description": description,
            "current_price": float(current_price)
        }
        documents_to_add.append(new_document)
    
    add_document(documents_to_add, collection)

print(search("green dress"))