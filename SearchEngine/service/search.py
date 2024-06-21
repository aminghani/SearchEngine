from SearchEngine.database.meili import search
from SearchEngine.ai.llm import portion
from SearchEngine.utils.utils import detect_language
from SearchEngine.database.qdrant import retrieve_nearest_samples
from SearchEngine.ai.mt import translate

def search_images_db(query, min_price, max_price, config):
    lang = detect_language(query)
    if lang == 'Persian':
        query = translate(query)
    
    semantic, keyword = int(config['search']['num_retrieve']), int(config['meili']['num_retrieve'])
    
    if int(config['together']['use']) == 1:
        semantic, keyword = portion(query, config['together']['num_retrieve'])

    print(semantic, keyword)
    result_semantic = retrieve_nearest_samples(query, min_price, max_price, 
                                               top_k=semantic)

    result_keyword = search(query, min=min_price, max=max_price, limit=keyword)

    images = [{"image_url": a.payload['image_url'], "name": a.payload.get('name', ''), 
               "caption": a.payload.get('description', ''), 
               "price": a.payload.get('price', 0)} for a in result_semantic]
    
    for item in result_keyword['hits']:
        doc = {"image_url": item['image'],
               "name": item['name'],
               'caption': item['description'],
               'price': item['current_price']}
        images.append(doc)
    
    return images